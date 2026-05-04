from .db import get_connection, init_db
from datetime import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_task(agent_name, title, description=None, date_due=None, priority='medium', subtask_of=None):
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, date_due, priority, subtask_of)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, date_due, priority, subtask_of))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_task(agent_name, task_id)

def update_task(agent_name, task_id, **kwargs):
    init_db(agent_name)
    allowed_fields = {'title', 'description', 'date_due', 'status', 'priority', 'date_completed', 'subtask_of'}
    fields_to_update = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not fields_to_update:
        return get_task(agent_name, task_id)
    
    if 'status' in fields_to_update and fields_to_update['status'] == 'complete':
        fields_to_update['date_completed'] = datetime.now().isoformat()
    
    query = 'UPDATE tasks SET ' + ', '.join([f"{k} = ?" for k in fields_to_update.keys()]) + ' WHERE id = ?'
    values = list(fields_to_update.values()) + [task_id]
    
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return get_task(agent_name, task_id)

def delete_task(agent_name, task_id):
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return True

def get_task(agent_name, task_id):
    init_db(agent_name)
    conn = get_connection(agent_name)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('SELECT * FROM updates WHERE task_id = ? ORDER BY date DESC', (task_id,))
        task['updates'] = cursor.fetchall()
        
        cursor.execute('SELECT * FROM artifacts WHERE task_id = ?', (task_id,))
        task['artifacts'] = cursor.fetchall()
        
        cursor.execute('SELECT id, title FROM tasks WHERE subtask_of = ?', (task_id,))
        task['subtasks'] = cursor.fetchall()
    conn.close()
    return task

def create_update(agent_name, task_id, comment):
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO updates (task_id, comment) VALUES (?, ?)', (task_id, comment))
    conn.commit()
    conn.close()
    return True

def update_update(agent_name, update_id, comment):
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('UPDATE updates SET comment = ? WHERE id = ?', (comment, update_id))
    conn.commit()
    conn.close()
    return True

def delete_update(agent_name, update_id):
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM updates WHERE id = ?', (update_id,))
    conn.commit()
    conn.close()
    return True

def add_artifact(agent_name, task_id, content, mimetype=None, artifact_type='Content'):
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO artifacts (task_id, content, mimetype, type)
        VALUES (?, ?, ?, ?)
    ''', (task_id, content, mimetype, artifact_type))
    conn.commit()
    conn.close()
    return True

def delete_artifact(agent_name, artifact_id):
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM artifacts WHERE id = ?', (artifact_id,))
    conn.commit()
    conn.close()
    return True

def get_tasks_by_urgency(agent_name):
    init_db(agent_name)
    conn = get_connection(agent_name)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tasks 
        WHERE status != 'complete'
        ORDER BY 
            CASE priority 
                WHEN 'urgent' THEN 0 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                WHEN 'low' THEN 3 
            END ASC,
            date_due ASC
    ''')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

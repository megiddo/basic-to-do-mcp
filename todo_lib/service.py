from .db import get_connection, init_db
from datetime import datetime, timedelta
from .config import validate_agent, get_agents, get_db_root, InvalidAgent, InvalidConfiguration
import os
from pathlib import Path

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_task(agent_name, title, description=None, date_due=None, priority='medium', subtask_of=None, collection='default'):
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, date_due, priority, subtask_of, collection)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, date_due, priority, subtask_of, collection))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_task(agent_name, task_id)

def update_task(agent_name, task_id, **kwargs):
    validate_agent(agent_name)
    init_db(agent_name)
    allowed_fields = {'title', 'description', 'date_due', 'status', 'priority', 'date_completed', 'subtask_of', 'collection'}
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
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return True

def get_task(agent_name, task_id):
    validate_agent(agent_name)
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
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO updates (task_id, comment) VALUES (?, ?)', (task_id, comment))
    conn.commit()
    conn.close()
    return True

def update_update(agent_name, update_id, comment):
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('UPDATE updates SET comment = ? WHERE id = ?', (comment, update_id))
    conn.commit()
    conn.close()
    return True

def delete_update(agent_name, update_id):
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM updates WHERE id = ?', (update_id,))
    conn.commit()
    conn.close()
    return True

def add_artifact(agent_name, task_id, content, mimetype=None, artifact_type='Content'):
    validate_agent(agent_name)
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
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM artifacts WHERE id = ?', (artifact_id,))
    conn.commit()
    conn.close()
    return True

def list_collections(agent_name):
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM collections ORDER BY name')
    cols = [row[0] for row in cursor.fetchall()]
    conn.close()
    return cols

def create_collection(agent_name, name):
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO collections (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return True

def delete_collection(agent_name, name):
    validate_agent(agent_name)
    if name == 'default':
        return False
    init_db(agent_name)
    conn = get_connection(agent_name)
    cursor = conn.cursor()
    # Tasks will automatically move to 'default' due to ON DELETE SET DEFAULT if we had it, 
    # but SQLite doesn't support SET DEFAULT with foreign keys easily in all versions.
    # We'll do it manually to be safe.
    cursor.execute('UPDATE tasks SET collection = "default" WHERE collection = ?', (name,))
    cursor.execute('DELETE FROM collections WHERE name = ?', (name,))
    conn.commit()
    conn.close()
    return True

def get_tasks_by_date_range(agent_name, start_date=None, end_date=None, is_past_due=False, collection=None):
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks WHERE status != 'complete'"
    params = []
    
    if collection:
        query += " AND collection = ?"
        params.append(collection)
        
    if is_past_due:
        query += " AND date_due < ?"
        params.append(datetime.now().isoformat())
    elif start_date and end_date:
        query += " AND date_due >= ? AND date_due <= ?"
        params.extend([start_date, end_date])
    elif start_date:
        query += " AND date_due >= ?"
        params.append(start_date)
    elif end_date:
        query += " AND date_due <= ?"
        params.append(end_date)
        
    query += " ORDER BY date_due ASC, priority DESC"
    
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_tasks_due_today(agent_name, collection=None):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()
    return get_tasks_by_date_range(agent_name, start_date=today_start, end_date=today_end, collection=collection)

def get_tasks_past_due(agent_name, collection=None):
    return get_tasks_by_date_range(agent_name, is_past_due=True, collection=collection)

def get_tasks_due_next_week(agent_name, collection=None):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    next_week = (datetime.now() + timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()
    return get_tasks_by_date_range(agent_name, start_date=today_start, end_date=next_week, collection=collection)

def get_tasks_by_urgency(agent_name, collection=None):
    validate_agent(agent_name)
    init_db(agent_name)
    conn = get_connection(agent_name)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    query = '''
        SELECT * FROM tasks 
        WHERE status != 'complete'
    '''
    params = []
    if collection:
        query += " AND collection = ?"
        params.append(collection)
        
    query += '''
        ORDER BY 
            CASE priority 
                WHEN 'urgent' THEN 0 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                WHEN 'low' THEN 3 
            END ASC,
            date_due ASC
    '''
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def list_agents():
    """Return the list of authorized agents."""
    return get_agents()

def install_library():
    """Create DB_FILE_ROOT and /etc/mcp/basic_todo/.env"""
    db_root = get_db_root()
    os.makedirs(db_root, exist_ok=True)
    
    etc_path = Path("/etc/mcp/basic_todo")
    try:
        etc_path.mkdir(parents=True, exist_ok=True)
        env_path = etc_path / ".env"
        if not env_path.exists():
            with open(env_path, "w") as f:
                f.write(f"AGENTS=alice,bob\nDB_FILE_ROOT={db_root}\n")
            return f"Successfully installed to {etc_path} and created DB root at {db_root}"
        else:
            return f"Directories ensured. {env_path} already exists."
    except PermissionError:
        # Fallback to local .env if /etc is not writable
        local_env = Path(__file__).parent.parent.absolute() / ".env"
        if not local_env.exists():
            with open(local_env, "w") as f:
                f.write(f"AGENTS=alice,bob\nDB_FILE_ROOT={db_root}\n")
            return f"Could not write to /etc (Permission Denied). Created local config at {local_env} and DB root at {db_root}"
        return f"Could not write to /etc. Local config already exists at {local_env}."

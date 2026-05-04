import sqlite3
import os
from datetime import datetime

def get_db_path(agent_name):
    return f"todo_{agent_name}.db"

def get_connection(agent_name):
    return sqlite3.connect(get_db_path(agent_name))

def init_db(agent_name):
    db_path = get_db_path(agent_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
        date_due DATETIME,
        status TEXT CHECK(status IN ('created', 'in-progress', 'complete')) DEFAULT 'created',
        priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')) DEFAULT 'medium',
        date_completed DATETIME,
        subtask_of INTEGER,
        FOREIGN KEY (subtask_of) REFERENCES tasks(id) ON DELETE CASCADE
    )
    ''')
    
    # Create updates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment TEXT NOT NULL,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        task_id INTEGER NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

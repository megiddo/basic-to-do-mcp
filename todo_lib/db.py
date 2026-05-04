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
    
    # Create collections table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS collections (
        name TEXT PRIMARY KEY
    )
    ''')
    
    # Ensure default collection exists
    cursor.execute("INSERT OR IGNORE INTO collections (name) VALUES ('default')")

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
        collection TEXT DEFAULT 'default',
        FOREIGN KEY (subtask_of) REFERENCES tasks(id) ON DELETE CASCADE,
        FOREIGN KEY (collection) REFERENCES collections(name) ON DELETE SET DEFAULT
    )
    ''')
    
    # Migration: add collection column if it doesn't exist
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'collection' not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN collection TEXT DEFAULT 'default'")

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
    
    # Create artifacts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS artifacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        mimetype TEXT,
        type TEXT CHECK(type IN ('URL', 'Content', 'File')),
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

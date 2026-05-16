import sqlite3
import os

DB_PATH = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant TEXT,
            workshop TEXT,
            station_no TEXT,
            process_name TEXT,
            tool_used TEXT,
            skill_required TEXT,
            theory_module TEXT,
            safety_concept TEXT
        )
    ''')
    conn.commit()
    conn.close()

def clear_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mappings')
    conn.commit()
    conn.close()

def insert_mappings(dataframe):
    conn = get_db_connection()
    # Ensure NaN values are replaced with empty strings
    dataframe = dataframe.fillna('')
    # Convert to list of tuples
    records = dataframe.to_records(index=False)
    
    # SQLite does not directly support numpy types properly sometimes, convert to standard types
    records = [tuple(str(item) if item != '' else '' for item in row) for row in records]
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO mappings (
            plant, workshop, station_no, process_name, 
            tool_used, skill_required, theory_module, safety_concept
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', records)
    conn.commit()
    conn.close()

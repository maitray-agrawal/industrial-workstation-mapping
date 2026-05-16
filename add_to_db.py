import pandas as pd
import sqlite3
from modules.database_handler import insert_mappings, clear_db, get_db_connection
import os

def run():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'dample.xlsx')
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    df = pd.read_excel(file_path)
    print(f"Read {len(df)} rows from excel.")
    
    clear_db()
    insert_mappings(df)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM mappings')
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Database successfully populated! Total records in DB: {count}")

if __name__ == "__main__":
    run()

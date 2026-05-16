from .database_handler import get_db_connection

def search_mappings(query):
    if not query:
        return []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    search_term = f'%{query}%'
    
    cursor.execute('''
        SELECT * FROM mappings
        WHERE theory_module LIKE ?
        OR process_name LIKE ?
        OR tool_used LIKE ?
        OR station_no LIKE ?
        OR workshop LIKE ?
        OR plant LIKE ?
        OR safety_concept LIKE ?
    ''', (search_term, search_term, search_term, search_term, search_term, search_term, search_term))
    
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

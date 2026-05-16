from .database_handler import get_db_connection

def get_cross_plant_relationships(query):
    # This function finds related applications based on search query
    # E.g., if we search "Torque", we want to see grouped plants/workshops
    if not query:
        return {}

    conn = get_db_connection()
    cursor = conn.cursor()
    search_term = f'%{query}%'

    cursor.execute('''
        SELECT DISTINCT plant, workshop FROM mappings
        WHERE theory_module LIKE ?
        OR process_name LIKE ?
        OR tool_used LIKE ?
        OR station_no LIKE ?
        OR safety_concept LIKE ?
    ''', (search_term, search_term, search_term, search_term, search_term))
    
    related_locations = cursor.fetchall()
    conn.close()

    grouped_locations = {}
    for row in related_locations:
        plant = row['plant']
        workshop = row['workshop']
        if plant not in grouped_locations:
            grouped_locations[plant] = []
        if workshop not in grouped_locations[plant]:
            grouped_locations[plant].append(workshop)

    return grouped_locations

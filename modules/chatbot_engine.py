from .database_handler import get_db_connection

STOP_WORDS = {
    "what", "where", "when", "why", "who", "how", "is", "are", "do", "does", "did",
    "show", "me", "tell", "give", "list", "find", "search", "about",
    "used", "uses", "using", "for", "the", "a", "an", "in", "with", "similar", 
    "applications", "related", "to", "which", "of", "and", "or", "on"
}

def preprocess_query(query):
    words = query.lower().replace('?', '').replace('.', '').replace(',', '').split()
    keywords = [w for w in words if w not in STOP_WORDS]
    # If everything is a stop word (e.g., "what is"), just return the original query
    if not keywords:
        return query.strip()
    return " ".join(keywords)

def get_chatbot_response(raw_query):
    if not raw_query or not raw_query.strip():
        return "Please ask a valid question."

    keyword = preprocess_query(raw_query)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    search_term = f'%{keyword}%'
    
    # Global search fallback across all relevant columns
    cursor.execute('''
        SELECT * FROM mappings
        WHERE theory_module LIKE ?
        OR process_name LIKE ?
        OR tool_used LIKE ?
        OR station_no LIKE ?
        OR workshop LIKE ?
        OR plant LIKE ?
        OR safety_concept LIKE ?
        OR skill_required LIKE ?
    ''', (search_term, search_term, search_term, search_term, search_term, search_term, search_term, search_term))
    
    results = cursor.fetchall()
    conn.close()

    if not results:
        return f"I couldn't find any industrial mapping records matching '{keyword}'. Try checking your spelling or using different keywords."

    # Format the response
    formatted_response = f"<strong>{keyword.title()}</strong> is found in the following applications:<br><br>"
    
    # Use HTML formatting for the chat UI
    for idx, row in enumerate(results, 1):
        formatted_response += f'''
        <div class="card mb-2 shadow-sm">
            <div class="card-body py-2">
                <strong>{idx}. {row['plant']} - {row['workshop']}</strong><br>
                <span class="text-primary">Station:</span> {row['station_no']}<br>
                <span class="text-success">Process:</span> {row['process_name']}<br>
                <span class="text-danger">Tool:</span> {row['tool_used']}<br>
                <span class="text-info">Theory/Module:</span> {row['theory_module']}
            </div>
        </div>
        '''
        
    # Cross-plant similarities
    plants = list(set([row['plant'] for row in results]))
    if len(plants) > 1:
        formatted_response += f'''
        <div class="alert alert-info mt-3 p-2">
            <i class="fa-solid fa-network-wired me-2"></i>
            <strong>Cross-Plant Similarity Detected:</strong> This concept/tool is utilized across multiple plants: {", ".join(plants)}.
        </div>
        '''
        
    return formatted_response

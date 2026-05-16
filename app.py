import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from modules.database_handler import init_db, clear_db, insert_mappings
from modules.excel_reader import validate_and_read_excel
from modules.search_engine import search_mappings
from modules.mapping_logic import get_cross_plant_relationships
from modules.chatbot_engine import get_chatbot_response

app = Flask(__name__)
app.secret_key = 'offline_industrial_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'master_mapping.xlsx')
            file.save(filepath)
            
            is_valid, msg, df = validate_and_read_excel(filepath)
            if not is_valid:
                flash(msg, 'danger')
            else:
                try:
                    clear_db()
                    insert_mappings(df)
                    flash('Data successfully imported and database updated!', 'success')
                except Exception as e:
                    flash(f'Database error: {str(e)}', 'danger')
        else:
            flash('Invalid file format. Please upload an Excel (.xlsx or .xls) file.', 'danger')
            
        return redirect(url_for('index'))
        
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index'))
        
    results = search_mappings(query)
    relationships = get_cross_plant_relationships(query)
    
    return render_template('results.html', query=query, results=results, relationships=relationships)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message', '')
        response = get_chatbot_response(user_message)
        return jsonify({'response': response})
    
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

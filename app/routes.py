from flask import Blueprint, request, render_template, jsonify, current_app
from app.utils import rag_processor

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    if file:
        try:
            file_content = file.read().decode('utf-8')
            rag_processor.process_file(file_content)
            return jsonify({'message': 'File processed successfully'})
        except Exception as e:
            return jsonify({'message': f'Error processing file: {str(e)}'}), 500

@main.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'answer': 'No question provided'}), 400
    
    try:
        response = rag_processor.get_response(question)
        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'answer': f'Error: {str(e)}'}), 500
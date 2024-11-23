from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize Ollama
llm = Ollama(model="llama3.2:3b-instruct-fp16")
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

class RAGProcessor:
    def __init__(self):
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def process_file(self, file_content):
        chunks = self.text_splitter.split_text(file_content)
        self.vector_store = FAISS.from_texts(chunks, embeddings)
        return self.vector_store

    def get_response(self, question):
        if not self.vector_store:
            return "Please upload FAQ data first"

        relevant_docs = self.vector_store.similarity_search(question, k=2)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        prompt = f'''Use the following context to answer the question. If you are less sure, use the word "probably" while answering.
        Only if the answer cannot be found, then say "I don't have enough information to answer that question, can you please ask something else"

        Context:
        {context}

        Question: {question}

        Answer:'''
        
        return llm.invoke(prompt)

# Create a global instance
rag_processor = RAGProcessor()
"""

# File: app/routes.py
"""
from flask import Blueprint, request, render_template, jsonify
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
from flask import Flask, request, jsonify
from flask_cors import CORS
from query_data import query_rag
import socket

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        response = query_rag(question)
        return jsonify({'answer': response, 'status': 'success'})
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/health', methods=['GET'])
def health():
    hostname = socket.gethostname()
    return jsonify({
        'status': 'healthy',
        'service': 'Seeweb RAG',
        'hostname': hostname
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'service': 'Seeweb Docs RAG API',
        'endpoints': {
            'POST /query': 'Query the RAG system',
            'GET /health': 'Health check'
        },
        'example': {
            'method': 'POST',
            'url': '/query',
            'body': {'question': 'Come creare un cluster Kubernetes?'}
        }
    })

if __name__ == '__main__':
    # Bind to all interfaces on port 8998
    app.run(host='0.0.0.0', port=8998, debug=False)


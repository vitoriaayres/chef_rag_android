#!/usr/bin/env python3
"""
Script simples para iniciar a API sem modo debug
"""

import os
import sys

# Adicionar o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_logic import config

# Verificar configuração básica
if not config.GOOGLE_API_KEY:
    print("❌ ERRO: Chave da API do Google não configurada!")
    print("Configure a variável GOOGLE_API_KEY no arquivo .env")
    sys.exit(1)

# Importar e configurar Flask
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'message': 'Chef RAG API is running'
    })

@app.route('/api/book/status', methods=['GET'])
def get_book_status():
    """Verifica o status do livro de receitas"""
    try:
        # Verificar se PDF existe
        pdf_exists = os.path.exists(config.PDF_FILE_PATH)
        
        # Verificar se ChromaDB foi criado
        chroma_db_file = os.path.join(config.CHROMA_DB_PATH, "chroma.sqlite3")
        chroma_exists = os.path.exists(chroma_db_file)
        
        return jsonify({
            'success': True,
            'pdf_exists': pdf_exists,
            'chroma_exists': chroma_exists,
            'is_ready': pdf_exists and chroma_exists,
            'pdf_path': config.PDF_FILE_PATH if pdf_exists else None
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao verificar status: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando Chef RAG API (modo simples)...")
    print("📡 API disponível em: http://localhost:8080")
    print("📊 Health check: http://localhost:8080/api/health")
    
    app.run(debug=False, host='0.0.0.0', port=8080)
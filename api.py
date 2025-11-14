#!/usr/bin/env python3
"""
API Flask para o Chef RAG - Ponte entre frontend e backend
"""

import os
import sys
import tempfile
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import time

# Adicionar o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_logic import rag_system, database
try:
    from core_logic.voice_recognition import voice_recognition
    VOICE_AVAILABLE = True
except ImportError:
    voice_recognition = None
    VOICE_AVAILABLE = False
    print("⚠️ Módulo de reconhecimento de voz não disponível")

app = Flask(__name__)
CORS(app)  # Permitir requests do frontend

# Configurações
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Chef RAG API is running'
    })

@app.route('/api/analyze-ingredient', methods=['POST'])
def analyze_ingredient():
    """Analisa uma imagem e retorna receitas sugeridas"""
    try:
        # Verificar se foi enviado um arquivo
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem foi enviada'}), 400
        
        file = request.files['image']
        source_mode = request.form.get('source', 'upload')
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Formato de arquivo não suportado'}), 400
        
        # Salvar arquivo temporário
        filename = secure_filename(file.filename)
        if not filename:
            filename = f"temp_image_{int(time.time())}.jpg"
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        try:
            start_time = time.time()
            
            # Identificar ingrediente
            ingredient = rag_system.extract_ingredients_from_image(file_path)
            
            if "Erro" in ingredient:
                return jsonify({
                    'error': f'Não foi possível identificar o ingrediente: {ingredient}'
                }), 400
            
            # Buscar receitas
            recipes = rag_system.find_recipes_by_ingredient(
                ingredient, 
                file_path, 
                source_mode
            )
            
            processing_time = time.time() - start_time
            
            # Retornar resultado
            return jsonify({
                'success': True,
                'ingredient': ingredient,
                'recipes': recipes,
                'processing_time': round(processing_time, 2),
                'source_mode': source_mode,
                'timestamp': datetime.now().isoformat()
            })
            
        finally:
            # Limpar arquivo temporário
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
                
    except Exception as e:
        return jsonify({
            'error': f'Erro interno do servidor: {str(e)}'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Retorna o histórico de análises"""
    try:
        # Obter parâmetros de consulta
        limit = request.args.get('limit', 20, type=int)
        
        # Buscar dados do histórico
        recent_analyses = database.history_db.get_recent_analyses(limit)
        statistics = database.history_db.get_statistics()
        all_ingredients = database.history_db.get_all_ingredients()
        
        # Formatar dados para o frontend
        formatted_analyses = []
        for analysis in recent_analyses:
            formatted_analyses.append({
                'timestamp': analysis[0],
                'image_name': analysis[1],
                'ingredient_identified': analysis[2],
                'chef_suggestion': analysis[3],
                'source_mode': analysis[4],
                'processing_time_seconds': analysis[5]
            })
        
        return jsonify({
            'success': True,
            'recent_analyses': formatted_analyses,
            'statistics': statistics,
            'ingredients_summary': all_ingredients[:10],  # Top 10 ingredientes
            'total_ingredients': len(all_ingredients)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao buscar histórico: {str(e)}'
        }), 500

@app.route('/api/history/search', methods=['GET'])
def search_history():
    """Busca no histórico por ingrediente"""
    try:
        ingredient = request.args.get('ingredient', '').strip()
        
        if not ingredient:
            return jsonify({'error': 'Parâmetro ingredient é obrigatório'}), 400
        
        results = database.history_db.search_by_ingredient(ingredient)
        
        # Formatar resultados
        formatted_results = []
        for result in results:
            formatted_results.append({
                'timestamp': result[0],
                'image_name': result[1],
                'chef_suggestion': result[2],
                'source_mode': result[3]
            })
        
        return jsonify({
            'success': True,
            'ingredient': ingredient,
            'results': formatted_results,
            'count': len(formatted_results)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro na busca: {str(e)}'
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Retorna estatísticas detalhadas"""
    try:
        stats = database.history_db.get_statistics()
        ingredients = database.history_db.get_all_ingredients()
        
        return jsonify({
            'success': True,
            'statistics': stats,
            'top_ingredients': ingredients[:10],
            'total_unique_ingredients': len(ingredients)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao obter estatísticas: {str(e)}'
        }), 500

@app.route('/api/book/status', methods=['GET'])
def get_book_status():
    """Verifica o status do livro de receitas"""
    try:
        from core_logic import config
        
        # Verificar se PDF existe
        pdf_exists = os.path.exists(config.PDF_FILE_PATH)
        
        # Verificar se ChromaDB foi criado
        chroma_db_file = os.path.join(config.CHROMA_DB_PATH, "chroma.sqlite3")
        chroma_exists = os.path.exists(chroma_db_file)
        
        # Contar páginas se PDF existir
        total_pages = 0
        processed_pages = 0
        
        if pdf_exists:
            try:
                import pdfplumber
                with pdfplumber.open(config.PDF_FILE_PATH) as pdf:
                    total_pages = len(pdf.pages)
            except Exception as e:
                return jsonify({'error': f'Erro ao ler PDF: {str(e)}'}), 500
        
        if chroma_exists:
            try:
                client = rag_system.get_db_client()
                collection = client.get_collection(name=config.CHROMA_COLLECTION_NAME)
                processed_pages = collection.count()
            except Exception:
                processed_pages = 0
        
        return jsonify({
            'success': True,
            'pdf_exists': pdf_exists,
            'pdf_path': config.PDF_FILE_PATH if pdf_exists else None,
            'chroma_exists': chroma_exists,
            'total_pages': total_pages,
            'processed_pages': processed_pages,
            'is_ready': pdf_exists and chroma_exists and processed_pages > 0,
            'needs_processing': pdf_exists and (not chroma_exists or processed_pages == 0)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao verificar status: {str(e)}'
        }), 500

@app.route('/api/book/upload', methods=['POST'])
def upload_book():
    """Upload do livro de receitas (PDF)"""
    try:
        if 'book' not in request.files:
            return jsonify({'error': 'Nenhum arquivo PDF foi enviado'}), 400
        
        file = request.files['book']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Arquivo deve ser um PDF'}), 400
        
        from core_logic import config
        
        # Criar diretório se não existir
        pdf_dir = os.path.dirname(config.PDF_FILE_PATH)
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Salvar arquivo
        file.save(config.PDF_FILE_PATH)
        
        # Verificar se foi salvo corretamente
        if os.path.exists(config.PDF_FILE_PATH):
            try:
                import pdfplumber
                with pdfplumber.open(config.PDF_FILE_PATH) as pdf:
                    total_pages = len(pdf.pages)
                
                return jsonify({
                    'success': True,
                    'message': 'Livro carregado com sucesso',
                    'total_pages': total_pages,
                    'filename': file.filename,
                    'needs_processing': True
                })
            except Exception as e:
                # Remove arquivo se estiver corrompido
                try:
                    os.remove(config.PDF_FILE_PATH)
                except:
                    pass
                return jsonify({'error': f'PDF inválido ou corrompido: {str(e)}'}), 400
        else:
            return jsonify({'error': 'Erro ao salvar arquivo'}), 500
            
    except Exception as e:
        return jsonify({
            'error': f'Erro no upload: {str(e)}'
        }), 500

@app.route('/api/book/process', methods=['POST'])
def process_book():
    """Processa o livro para criar a base de dados vetorial"""
    try:
        from core_logic import config
        
        if not os.path.exists(config.PDF_FILE_PATH):
            return jsonify({'error': 'Nenhum livro encontrado. Faça upload primeiro.'}), 400
        
        # Importar funções necessárias
        import pdfplumber
        import google.generativeai as genai
        
        # Configurar API
        genai.configure(api_key=config.GOOGLE_API_KEY)
        
        # Inicializar cliente ChromaDB
        client = rag_system.get_db_client()
        
        try:
            # Deletar coleção antiga se existir
            client.delete_collection(name=config.CHROMA_COLLECTION_NAME)
        except Exception:
            pass
        
        # Criar nova coleção
        collection = client.get_or_create_collection(name=config.CHROMA_COLLECTION_NAME)
        
        documents = []
        metadatas = []
        ids = []
        
        # Ler PDF
        with pdfplumber.open(config.PDF_FILE_PATH) as pdf:
            total_pages = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages):
                texto = page.extract_text()
                if texto and len(texto) > 50:
                    documents.append(texto)
                    metadatas.append({"page_number": i + 1})
                    ids.append(f"page_{i + 1}")
        
        if not documents:
            return jsonify({'error': 'Nenhum texto extraído do PDF'}), 400
        
        # Processar documentos em lotes para evitar timeout
        processed = 0
        batch_size = 10
        
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_meta = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            
            # Gerar embeddings para o lote
            embeddings = []
            for doc in batch_docs:
                embedding = rag_system.get_text_embedding(doc)
                if embedding:
                    embeddings.append(embedding)
                else:
                    return jsonify({'error': f'Erro ao gerar embedding para página {i//batch_size + 1}'}), 500
            
            # Adicionar ao ChromaDB
            collection.add(
                embeddings=embeddings,
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
            
            processed += len(batch_docs)
        
        return jsonify({
            'success': True,
            'message': 'Livro processado com sucesso',
            'total_pages_processed': processed,
            'is_ready': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar livro: {str(e)}'
        }), 500

@app.route('/api/clear-history', methods=['DELETE'])
def clear_history():
    """Limpa todo o histórico (apenas para desenvolvimento)"""
    try:
        # Por segurança, só permitir em desenvolvimento
        if app.debug:
            import sqlite3
            with sqlite3.connect(database.history_db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM ingredient_history')
                cursor.execute('DELETE FROM statistics')
                cursor.execute('''
                    INSERT INTO statistics (total_analyses, webcam_analyses, folder_analyses, 
                                          successful_analyses, failed_analyses, last_updated)
                    VALUES (0, 0, 0, 0, 0, ?)
                ''', (datetime.now().isoformat(),))
                conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Histórico limpo com sucesso'
            })
        else:
            return jsonify({
                'error': 'Operação não permitida em produção'
            }), 403
            
    except Exception as e:
        return jsonify({
            'error': f'Erro ao limpar histórico: {str(e)}'
        }), 500

# === ENDPOINTS DE PERFIL DO USUÁRIO ===

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """Obtém o perfil do usuário"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        profile = database.history_db.get_user_profile(user_id)
        
        if profile:
            return jsonify({
                'success': True,
                'profile': profile
            })
        else:
            # Retorna perfil padrão se não existir
            default_profile = {
                'user_id': user_id,
                'name': '',
                'skill_level': 'iniciante',
                'dietary_restrictions': [],
                'favorite_cuisines': [],
                'allergies': [],
                'cooking_equipment': [],
                'preferred_cooking_time': 60,
                'budget_preference': 'medio',
                'health_goals': []
            }
            return jsonify({
                'success': True,
                'profile': default_profile
            })
            
    except Exception as e:
        return jsonify({
            'error': f'Erro ao obter perfil: {str(e)}'
        }), 500

@app.route('/api/user/profile', methods=['POST'])
def update_user_profile():
    """Atualiza o perfil do usuário"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        user_id = data.get('user_id', 'default_user')
        
        # Remove user_id dos dados para atualização
        profile_data = {k: v for k, v in data.items() if k != 'user_id'}
        
        database.history_db.update_user_profile(user_id, **profile_data)
        
        return jsonify({
            'success': True,
            'message': 'Perfil atualizado com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao atualizar perfil: {str(e)}'
        }), 500

@app.route('/api/user/preferences-summary', methods=['GET'])
def get_user_preferences_summary():
    """Obtém resumo das preferências baseado no histórico"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        summary = database.history_db.get_user_preferences_summary(user_id)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao obter resumo: {str(e)}'
        }), 500

@app.route('/api/recipes/rate', methods=['POST'])
def rate_recipe():
    """Adiciona avaliação para uma receita"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        recipe_name = data.get('recipe_name')
        rating = data.get('rating')
        
        if not recipe_name or not rating:
            return jsonify({'error': 'Nome da receita e avaliação são obrigatórios'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Avaliação deve ser entre 1 e 5'}), 400
        
        user_id = data.get('user_id', 'default_user')
        
        # Remove campos não relacionados à avaliação
        rating_data = {k: v for k, v in data.items() 
                      if k not in ['recipe_name', 'rating', 'user_id']}
        
        database.history_db.add_recipe_rating(
            recipe_name=recipe_name,
            rating=rating,
            user_id=user_id,
            **rating_data
        )
        
        return jsonify({
            'success': True,
            'message': 'Avaliação adicionada com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao avaliar receita: {str(e)}'
        }), 500

@app.route('/api/user/recipe-ratings', methods=['GET'])
def get_user_recipe_ratings():
    """Obtém avaliações de receitas do usuário"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        limit = int(request.args.get('limit', 10))
        
        ratings = database.history_db.get_user_recipe_ratings(user_id, limit)
        
        return jsonify({
            'success': True,
            'ratings': ratings
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao obter avaliações: {str(e)}'
        }), 500

@app.route('/api/recipes/extract-for-rating', methods=['POST'])
def extract_recipes_for_rating():
    """Extrai receitas da resposta do chef para permitir avaliações"""
    try:
        data = request.get_json()
        if not data or 'recipes_response' not in data:
            return jsonify({'error': 'Response de receitas não fornecida'}), 400
        
        recipes_response = data['recipes_response']
        extracted_recipes = rag_system.extract_recipes_for_rating(recipes_response)
        
        # Adiciona informações de avaliação para cada receita
        for recipe in extracted_recipes:
            rating_summary = rag_system.get_recipe_rating_summary(
                recipe['name'], 
                recipe.get('page')
            )
            recipe['rating_summary'] = rating_summary
        
        return jsonify({
            'success': True,
            'recipes': extracted_recipes
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao extrair receitas: {str(e)}'
        }), 500

@app.route('/api/recipes/quick-rate', methods=['POST'])
def quick_rate_recipe():
    """Avaliação rápida de receita com dados mínimos"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        recipe_name = data.get('recipe_name')
        rating = data.get('rating')
        
        if not recipe_name or not rating:
            return jsonify({'error': 'Nome da receita e avaliação são obrigatórios'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Avaliação deve ser entre 1 e 5'}), 400
        
        user_id = data.get('user_id', 'default_user')
        
        # Dados opcionais
        rating_data = {
            'recipe_page': data.get('recipe_page'),
            'comment': data.get('comment', ''),
            'ingredients_used': data.get('ingredients_used', []),
            'cooking_time_actual': data.get('cooking_time_actual'),
            'difficulty_perceived': data.get('difficulty_perceived', 'medio'),
            'would_cook_again': data.get('would_cook_again', True)
        }
        
        # Remove campos None
        rating_data = {k: v for k, v in rating_data.items() if v is not None}
        
        database.history_db.add_recipe_rating(
            recipe_name=recipe_name,
            rating=rating,
            user_id=user_id,
            **rating_data
        )
        
        # Retorna novo resumo de avaliações
        new_summary = rag_system.get_recipe_rating_summary(
            recipe_name, 
            data.get('recipe_page')
        )
        
        return jsonify({
            'success': True,
            'message': 'Avaliação salva com sucesso!',
            'new_rating_summary': new_summary
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao salvar avaliação: {str(e)}'
        }), 500

@app.route('/api/recipes/ratings-summary/<recipe_name>', methods=['GET'])
def get_recipe_ratings_summary(recipe_name):
    """Obtém resumo de avaliações para uma receita"""
    try:
        recipe_page = request.args.get('page', type=int)
        summary = rag_system.get_recipe_rating_summary(recipe_name, recipe_page)
        
        return jsonify({
            'success': True,
            'recipe_name': recipe_name,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao obter resumo: {str(e)}'
        }), 500

# === ENDPOINTS DE RECONHECIMENTO DE VOZ ===

@app.route('/api/voice/status', methods=['GET'])
def voice_status():
    """Verifica se o reconhecimento de voz está disponível"""
    if not VOICE_AVAILABLE:
        return jsonify({
            'available': False,
            'message': 'Módulo de reconhecimento de voz não instalado'
        })
    
    try:
        test_result = voice_recognition.test_microphone()
        return jsonify({
            'available': test_result['available'],
            'message': test_result['message'],
            'details': test_result.get('details', {})
        })
    except Exception as e:
        return jsonify({
            'available': False,
            'message': f'Erro ao testar microfone: {str(e)}'
        })

@app.route('/api/voice/recognize', methods=['POST'])
def voice_recognize():
    """Reconhece ingredientes por voz"""
    if not VOICE_AVAILABLE:
        return jsonify({
            'error': 'Reconhecimento de voz não disponível'
        }), 400
    
    try:
        data = request.get_json() or {}
        timeout = data.get('timeout', 5)
        phrase_limit = data.get('phrase_limit', 10)
        
        print("🎤 Iniciando reconhecimento de voz...")
        ingredients = voice_recognition.recognize_ingredients(
            timeout=timeout, 
            phrase_time_limit=phrase_limit
        )
        
        if ingredients:
            return jsonify({
                'success': True,
                'ingredients': ingredients,
                'message': 'Ingredientes reconhecidos com sucesso'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Não foi possível reconhecer ingredientes'
            })
            
    except Exception as e:
        return jsonify({
            'error': f'Erro durante reconhecimento: {str(e)}'
        }), 500

@app.route('/api/voice/analyze-speech', methods=['POST'])
def analyze_speech_ingredients():
    """Analisa ingredientes reconhecidos por voz e retorna receitas"""
    if not VOICE_AVAILABLE:
        return jsonify({
            'error': 'Reconhecimento de voz não disponível'
        }), 400
    
    try:
        data = request.get_json() or {}
        timeout = data.get('timeout', 5)
        phrase_limit = data.get('phrase_limit', 10)
        
        print("🎤 Reconhecendo ingredientes por voz...")
        ingredients = voice_recognition.recognize_ingredients(
            timeout=timeout, 
            phrase_time_limit=phrase_limit
        )
        
        if not ingredients:
            return jsonify({
                'success': False,
                'message': 'Não foi possível reconhecer ingredientes'
            })
        
        print(f"✅ Ingredientes reconhecidos: {ingredients}")
        
        # Processa os ingredientes como se fosse uma análise normal
        start_time = time.time()
        recipes_response = rag_system.find_recipes_by_ingredient(
            ingredients, 
            source_mode='voice'
        )
        processing_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'ingredient': ingredients,
            'recipes': recipes_response,
            'processing_time': round(processing_time, 2),
            'source': 'voice_recognition'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar voz: {str(e)}'
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handler para arquivos muito grandes"""
    return jsonify({
        'error': 'Arquivo muito grande. Tamanho máximo: 16MB'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handler para rotas não encontradas"""
    return jsonify({
        'error': 'Endpoint não encontrado'
    }), 404

# === NOVOS ENDPOINTS PARA FILTROS E TIMERS ===

@app.route('/api/recipes/filter', methods=['POST'])
def filter_recipes_by_diet():
    """Filtra receitas por restrições alimentares"""
    try:
        data = request.json
        ingredients = data.get('ingredients', '')
        filters = data.get('filters', {})
        
        if not ingredients:
            return jsonify({
                'success': False,
                'error': 'Ingredientes são obrigatórios'
            }), 400
        
        # Gera receitas filtradas
        result = rag_system.generate_filtered_recipe_suggestions(ingredients, filters)
        
        return jsonify({
            'success': True,
            'recipes': result,
            'filters_applied': filters,
            'ingredients': ingredients
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recipes/analyze-dietary', methods=['POST'])
def analyze_recipe_dietary():
    """Analisa restrições alimentares de uma receita"""
    try:
        data = request.json
        recipe_text = data.get('recipe_text', '')
        
        if not recipe_text:
            return jsonify({
                'success': False,
                'error': 'Texto da receita é obrigatório'
            }), 400
        
        dietary_info = rag_system.analyze_recipe_dietary_info(recipe_text)
        
        return jsonify({
            'success': True,
            'dietary_info': dietary_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ENDPOINTS PARA TIMERS ===

@app.route('/api/timers/create', methods=['POST'])
def create_timer():
    """Cria um novo timer"""
    try:
        from core_logic.timer_manager import timer_manager
        
        data = request.json
        timer_name = data.get('timer_name', '')
        duration_minutes = data.get('duration_minutes', 0)
        recipe_name = data.get('recipe_name', '')
        step_description = data.get('step_description', '')
        user_id = data.get('user_id', 'default_user')
        
        if not timer_name or duration_minutes <= 0:
            return jsonify({
                'success': False,
                'error': 'Nome do timer e duração são obrigatórios'
            }), 400
        
        timer_id = timer_manager.create_timer(
            timer_name=timer_name,
            duration_minutes=duration_minutes,
            recipe_name=recipe_name,
            step_description=step_description,
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'timer_id': timer_id,
            'message': f'Timer "{timer_name}" criado com sucesso!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/timers/active', methods=['GET'])
def get_active_timers():
    """Retorna timers ativos"""
    try:
        from core_logic.timer_manager import timer_manager
        
        user_id = request.args.get('user_id', 'default_user')
        active_timers = timer_manager.get_active_timers(user_id)
        
        return jsonify({
            'success': True,
            'timers': active_timers
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/timers/<int:timer_id>/stop', methods=['POST'])
def stop_timer(timer_id):
    """Para um timer específico"""
    try:
        from core_logic.timer_manager import timer_manager
        
        success = timer_manager.stop_timer(timer_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Timer {timer_id} parado com sucesso!'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Timer não encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recipes/extract-timers', methods=['POST'])
def extract_recipe_timers():
    """Extrai timers de uma receita"""
    try:
        data = request.json
        recipe_text = data.get('recipe_text', '')
        
        if not recipe_text:
            return jsonify({
                'success': False,
                'error': 'Texto da receita é obrigatório'
            }), 400
        
        steps_data = rag_system.extract_recipe_steps_with_timers(recipe_text)
        
        return jsonify({
            'success': True,
            'steps_data': steps_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/timers/presets', methods=['GET'])
def get_timer_presets():
    """Retorna presets de timers"""
    try:
        from core_logic.timer_manager import timer_manager
        
        presets = timer_manager.list_timer_presets()
        
        return jsonify({
            'success': True,
            'presets': presets
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Configurar Flask
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Verificar se o sistema está configurado
    try:
        from core_logic import config
        if not config.GOOGLE_API_KEY:
            print("❌ ERRO: Chave da API do Google não configurada!")
            print("Configure a variável GOOGLE_API_KEY no arquivo .env")
            sys.exit(1)
            
        print("🚀 Iniciando Chef RAG API...")
        print("📡 API disponível em: http://localhost:5000")
        print("🌐 Frontend deve estar em: http://localhost:3000")
        print("📊 Health check: http://localhost:5000/api/health")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar API: {e}")
        sys.exit(1)
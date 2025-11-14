#!/usr/bin/env python3
"""
API Flask para o Chef RAG Mobile
Conecta o aplicativo React Native com o sistema Chef RAG
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import base64
import tempfile
from werkzeug.utils import secure_filename

# Adicionar o path do Chef RAG v2
sys.path.append('../')

# Importações básicas do Chef RAG
try:
    from core_logic.rag_system import identify_ingredient_from_image
    from core_logic.ai_providers import get_ai_response
    CHEF_RAG_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Chef RAG não disponível: {e}")
    CHEF_RAG_AVAILABLE = False

# Importações opcionais
try:
    from core_logic.database import save_analysis_to_db, get_analysis_history
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

try:
    from core_logic.user_profile import get_user_profile, update_user_profile
    PROFILE_AVAILABLE = True
except ImportError:
    PROFILE_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Permitir requisições do React Native

# Configurações
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API"""
    return jsonify({'status': 'ok', 'message': 'Chef RAG API funcionando!'})

@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    """Analisar imagem para detectar ingredientes"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and file.filename and allowed_file(file.filename):
            # Salvar arquivo temporariamente
            filename = secure_filename(file.filename) or 'image_upload.jpg'
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Detectar se deve buscar múltiplos ingredientes
            multiple_ingredients = request.form.get('multiple_ingredients', 'false').lower() == 'true'
            
            try:
                # Analisar imagem se Chef RAG disponível
                if CHEF_RAG_AVAILABLE:
                    ingredients = identify_ingredient_from_image(filepath, multiple_ingredients)
                else:
                    # Fallback: retornar ingredientes mockados
                    ingredients = "Tomate, Cebola" if multiple_ingredients else "Tomate"
                
                # Limpar arquivo temporário
                os.remove(filepath)
                
                # Converter string em lista se necessário
                if isinstance(ingredients, str):
                    ingredients_list = [ing.strip() for ing in ingredients.split(',')]
                else:
                    ingredients_list = ingredients if isinstance(ingredients, list) else [ingredients]
                
                # Salvar no histórico se disponível
                if DATABASE_AVAILABLE:
                    try:
                        save_analysis_to_db(ingredients_list[0], 'mobile', filepath)
                    except:
                        pass
                
                return jsonify({
                    'success': True,
                    'ingredients': ingredients_list,
                    'count': len(ingredients_list)
                })
                
            except Exception as e:
                # Limpar arquivo em caso de erro
                if os.path.exists(filepath):
                    os.remove(filepath)
                raise e
                
        else:
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/search', methods=['GET'])
def search_recipes():
    """Buscar receitas por ingrediente"""
    try:
        ingredient = request.args.get('ingredient', '')
        if not ingredient:
            return jsonify({'error': 'Ingrediente é obrigatório'}), 400
        
        # Buscar receitas se Chef RAG disponível
        if CHEF_RAG_AVAILABLE:
            recipes_result = find_recipes_by_ingredient(ingredient, 'mobile', 'api')
            
            # Processar resultado para formato esperado pelo mobile
            if isinstance(recipes_result, str):
                # Se retornou string, criar uma receita simples
                recipes = [{
                    'id': 1,
                    'title': f'Receita com {ingredient}',
                    'description': recipes_result,
                    'ingredients': [ingredient],
                    'cookTime': 30,
                    'difficulty': 'Fácil',
                    'servings': 4
                }]
            else:
                recipes = recipes_result
        else:
            # Fallback: receitas mockadas
            recipes = [{
                'id': 1,
                'title': f'Receita Mock com {ingredient}',
                'description': f'Uma deliciosa receita utilizando {ingredient} como ingrediente principal.',
                'ingredients': [ingredient, 'Sal', 'Pimenta', 'Azeite'],
                'cookTime': 25,
                'difficulty': 'Fácil',
                'servings': 4
            }]
        
        return jsonify({
            'success': True,
            'recipes': recipes,
            'count': len(recipes)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):
    """Obter detalhes específicos de uma receita"""
    try:
        # Por enquanto, retornar dados mockados
        # Futuramente conectar com base de dados de receitas
        recipe_details = {
            'id': recipe_id,
            'title': 'Receita Detalhada',
            'description': 'Descrição detalhada da receita...',
            'ingredients': ['Ingrediente 1', 'Ingrediente 2'],
            'instructions': [
                'Passo 1: Preparar ingredientes',
                'Passo 2: Cozinhar conforme instrução',
                'Passo 3: Finalizar prato'
            ],
            'cookTime': 30,
            'difficulty': 'Fácil',
            'servings': 4
        }
        
        return jsonify({
            'success': True,
            'recipe': recipe_details
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/timers/extract', methods=['POST'])
def extract_recipe_timers():
    """Extrair timers de uma receita"""
    try:
        data = request.get_json()
        recipe_text = data.get('recipe_text', '')
        
        if not recipe_text:
            return jsonify({'error': 'Texto da receita é obrigatório'}), 400
        
        # Extrair timers usando o sistema do Chef RAG se disponível
        if CHEF_RAG_AVAILABLE:
            try:
                timers = extract_timers_from_recipe(recipe_text)
            except (NameError, ImportError):
                timers = []
        else:
            # Fallback: buscar padrões simples de tempo
            import re
            time_patterns = re.findall(r'(\d+)\s*(?:min|minuto|minutos)', recipe_text.lower())
            timers = []
            for i, time_match in enumerate(time_patterns):
                timers.append({
                    'label': f'Etapa {i+1}',
                    'duration': int(time_match)
                })
        
        return jsonify({
            'success': True,
            'timers': timers,
            'count': len(timers)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET', 'PUT'])
def user_profile():
    """Gerenciar perfil do usuário"""
    try:
        if request.method == 'GET':
            # Obter perfil do usuário
            try:
                profile = get_user_profile()
            except:
                profile = {
                    'name': '',
                    'email': '',
                    'dietary_restrictions': {
                        'vegetarian': False,
                        'vegan': False,
                        'gluten_free': False,
                        'low_carb': False,
                        'diabetic': False
                    },
                    'culinary_level': 'beginner',
                    'preferences': {
                        'spicy_food': False,
                        'seafood': True,
                        'dairy': True
                    }
                }
            
            return jsonify({
                'success': True,
                'profile': profile
            })
            
        elif request.method == 'PUT':
            # Atualizar perfil
            data = request.get_json()
            try:
                update_user_profile(data)
            except:
                # Se não existir sistema de perfil, apenas retornar sucesso
                pass
            
            return jsonify({
                'success': True,
                'message': 'Perfil atualizado com sucesso'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def analysis_history():
    """Obter histórico de análises"""
    try:
        if DATABASE_AVAILABLE:
            try:
                history = get_analysis_history()
            except Exception:
                history = []
        else:
            # Fallback: histórico mockado
            history = [
                {
                    'id': 1,
                    'ingredient': 'Tomate',
                    'date': '2024-01-15',
                    'source': 'mobile'
                },
                {
                    'id': 2,
                    'ingredient': 'Cebola',
                    'date': '2024-01-14',
                    'source': 'mobile'
                }
            ]
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/filters', methods=['POST'])
def filter_recipes():
    """Aplicar filtros às receitas"""
    try:
        filters = request.get_json()
        
        # Por enquanto, retornar receitas mockadas baseadas nos filtros
        # Futuramente implementar filtragem real
        filtered_recipes = []
        
        if filters.get('vegetarian'):
            filtered_recipes.append({
                'id': 2,
                'title': 'Salada Vegetariana',
                'description': 'Receita vegetariana deliciosa',
                'cookTime': 15,
                'difficulty': 'Fácil'
            })
        
        if filters.get('vegan'):
            filtered_recipes.append({
                'id': 3,
                'title': 'Bowl Vegano',
                'description': 'Receita vegana nutritiva',
                'cookTime': 20,
                'difficulty': 'Fácil'
            })
        
        return jsonify({
            'success': True,
            'recipes': filtered_recipes,
            'count': len(filtered_recipes)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/process', methods=['POST'])
def process_voice():
    """Processar entrada de voz"""
    try:
        # Funcionalidade futura
        return jsonify({
            'success': False,
            'message': 'Reconhecimento de voz em desenvolvimento'
        }), 501
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import time
    print("🚀 Iniciando Chef RAG Mobile API...")
    print("📱 API disponível em: http://localhost:5000")
    print("📖 Endpoints disponíveis:")
    print("   GET  /api/health - Verificação de saúde")
    print("   POST /api/analyze-image - Análise de ingredientes")
    print("   GET  /api/recipes/search - Busca de receitas")
    print("   GET  /api/recipes/<id> - Detalhes da receita")
    print("   POST /api/timers/extract - Extração de timers")
    print("   GET/PUT /api/profile - Gerenciamento de perfil")
    print("   GET  /api/history - Histórico de análises")
    print("   POST /api/recipes/filters - Filtros de receitas")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
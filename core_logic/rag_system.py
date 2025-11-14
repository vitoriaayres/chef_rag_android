import chromadb
from PIL import Image
from . import config
from . import database
from .ai_providers import ai_provider, get_ai_response, analyze_image_with_ai
import time 
import requests

def get_text_embedding(text: str) -> list[float]:
    """Gera o embedding usando OpenAI."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        response = client.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Erro ao gerar embedding: {e}")
        return []

def get_db_client():
    """Conecta ao banco de dados vetorial local."""
    client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
    return client

# --- Lógica Principal do Agente ---

def identify_ingredient_from_image(image_path: str, multiple_ingredients: bool = True) -> str:
    """
    Usa o modelo multimodal (Visão) do Gemini para identificar 
    ingrediente(s) na imagem.
    
    Args:
        image_path: Caminho para a imagem
        multiple_ingredients: Se True, detecta múltiplos ingredientes
    
    Returns:
        String com ingrediente(s) separados por vírgula
    """
    import time
    import os
    
    print(f"🧠 Analisando imagem: {image_path}...")
    
    # Aguarda um pouco para garantir que o arquivo foi completamente salvo
    time.sleep(2)
    
    # Verifica se o arquivo existe e tem permissão de leitura
    if not os.path.exists(image_path):
        print(f"❌ Arquivo não encontrado: {image_path}")
        return "Erro"
    
    # Tenta abrir o arquivo algumas vezes em caso de problema de permissão
    max_tentativas = 3
    for tentativa in range(max_tentativas):
        try:
            with open(image_path, 'rb') as f:
                # Testa se consegue ler o arquivo
                f.read(1)
            
            if multiple_ingredients:
                prompt = (
                    "Identify ALL culinary ingredients visible in this image. "
                    "Return a comma-separated list, with each ingredient in English. "
                    "If there's only one ingredient, return just that one. "
                    "Ignore utensils, plates or containers. "
                    "Example: 'Tomato, Onion, Garlic' or just 'Tomato'"
                )
            else:
                prompt = (
                    "What is this culinary ingredient? "
                    "Respond ONLY with the ingredient name in English "
                    "(ex: 'Tomato', 'Egg', 'Wheat Flour')."
                )
            
            # Usar o sistema unificado de IA
            response_text = analyze_image_with_ai(image_path, prompt)
            ingredients = response_text.strip()
            
            if multiple_ingredients:
                # Limpa e formata a resposta
                ingredients_list = [ing.strip() for ing in ingredients.split(',')]
                ingredients_list = [ing for ing in ingredients_list if ing and ing != ""]
                
                if len(ingredients_list) > 1:
                    print(f"✅ Ingredientes identificados: {', '.join(ingredients_list)}")
                else:
                    print(f"✅ Ingrediente identificado: {ingredients}")
            else:
                print(f"✅ Ingrediente identificado: {ingredients}")
                
            return ingredients
            
        except PermissionError as e:
            print(f"⚠️ Tentativa {tentativa + 1}/{max_tentativas}: Arquivo ainda sendo escrito, aguardando...")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Erro ao analisar imagem: {e}")
            if tentativa == max_tentativas - 1:
                return "Erro"
            time.sleep(1)
    
    print(f"❌ Não foi possível acessar o arquivo após {max_tentativas} tentativas")
    return "Erro"

def find_relevant_recipes(ingredient_name: str, n_results: int = 5) -> dict:
    """
    Busca no banco de dados vetorial (ChromaDB) as receitas 
    mais relevantes para o ingrediente.
    """
    print(f"🔍 Buscando receitas com '{ingredient_name}'...")
    try:
        client = get_db_client()
        collection = client.get_collection(name=config.CHROMA_COLLECTION_NAME)
        
        # Gera um embedding para a consulta (o nome do ingrediente)
        query_embedding = get_text_embedding(ingredient_name)
        
        # Faz a busca no ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas"]
        )
        
        # Retorna tanto os documentos quanto os metadados (páginas)
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0]
        }
        
    except Exception as e:
        print(f"Erro ao buscar no ChromaDB (A coleção 'receitas' existe?): {e}")
        return {'documents': [], 'metadatas': []}

def find_relevant_recipes_multiple_ingredients(ingredients_list: list, n_results: int = 8) -> dict:
    """
    Busca receitas que contenham qualquer um dos ingredientes fornecidos.
    Combina resultados de múltiplas consultas para maior cobertura.
    """
    print(f"🔍 Buscando receitas com ingredientes: {', '.join(ingredients_list)}...")
    
    all_documents = []
    all_metadatas = []
    seen_recipes = set()  # Para evitar duplicatas
    
    try:
        client = get_db_client()
        collection = client.get_collection(name=config.CHROMA_COLLECTION_NAME)
        
        # Busca para cada ingrediente individualmente
        for ingredient in ingredients_list:
            print(f"  🔍 Buscando receitas com '{ingredient}'...")
            
            query_embedding = get_text_embedding(ingredient)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results // len(ingredients_list) + 2,  # Distribui os resultados
                include=["documents", "metadatas"]
            )
            
            # Adiciona resultados únicos
            for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                recipe_id = f"{meta.get('page', '')}-{doc[:50]}"  # ID único baseado na página e conteúdo
                if recipe_id not in seen_recipes:
                    seen_recipes.add(recipe_id)
                    all_documents.append(doc)
                    all_metadatas.append(meta)
        
        # Busca combinada com todos os ingredientes
        combined_query = f"receita com {' '.join(ingredients_list)}"
        print(f"  🔍 Busca combinada: '{combined_query}'...")
        
        combined_embedding = get_text_embedding(combined_query)
        
        combined_results = collection.query(
            query_embeddings=[combined_embedding],
            n_results=min(n_results, 5),
            include=["documents", "metadatas"]
        )
        
        # Adiciona resultados da busca combinada
        for doc, meta in zip(combined_results['documents'][0], combined_results['metadatas'][0]):
            recipe_id = f"{meta.get('page', '')}-{doc[:50]}"
            if recipe_id not in seen_recipes:
                seen_recipes.add(recipe_id)
                all_documents.append(doc)
                all_metadatas.append(meta)
        
        # Limita o número total de resultados
        if len(all_documents) > n_results:
            all_documents = all_documents[:n_results]
            all_metadatas = all_metadatas[:n_results]
        
        print(f"✅ Encontradas {len(all_documents)} receitas relevantes")
        return {
            'documents': all_documents,
            'metadatas': all_metadatas
        }
        
    except Exception as e:
        print(f"Erro ao buscar receitas para múltiplos ingredientes: {e}")
        return {'documents': [], 'metadatas': []}

def generate_recipe_suggestion(ingredient: str, recipes_data: dict) -> str:
    """
    Usa o LLM configurado para gerar a resposta final, usando as
    receitas encontradas como contexto (RAG).
    """
    print("🤖 Gerando sugestão de chef...")
    try:
        documents = recipes_data.get('documents', [])
        metadatas = recipes_data.get('metadatas', [])
        
        if not documents:
            return "Desculpe, não encontrei receitas relevantes para esse ingrediente no livro."
        
        # Cria o contexto com numeração das receitas e páginas
        context_parts = []
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            page_num = meta.get('page_number', 'Desconhecida')
            context_parts.append(f"RECEITA {i+1} (Página {page_num}):\n{doc}")
        
        context_text = "\n\n---\n\n".join(context_parts)
        
        prompt = f"""
        Você é um assistente de culinária gourmet.
        O usuário quer fazer uma receita usando o ingrediente: {ingredient}

        Eu encontrei as seguintes receitas no livro de culinária dele que parecem
        ser relevantes para este ingrediente:

        --- CONTEXTO DO LIVRO ---
        {context_text}
        --- FIM DO CONTEXTO ---

        Com base **apenas** nas receitas do contexto acima, crie uma resposta organizada seguindo este formato:
        
        📋 **RECEITAS ENCONTRADAS COM {ingredient.upper()}:**
        
        1. **Nome da Receita 1** (Página X) - Breve descrição dos pratos principais
        2. **Nome da Receita 2** (Página Y) - Breve descrição dos pratos principais  
        3. **Nome da Receita 3** (Página Z) - Breve descrição dos pratos principais
        (e assim por diante...)
        
        🍽️ **SUGESTÃO DO CHEF:**
        [Sua recomendação de qual receita escolher e por quê]
        
        IMPORTANTE: 
        - Liste até 5 receitas numeradas
        - Inclua sempre a página de cada receita
        - Extraia o nome principal do prato de cada receita
        - Seja conciso e organizado
        """
        
        response_text = get_ai_response(prompt)
        return response_text
        
    except Exception as e:
        print(f"Erro ao gerar resposta final: {e}")
        return "Desculpe, não consegui pensar em uma sugestão no momento."

def generate_recipe_suggestion_multiple(ingredients_list: list, recipes_data: dict) -> str:
    """
    Gera sugestão de receitas para múltiplos ingredientes usando LLM (Gemini).
    """
    print(f"🤖 Gerando sugestão para {len(ingredients_list)} ingredientes...")
    try:
        if not recipes_data['documents']:
            return f"Não foram encontradas receitas para os ingredientes: {', '.join(ingredients_list)}"
        
        # Monta o contexto com as receitas encontradas
        context_text = ""
        for i, (doc, meta) in enumerate(zip(recipes_data['documents'], recipes_data['metadatas'])):
            page = meta.get('page', 'N/A')
            context_text += f"=== RECEITA {i+1} (Página {page}) ===\n{doc}\n\n"
        
        ingredients_str = ', '.join(ingredients_list)
        
        prompt = f"""
        Você é um chef experiente. O usuário tem os seguintes ingredientes: **{ingredients_str}**.
        
        Analise as receitas do contexto abaixo e encontre as que podem ser feitas com esses ingredientes (total ou parcialmente).
        
        --- CONTEXTO DO LIVRO ---
        {context_text}
        --- FIM DO CONTEXTO ---

        Com base **apenas** nas receitas do contexto acima, crie uma resposta organizada seguindo este formato:
        
        📋 **RECEITAS ENCONTRADAS COM {ingredients_str.upper()}:**
        
        🟢 **RECEITAS COMPLETAS** (usam vários dos seus ingredientes):
        1. **Nome da Receita 1** (Página X) - Ingredientes que você tem: [listar]
        
        🟡 **RECEITAS PARCIAIS** (usam alguns dos seus ingredientes):
        2. **Nome da Receita 2** (Página Y) - Ingrediente principal que você tem: [ingrediente]
        
        🍽️ **SUGESTÃO DO CHEF:**
        [Recomendação prioritária baseada nos ingredientes disponíveis, explicando qual receita aproveita melhor seus ingredientes]
        
        💡 **DICA EXTRA:**
        [Sugestão de como combinar os ingredientes ou o que poderia comprar para complementar]
        
        IMPORTANTE: 
        - Priorize receitas que usam múltiplos ingredientes que o usuário possui
        - Seja criativo ao identificar combinações possíveis
        - Inclua sempre a página de cada receita
        - Separe receitas completas de parciais
        """
        
        response_text = get_ai_response(prompt)
        return response_text
        
    except Exception as e:
        print(f"Erro ao gerar resposta para múltiplos ingredientes: {e}")
        return f"Desculpe, não consegui processar a sugestão para {', '.join(ingredients_list)}."

def extract_recipes_for_rating(recipes_response: str) -> list:
    """
    Extrai receitas estruturadas da resposta do chef para permitir avaliações
    
    Args:
        recipes_response: Resposta formatada do chef com receitas
        
    Returns:
        Lista de dicionários com receitas estruturadas
    """
    import re
    
    recipes = []
    
    try:
        # Busca por padrões de receitas numeradas com páginas
        pattern = r'(\d+)\.\s*\*\*([^*]+)\*\*\s*\(Página\s*(\d+)\)\s*-?\s*([^\n]*)'
        matches = re.findall(pattern, recipes_response)
        
        for match in matches:
            number, name, page, description = match
            
            # Limpa o nome da receita
            recipe_name = name.strip()
            if recipe_name:
                recipe_data = {
                    'id': f"{recipe_name}_{page}".replace(' ', '_').lower(),
                    'name': recipe_name,
                    'page': int(page),
                    'description': description.strip(),
                    'number': int(number)
                }
                recipes.append(recipe_data)
        
        # Se não encontrou receitas com o padrão principal, tenta padrão alternativo
        if not recipes:
            alt_pattern = r'(\d+)\.\s*([^(]+)\s*\(Página\s*(\d+)\)'
            alt_matches = re.findall(alt_pattern, recipes_response)
            
            for match in alt_matches:
                number, name, page = match
                recipe_name = name.strip().replace('**', '')
                
                if recipe_name:
                    recipe_data = {
                        'id': f"{recipe_name}_{page}".replace(' ', '_').lower(),
                        'name': recipe_name,
                        'page': int(page),
                        'description': '',
                        'number': int(number)
                    }
                    recipes.append(recipe_data)
    
    except Exception as e:
        print(f"⚠️ Erro ao extrair receitas: {e}")
    
    return recipes

def get_recipe_rating_summary(recipe_name: str, recipe_page: int = None) -> dict:
    """
    Obtém resumo de avaliações para uma receita específica
    
    Args:
        recipe_name: Nome da receita
        recipe_page: Página da receita (opcional)
        
    Returns:
        Dicionário com estatísticas de avaliação
    """
    from . import database
    
    try:
        with database.sqlite3.connect(database.history_db.db_path) as conn:
            cursor = conn.cursor()
            
            # Query base
            query = '''
                SELECT AVG(rating) as avg_rating, 
                       COUNT(*) as total_ratings,
                       COUNT(CASE WHEN rating >= 4 THEN 1 END) as positive_ratings
                FROM recipe_ratings 
                WHERE recipe_name LIKE ?
            '''
            params = [f'%{recipe_name}%']
            
            # Adiciona filtro de página se fornecido
            if recipe_page:
                query += ' AND recipe_page = ?'
                params.append(recipe_page)
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            avg_rating = result[0] if result[0] else 0
            total_ratings = result[1] if result[1] else 0
            positive_ratings = result[2] if result[2] else 0
            
            return {
                'average_rating': round(avg_rating, 1) if avg_rating > 0 else None,
                'total_ratings': total_ratings,
                'positive_percentage': round((positive_ratings / total_ratings * 100), 1) if total_ratings > 0 else 0,
                'stars_display': '⭐' * int(avg_rating) if avg_rating > 0 else '☆☆☆☆☆'
            }
            
    except Exception as e:
        print(f"⚠️ Erro ao obter avaliações: {e}")
        return {
            'average_rating': None,
            'total_ratings': 0,
            'positive_percentage': 0,
            'stars_display': '☆☆☆☆☆'
        }

# Funções de compatibilidade para o monitor.py
def extract_ingredients_from_image(image_path: str, multiple_ingredients: bool = True) -> str:
    """Extrai ingredientes da imagem - compatibilidade com monitor.py"""
    start_time = time.time()
    ingredients = identify_ingredient_from_image(image_path, multiple_ingredients)
    processing_time = time.time() - start_time
    
    # Se não houve erro, registra no banco
    if "Erro" not in ingredients:
        # A resposta completa será registrada pela função find_recipes_by_ingredient
        pass
    
    return ingredients

def find_recipes_by_ingredient(ingredients: str, image_path=None, source_mode: str = "folder") -> str:
    """Busca receitas por ingrediente(s) - compatibilidade com monitor.py"""
    start_time = time.time()
    
    # Verifica se temos múltiplos ingredientes
    if ',' in ingredients:
        ingredients_list = [ing.strip() for ing in ingredients.split(',')]
        ingredients_list = [ing for ing in ingredients_list if ing]
        
        if len(ingredients_list) > 1:
            print(f"🔍 Processando {len(ingredients_list)} ingredientes: {', '.join(ingredients_list)}")
            # Busca receitas para múltiplos ingredientes
            recipes_data = find_relevant_recipes_multiple_ingredients(ingredients_list)
            response = generate_recipe_suggestion_multiple(ingredients_list, recipes_data)
        else:
            # Apenas um ingrediente
            recipes_data = find_relevant_recipes(ingredients_list[0])
            response = generate_recipe_suggestion(ingredients_list[0], recipes_data)
    else:
        # Ingrediente único
        recipes_data = find_relevant_recipes(ingredients)
        response = generate_recipe_suggestion(ingredients, recipes_data)
    
    processing_time = time.time() - start_time
    
    # Registra no banco de dados
    try:
        database.history_db.add_analysis(
            ingredient=ingredients,
            recipes_response=response,
            image_path=image_path,
            source_mode=source_mode,
            processing_time=processing_time
        )
    except Exception as e:
        print(f"⚠️ Erro ao salvar no banco: {e}")
    
    return response

def analyze_recipe_dietary_info(recipe_text: str) -> dict:
    """
    Analisa se uma receita atende a restrições alimentares específicas.
    
    Args:
        recipe_text: Texto da receita para analisar
    
    Returns:
        dict com informações sobre restrições alimentares
    """
    try:
        prompt = f"""
        Analise a seguinte receita e determine quais restrições alimentares ela atende:

        RECEITA:
        {recipe_text}

        Por favor, analise e responda APENAS com um JSON no seguinte formato:
        {{
            "is_vegetarian": true/false,
            "is_vegan": true/false,
            "is_gluten_free": true/false,
            "is_low_carb": true/false,
            "is_diabetic_friendly": true/false,
            "is_lactose_free": true/false,
            "allergens": ["lista", "de", "possíveis", "alérgenos"],
            "confidence": "alta/média/baixa",
            "reasoning": "breve explicação da análise"
        }}

        CRITÉRIOS:
        - Vegetariano: Não contém carne, peixe ou frutos do mar
        - Vegano: Não contém produtos de origem animal (leite, ovos, mel, etc.)
        - Sem glúten: Não contém trigo, centeio, cevada ou aveia contaminada
        - Low carb: Baixo em carboidratos (menos de 20g por porção)
        - Diabético: Sem açúcar refinado, baixo índice glicêmico
        - Sem lactose: Não contém leite ou derivados com lactose
        
        Seja conservador na análise - se houver dúvida, marque como false.
        """
        
        response_text = get_ai_response(prompt)
        
        # Tenta extrair JSON da resposta
        import json
        import re
        
        # Procura por JSON na resposta
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            dietary_info = json.loads(json_str)
            return dietary_info
        else:
            print(f"⚠️ Não foi possível extrair JSON da resposta: {response_text}")
            return {}
            
    except Exception as e:
        print(f"❌ Erro ao analisar restrições alimentares: {e}")
        return {}

def find_recipes_by_dietary_filters(filters: dict) -> list:
    """
    Busca receitas que atendem aos filtros alimentares especificados.
    
    Args:
        filters: Dict com filtros (ex: {'vegetarian': True, 'gluten_free': True})
    
    Returns:
        Lista de receitas que atendem aos filtros
    """
    try:
        # Busca no banco de dados local primeiro
        db_recipes = database.history_db.get_recipes_by_dietary_filter(filters)
        
        if db_recipes:
            return [
                {
                    'name': recipe[0],
                    'page': recipe[1],
                    'vegetarian': recipe[2],
                    'vegan': recipe[3],
                    'gluten_free': recipe[4],
                    'low_carb': recipe[5],
                    'diabetic_friendly': recipe[6],
                    'lactose_free': recipe[7],
                    'allergens': recipe[8]
                }
                for recipe in db_recipes
            ]
        
        # Se não encontrou no banco, busca no ChromaDB com filtros
        filter_terms = []
        if filters.get('vegetarian'):
            filter_terms.append('vegetariano')
        if filters.get('vegan'):
            filter_terms.append('vegano')
        if filters.get('gluten_free'):
            filter_terms.append('sem glúten')
        if filters.get('low_carb'):
            filter_terms.append('low carb')
        if filters.get('diabetic_friendly'):
            filter_terms.append('diabético')
        if filters.get('lactose_free'):
            filter_terms.append('sem lactose')
        
        if not filter_terms:
            return []
        
        # Busca receitas com os termos dos filtros
        search_query = ' '.join(filter_terms)
        recipes_data = find_relevant_recipes(search_query)
        
        return recipes_data
        
    except Exception as e:
        print(f"❌ Erro ao buscar receitas por filtros: {e}")
        return []

def generate_filtered_recipe_suggestions(ingredients: str, dietary_filters: dict) -> str:
    """
    Gera sugestões de receitas considerando ingredientes e filtros alimentares.
    
    Args:
        ingredients: Ingredientes disponíveis
        dietary_filters: Filtros alimentares a aplicar
    
    Returns:
        String com receitas sugeridas considerando os filtros
    """
    try:
        # Primeiro busca receitas relevantes para os ingredientes
        recipes_data = find_relevant_recipes(ingredients)
        
        # Cria prompt incluindo filtros alimentares
        filter_descriptions = []
        if dietary_filters.get('vegetarian'):
            filter_descriptions.append('VEGETARIANO (sem carne, peixe ou frutos do mar)')
        if dietary_filters.get('vegan'):
            filter_descriptions.append('VEGANO (sem produtos de origem animal)')
        if dietary_filters.get('gluten_free'):
            filter_descriptions.append('SEM GLÚTEN (sem trigo, centeio, cevada)')
        if dietary_filters.get('low_carb'):
            filter_descriptions.append('LOW CARB (baixo em carboidratos)')
        if dietary_filters.get('diabetic_friendly'):
            filter_descriptions.append('DIABÉTICO (sem açúcar, baixo IG)')
        if dietary_filters.get('lactose_free'):
            filter_descriptions.append('SEM LACTOSE (sem leite e derivados)')
        
        filters_text = ', '.join(filter_descriptions) if filter_descriptions else 'Nenhum filtro específico'
        
        prompt = f"""
        Você é um chef especializado que deve sugerir receitas usando os ingredientes fornecidos.
        
        INGREDIENTES DISPONÍVEIS: {ingredients}
        
        RESTRIÇÕES ALIMENTARES OBRIGATÓRIAS: {filters_text}
        
        RECEITAS DA BASE DE CONHECIMENTO:
        {recipes_data if recipes_data else "Nenhuma receita específica encontrada na base."}
        
        INSTRUÇÕES:
        1. Sugira 3-4 receitas que usem os ingredientes disponíveis
        2. TODAS as receitas DEVEM atender às restrições alimentares especificadas
        3. Se uma receita da base não atender aos filtros, adapte-a ou sugira alternativa
        4. Seja específico sobre ingredientes de substituição quando necessário
        5. Marque claramente quais restrições cada receita atende
        
        FORMATO DA RESPOSTA:
        ## 🍽️ Receitas Filtradas para: {ingredients}
        
        ### 📋 Filtros Aplicados: {filters_text}
        
        ### Receita 1: [Nome]
        **Restrições atendidas:** [listar filtros]
        **Ingredientes:** [lista completa]
        **Modo de preparo:** [passo a passo]
        **Tempo:** [tempo estimado]
        
        (Repetir para outras receitas)
        
        ### 💡 Dicas de Substituição:
        [Dicas específicas para as restrições aplicadas]
        """
        
        response_text = get_ai_response(prompt)
        return response_text
        
    except Exception as e:
        print(f"❌ Erro ao gerar receitas filtradas: {e}")
        return f"Erro ao processar receitas com filtros: {str(e)}"

def extract_recipe_steps_with_timers(recipe_text: str) -> dict:
    """
    Extrai etapas da receita e sugere timers para cada uma.
    
    Args:
        recipe_text: Texto completo da receita
    
    Returns:
        Dict com etapas e timers sugeridos
    """
    try:        
        prompt = f"""
        Analise a seguinte receita e extraia as etapas que podem se beneficiar de timers:

        RECEITA:
        {recipe_text}

        Por favor, responda APENAS com um JSON no seguinte formato:
        {{
            "recipe_name": "Nome da receita",
            "total_time": 45,
            "steps_with_timers": [
                {{
                    "step_number": 1,
                    "description": "Descrição da etapa",
                    "timer_minutes": 5,
                    "timer_name": "Nome do timer",
                    "is_critical": true
                }}
            ],
            "preparation_tips": [
                "Dica 1 para otimizar o tempo",
                "Dica 2 para organização"
            ]
        }}

        CRITÉRIOS PARA TIMERS:
        - Cozimento no fogo (ferver, refogar, etc.)
        - Tempo no forno
        - Descanso de massas
        - Marinadas
        - Fermentação
        - Qualquer etapa com tempo específico

        Marque como "is_critical": true apenas para etapas onde o tempo é crucial para o resultado.
        """
        
        response_text = get_ai_response(prompt)
        
        # Tenta extrair JSON da resposta
        import json
        import re
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            steps_data = json.loads(json_str)
            return steps_data
        else:
            print(f"⚠️ Não foi possível extrair JSON da resposta: {response_text}")
            return {}
            
    except Exception as e:
        print(f"❌ Erro ao extrair etapas com timers: {e}")
        return {}
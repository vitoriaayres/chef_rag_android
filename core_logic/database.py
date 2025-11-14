import sqlite3
import os
import json
from datetime import datetime
from core_logic import config

class HistoryDatabase:
    """
    Classe para gerenciar o histórico de ingredientes analisados e respostas geradas
    """
    
    def __init__(self):
        self.db_path = os.path.join(config.BASE_DIR, "..", "data", "history.db")
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados criando as tabelas necessárias"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela principal de histórico
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ingredient_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    image_path TEXT,
                    image_name TEXT,
                    ingredient_identified TEXT NOT NULL,
                    recipes_found TEXT,
                    chef_suggestion TEXT,
                    source_mode TEXT NOT NULL,
                    processing_time_seconds REAL
                )
            ''')
            
            # Tabela de estatísticas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_analyses INTEGER DEFAULT 0,
                    webcam_analyses INTEGER DEFAULT 0,
                    folder_analyses INTEGER DEFAULT 0,
                    successful_analyses INTEGER DEFAULT 0,
                    failed_analyses INTEGER DEFAULT 0,
                    last_updated TEXT
                )
            ''')
            
            # Tabela de perfil do usuário
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE DEFAULT 'default_user',
                    name TEXT DEFAULT '',
                    skill_level TEXT DEFAULT 'iniciante',
                    dietary_restrictions TEXT DEFAULT '[]',
                    favorite_cuisines TEXT DEFAULT '[]',
                    allergies TEXT DEFAULT '[]',
                    cooking_equipment TEXT DEFAULT '[]',
                    preferred_cooking_time INTEGER DEFAULT 60,
                    budget_preference TEXT DEFAULT 'medio',
                    health_goals TEXT DEFAULT '[]',
                    created_at TEXT DEFAULT (datetime('now')),
                    updated_at TEXT DEFAULT (datetime('now'))
                )
            ''')
            
            # Tabela de avaliações de receitas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipe_ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT DEFAULT 'default_user',
                    recipe_name TEXT NOT NULL,
                    recipe_page INTEGER,
                    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                    comment TEXT DEFAULT '',
                    ingredients_used TEXT DEFAULT '[]',
                    cooking_time_actual INTEGER,
                    difficulty_perceived TEXT,
                    would_cook_again BOOLEAN DEFAULT TRUE,
                    created_at TEXT DEFAULT (datetime('now'))
                )
            ''')
            
            # Inicializa perfil padrão se não existir
            cursor.execute('''
                INSERT OR IGNORE INTO user_profile (user_id) VALUES ('default_user')
            ''')
            
            # Inicializa estatísticas se não existirem
            cursor.execute('SELECT COUNT(*) FROM statistics')
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO statistics (total_analyses, webcam_analyses, folder_analyses, 
                                          successful_analyses, failed_analyses, last_updated)
                    VALUES (0, 0, 0, 0, 0, ?)
                ''', (datetime.now().isoformat(),))
            
            conn.commit()
    
    def add_analysis(self, ingredient, recipes_response, image_path=None, 
                    source_mode="folder", processing_time=0.0):
        """
        Adiciona uma nova análise ao histórico
        
        Args:
            ingredient (str): Ingrediente identificado
            recipes_response (str): Resposta das receitas gerada
            image_path (str): Caminho da imagem analisada
            source_mode (str): Modo de captura ('webcam' ou 'folder')
            processing_time (float): Tempo de processamento em segundos
        """
        timestamp = datetime.now().isoformat()
        image_name = os.path.basename(image_path) if image_path else None
        
        # Determina se foi bem-sucedida
        success = "Erro" not in ingredient and recipes_response is not None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Adiciona o registro
            cursor.execute('''
                INSERT INTO ingredient_history 
                (timestamp, image_path, image_name, ingredient_identified, 
                 recipes_found, chef_suggestion, source_mode, processing_time_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, image_path, image_name, ingredient, 
                  None, recipes_response, source_mode, processing_time))
            
            # Atualiza estatísticas
            cursor.execute('''
                UPDATE statistics SET 
                    total_analyses = total_analyses + 1,
                    webcam_analyses = webcam_analyses + ?,
                    folder_analyses = folder_analyses + ?,
                    successful_analyses = successful_analyses + ?,
                    failed_analyses = failed_analyses + ?,
                    last_updated = ?
            ''', (
                1 if source_mode == "webcam" else 0,
                1 if source_mode == "folder" else 0,
                1 if success else 0,
                0 if success else 1,
                timestamp
            ))
            
            conn.commit()
            
        print(f"📝 Análise salva no histórico: {ingredient}")
    
    def get_recent_analyses(self, limit=10):
        """Retorna as análises mais recentes"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, image_name, ingredient_identified, 
                       chef_suggestion, source_mode, processing_time_seconds
                FROM ingredient_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            return cursor.fetchall()
    
    def get_ingredient_count(self, ingredient):
        """Retorna quantas vezes um ingrediente foi analisado"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM ingredient_history 
                WHERE ingredient_identified = ?
            ''', (ingredient,))
            
            return cursor.fetchone()[0]
    
    def get_statistics(self):
        """Retorna estatísticas gerais"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT total_analyses, webcam_analyses, folder_analyses,
                       successful_analyses, failed_analyses, last_updated
                FROM statistics LIMIT 1
            ''')
            
            result = cursor.fetchone()
            if result:
                return {
                    'total_analyses': result[0],
                    'webcam_analyses': result[1],
                    'folder_analyses': result[2],
                    'successful_analyses': result[3],
                    'failed_analyses': result[4],
                    'last_updated': result[5]
                }
            return None
    
    def get_all_ingredients(self):
        """Retorna lista de todos os ingredientes únicos analisados"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ingredient_identified, COUNT(*) as count
                FROM ingredient_history 
                WHERE ingredient_identified NOT LIKE '%Erro%'
                GROUP BY ingredient_identified
                ORDER BY count DESC
            ''')
            
            return cursor.fetchall()
    
    def search_by_ingredient(self, ingredient_name):
        """Busca análises por nome do ingrediente"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, image_name, chef_suggestion, source_mode
                FROM ingredient_history 
                WHERE ingredient_identified LIKE ?
                ORDER BY timestamp DESC
            ''', (f'%{ingredient_name}%',))
            
            return cursor.fetchall()
    
    def export_history_to_json(self, output_file=None):
        """Exporta todo o histórico para um arquivo JSON"""
        if not output_file:
            output_file = os.path.join(config.BASE_DIR, "..", "data", "history_export.json")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM ingredient_history ORDER BY timestamp DESC
            ''')
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            history_data = []
            for row in rows:
                history_data.append(dict(zip(columns, row)))
            
            # Adiciona estatísticas
            stats = self.get_statistics()
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'statistics': stats,
                'history': history_data
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Histórico exportado para: {output_file}")
            return output_file
    
    def show_summary(self):
        """Exibe um resumo do histórico"""
        stats = self.get_statistics()
        ingredients = self.get_all_ingredients()
        
        print("\n" + "="*50)
        print("📊 RESUMO DO HISTÓRICO DE ANÁLISES")
        print("="*50)
        
        if stats:
            print(f"🔢 Total de análises: {stats['total_analyses']}")
            print(f"📷 Webcam: {stats['webcam_analyses']}")
            print(f"📁 Pasta: {stats['folder_analyses']}")
            print(f"✅ Sucessos: {stats['successful_analyses']}")
            print(f"❌ Falhas: {stats['failed_analyses']}")
            
            if stats['total_analyses'] > 0:
                success_rate = (stats['successful_analyses'] / stats['total_analyses']) * 100
                print(f"📈 Taxa de sucesso: {success_rate:.1f}%")
        
        print(f"\n🥕 INGREDIENTES MAIS ANALISADOS:")
        for i, (ingredient, count) in enumerate(ingredients[:5], 1):
            print(f"{i}. {ingredient}: {count} vez(es)")
        
        print("="*50)

    # === MÉTODOS DE PERFIL DO USUÁRIO ===
    
    def get_user_profile(self, user_id='default_user'):
        """Obtém o perfil do usuário"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM user_profile WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                profile = dict(zip(columns, row))
                # Converte strings JSON de volta para listas
                for field in ['dietary_restrictions', 'favorite_cuisines', 'allergies', 'cooking_equipment', 'health_goals']:
                    profile[field] = json.loads(profile[field])
                return profile
            return None
    
    def update_user_profile(self, user_id='default_user', **kwargs):
        """Atualiza o perfil do usuário"""
        # Campos que devem ser convertidos para JSON
        json_fields = ['dietary_restrictions', 'favorite_cuisines', 'allergies', 'cooking_equipment', 'health_goals']
        
        # Converte listas para JSON
        for field in json_fields:
            if field in kwargs and isinstance(kwargs[field], list):
                kwargs[field] = json.dumps(kwargs[field])
        
        # Adiciona timestamp de atualização
        kwargs['updated_at'] = datetime.now().isoformat()
        
        # Constrói a query dinamicamente
        if kwargs:
            fields = ', '.join([f'{key} = ?' for key in kwargs.keys()])
            values = list(kwargs.values()) + [user_id]
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    UPDATE user_profile SET {fields} WHERE user_id = ?
                ''', values)
                
                if cursor.rowcount == 0:
                    # Se usuário não existe, cria um novo
                    kwargs['user_id'] = user_id
                    kwargs['created_at'] = datetime.now().isoformat()
                    
                    fields_str = ', '.join(kwargs.keys())
                    placeholders = ', '.join(['?' for _ in kwargs])
                    
                    cursor.execute(f'''
                        INSERT INTO user_profile ({fields_str}) VALUES ({placeholders})
                    ''', list(kwargs.values()))
    
    def add_recipe_rating(self, recipe_name, rating, user_id='default_user', **kwargs):
        """Adiciona avaliação de uma receita"""
        rating_data = {
            'user_id': user_id,
            'recipe_name': recipe_name,
            'rating': rating,
            'created_at': datetime.now().isoformat()
        }
        rating_data.update(kwargs)
        
        # Converte ingredientes para JSON se for lista
        if 'ingredients_used' in rating_data and isinstance(rating_data['ingredients_used'], list):
            rating_data['ingredients_used'] = json.dumps(rating_data['ingredients_used'])
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            fields = ', '.join(rating_data.keys())
            placeholders = ', '.join(['?' for _ in rating_data])
            
            cursor.execute(f'''
                INSERT INTO recipe_ratings ({fields}) VALUES ({placeholders})
            ''', list(rating_data.values()))
    
    def get_user_recipe_ratings(self, user_id='default_user', limit=10):
        """Obtém avaliações de receitas do usuário"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT recipe_name, rating, comment, created_at, ingredients_used
                FROM recipe_ratings 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            rows = cursor.fetchall()
            ratings = []
            for row in rows:
                rating_data = {
                    'recipe_name': row[0],
                    'rating': row[1],
                    'comment': row[2],
                    'created_at': row[3],
                    'ingredients_used': json.loads(row[4]) if row[4] else []
                }
                ratings.append(rating_data)
            
            return ratings
    
    def get_user_preferences_summary(self, user_id='default_user'):
        """Obtém resumo das preferências do usuário baseado no histórico"""
        profile = self.get_user_profile(user_id)
        if not profile:
            return None
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Ingredientes mais usados
            cursor.execute('''
                SELECT ingredient_identified, COUNT(*) as count
                FROM ingredient_history 
                WHERE ingredient_identified NOT LIKE '%Erro%'
                GROUP BY ingredient_identified
                ORDER BY count DESC
                LIMIT 5
            ''')
            top_ingredients = cursor.fetchall()
            
            # Média de avaliações
            cursor.execute('''
                SELECT AVG(rating) as avg_rating, COUNT(*) as total_ratings
                FROM recipe_ratings 
                WHERE user_id = ?
            ''', (user_id,))
            rating_stats = cursor.fetchone()
            
            return {
                'profile': profile,
                'top_ingredients': top_ingredients,
                'avg_rating': rating_stats[0] if rating_stats[0] else 0,
                'total_ratings': rating_stats[1] if rating_stats[1] else 0
            }

    def init_additional_tables(self):
        """Inicializa tabelas adicionais para filtros alimentares e timers"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela para filtros alimentares das receitas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipe_dietary_filters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_name TEXT NOT NULL,
                    recipe_page INTEGER,
                    is_vegetarian BOOLEAN DEFAULT 0,
                    is_vegan BOOLEAN DEFAULT 0,
                    is_gluten_free BOOLEAN DEFAULT 0,
                    is_low_carb BOOLEAN DEFAULT 0,
                    is_diabetic_friendly BOOLEAN DEFAULT 0,
                    is_lactose_free BOOLEAN DEFAULT 0,
                    allergens TEXT DEFAULT '',
                    created_at TEXT DEFAULT (datetime('now')),
                    UNIQUE(recipe_name, recipe_page)
                )
            ''')
            
            # Tabela para timers ativos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipe_timers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timer_name TEXT NOT NULL,
                    recipe_name TEXT DEFAULT '',
                    step_description TEXT DEFAULT '',
                    duration_minutes INTEGER NOT NULL,
                    start_time TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    user_id TEXT DEFAULT 'default_user',
                    created_at TEXT DEFAULT (datetime('now'))
                )
            ''')
            
            conn.commit()

    def add_recipe_dietary_info(self, recipe_name, recipe_page, is_vegetarian=False, is_vegan=False, 
                               is_gluten_free=False, is_low_carb=False, is_diabetic_friendly=False,
                               is_lactose_free=False, allergens=''):
        """Adiciona informações alimentares de uma receita"""
        self.init_additional_tables()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO recipe_dietary_filters 
                (recipe_name, recipe_page, is_vegetarian, is_vegan, is_gluten_free, 
                 is_low_carb, is_diabetic_friendly, is_lactose_free, allergens)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (recipe_name, recipe_page, is_vegetarian, is_vegan, is_gluten_free,
                  is_low_carb, is_diabetic_friendly, is_lactose_free, allergens))
            conn.commit()
            return cursor.lastrowid

    def get_recipes_by_dietary_filter(self, filters):
        """Busca receitas por filtros alimentares"""
        self.init_additional_tables()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            conditions = []
            
            if filters.get('vegetarian'):
                conditions.append('is_vegetarian = 1')
            if filters.get('vegan'):
                conditions.append('is_vegan = 1')
            if filters.get('gluten_free'):
                conditions.append('is_gluten_free = 1')
            if filters.get('low_carb'):
                conditions.append('is_low_carb = 1')
            if filters.get('diabetic_friendly'):
                conditions.append('is_diabetic_friendly = 1')
            if filters.get('lactose_free'):
                conditions.append('is_lactose_free = 1')
            
            if not conditions:
                return []
            
            query = f'''
                SELECT recipe_name, recipe_page, is_vegetarian, is_vegan, is_gluten_free,
                       is_low_carb, is_diabetic_friendly, is_lactose_free, allergens
                FROM recipe_dietary_filters 
                WHERE {' AND '.join(conditions)}
                ORDER BY recipe_name
            '''
            
            cursor.execute(query)
            return cursor.fetchall()

    def add_timer(self, timer_name, recipe_name='', step_description='', duration_minutes=0, user_id='default_user'):
        """Adiciona um novo timer"""
        self.init_additional_tables()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            start_time = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO recipe_timers 
                (timer_name, recipe_name, step_description, duration_minutes, start_time, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timer_name, recipe_name, step_description, duration_minutes, start_time, user_id))
            conn.commit()
            return cursor.lastrowid

    def get_active_timers(self, user_id='default_user'):
        """Busca timers ativos"""
        self.init_additional_tables()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, timer_name, recipe_name, step_description, duration_minutes, 
                       start_time, created_at
                FROM recipe_timers 
                WHERE is_active = 1 AND user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
            return cursor.fetchall()

    def stop_timer(self, timer_id):
        """Para um timer"""
        self.init_additional_tables()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE recipe_timers 
                SET is_active = 0 
                WHERE id = ?
            ''', (timer_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_all_timers(self, user_id='default_user'):
        """Busca todos os timers (ativos e inativos)"""
        self.init_additional_tables()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, timer_name, recipe_name, step_description, duration_minutes, 
                       start_time, is_active, created_at
                FROM recipe_timers 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT 20
            ''', (user_id,))
            return cursor.fetchall()

# Instância global do banco de dados
history_db = HistoryDatabase()
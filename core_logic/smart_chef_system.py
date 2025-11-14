"""
Sistema Simplificado de IA para Chef RAG - Inspirado em LangChain/LangGraph

Esta implementação simula os conceitos do LangChain/LangGraph sem dependências externas complexas,
fornecendo funcionalidades avançadas usando apenas o sistema existente.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field

# ======================= CONCEPTS INSPIRADOS EM LANGCHAIN =======================

@dataclass
class ChefMemory:
    """Sistema de memória conversacional inspirado no ConversationBufferMemory"""
    messages: List[Dict[str, str]] = field(default_factory=list)
    max_messages: int = 10
    
    def add_message(self, role: str, content: str):
        """Adiciona mensagem à memória"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Manter apenas últimas N mensagens
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_context(self) -> str:
        """Retorna contexto da conversa"""
        context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.messages[-5:]  # Últimas 5 mensagens
        ])
        return context

@dataclass
class ChefTool:
    """Ferramenta do sistema inspirada no BaseTool do LangChain"""
    name: str
    description: str
    function: callable
    
    def run(self, *args, **kwargs):
        """Executa a ferramenta"""
        try:
            return self.function(*args, **kwargs)
        except Exception as e:
            return f"Erro na ferramenta {self.name}: {str(e)}"

class ChefAgent:
    """Agente inspirado no sistema de agents do LangChain"""
    
    def __init__(self):
        self.memory = ChefMemory()
        self.tools = self._create_tools()
        print("🤖 Chef Agent inicializado com ferramentas personalizadas")
    
    def _create_tools(self) -> List[ChefTool]:
        """Cria ferramentas disponíveis para o agente"""
        return [
            ChefTool(
                name="analyze_image",
                description="Analisa ingredientes em imagens",
                function=self._analyze_image_tool
            ),
            ChefTool(
                name="search_recipes",
                description="Busca receitas baseadas em ingredientes",
                function=self._search_recipes_tool
            ),
            ChefTool(
                name="calculate_nutrition",
                description="Calcula informações nutricionais",
                function=self._calculate_nutrition_tool
            ),
            ChefTool(
                name="manage_timer",
                description="Gerencia timers de cozinha",
                function=self._manage_timer_tool
            ),
            ChefTool(
                name="generate_shopping_list",
                description="Gera lista de compras",
                function=self._generate_shopping_list_tool
            )
        ]
    
    def _analyze_image_tool(self, image_path: str) -> str:
        """Ferramenta de análise de imagem"""
        try:
            from core_logic.rag_system import identify_ingredient_from_image
            result = identify_ingredient_from_image(image_path, multiple_ingredients=True)
            return f"Ingredientes detectados: {result}"
        except Exception as e:
            return f"Erro na análise: {str(e)}"
    
    def _search_recipes_tool(self, ingredients: str) -> str:
        """Ferramenta de busca de receitas"""
        try:
            # Simular busca inteligente
            ingredient_list = [ing.strip() for ing in ingredients.split(',')]
            
            recipes = []
            for ingredient in ingredient_list[:3]:
                recipe = {
                    "name": f"Receita Especial com {ingredient}",
                    "prep_time": "25-30 min",
                    "difficulty": "Médio",
                    "rating": "4.5/5"
                }
                recipes.append(recipe)
            
            return json.dumps(recipes, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Erro na busca: {str(e)}"
    
    def _calculate_nutrition_tool(self, ingredients: str) -> str:
        """Ferramenta de cálculo nutricional"""
        try:
            # Simular cálculo nutricional inteligente
            ingredient_count = len(ingredients.split(','))
            nutrition = {
                "calorias_estimadas": ingredient_count * 80,
                "proteinas": f"{ingredient_count * 12}g",
                "carboidratos": f"{ingredient_count * 15}g",
                "gorduras": f"{ingredient_count * 6}g",
                "fibras": f"{ingredient_count * 3}g"
            }
            return json.dumps(nutrition, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Erro no cálculo: {str(e)}"
    
    def _manage_timer_tool(self, action: str) -> str:
        """Ferramenta de gerenciamento de timer"""
        try:
            if "criar" in action.lower() or "timer" in action.lower():
                return "⏰ Timer criado com sucesso para a receita"
            elif "parar" in action.lower():
                return "⏹️ Timer pausado"
            else:
                return "⏱️ Timer gerenciado"
        except Exception as e:
            return f"Erro no timer: {str(e)}"
    
    def _generate_shopping_list_tool(self, ingredients: str) -> str:
        """Ferramenta de lista de compras"""
        try:
            ingredient_list = [ing.strip() for ing in ingredients.split(',')]
            
            # Adicionar ingredientes complementares inteligentemente
            smart_additions = []
            for ingredient in ingredient_list:
                if "tomate" in ingredient.lower():
                    smart_additions.extend(["cebola", "alho", "azeite"])
                elif "ovo" in ingredient.lower():
                    smart_additions.extend(["sal", "manteiga"])
                elif "frango" in ingredient.lower():
                    smart_additions.extend(["limão", "temperos"])
            
            complete_list = list(set(ingredient_list + smart_additions))
            
            return "🛒 Lista de Compras:\n" + "\n".join([f"• {item}" for item in complete_list])
            
        except Exception as e:
            return f"Erro na lista: {str(e)}"
    
    def process_query(self, user_input: str, image_path: Optional[str] = None) -> str:
        """Processa query do usuário usando as ferramentas disponíveis"""
        
        # Adicionar à memória
        self.memory.add_message("user", user_input)
        
        # Analisar a intenção do usuário
        intent = self._analyze_intent(user_input, image_path)
        
        # Executar ferramentas baseadas na intenção
        response_parts = []
        
        if intent["analyze_image"] and image_path:
            tool_result = self.tools[0].run(image_path)
            response_parts.append(f"📸 {tool_result}")
        
        if intent["search_recipes"]:
            ingredients = intent.get("ingredients", user_input)
            tool_result = self.tools[1].run(ingredients)
            response_parts.append(f"🍽️ Receitas encontradas:\n{tool_result}")
        
        if intent["calculate_nutrition"]:
            ingredients = intent.get("ingredients", user_input)
            tool_result = self.tools[2].run(ingredients)
            response_parts.append(f"📊 Informações Nutricionais:\n{tool_result}")
        
        if intent["manage_timer"]:
            tool_result = self.tools[3].run(user_input)
            response_parts.append(f"⏰ {tool_result}")
        
        if intent["shopping_list"]:
            ingredients = intent.get("ingredients", user_input)
            tool_result = self.tools[4].run(ingredients)
            response_parts.append(tool_result)
        
        # Gerar resposta final
        if not response_parts:
            response = f"🤖 Entendi que você quer saber sobre: {user_input}"
        else:
            response = "\n\n".join(response_parts)
        
        # Adicionar à memória
        self.memory.add_message("assistant", response)
        
        return response
    
    def _analyze_intent(self, user_input: str, image_path: Optional[str] = None) -> Dict[str, Any]:
        """Analisa intenção do usuário (simula NLU do LangChain)"""
        user_lower = user_input.lower()
        
        intent = {
            "analyze_image": bool(image_path) or "imagem" in user_lower or "foto" in user_lower,
            "search_recipes": "receita" in user_lower or "como fazer" in user_lower,
            "calculate_nutrition": "nutri" in user_lower or "caloria" in user_lower,
            "manage_timer": "timer" in user_lower or "cronômetro" in user_lower,
            "shopping_list": "compra" in user_lower or "lista" in user_lower,
            "ingredients": self._extract_ingredients(user_input)
        }
        
        return intent
    
    def _extract_ingredients(self, text: str) -> str:
        """Extrai ingredientes do texto (simula NER)"""
        # Lista de ingredientes conhecidos
        known_ingredients = [
            "tomate", "cebola", "alho", "ovo", "frango", "carne", "peixe",
            "batata", "cenoura", "brócolis", "arroz", "feijão", "macarrão",
            "queijo", "leite", "manteiga", "azeite", "sal", "pimenta"
        ]
        
        found_ingredients = []
        text_lower = text.lower()
        
        for ingredient in known_ingredients:
            if ingredient in text_lower:
                found_ingredients.append(ingredient)
        
        return ", ".join(found_ingredients) if found_ingredients else text

# ======================= WORKFLOW INSPIRADO EM LANGGRAPH =======================

@dataclass
class WorkflowState:
    """Estado do workflow inspirado no StateGraph"""
    user_input: str = ""
    image_path: Optional[str] = None
    detected_ingredients: List[str] = field(default_factory=list)
    suggested_recipes: List[Dict] = field(default_factory=list)
    nutritional_info: Dict = field(default_factory=dict)
    shopping_list: List[str] = field(default_factory=list)
    timeline: Dict = field(default_factory=dict)
    final_response: str = ""
    step_count: int = 0

class ChefWorkflow:
    """Sistema de workflow inspirado no LangGraph"""
    
    def __init__(self):
        self.steps = [
            ("analyze_input", self._analyze_input_step),
            ("process_image", self._process_image_step),
            ("search_recipes", self._search_recipes_step),
            ("calculate_nutrition", self._calculate_nutrition_step),
            ("generate_shopping_list", self._generate_shopping_list_step),
            ("create_timeline", self._create_timeline_step),
            ("generate_response", self._generate_response_step)
        ]
        print("🕸️ Chef Workflow inicializado com 7 etapas")
    
    def _analyze_input_step(self, state: WorkflowState) -> WorkflowState:
        """Etapa 1: Análise da entrada"""
        print("🔍 Etapa 1: Analisando entrada do usuário...")
        
        if state.user_input:
            # Extrair ingredientes do texto
            known_ingredients = ["tomate", "ovo", "frango", "cebola", "alho"]
            found = [ing for ing in known_ingredients if ing in state.user_input.lower()]
            state.detected_ingredients.extend(found)
        
        state.step_count += 1
        return state
    
    def _process_image_step(self, state: WorkflowState) -> WorkflowState:
        """Etapa 2: Processar imagem se disponível"""
        print("📸 Etapa 2: Processando imagem...")
        
        if state.image_path:
            try:
                from core_logic.rag_system import identify_ingredient_from_image
                ingredients = identify_ingredient_from_image(state.image_path, multiple_ingredients=True)
                
                if isinstance(ingredients, str):
                    ingredient_list = [ing.strip() for ing in ingredients.split(',')]
                    state.detected_ingredients.extend(ingredient_list)
            except Exception as e:
                print(f"Erro na imagem: {e}")
                state.detected_ingredients.append("ingrediente_exemplo")
        
        state.step_count += 1
        return state
    
    def _search_recipes_step(self, state: WorkflowState) -> WorkflowState:
        """Etapa 3: Buscar receitas"""
        print("🍽️ Etapa 3: Buscando receitas...")
        
        for ingredient in state.detected_ingredients[:3]:  # Máximo 3
            recipe = {
                "name": f"Receita Gourmet com {ingredient.title()}",
                "prep_time": "30 min",
                "difficulty": "Médio",
                "ingredients": state.detected_ingredients,
                "rating": 4.5
            }
            state.suggested_recipes.append(recipe)
        
        state.step_count += 1
        return state
    
    def _calculate_nutrition_step(self, state: WorkflowState) -> WorkflowState:
        """Etapa 4: Calcular nutrição"""
        print("📊 Etapa 4: Calculando informações nutricionais...")
        
        ingredient_count = len(state.detected_ingredients)
        state.nutritional_info = {
            "total_calories": ingredient_count * 120,
            "protein": f"{ingredient_count * 15}g",
            "carbs": f"{ingredient_count * 20}g",
            "fat": f"{ingredient_count * 8}g",
            "fiber": f"{ingredient_count * 4}g"
        }
        
        state.step_count += 1
        return state
    
    def _generate_shopping_list_step(self, state: WorkflowState) -> WorkflowState:
        """Etapa 5: Gerar lista de compras"""
        print("🛒 Etapa 5: Gerando lista de compras...")
        
        base_items = state.detected_ingredients.copy()
        
        # Adicionar itens complementares
        complementary = ["sal", "azeite", "cebola", "alho"]
        for item in complementary:
            if item not in base_items:
                base_items.append(item)
        
        state.shopping_list = base_items
        
        state.step_count += 1
        return state
    
    def _create_timeline_step(self, state: WorkflowState) -> WorkflowState:
        """Etapa 6: Criar cronograma"""
        print("⏰ Etapa 6: Criando cronograma...")
        
        state.timeline = {
            "prep_time": "15 min",
            "cook_time": "25 min",
            "total_time": "40 min",
            "steps": [
                "Preparar ingredientes (15 min)",
                "Cozinhar (20 min)",
                "Finalizar e servir (5 min)"
            ]
        }
        
        state.step_count += 1
        return state
    
    def _generate_response_step(self, state: WorkflowState) -> WorkflowState:
        """Etapa 7: Gerar resposta final"""
        print("📝 Etapa 7: Gerando resposta final...")
        
        response = f"""
🧑‍🍳 **CHEF RAG - ANÁLISE COMPLETA**

📍 **Ingredientes Detectados:**
{', '.join(state.detected_ingredients) if state.detected_ingredients else 'Nenhum ingrediente específico detectado'}

🍽️ **Receitas Sugeridas:**
{chr(10).join([f"• {recipe['name']} ({recipe['prep_time']})" for recipe in state.suggested_recipes]) if state.suggested_recipes else '• Receitas básicas disponíveis'}

📊 **Informação Nutricional:**
• Calorias: {state.nutritional_info.get('total_calories', 'N/A')}
• Proteína: {state.nutritional_info.get('protein', 'N/A')}
• Carboidratos: {state.nutritional_info.get('carbs', 'N/A')}

🛒 **Lista de Compras:**
{chr(10).join([f"• {item}" for item in state.shopping_list[:6]]) if state.shopping_list else '• Lista básica de ingredientes'}

⏰ **Cronograma de Preparo:**
• Tempo Total: {state.timeline.get('total_time', '30 min')}
• Preparação: {state.timeline.get('prep_time', '15 min')}

✨ **Processado em {state.step_count} etapas com workflow inteligente!**
        """
        
        state.final_response = response.strip()
        state.step_count += 1
        return state
    
    def execute(self, user_input: str = "", image_path: Optional[str] = None) -> str:
        """Executa o workflow completo"""
        print("🚀 Iniciando workflow Chef RAG...")
        
        # Estado inicial
        state = WorkflowState(
            user_input=user_input,
            image_path=image_path
        )
        
        # Executar todas as etapas
        for step_name, step_function in self.steps:
            try:
                state = step_function(state)
                time.sleep(0.1)  # Simular processamento
            except Exception as e:
                print(f"❌ Erro na etapa {step_name}: {e}")
                continue
        
        print("✅ Workflow concluído!")
        return state.final_response

# ======================= SISTEMA RAG SIMPLIFICADO =======================

class SimpleRAGSystem:
    """Sistema RAG simplificado inspirado no LangChain"""
    
    def __init__(self):
        self.knowledge_base = self._create_knowledge_base()
        self.embeddings_cache = {}
        print("📚 Sistema RAG simplificado inicializado")
    
    def _create_knowledge_base(self) -> List[Dict]:
        """Cria base de conhecimento de receitas"""
        return [
            {
                "title": "Omelete Perfeita",
                "ingredients": ["ovo", "sal", "manteiga", "queijo"],
                "instructions": "Bata os ovos, tempere, aqueça a manteiga, cozinhe e adicione queijo.",
                "category": "café da manhã",
                "prep_time": "10 min"
            },
            {
                "title": "Salada de Tomate",
                "ingredients": ["tomate", "cebola", "azeite", "sal"],
                "instructions": "Corte os tomates, adicione cebola, tempere com azeite e sal.",
                "category": "salada",
                "prep_time": "5 min"
            },
            {
                "title": "Frango Grelhado",
                "ingredients": ["frango", "alho", "limão", "sal", "pimenta"],
                "instructions": "Tempere o frango, marine por 30 min, grelhe até dourar.",
                "category": "prato principal",
                "prep_time": "45 min"
            }
        ]
    
    def search_similar_recipes(self, query: str, top_k: int = 3) -> List[Dict]:
        """Busca receitas similares (simula similarity search)"""
        query_lower = query.lower()
        
        scored_recipes = []
        for recipe in self.knowledge_base:
            score = 0
            
            # Pontuação por ingredientes
            for ingredient in recipe["ingredients"]:
                if ingredient in query_lower:
                    score += 3
            
            # Pontuação por título
            if any(word in recipe["title"].lower() for word in query_lower.split()):
                score += 2
            
            # Pontuação por categoria
            if recipe["category"] in query_lower:
                score += 1
            
            if score > 0:
                scored_recipes.append((recipe, score))
        
        # Ordenar por pontuação
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        
        return [recipe for recipe, score in scored_recipes[:top_k]]
    
    def generate_response(self, query: str, recipes: List[Dict]) -> str:
        """Gera resposta baseada nas receitas encontradas"""
        if not recipes:
            return f"Não encontrei receitas específicas para '{query}', mas posso sugerir receitas básicas."
        
        response = f"🔍 **Encontrei {len(recipes)} receita(s) para '{query}':**\n\n"
        
        for i, recipe in enumerate(recipes, 1):
            response += f"**{i}. {recipe['title']}**\n"
            response += f"• Ingredientes: {', '.join(recipe['ingredients'])}\n"
            response += f"• Preparo: {recipe['prep_time']}\n"
            response += f"• Categoria: {recipe['category']}\n"
            response += f"• Como fazer: {recipe['instructions']}\n\n"
        
        return response
    
    def query(self, question: str) -> str:
        """Interface principal para consultas"""
        recipes = self.search_similar_recipes(question)
        return self.generate_response(question, recipes)

# ======================= INTERFACES SIMPLIFICADAS =======================

# Instâncias globais
chef_agent = ChefAgent()
chef_workflow = ChefWorkflow()
simple_rag = SimpleRAGSystem()

def process_with_smart_agent(user_input: str, image_path: Optional[str] = None) -> str:
    """Interface para usar o agente inteligente"""
    return chef_agent.process_query(user_input, image_path)

def process_with_smart_workflow(user_input: str = "", image_path: Optional[str] = None) -> str:
    """Interface para usar o workflow inteligente"""
    return chef_workflow.execute(user_input, image_path)

def query_with_smart_rag(question: str) -> str:
    """Interface para usar o sistema RAG simplificado"""
    return simple_rag.query(question)

def get_smart_system_status() -> Dict[str, bool]:
    """Status dos sistemas inteligentes"""
    return {
        "smart_agent": True,
        "smart_workflow": True,
        "smart_rag": True,
        "memory_system": True
    }
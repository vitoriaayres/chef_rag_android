"""
Sistema de Workflows Culinários usando LangGraph
"""

from langgraph.graph import StateGraph, END
from langgraph_checkpoint_sqlite import SqliteSaver
from typing import TypedDict, Annotated
import operator
from datetime import datetime
import json

class ChefWorkflowState(TypedDict):
    """Estado do workflow culinário"""
    user_input: str
    image_path: str
    detected_ingredients: list[str]
    user_preferences: dict
    dietary_restrictions: list[str]
    suggested_recipes: list[dict]
    nutritional_info: dict
    shopping_list: list[str]
    cooking_timeline: dict
    final_response: str
    step_count: Annotated[int, operator.add]

class ChefWorkflow:
    """Workflow principal do Chef RAG com LangGraph"""
    
    def __init__(self):
        """Inicializa o workflow"""
        self.graph = self._create_workflow_graph()
        
        # Configurar checkpoint para persistência
        self.checkpointer = SqliteSaver.from_conn_string("chef_workflow.db")
        
        # Compilar o grafo
        self.app = self.graph.compile(checkpointer=self.checkpointer)
    
    def _create_workflow_graph(self) -> StateGraph:
        """Cria o grafo do workflow"""
        workflow = StateGraph(ChefWorkflowState)
        
        # Definir nós do workflow
        workflow.add_node("analyze_image", self.analyze_image_node)
        workflow.add_node("get_user_profile", self.get_user_profile_node)
        workflow.add_node("search_recipes", self.search_recipes_node)
        workflow.add_node("calculate_nutrition", self.calculate_nutrition_node)
        workflow.add_node("generate_shopping_list", self.generate_shopping_list_node)
        workflow.add_node("create_timeline", self.create_timeline_node)
        workflow.add_node("generate_response", self.generate_response_node)
        
        # Definir o fluxo
        workflow.set_entry_point("analyze_image")
        workflow.add_edge("analyze_image", "get_user_profile")
        workflow.add_edge("get_user_profile", "search_recipes")
        workflow.add_edge("search_recipes", "calculate_nutrition")
        workflow.add_edge("calculate_nutrition", "generate_shopping_list")
        workflow.add_edge("generate_shopping_list", "create_timeline")
        workflow.add_edge("create_timeline", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow
    
    def analyze_image_node(self, state: ChefWorkflowState) -> dict:
        """Nó para análise de imagem"""
        print("🔍 Analisando imagem...")
        
        try:
            if state.get("image_path"):
                from core_logic.rag_system import identify_ingredient_from_image
                ingredients = identify_ingredient_from_image(state["image_path"], multiple_ingredients=True)
                
                # Processar resultado
                if isinstance(ingredients, str):
                    ingredient_list = [ing.strip() for ing in ingredients.split(',')]
                else:
                    ingredient_list = ingredients if isinstance(ingredients, list) else [str(ingredients)]
                
                return {
                    "detected_ingredients": ingredient_list,
                    "step_count": 1
                }
            else:
                # Processar entrada de texto
                user_input = state.get("user_input", "")
                ingredients = [word for word in user_input.split() if len(word) > 3]
                
                return {
                    "detected_ingredients": ingredients[:3],  # Máximo 3 ingredientes
                    "step_count": 1
                }
                
        except Exception as e:
            print(f"Erro na análise: {e}")
            return {
                "detected_ingredients": ["Tomate"],  # Fallback
                "step_count": 1
            }
    
    def get_user_profile_node(self, state: ChefWorkflowState) -> dict:
        """Nó para obter perfil do usuário"""
        print("👤 Carregando perfil do usuário...")
        
        try:
            from core_logic.database import get_user_profile
            profile = get_user_profile(user_id=1)  # Usuário padrão
            
            preferences = {
                "cuisine_type": profile.get("preferred_cuisine", "brasileira"),
                "cooking_level": profile.get("cooking_level", "intermediario"),
                "spice_level": profile.get("spice_preference", "medio")
            }
            
            restrictions = profile.get("dietary_restrictions", [])
            
            return {
                "user_preferences": preferences,
                "dietary_restrictions": restrictions,
                "step_count": 1
            }
            
        except Exception as e:
            print(f"Erro ao carregar perfil: {e}")
            return {
                "user_preferences": {"cuisine_type": "brasileira", "cooking_level": "intermediario"},
                "dietary_restrictions": [],
                "step_count": 1
            }
    
    def search_recipes_node(self, state: ChefWorkflowState) -> dict:
        """Nó para buscar receitas"""
        print("🔍 Buscando receitas...")
        
        try:
            ingredients = state.get("detected_ingredients", [])
            restrictions = state.get("dietary_restrictions", [])
            
            # Simulação de busca avançada
            recipes = []
            for ingredient in ingredients:
                recipe = {
                    "name": f"Receita com {ingredient}",
                    "ingredients": ingredients,
                    "prep_time": "30 min",
                    "difficulty": "Médio",
                    "cuisine": state["user_preferences"]["cuisine_type"]
                }
                recipes.append(recipe)
            
            return {
                "suggested_recipes": recipes,
                "step_count": 1
            }
            
        except Exception as e:
            print(f"Erro na busca: {e}")
            return {
                "suggested_recipes": [],
                "step_count": 1
            }
    
    def calculate_nutrition_node(self, state: ChefWorkflowState) -> dict:
        """Nó para calcular informações nutricionais"""
        print("📊 Calculando informações nutricionais...")
        
        try:
            recipes = state.get("suggested_recipes", [])
            
            # Cálculo nutricional simulado
            nutrition = {
                "total_calories": len(recipes) * 250,
                "protein": f"{len(recipes) * 15}g",
                "carbs": f"{len(recipes) * 30}g",
                "fat": f"{len(recipes) * 8}g",
                "fiber": f"{len(recipes) * 5}g"
            }
            
            return {
                "nutritional_info": nutrition,
                "step_count": 1
            }
            
        except Exception as e:
            print(f"Erro no cálculo nutricional: {e}")
            return {
                "nutritional_info": {},
                "step_count": 1
            }
    
    def generate_shopping_list_node(self, state: ChefWorkflowState) -> dict:
        """Nó para gerar lista de compras"""
        print("🛒 Gerando lista de compras...")
        
        try:
            ingredients = state.get("detected_ingredients", [])
            recipes = state.get("suggested_recipes", [])
            
            # Gerar lista baseada nas receitas
            shopping_items = []
            for recipe in recipes:
                recipe_ingredients = recipe.get("ingredients", [])
                shopping_items.extend(recipe_ingredients)
            
            # Remover duplicatas e organizar
            unique_items = list(set(shopping_items))
            
            return {
                "shopping_list": unique_items,
                "step_count": 1
            }
            
        except Exception as e:
            print(f"Erro na lista de compras: {e}")
            return {
                "shopping_list": [],
                "step_count": 1
            }
    
    def create_timeline_node(self, state: ChefWorkflowState) -> dict:
        """Nó para criar cronograma de cozimento"""
        print("⏰ Criando cronograma...")
        
        try:
            recipes = state.get("suggested_recipes", [])
            
            timeline = {
                "prep_phase": "15 min - Preparar ingredientes",
                "cooking_phase": "25 min - Cozinhar",
                "finishing_phase": "5 min - Finalização",
                "total_time": "45 min"
            }
            
            return {
                "cooking_timeline": timeline,
                "step_count": 1
            }
            
        except Exception as e:
            print(f"Erro no cronograma: {e}")
            return {
                "cooking_timeline": {},
                "step_count": 1
            }
    
    def generate_response_node(self, state: ChefWorkflowState) -> dict:
        """Nó para gerar resposta final"""
        print("📝 Gerando resposta final...")
        
        try:
            ingredients = state.get("detected_ingredients", [])
            recipes = state.get("suggested_recipes", [])
            nutrition = state.get("nutritional_info", {})
            shopping = state.get("shopping_list", [])
            timeline = state.get("cooking_timeline", {})
            
            response = f"""
🧑‍🍳 **ANÁLISE CHEF RAG COMPLETA**

📍 **Ingredientes Detectados:** {', '.join(ingredients)}

🍽️ **Receitas Sugeridas:**
{chr(10).join([f"• {recipe['name']}" for recipe in recipes])}

📊 **Informação Nutricional:**
• Calorias: {nutrition.get('total_calories', 'N/A')}
• Proteína: {nutrition.get('protein', 'N/A')}
• Carboidratos: {nutrition.get('carbs', 'N/A')}

🛒 **Lista de Compras:**
{chr(10).join([f"• {item}" for item in shopping[:5]])}

⏰ **Cronograma:**
• Tempo Total: {timeline.get('total_time', '45 min')}
• Preparação: {timeline.get('prep_phase', '15 min')}

✨ Receitas personalizadas baseadas no seu perfil!
            """
            
            return {
                "final_response": response.strip(),
                "step_count": 1
            }
            
        except Exception as e:
            print(f"Erro na resposta: {e}")
            return {
                "final_response": "Erro ao gerar resposta completa.",
                "step_count": 1
            }
    
    def process_request(self, user_input: str = "", image_path: str = None) -> str:
        """Processa requisição completa usando o workflow"""
        try:
            # Estado inicial
            initial_state = {
                "user_input": user_input,
                "image_path": image_path,
                "detected_ingredients": [],
                "user_preferences": {},
                "dietary_restrictions": [],
                "suggested_recipes": [],
                "nutritional_info": {},
                "shopping_list": [],
                "cooking_timeline": {},
                "final_response": "",
                "step_count": 0
            }
            
            # Executar workflow
            config = {"configurable": {"thread_id": f"chef_{datetime.now().isoformat()}"}}
            result = self.app.invoke(initial_state, config=config)
            
            return result.get("final_response", "Erro no processamento")
            
        except Exception as e:
            return f"Erro no workflow: {str(e)}"

# Instância global do workflow
chef_workflow = None

def get_chef_workflow():
    """Retorna instância do workflow"""
    global chef_workflow
    if chef_workflow is None:
        chef_workflow = ChefWorkflow()
    return chef_workflow

def process_with_langgraph(user_input: str = "", image_path: str = None) -> str:
    """Interface simplificada para usar o workflow"""
    workflow = get_chef_workflow()
    return workflow.process_request(user_input, image_path)
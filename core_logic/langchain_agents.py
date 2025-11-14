"""
Sistema de Agentes Culinários usando LangChain
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain import hub
from typing import Optional, Type
from pydantic import BaseModel, Field
import json

class IngredientAnalysisTool(BaseTool):
    name = "ingredient_analyzer"
    description = "Analisa ingredientes em imagens e retorna informações nutricionais"
    
    def _run(self, image_path: str) -> str:
        """Analisa ingrediente na imagem"""
        # Integração com o sistema existente
        from core_logic.rag_system import identify_ingredient_from_image
        try:
            ingredient = identify_ingredient_from_image(image_path)
            return f"Ingrediente detectado: {ingredient}"
        except Exception as e:
            return f"Erro na análise: {str(e)}"
    
    async def _arun(self, image_path: str) -> str:
        raise NotImplementedError("Tool não suporta execução async")

class RecipeSearchTool(BaseTool):
    name = "recipe_searcher"
    description = "Busca receitas baseadas em ingredientes e restrições alimentares"
    
    def _run(self, query: str) -> str:
        """Busca receitas relevantes"""
        # Integração com sistema de busca existente
        try:
            # Simular busca de receitas
            return f"Encontradas receitas para: {query}"
        except Exception as e:
            return f"Erro na busca: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Tool não suporta execução async")

class NutritionalCalculatorTool(BaseTool):
    name = "nutrition_calculator"
    description = "Calcula informações nutricionais de receitas e ingredientes"
    
    def _run(self, ingredients: str) -> str:
        """Calcula valores nutricionais"""
        try:
            # Simulação de cálculo nutricional
            nutrition = {
                "calorias": "250 kcal",
                "proteinas": "15g",
                "carboidratos": "30g",
                "gorduras": "8g"
            }
            return json.dumps(nutrition, ensure_ascii=False)
        except Exception as e:
            return f"Erro no cálculo: {str(e)}"
    
    async def _arun(self, ingredients: str) -> str:
        raise NotImplementedError("Tool não suporta execução async")

class TimerManagerTool(BaseTool):
    name = "timer_manager"
    description = "Gerencia timers para etapas de receitas"
    
    def _run(self, action: str) -> str:
        """Gerencia timers de cozinha"""
        try:
            from core_logic.timer_manager import TimerManager
            timer_manager = TimerManager()
            
            if "criar" in action.lower():
                # Extrair tempo do comando
                import re
                time_match = re.search(r'(\d+)', action)
                if time_match:
                    minutes = int(time_match.group(1))
                    timer_id = timer_manager.create_timer(f"Timer de {minutes}min", minutes * 60)
                    return f"Timer criado: {timer_id}"
            
            return "Timer gerenciado com sucesso"
        except Exception as e:
            return f"Erro no timer: {str(e)}"
    
    async def _arun(self, action: str) -> str:
        raise NotImplementedError("Tool não suporta execução async")

class ChefAgent:
    """Agente principal do Chef RAG com LangChain"""
    
    def __init__(self, openai_api_key: str = None):
        """Inicializa o agente culinário"""
        
        # Configurar LLM
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4o-mini",
            openai_api_key=openai_api_key
        )
        
        # Configurar memória
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  # Manter últimas 10 mensagens
        )
        
        # Definir ferramentas
        self.tools = [
            IngredientAnalysisTool(),
            RecipeSearchTool(),
            NutritionalCalculatorTool(),
            TimerManagerTool()
        ]
        
        # Inicializar agente
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            system_message=SystemMessage(content="""
            Você é um chef assistente especializado em culinária brasileira e internacional. 
            Suas especialidades incluem:
            - Análise de ingredientes em imagens
            - Sugestão de receitas personalizadas
            - Cálculos nutricionais
            - Gerenciamento de timers de cozinha
            - Adaptação de receitas para restrições alimentares
            
            Sempre seja prestativo, detalhado e forneça instruções claras.
            Use as ferramentas disponíveis para fornecer informações precisas.
            """)
        )
    
    def process_user_input(self, user_input: str, image_path: str = None) -> str:
        """Processa entrada do usuário e retorna resposta"""
        try:
            # Se há imagem, incluir na entrada
            if image_path:
                user_input += f" [Imagem: {image_path}]"
            
            # Executar agente
            response = self.agent.run(input=user_input)
            return response
            
        except Exception as e:
            return f"Erro no processamento: {str(e)}"
    
    def get_conversation_history(self) -> list:
        """Retorna histórico da conversa"""
        return self.memory.chat_memory.messages

# Instância global do agente
chef_agent = None

def get_chef_agent():
    """Retorna instância do agente culinário"""
    global chef_agent
    if chef_agent is None:
        from core_logic.config import OPENAI_API_KEY
        chef_agent = ChefAgent(openai_api_key=OPENAI_API_KEY)
    return chef_agent

def process_with_langchain_agent(user_input: str, image_path: str = None) -> str:
    """Interface simplificada para usar o agente"""
    agent = get_chef_agent()
    return agent.process_user_input(user_input, image_path)
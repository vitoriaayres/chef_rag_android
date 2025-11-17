#!/usr/bin/env python3
"""
Sistema de Agente Ambiente - Chef RAG v2
=======================================

Sistema inteligente de agentes para gerenciar interações e monitorar custos.
Integrado com LangSmith para rastreamento de performances e outputs.

Funcionalidades:
- Agente de culinária principal
- Agente de análise nutricional
- Agente de recomendação
- Monitoramento de custos em tempo real
- Rastreamento de sessões
- Analytics de uso
"""

import os
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from contextlib import contextmanager

# Imports LangChain
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.runnable import RunnableConfig

# Imports para LangSmith
from langsmith import Client
import langsmith
from langsmith.run_helpers import trace

# Configurações
from .config import (
    OPENAI_API_KEY, LANGCHAIN_API_KEY, LANGCHAIN_PROJECT, 
    MODEL_NAME, LANGCHAIN_TRACING_V2, LANGCHAIN_ENDPOINT
)

@dataclass
class SessionMetrics:
    """Métricas de uma sessão de uso"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_tokens: int = 0
    total_cost: float = 0.0
    interactions: int = 0
    success_rate: float = 0.0
    agent_calls: Dict[str, int] = None
    
    def __post_init__(self):
        if self.agent_calls is None:
            self.agent_calls = {}

@dataclass
class CostTracker:
    """Rastreador de custos por modelo"""
    input_tokens: int = 0
    output_tokens: int = 0
    total_cost: float = 0.0
    
    # Preços por 1K tokens (Nov 2025)
    PRICING = {
        "gpt-4o-mini": {"input": 0.000150, "output": 0.000600},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "text-embedding-3-small": {"input": 0.00002, "output": 0.0}
    }
    
    def add_usage(self, model: str, input_tokens: int, output_tokens: int):
        """Adiciona uso de tokens e calcula custo"""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        
        if model in self.PRICING:
            input_cost = (input_tokens / 1000) * self.PRICING[model]["input"]
            output_cost = (output_tokens / 1000) * self.PRICING[model]["output"]
            self.total_cost += input_cost + output_cost

class ChefRAGCostCallback(BaseCallbackHandler):
    """Callback para rastrear custos das chamadas LLM"""
    
    def __init__(self, cost_tracker: CostTracker):
        self.cost_tracker = cost_tracker
        self.current_model = MODEL_NAME
    
    def on_llm_end(self, response, **kwargs):
        """Chamado quando uma chamada LLM termina"""
        if hasattr(response, 'llm_output') and response.llm_output:
            token_usage = response.llm_output.get('token_usage', {})
            input_tokens = token_usage.get('prompt_tokens', 0)
            output_tokens = token_usage.get('completion_tokens', 0)
            
            self.cost_tracker.add_usage(
                self.current_model, 
                input_tokens, 
                output_tokens
            )

class EnvironmentAgentSystem:
    """Sistema de Agentes para Chef RAG v2"""
    
    def __init__(self):
        self.session_id = f"session_{int(time.time())}"
        self.cost_tracker = CostTracker()
        self.session_metrics = SessionMetrics(
            session_id=self.session_id,
            start_time=datetime.now()
        )
        
        # Configurar LangSmith
        self.setup_langsmith()
        
        # Inicializar LLM com callback de custo
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            openai_api_key=OPENAI_API_KEY,
            callbacks=[ChefRAGCostCallback(self.cost_tracker)],
            temperature=0.7
        )
        
        # Ferramentas do sistema
        self.tools = self._create_tools()
        
        # Agentes especializados
        self.agents = self._create_agents()
        
        # Cliente LangSmith
        self.langsmith_client = Client(api_key=LANGCHAIN_API_KEY) if LANGCHAIN_API_KEY else None
        
    def setup_langsmith(self):
        """Configura LangSmith para rastreamento"""
        if LANGCHAIN_API_KEY:
            os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
            os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
            os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
            os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
    
    def _create_tools(self) -> List:
        """Cria ferramentas disponíveis para os agentes"""
        
        @tool
        def search_recipes(ingredients: str, dietary_restrictions: str = "") -> str:
            """Busca receitas baseadas em ingredientes e restrições dietéticas"""
            try:
                from .sistema_rag import find_recipes_by_ingredient
                recipes = find_recipes_by_ingredient(ingredients, dietary_restrictions)
                return json.dumps(recipes[:3], ensure_ascii=False, indent=2)
            except Exception as e:
                return f"Erro na busca: {str(e)}"
        
        @tool
        def analyze_nutrition(recipe_text: str) -> str:
            """Analisa informações nutricionais de uma receita"""
            # Simulação de análise nutricional
            nutrition = {
                "calorias_estimadas": "250-400 por porção",
                "proteinas": "Médio",
                "carboidratos": "Alto",
                "gorduras": "Baixo",
                "fibras": "Médio"
            }
            return json.dumps(nutrition, ensure_ascii=False, indent=2)
        
        @tool
        def get_cooking_tips(recipe_name: str, difficulty: str = "médio") -> str:
            """Fornece dicas de preparo para receitas"""
            tips = [
                "Prepare todos os ingredientes antes de começar",
                "Use fogo médio para evitar queimar",
                "Prove durante o preparo e ajuste temperos",
                "Deixe descansar por alguns minutos antes de servir"
            ]
            return json.dumps(tips, ensure_ascii=False, indent=2)
        
        @tool
        def track_session_cost() -> str:
            """Retorna informações de custo da sessão atual"""
            cost_info = {
                "sessao": self.session_id,
                "tokens_input": self.cost_tracker.input_tokens,
                "tokens_output": self.cost_tracker.output_tokens,
                "custo_total_usd": round(self.cost_tracker.total_cost, 6),
                "interacoes": self.session_metrics.interactions
            }
            return json.dumps(cost_info, ensure_ascii=False, indent=2)
        
        return [search_recipes, analyze_nutrition, get_cooking_tips, track_session_cost]
    
    def _create_agents(self) -> Dict:
        """Cria agentes especializados"""
        
        # Agente Culinário Principal
        culinary_prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é o Chef RAG, um assistente culinário especializado. 
            Suas responsabilidades:
            - Sugerir receitas baseadas em ingredientes
            - Dar instruções de preparo detalhadas
            - Adaptar receitas para restrições dietéticas
            - Explicar técnicas culinárias
            
            Seja sempre útil, criativo e considere segurança alimentar."""),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])
        
        # Agente Nutricional
        nutrition_prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um especialista em nutrição integrado ao Chef RAG.
            Suas responsabilidades:
            - Analisar valor nutricional de receitas
            - Sugerir substituições mais saudáveis
            - Calcular calorias e macros
            - Orientar sobre alimentação balanceada
            
            Base suas respostas em conhecimento nutricional científico."""),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])
        
        # Criar executores de agentes
        culinary_agent = create_openai_tools_agent(self.llm, self.tools, culinary_prompt)
        nutrition_agent = create_openai_tools_agent(self.llm, self.tools, nutrition_prompt)
        
        culinary_executor = AgentExecutor(
            agent=culinary_agent, 
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
        nutrition_executor = AgentExecutor(
            agent=nutrition_agent,
            tools=self.tools, 
            verbose=True,
            handle_parsing_errors=True
        )
        
        return {
            "culinary": culinary_executor,
            "nutrition": nutrition_executor
        }
    
    @trace(name="chef_rag_interaction")
    def interact(self, user_input: str, agent_type: str = "culinary", 
                 chat_history: List = None) -> Dict[str, Any]:
        """Interage com um agente específico"""
        
        start_time = time.time()
        
        if chat_history is None:
            chat_history = []
        
        if agent_type not in self.agents:
            agent_type = "culinary"
        
        try:
            # Executar agente
            response = self.agents[agent_type].invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            # Atualizar métricas
            self.session_metrics.interactions += 1
            if agent_type not in self.session_metrics.agent_calls:
                self.session_metrics.agent_calls[agent_type] = 0
            self.session_metrics.agent_calls[agent_type] += 1
            
            execution_time = time.time() - start_time
            
            result = {
                "response": response.get("output", ""),
                "agent_type": agent_type,
                "execution_time": execution_time,
                "session_cost": self.cost_tracker.total_cost,
                "tokens_used": {
                    "input": self.cost_tracker.input_tokens,
                    "output": self.cost_tracker.output_tokens
                }
            }
            
            # Log para LangSmith
            if self.langsmith_client:
                self._log_to_langsmith(user_input, result)
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "agent_type": agent_type,
                "execution_time": time.time() - start_time
            }
    
    def _log_to_langsmith(self, user_input: str, result: Dict):
        """Envia logs para LangSmith"""
        try:
            run_data = {
                "session_id": self.session_id,
                "user_input": user_input,
                "response": result.get("response", ""),
                "agent_type": result.get("agent_type", ""),
                "cost": result.get("session_cost", 0),
                "tokens": result.get("tokens_used", {}),
                "timestamp": datetime.now().isoformat()
            }
            
            # Criar run no LangSmith
            self.langsmith_client.create_run(
                name=f"chef_rag_{result.get('agent_type', 'unknown')}",
                run_type="chain",
                inputs={"input": user_input},
                outputs={"output": result.get("response", "")},
                project_name=LANGCHAIN_PROJECT,
                metadata=run_data
            )
            
        except Exception as e:
            print(f"Erro ao enviar para LangSmith: {e}")
    
    def get_session_summary(self) -> Dict:
        """Retorna resumo da sessão atual"""
        self.session_metrics.end_time = datetime.now()
        self.session_metrics.total_tokens = (
            self.cost_tracker.input_tokens + self.cost_tracker.output_tokens
        )
        self.session_metrics.total_cost = self.cost_tracker.total_cost
        
        if self.session_metrics.interactions > 0:
            self.session_metrics.success_rate = 1.0  # Placeholder - implementar lógica real
        
        return asdict(self.session_metrics)
    
    @contextmanager
    def cost_monitoring(self):
        """Context manager para monitoramento de custo"""
        initial_cost = self.cost_tracker.total_cost
        yield self.cost_tracker
        final_cost = self.cost_tracker.total_cost
        cost_diff = final_cost - initial_cost
        print(f"💰 Custo da operação: ${cost_diff:.6f}")

# Instância global do sistema de agentes
agent_system = None

def get_agent_system() -> EnvironmentAgentSystem:
    """Retorna instância singleton do sistema de agentes"""
    global agent_system
    if agent_system is None:
        agent_system = EnvironmentAgentSystem()
    return agent_system

def reset_agent_session():
    """Reseta a sessão atual do agente"""
    global agent_system
    if agent_system:
        # Salvar métricas da sessão anterior se necessário
        summary = agent_system.get_session_summary()
        print(f"📊 Sessão finalizada: {summary['interactions']} interações, ${summary['total_cost']:.6f}")
    
    agent_system = EnvironmentAgentSystem()
    return agent_system
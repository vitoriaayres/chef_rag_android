"""
Integração das funcionalidades LangChain/LangGraph com o sistema existente
"""

from typing import Optional, List, Dict, Any
import os

# Flags para controlar qual sistema usar
USE_LANGCHAIN_AGENTS = False
USE_LANGGRAPH_WORKFLOWS = False  
USE_ADVANCED_RAG = False

def initialize_langchain_systems():
    """Inicializa sistemas LangChain/LangGraph se disponíveis"""
    global USE_LANGCHAIN_AGENTS, USE_LANGGRAPH_WORKFLOWS, USE_ADVANCED_RAG
    
    try:
        # Verificar se LangChain está instalado
        import langchain
        print("🔗 LangChain detectado")
        
        # Verificar se LangGraph está instalado
        try:
            import langgraph
            USE_LANGGRAPH_WORKFLOWS = True
            print("🕸️ LangGraph detectado - Workflows habilitados")
        except ImportError:
            print("⚠️ LangGraph não instalado - Workflows desabilitados")
        
        # Verificar se há chave da OpenAI
        from core_logic.config import OPENAI_API_KEY
        if OPENAI_API_KEY and OPENAI_API_KEY != "your-openai-api-key":
            USE_LANGCHAIN_AGENTS = True
            USE_ADVANCED_RAG = True
            print("🤖 Sistemas LangChain habilitados")
        else:
            print("⚠️ OpenAI API Key necessária para LangChain")
            
    except ImportError:
        print("⚠️ LangChain não instalado - Usando sistema tradicional")

def smart_recipe_analysis(user_input: str = "", image_path: str = None) -> str:
    """
    Análise inteligente usando o melhor sistema disponível
    Prioridade: LangGraph > LangChain Agents > Sistema Tradicional
    """
    
    # 1. Tentar LangGraph Workflow (mais avançado)
    if USE_LANGGRAPH_WORKFLOWS:
        try:
            from core_logic.langgraph_workflows import process_with_langgraph
            print("🕸️ Usando LangGraph Workflow")
            return process_with_langgraph(user_input, image_path)
        except Exception as e:
            print(f"❌ Erro no LangGraph: {e}")
    
    # 2. Tentar LangChain Agents
    if USE_LANGCHAIN_AGENTS:
        try:
            from core_logic.langchain_agents import process_with_langchain_agent
            print("🤖 Usando LangChain Agent")
            return process_with_langchain_agent(user_input, image_path)
        except Exception as e:
            print(f"❌ Erro no LangChain Agent: {e}")
    
    # 3. Fallback para sistema tradicional
    print("🔄 Usando sistema tradicional")
    return traditional_recipe_analysis(user_input, image_path)

def smart_recipe_search(query: str, use_advanced: bool = True) -> str:
    """
    Busca inteligente usando RAG avançado ou sistema tradicional
    """
    
    if USE_ADVANCED_RAG and use_advanced:
        try:
            from core_logic.advanced_rag import query_with_langchain_rag
            print("🔍 Usando RAG Avançado")
            return query_with_langchain_rag(query)
        except Exception as e:
            print(f"❌ Erro no RAG avançado: {e}")
    
    # Fallback para sistema tradicional
    print("📚 Usando busca tradicional")
    return traditional_recipe_search(query)

def traditional_recipe_analysis(user_input: str = "", image_path: str = None) -> str:
    """Sistema tradicional de análise"""
    try:
        if image_path:
            from core_logic.rag_system import identify_ingredient_from_image, find_recipes_by_ingredient
            
            # Detectar ingredientes
            ingredients = identify_ingredient_from_image(image_path, multiple_ingredients=True)
            print(f"🔍 Ingredientes detectados: {ingredients}")
            
            # Buscar receitas
            if isinstance(ingredients, str):
                ingredient_list = [ing.strip() for ing in ingredients.split(',')]
            else:
                ingredient_list = [str(ingredients)]
            
            recipes = []
            for ingredient in ingredient_list[:3]:  # Máximo 3 ingredientes
                recipe = find_recipes_by_ingredient(ingredient, image_path, "traditional")
                recipes.append(recipe)
            
            return f"🍽️ Receitas encontradas para {', '.join(ingredient_list)}:\n" + "\n".join(recipes)
        
        else:
            # Análise de texto
            return f"📝 Processando: {user_input}"
            
    except Exception as e:
        return f"❌ Erro na análise tradicional: {str(e)}"

def traditional_recipe_search(query: str) -> str:
    """Busca tradicional no sistema"""
    try:
        from core_logic.rag_system import search_recipes_by_text
        return search_recipes_by_text(query)
    except Exception as e:
        return f"❌ Erro na busca: {str(e)}"

def get_system_status() -> Dict[str, bool]:
    """Retorna status dos sistemas disponíveis"""
    return {
        "langchain_agents": USE_LANGCHAIN_AGENTS,
        "langgraph_workflows": USE_LANGGRAPH_WORKFLOWS,
        "advanced_rag": USE_ADVANCED_RAG,
        "traditional_system": True
    }

def install_langchain_dependencies() -> str:
    """Instala dependências LangChain se necessário"""
    try:
        import subprocess
        import sys
        
        packages = [
            "langchain",
            "langgraph", 
            "langchain-openai",
            "langchain-community",
            "chromadb",
            "pypdf"
        ]
        
        installation_results = []
        
        for package in packages:
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    installation_results.append(f"✅ {package}")
                else:
                    installation_results.append(f"❌ {package}: {result.stderr}")
                    
            except Exception as e:
                installation_results.append(f"❌ {package}: {str(e)}")
        
        return "Instalação LangChain:\n" + "\n".join(installation_results)
        
    except Exception as e:
        return f"❌ Erro na instalação: {str(e)}"

# Inicializar sistemas na importação
initialize_langchain_systems()
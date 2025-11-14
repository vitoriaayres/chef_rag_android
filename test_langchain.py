#!/usr/bin/env python3
"""
Teste das funcionalidades LangChain/LangGraph no Chef RAG
"""

import os
import sys
from pathlib import Path

def test_langchain_integration():
    """Testa a integração LangChain/LangGraph"""
    
    print("🧪 TESTE DE INTEGRAÇÃO LANGCHAIN/LANGGRAPH")
    print("=" * 60)
    
    try:
        # Importar sistema integrado
        from core_logic.smart_integration import (
            get_system_status, 
            smart_recipe_analysis,
            smart_recipe_search
        )
        
        # Verificar status dos sistemas
        status = get_system_status()
        print("\n📊 STATUS DOS SISTEMAS:")
        print(f"🤖 LangChain Agents: {'✅' if status['langchain_agents'] else '❌'}")
        print(f"🕸️ LangGraph Workflows: {'✅' if status['langgraph_workflows'] else '❌'}")
        print(f"🔍 RAG Avançado: {'✅' if status['advanced_rag'] else '❌'}")
        print(f"🔄 Sistema Tradicional: {'✅' if status['traditional_system'] else '❌'}")
        
        # Teste 1: Análise de texto
        print("\n🔤 TESTE 1: Análise de texto")
        print("-" * 30)
        text_result = smart_recipe_analysis("Quero uma receita com tomate e ovo")
        print(f"Resultado: {text_result[:200]}...")
        
        # Teste 2: Busca inteligente
        print("\n🔍 TESTE 2: Busca inteligente")
        print("-" * 30)
        search_result = smart_recipe_search("receitas veganas com legumes")
        print(f"Resultado: {search_result[:200]}...")
        
        # Teste 3: Análise de imagem (se disponível)
        print("\n📸 TESTE 3: Análise de imagem")
        print("-" * 30)
        
        # Verificar se existe imagem de teste
        test_images = [
            "data/imagens/teste.jpg",
            "data/imagens/alho.jpg", 
            "data/imagens/ovo.jpg"
        ]
        
        test_image = None
        for img_path in test_images:
            if Path(img_path).exists():
                test_image = img_path
                break
        
        if test_image:
            print(f"📷 Usando imagem: {test_image}")
            image_result = smart_recipe_analysis(image_path=test_image)
            print(f"Resultado: {image_result[:300]}...")
        else:
            print("❌ Nenhuma imagem de teste encontrada")
            # Criar imagem de teste simples
            Path("data/imagens").mkdir(parents=True, exist_ok=True)
            with open("data/imagens/teste_lang.jpg", "w") as f:
                f.write("test image content")
            
            print("📝 Imagem de teste criada")
            image_result = smart_recipe_analysis(
                user_input="análise de imagem", 
                image_path="data/imagens/teste_lang.jpg"
            )
            print(f"Resultado: {image_result[:200]}...")
        
        print("\n✅ Todos os testes concluídos!")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Tente instalar: pip install langchain langgraph langchain-openai")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()

def test_individual_components():
    """Testa componentes individuais"""
    
    print("\n🔧 TESTE DE COMPONENTES INDIVIDUAIS")
    print("=" * 60)
    
    # Teste LangChain Agents
    print("\n🤖 Testando LangChain Agents:")
    try:
        from core_logic.langchain_agents import get_chef_agent
        agent = get_chef_agent()
        print("✅ Agent criado com sucesso")
        
        # Teste simples
        response = agent.process_user_input("O que posso fazer com ovos?")
        print(f"Resposta: {response[:150]}...")
        
    except Exception as e:
        print(f"❌ Erro no agent: {e}")
    
    # Teste LangGraph Workflows  
    print("\n🕸️ Testando LangGraph Workflows:")
    try:
        from core_logic.langgraph_workflows import get_chef_workflow
        workflow = get_chef_workflow()
        print("✅ Workflow criado com sucesso")
        
        # Teste simples
        response = workflow.process_request("Receita com frango")
        print(f"Resposta: {response[:150]}...")
        
    except Exception as e:
        print(f"❌ Erro no workflow: {e}")
    
    # Teste RAG Avançado
    print("\n🔍 Testando RAG Avançado:")
    try:
        from core_logic.advanced_rag import get_advanced_rag_system
        rag = get_advanced_rag_system()
        print("✅ RAG sistema criado com sucesso")
        
        # Teste simples
        result = rag.query_recipes("receitas com legumes")
        print(f"Resposta: {result['answer'][:150]}...")
        
    except Exception as e:
        print(f"❌ Erro no RAG: {e}")

def interactive_test():
    """Teste interativo com usuário"""
    
    print("\n🎮 TESTE INTERATIVO")
    print("=" * 60)
    print("Digite perguntas sobre receitas (ou 'quit' para sair)")
    
    try:
        from core_logic.smart_integration import smart_recipe_analysis, smart_recipe_search
        
        while True:
            query = input("\n🍽️ Sua pergunta: ").strip()
            
            if query.lower() in ['quit', 'sair', 'exit']:
                break
            
            if not query:
                continue
            
            # Escolher tipo de processamento
            print("1. Análise completa (LangGraph)")
            print("2. Busca inteligente (RAG)")
            print("3. Análise simples")
            
            choice = input("Escolha (1-3): ").strip()
            
            if choice == "1":
                result = smart_recipe_analysis(query)
            elif choice == "2":
                result = smart_recipe_search(query)
            else:
                result = f"Processando: {query}"
            
            print(f"\n🤖 Resposta:\n{result}")
            print("-" * 50)
    
    except KeyboardInterrupt:
        print("\n👋 Teste interativo encerrado")
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    # Executar todos os testes
    test_langchain_integration()
    
    print("\n" + "=" * 60)
    
    # Testes individuais
    test_individual_components()
    
    print("\n" + "=" * 60)
    
    # Teste interativo opcional
    response = input("\n🎮 Executar teste interativo? (y/n): ").strip().lower()
    if response in ['y', 'yes', 's', 'sim']:
        interactive_test()
    
    print("\n🎉 Testes concluídos!")
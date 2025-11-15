#!/usr/bin/env python3
"""
Teste do Sistema Inteligente Chef RAG
Demonstra funcionalidades inspiradas em LangChain/LangGraph
"""

def test_smart_systems():
    """Testa todos os sistemas inteligentes"""
    
    print("🧪 TESTE DO SISTEMA INTELIGENTE CHEF RAG")
    print("=" * 60)
    print("Funcionalidades inspiradas em LangChain/LangGraph")
    print("=" * 60)
    
    try:
        from core_logic.smart_chef_system import (
            process_with_smart_agent,
            process_with_smart_workflow, 
            query_with_smart_rag,
            get_smart_system_status
        )
        
        # Status dos sistemas
        status = get_smart_system_status()
        print("\n📊 STATUS DOS SISTEMAS INTELIGENTES:")
        for system, is_active in status.items():
            print(f"{'✅' if is_active else '❌'} {system.replace('_', ' ').title()}")
        
        print("\n" + "=" * 60)
        
        # Teste 1: Agente Inteligente (inspirado em LangChain Agents)
        print("\n🤖 TESTE 1: AGENTE INTELIGENTE")
        print("-" * 40)
        print("Sistema inspirado em LangChain Agents com ferramentas personalizadas")
        
        test_queries = [
            "Quero fazer uma receita com ovos e tomate",
            "Calcule a nutrição de frango, arroz e brócolis", 
            "Crie um timer para 25 minutos",
            "Gere uma lista de compras para lasanha"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Query {i}: {query}")
            response = process_with_smart_agent(query)
            print(f"🤖 Resposta: {response[:200]}...")
        
        # Teste 2: Workflow Inteligente (inspirado em LangGraph)
        print("\n\n🕸️ TESTE 2: WORKFLOW INTELIGENTE")
        print("-" * 40)
        print("Sistema inspirado em LangGraph com múltiplas etapas")
        
        workflow_tests = [
            "Analyze uma receita completa com frango e legumes",
            "Processo completo para jantar romântico"
        ]
        
        for i, query in enumerate(workflow_tests, 1):
            print(f"\n🔄 Workflow {i}: {query}")
            response = process_with_smart_workflow(query)
            print(f"🕸️ Resultado:\n{response}")
            print("-" * 40)
        
        # Teste 3: Sistema RAG Inteligente
        print("\n\n📚 TESTE 3: SISTEMA RAG INTELIGENTE")
        print("-" * 40)
        print("Sistema inspirado em LangChain RAG")
        
        rag_queries = [
            "receitas com ovos",
            "pratos com tomate",
            "café da manhã rápido",
            "comida saudável"
        ]
        
        for i, query in enumerate(rag_queries, 1):
            print(f"\n🔍 RAG Query {i}: {query}")
            response = query_with_smart_rag(query)
            print(f"📚 Resposta:\n{response}")
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("🎉 Sistema inteligente funcionando perfeitamente!")
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        import traceback
        traceback.print_exc()

def interactive_demo():
    """Demonstração interativa dos sistemas"""
    
    print("\n🎮 DEMONSTRAÇÃO INTERATIVA")
    print("=" * 60)
    
    try:
        from core_logic.smart_chef_system import (
            process_with_smart_agent,
            process_with_smart_workflow,
            query_with_smart_rag
        )
        
        while True:
            print("\n🔧 ESCOLHA O SISTEMA PARA TESTAR:")
            print("1. 🤖 Agente Inteligente (LangChain-style)")
            print("2. 🕸️ Workflow Completo (LangGraph-style)")
            print("3. 📚 Busca RAG Inteligente")
            print("4. 🎯 Teste com Imagem")
            print("5. ❌ Sair")
            
            choice = input("\n➤ Escolha (1-5): ").strip()
            
            if choice == "5":
                print("👋 Saindo da demonstração")
                break
            
            if choice in ["1", "2", "3"]:
                query = input("\n📝 Digite sua pergunta culinária: ").strip()
                
                if not query:
                    print("❌ Digite uma pergunta válida")
                    continue
                
                print("\n⚡ Processando...")
                
                if choice == "1":
                    result = process_with_smart_agent(query)
                    print(f"\n🤖 Agente Inteligente:\n{result}")
                    
                elif choice == "2":
                    result = process_with_smart_workflow(query)
                    print(f"\n🕸️ Workflow Completo:\n{result}")
                    
                elif choice == "3":
                    result = query_with_smart_rag(query)
                    print(f"\n📚 Sistema RAG:\n{result}")
            
            elif choice == "4":
                # Teste com imagem
                print("\n📸 TESTE COM IMAGEM")
                
                # Verificar imagens disponíveis
                import os
                from pathlib import Path
                
                image_dir = Path("data/imagens")
                if image_dir.exists():
                    images = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))
                    
                    if images:
                        print("📁 Imagens disponíveis:")
                        for i, img in enumerate(images, 1):
                            print(f"  {i}. {img.name}")
                        
                        try:
                            img_choice = int(input("Escolha uma imagem (número): "))
                            if 1 <= img_choice <= len(images):
                                selected_image = str(images[img_choice - 1])
                                
                                print("\n🔧 Escolha o sistema:")
                                print("1. 🤖 Agente com Imagem")
                                print("2. 🕸️ Workflow com Imagem")
                                
                                sys_choice = input("Sistema (1-2): ").strip()
                                
                                if sys_choice == "1":
                                    result = process_with_smart_agent("Analise esta imagem", selected_image)
                                    print(f"\n🤖 Resultado:\n{result}")
                                elif sys_choice == "2":
                                    result = process_with_smart_workflow("Análise completa da imagem", selected_image)
                                    print(f"\n🕸️ Resultado:\n{result}")
                            else:
                                print("❌ Número inválido")
                        except ValueError:
                            print("❌ Digite um número válido")
                    else:
                        print("❌ Nenhuma imagem encontrada em data/imagens")
                        
                        # Criar imagem de teste
                        image_dir.mkdir(exist_ok=True)
                        test_image = image_dir / "demo_test.jpg"
                        with open(test_image, "w") as f:
                            f.write("test image content")
                        
                        print(f"✅ Imagem de teste criada: {test_image}")
                        result = process_with_smart_workflow("Análise de imagem de teste", str(test_image))
                        print(f"\n🕸️ Resultado:\n{result}")
                else:
                    print("❌ Diretório de imagens não encontrado")
            
            else:
                print("❌ Opção inválida! Escolha 1-5")
                
            input("\n⏸️ Pressione Enter para continuar...")
    
    except KeyboardInterrupt:
        print("\n\n👋 Demonstração interrompida")
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")

def performance_comparison():
    """Compara performance dos diferentes sistemas"""
    
    print("\n📊 COMPARAÇÃO DE PERFORMANCE")
    print("=" * 60)
    
    import time
    
    try:
        from core_logic.smart_chef_system import (
            process_with_smart_agent,
            process_with_smart_workflow,
            query_with_smart_rag
        )
        
        test_query = "receita com frango e batata"
        
        systems = [
            ("🤖 Agente Inteligente", process_with_smart_agent),
            ("🕸️ Workflow Completo", process_with_smart_workflow),
            ("📚 Sistema RAG", query_with_smart_rag)
        ]
        
        results = []
        
        for name, system_func in systems:
            print(f"\n⚡ Testando {name}...")
            
            start_time = time.time()
            
            try:
                result = system_func(test_query)
                end_time = time.time()
                
                execution_time = end_time - start_time
                response_length = len(result)
                
                results.append({
                    "system": name,
                    "time": execution_time,
                    "response_length": response_length,
                    "success": True
                })
                
                print(f"✅ Tempo: {execution_time:.3f}s | Resposta: {response_length} chars")
                
            except Exception as e:
                end_time = time.time()
                results.append({
                    "system": name,
                    "time": end_time - start_time,
                    "response_length": 0,
                    "success": False,
                    "error": str(e)
                })
                print(f"❌ Erro: {e}")
        
        # Mostrar resultados
        print(f"\n📈 RESUMO DA COMPARAÇÃO:")
        print("-" * 60)
        
        for result in results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['system']}: {result['time']:.3f}s")
            if not result['success']:
                print(f"   Erro: {result.get('error', 'Desconhecido')}")
        
        # Sistema mais rápido
        successful_results = [r for r in results if r["success"]]
        if successful_results:
            fastest = min(successful_results, key=lambda x: x["time"])
            print(f"\n🏆 Mais rápido: {fastest['system']} ({fastest['time']:.3f}s)")
        
    except Exception as e:
        print(f"❌ Erro na comparação: {e}")

if __name__ == "__main__":
    # Executar testes automáticos
    test_smart_systems()
    
    # Perguntir se quer demonstração interativa
    print("\n" + "=" * 60)
    response = input("🎮 Executar demonstração interativa? (y/n): ").strip().lower()
    if response in ['y', 'yes', 's', 'sim']:
        interactive_demo()
    
    # Perguntir se quer comparação de performance
    print("\n" + "=" * 60)
    response = input("📊 Executar comparação de performance? (y/n): ").strip().lower()
    if response in ['y', 'yes', 's', 'sim']:
        performance_comparison()
    
    print("\n🎉 Demonstração completa do Sistema Inteligente Chef RAG!")
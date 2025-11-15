#!/usr/bin/env python3
"""
Sistema Chef RAG v2 - Sistema Avançado de Análise de Ingredientes e Sugestão de Receitas

Permite ao usuário escolher entre:
1. Webcam - Captura imagens em tempo real da webcam
2. Pasta - Monitor uma pasta para novas imagens
3. Câmera Mobile - Acesso via dispositivo móvel
4. Visualizar Histórico - Análise de dados e estatísticas
5. Interface de Voz Avançada - Reconhecimento de voz com IA

Versão: 2.0 - Novembro 2025
Desenvolvido com LangChain, ChromaDB e OpenAI
"""

import sys
import os
from core_logic import config
from core_logic.cleanup_manager import setup_image_cleanup

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Exibe o menu principal do sistema"""
    limpar_tela()
    print("\n" + "="*70)
    print("🧑‍🍳  CHEF RAG - Seu Assistente Culinário Inteligente")
    print("="*70)
    print("🤖 Inteligência Artificial  |  📚 Base de Receitas  |  🎯 Análise Avançada")
    print("="*70)
    
    print("\n📸  COMO VOCÊ QUER ENCONTRAR RECEITAS HOJE?")
    print()
    print("   1. 📷 Usar Câmera do Computador")
    print("   2. 📱 Usar Câmera do Celular (QR Code)")
    print("   3. 🖼️  Enviar Foto dos Ingredientes")
    print("   4. ✍️  Digitar os Ingredientes")
    print("   5. 🎤 Interface de Voz Avançada")
    print()
    print("🔧  OUTRAS OPÇÕES:")
    print()
    print("   6. 🥗 Filtrar por Dieta Especial")
    print("   7. ⏰ Gerenciar Cronômetros")
    print("   8. 📊 Ver Histórico de Receitas")
    print("   9. 👤 Meu Perfil")
    print()
    print("  10. ❌ Sair do Sistema")
    print()
    print("="*70)

def executar_historico():
    """Executa o visualizador de histórico"""
    try:
        from history_viewer import main as history_main
        print("\n📄 Abrindo seu histórico de receitas...")
        history_main()
    except ImportError:
        print("❌ Sistema de histórico não encontrado")
    except Exception as e:
        print(f"❌ Erro ao abrir histórico: {e}")

def usar_camera_pc():
    """Executa a câmera do computador"""
    try:
        from webcam import run_webcam_capture
        print("\n📷 Preparando câmera do computador...")
        print("💡 Posicione os ingredientes na frente da câmera")
        run_webcam_capture()
    except ImportError:
        print("❌ Sistema de câmera não encontrado")
        print("💡 Verifique se a webcam está conectada")
    except Exception as e:
        print(f"❌ Erro na câmera: {e}")
        input("\nPressione ENTER para continuar...")

def usar_camera_celular():
    """Executa o servidor para câmera do celular"""
    try:
        from mobile_camera import start_mobile_server
        print("\n📱 Iniciando conexão com seu celular...")
        print("💡 Mantenha este terminal aberto e use seu celular!")
        print("📱 Um QR Code será gerado para conexão rápida")
        start_mobile_server()
    except ImportError:
        print("❌ Sistema mobile não encontrado")
        print("💡 Execute: pip install flask qrcode pillow")
    except Exception as e:
        print(f"❌ Erro no servidor mobile: {e}")
        input("\nPressione ENTER para continuar...")
    except Exception as e:
        print(f"❌ Erro: {e}")

def enviar_foto_ingredientes():
    """Permite enviar uma foto dos ingredientes"""
    limpar_tela()
    print("\n📸 ENVIAR FOTO DOS INGREDIENTES")
    print("="*50)
    print("📁 Você pode enviar uma foto que já tem salva no computador")
    print()
    
    try:
        from core_logic import rag_system
        
        # Solicitar caminho da imagem
        print("💡 Digite o caminho completo da imagem")
        print("   Exemplo: C:\\Users\\Seu_Usuario\\Fotos\\ingredientes.jpg")
        print()
        
        caminho_imagem = input("📂 Caminho da imagem: ").strip()
        
        if not caminho_imagem:
            print("❌ Nenhum caminho foi informado")
            return
            
        if not os.path.exists(caminho_imagem):
            print("❌ Arquivo não encontrado!")
            print("🔍 Verifique se o caminho está correto")
            return
        
        print(f"\n🔍 Analisando imagem: {os.path.basename(caminho_imagem)}")
        print("⏳ Aguarde, a inteligência artificial está trabalhando...")
        
        # Extrair ingredientes
        ingrediente = rag_system.extract_ingredients_from_image(caminho_imagem)
        
        if "Erro" in ingrediente:
            print("❌ Não foi possível identificar os ingredientes")
            print("💡 Tente uma imagem mais clara ou com melhor qualidade")
            return
            
        print(f"✅ Ingrediente identificado: {ingrediente}")
        
        # Buscar receitas
        print("\n🔍 Procurando receitas no seu livro de receitas...")
        receitas = rag_system.find_recipes_by_ingredient(ingrediente, caminho_imagem, "upload")
        
        if receitas:
            print("\n🍽️ RECEITAS ENCONTRADAS:")
            print("="*60)
            print(receitas)
            print("="*60)
        else:
            print(f"❌ Nenhuma receita encontrada para: {ingrediente}")
            
    except ImportError:
        print("❌ Sistema de análise não disponível")
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")

def digitar_ingredientes():
    """Permite digitar os ingredientes manualmente"""
    limpar_tela()
    print("\n✍️ DIGITAR INGREDIENTES")
    print("="*50)
    print("📝 Digite os ingredientes que você tem disponível")
    print()
    
    try:
        from core_logic import rag_system
        
        print("💡 Exemplos:")
        print("   • tomate, cebola, alho")
        print("   • frango, batata, cenoura")
        print("   • ovos, leite, farinha")
        print()
        
        ingredientes = input("🥬 Digite seus ingredientes: ").strip()
        
        if not ingredientes:
            print("❌ Nenhum ingrediente foi informado")
            return
            
        print(f"\n🔍 Procurando receitas com: {ingredientes}")
        print("⏳ Consultando base de receitas...")
        
        # Buscar receitas
        receitas = rag_system.generate_recipe_suggestion_multiple(ingredientes.split(","))
        
        if receitas:
            print("\n🍽️ SUGESTÕES DE RECEITAS:")
            print("="*60)
            print(receitas)
            print("="*60)
        else:
            print("❌ Nenhuma receita encontrada com esses ingredientes")
            print("💡 Tente ingredientes mais comuns ou uma combinação diferente")
            
    except ImportError:
        print("❌ Sistema de receitas não disponível")
    except Exception as e:
        print(f"❌ Erro ao buscar receitas: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")

def falar_ingredientes():
    """Abre a interface avançada de reconhecimento de voz"""
    limpar_tela()
    print("\n🎤 INTERFACE DE VOZ AVANÇADA")
    print("="*50)
    print("🚀 Abrindo interface visual com métricas de acurácia...")
    print()
    
    try:
        # Tentar interface completa primeiro
        try:
            from voice_interface_gui import VoiceInterfaceGUI
            
            print("🎧 Iniciando interface de reconhecimento completa...")
            print("📊 Funcionalidades avançadas:")
            print("   • Reconhecimento de voz real")
            print("   • Métricas de acurácia visual")
            print("   • Comparação com PDF")
            print("   • Histórico detalhado")
            print("   • Múltiplas engines de reconhecimento")
            print()
            print("⚡ Interface será aberta em nova janela...")
            
            app = VoiceInterfaceGUI()
            app.run()
            
        except ImportError:
            print("⚠️ Interface completa não disponível. Usando versão simplificada...")
            print()
            
            # Interface simplificada
            from simple_voice_interface import SimpleVoiceInterface
            
            print("🎧 Iniciando interface simplificada...")
            print("📊 Funcionalidades disponíveis:")
            print("   • Simulação de reconhecimento")
            print("   • Entrada manual de ingredientes")
            print("   • Análise de texto completa")
            print("   • Histórico local")
            print("   • Comparação de ingredientes")
            print("   • Métricas e estatísticas")
            print()
            print("⚡ Interface será aberta em nova janela...")
            
            app = SimpleVoiceInterface()
            app.run()
        
        print("\n✅ Interface de voz finalizada!")
        
    except ImportError as e:
        print(f"❌ Erro ao importar interface de voz: {e}")
        print("🔧 Dependências necessárias:")
        print("   • tkinter (geralmente incluído no Python)")
        print("   • Para reconhecimento real: SpeechRecognition, pyaudio")
        
        # Fallback para reconhecimento básico no terminal
        print("\n🔄 Tentando reconhecimento básico no terminal...")
        try:
            from core_logic.voice_recognition import voice_recognition
            from core_logic import rag_system
            
            print("🎙️ Fale seus ingredientes...")
            ingredientes = voice_recognition.recognize_ingredients()
            
            if ingredientes and "erro" not in ingredientes.lower():
                print(f"\n✅ Ingredientes identificados: {ingredientes}")
                print("\n🔍 Buscando receitas...")
                
                resposta = rag_system.find_recipes_by_ingredient(ingredientes, source_mode="voice")
                print(f"\n📖 Receitas encontradas:")
                print(resposta)
            else:
                print("❌ Não foi possível reconhecer os ingredientes")
                print("\n💡 Alternativa: Digite manualmente os ingredientes")
                ingredientes_manuais = input("🖊️ Digite os ingredientes: ").strip()
                
                if ingredientes_manuais:
                    print(f"\n✅ Ingredientes digitados: {ingredientes_manuais}")
                    resposta = rag_system.find_recipes_by_ingredient(ingredientes_manuais, source_mode="manual")
                    print(f"\n📖 Receitas encontradas:")
                    print(resposta)
                
        except Exception as basic_error:
            print(f"❌ Erro no reconhecimento básico: {basic_error}")
            print("\n💡 Alternativa simples: Digite os ingredientes")
            ingredientes_manuais = input("🖊️ Digite os ingredientes que você tem: ").strip()
            
            if ingredientes_manuais:
                try:
                    from core_logic import rag_system
                    print(f"\n✅ Ingredientes: {ingredientes_manuais}")
                    resposta = rag_system.find_recipes_by_ingredient(ingredientes_manuais, source_mode="manual")
                    print(f"\n📖 Receitas encontradas:")
                    print(resposta)
                except Exception:
                    print("✅ Ingredientes anotados! Você pode buscar receitas manualmente.")
            
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("🔧 Tente reiniciar o programa")
        
        input("🎤 Pressione ENTER e comece a falar...")
        
        print("🔴 GRAVANDO... (fale agora!)")
        ingredientes = voice_recognition.recognize_ingredients(timeout=10, phrase_time_limit=15)
        
        if not ingredientes or "erro" in ingredientes.lower():
            print("❌ Não foi possível entender o áudio")
            print("💡 Tente falar mais claramente ou verificar o microfone")
            return
            
        print(f"✅ Entendi: {ingredientes}")
        
        print("\n🔍 Procurando receitas...")
        receitas = rag_system.generate_recipe_suggestion(ingredientes)
        
        if receitas:
            print("\n🍽️ RECEITAS SUGERIDAS:")
            print("="*60)
            print(receitas)
            print("="*60)
        else:
            print("❌ Nenhuma receita encontrada")
            
    except ImportError:
        print("❌ Sistema de voz não disponível")
        print("🔧 Execute: pip install SpeechRecognition pyaudio")
    except Exception as e:
        print(f"❌ Erro no reconhecimento de voz: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")

def filtrar_por_dieta():
    """Sistema de filtros por restrições alimentares"""
    limpar_tela()
    print("\n🥗 FILTROS POR DIETA ESPECIAL")
    print("="*50)
    print("🎯 Encontre receitas adequadas às suas necessidades")
    print()
    
    try:
        from core_logic import rag_system
        
        print("🍽️ Escolha seu tipo de dieta:")
        print("   1. 🌱 Vegetariano")
        print("   2. 🥬 Vegano")
        print("   3. 🚫 Sem Glúten")
        print("   4. 🥩 Low Carb")
        print("   5. 🍯 Para Diabéticos")
        print("   6. ⬅️ Voltar ao Menu")
        print()
        
        opcao = input("🎯 Sua escolha: ").strip()
        
        filtros = {
            "1": ("vegetariano", "🌱 Receitas Vegetarianas"),
            "2": ("vegano", "🥬 Receitas Veganas"),
            "3": ("sem glúten", "🚫 Receitas Sem Glúten"),
            "4": ("low carb", "🥩 Receitas Low Carb"),
            "5": ("diabético", "🍯 Receitas para Diabéticos")
        }
        
        if opcao == "6":
            return
            
        if opcao in filtros:
            filtro, titulo = filtros[opcao]
            print(f"\n{titulo}")
            print("="*60)
            print("🔍 Procurando receitas especiais...")
            
            receitas = rag_system.find_recipes_by_dietary_filter(filtro)
            
            if receitas:
                print(receitas)
                print("="*60)
            else:
                print("❌ Nenhuma receita encontrada para esse filtro")
        else:
            print("❌ Opção inválida!")
            
    except ImportError:
        print("❌ Sistema de filtros não disponível")
    except Exception as e:
        print(f"❌ Erro ao aplicar filtro: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")

def gerenciar_cronometros():
    """Sistema de gerenciamento de cronômetros"""
    limpar_tela()
    print("\n⏰ GERENCIAR CRONÔMETROS")
    print("="*50)
    print("🕐 Controle o tempo de preparo das suas receitas")
    print()
    
    try:
        from core_logic.timer_manager import timer_manager
        
        while True:
            print("\n⏰ O que você quer fazer?")
            print("   1. ➕ Criar Novo Cronômetro")
            print("   2. 📋 Ver Cronômetros Ativos")
            print("   3. ⏹️ Parar Cronômetro")
            print("   4. ⬅️ Voltar ao Menu")
            print()
            
            opcao = input("🎯 Sua escolha: ").strip()
            
            if opcao == "1":
                nome = input("\n📝 Nome do cronômetro (ex: 'Ferver ovos'): ").strip()
                if nome:
                    try:
                        minutos = int(input("⏲️ Quantos minutos? ").strip())
                        if minutos > 0:
                            timer_manager.create_timer(nome, minutos * 60)
                            print(f"✅ Cronômetro '{nome}' criado para {minutos} minutos!")
                        else:
                            print("❌ Tempo deve ser maior que zero")
                    except ValueError:
                        print("❌ Digite um número válido de minutos")
                        
            elif opcao == "2":
                timers = timer_manager.get_active_timers()
                if timers:
                    print("\n⏰ CRONÔMETROS ATIVOS:")
                    print("-" * 40)
                    for timer_id, info in timers.items():
                        tempo_restante = info['remaining_time']
                        mins, secs = divmod(int(tempo_restante), 60)
                        print(f"🕐 {info['name']}: {mins:02d}:{secs:02d}")
                    print("-" * 40)
                else:
                    print("📭 Nenhum cronômetro ativo no momento")
                    
            elif opcao == "3":
                timers = timer_manager.get_active_timers()
                if timers:
                    print("\n⏹️ PARAR CRONÔMETRO:")
                    for i, (timer_id, info) in enumerate(timers.items(), 1):
                        print(f"   {i}. {info['name']}")
                    
                    try:
                        escolha = int(input("Número do cronômetro para parar: "))
                        timer_ids = list(timers.keys())
                        if 1 <= escolha <= len(timer_ids):
                            timer_manager.stop_timer(timer_ids[escolha - 1])
                            print("✅ Cronômetro parado!")
                        else:
                            print("❌ Número inválido")
                    except ValueError:
                        print("❌ Digite um número válido")
                else:
                    print("📭 Nenhum cronômetro ativo para parar")
                    
            elif opcao == "4":
                break
            else:
                print("❌ Opção inválida!")
                
    except ImportError:
        print("❌ Sistema de cronômetros não disponível")
    except Exception as e:
        print(f"❌ Erro no gerenciamento de cronômetros: {e}")
    
    input("\nPressione ENTER para continuar...")

def gerenciar_perfil():
    """Sistema de gerenciamento do perfil do usuário"""
    limpar_tela()
    print("\n👤 MEU PERFIL")
    print("="*50)
    print("⚙️ Gerencie suas preferências culinárias")
    print()
    
    try:
        from core_logic.database import db_manager
        
        while True:
            print("\n👤 O que você quer fazer?")
            print("   1. 📝 Atualizar Nome")
            print("   2. 🍽️ Definir Nível Culinário")
            print("   3. 🚫 Configurar Restrições Alimentares")
            print("   4. 📊 Ver Meu Perfil Atual")
            print("   5. ⬅️ Voltar ao Menu")
            print()
            
            opcao = input("🎯 Sua escolha: ").strip()
            
            if opcao == "1":
                nome = input("\n👤 Seu nome: ").strip()
                if nome:
                    db_manager.update_user_profile(name=nome)
                    print(f"✅ Nome atualizado para: {nome}")
                    
            elif opcao == "2":
                print("\n🎯 Qual seu nível na cozinha?")
                print("   1. 🔰 Iniciante")
                print("   2. 🥄 Intermediário")
                print("   3. 👨‍🍳 Avançado")
                
                nivel_opcao = input("Nível: ").strip()
                niveis = {"1": "iniciante", "2": "intermediario", "3": "avancado"}
                
                if nivel_opcao in niveis:
                    db_manager.update_user_profile(cooking_level=niveis[nivel_opcao])
                    print(f"✅ Nível definido como: {niveis[nivel_opcao].title()}")
                    
            elif opcao == "3":
                print("\n🚫 Restrições alimentares (separadas por vírgula):")
                print("💡 Ex: vegetariano, sem glúten, sem lactose")
                restricoes = input("Suas restrições: ").strip()
                if restricoes:
                    lista_restricoes = [r.strip() for r in restricoes.split(",")]
                    db_manager.update_user_profile(dietary_restrictions=lista_restricoes)
                    print("✅ Restrições atualizadas!")
                    
            elif opcao == "4":
                perfil = db_manager.get_user_profile()
                print("\n📋 SEU PERFIL ATUAL:")
                print("="*40)
                print(f"👤 Nome: {perfil.get('name', 'Não definido')}")
                print(f"🎯 Nível: {perfil.get('cooking_level', 'Não definido')}")
                restricoes = perfil.get('dietary_restrictions', [])
                print(f"🚫 Restrições: {', '.join(restricoes) if restricoes else 'Nenhuma'}")
                print("="*40)
                
            elif opcao == "5":
                break
            else:
                print("❌ Opção inválida!")
                
    except ImportError:
        print("❌ Sistema de perfil não disponível")
    except Exception as e:
        print(f"❌ Erro no gerenciamento de perfil: {e}")
    
    input("\nPressione ENTER para continuar...")

def run_voice_mode():
    """Executa o modo reconhecimento de voz"""
    try:
        from core_logic.voice_recognition import voice_recognition
        from core_logic import rag_system
        
        clear_screen()
        print("\n🎤 Reconhecimento de Voz")
        print("="*30)
        
        # Testa microfone
        test_result = voice_recognition.test_microphone()
        
        if not test_result['available']:
            print(f"❌ {test_result['message']}")
            input("\nPressione ENTER para voltar...")
            return
        
        print("✅ Microfone OK")
        
        # Loop para reconhecimento contínuo
        while True:
            print("\n" + "-" * 30)
            print("1. 🎙️ Reconhecer")
            print("2. ⬅️ Voltar")
            
            sub_choice = input("\n➤ Escolha: ").strip()
            
            if sub_choice == "1":
                print("\n💡 Fale após pressionar ENTER")
                print("   Ex: 'Tenho tomate, cebola e alho'")
                
                input("\nPressione ENTER e fale...")
                
                # Reconhece ingredientes
                ingredients = voice_recognition.recognize_ingredients(timeout=8, phrase_time_limit=15)
                
                if ingredients:
                    print(f"\n✅ Reconhecido: {ingredients}")
                    
                    # Busca receitas
                    print("🔍 Buscando receitas...")
                    recipes_response = rag_system.find_recipes_by_ingredient(
                        ingredients, 
                        source_mode='voice_terminal'
                    )
                    
                    print("\n📋 RECEITAS:")
                    print("=" * 25)
                    print(recipes_response)
                    print("=" * 25)
                    
                else:
                    print("❌ Não reconhecido")
                
                input("\nPressione ENTER para continuar...")
                
            elif sub_choice == "2":
                break
            else:
                print("❌ Opção inválida!")
                
    except ImportError:
        print("❌ Módulo de voz não disponível")
        print("💡 Instale: pip install SpeechRecognition pyaudio")
        input("\nPressione ENTER para voltar...")
    except Exception as e:
        print(f"❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

def run_user_profile():
    """Executa o gerenciador de perfil do usuário"""
    try:
        from core_logic.database import history_db
        import json
        
        print("\n👤 Perfil do Usuário")
        print("="*30)
        
        # Carrega perfil atual
        profile_data = history_db.get_user_profile_with_stats()
        profile = profile_data['profile']
        
        print("\n📊 Informações Atuais:")
        print(f"👤 Nome: {profile.get('name', 'Não definido')}")
        print(f"🎯 Nível: {profile.get('skill_level', 'iniciante')}")
        print(f"⏰ Tempo preferido: {profile.get('preferred_cooking_time', 60)} min")
        print(f"💰 Orçamento: {profile.get('budget_preference', 'medio')}")
        
        # Restrições alimentares
        restrictions = json.loads(profile.get('dietary_restrictions', '[]'))
        print(f"🥗 Restrições: {', '.join(restrictions) if restrictions else 'Nenhuma'}")
        
        # Estatísticas
        print(f"\n📈 Estatísticas:")
        print(f"🔝 Ingredientes favoritos: {', '.join([f'{ing[0]} ({ing[1]}x)' for ing in profile_data['top_ingredients'][:3]])}")
        print(f"⭐ Avaliação média: {profile_data['avg_rating']:.1f}/5.0")
        print(f"📝 Total de avaliações: {profile_data['total_ratings']}")
        
        while True:
            print("\nEscolha uma opção:")
            print("1. ✏️ Editar Nome")
            print("2. 🎯 Alterar Nível Culinário")
            print("3. 🥗 Gerenciar Restrições Alimentares")
            print("4. ⏰ Definir Tempo de Cozinha Preferido")
            print("5. 💰 Configurar Orçamento")
            print("6. 🔙 Voltar ao Menu Principal")
            
            choice = input("\n➤ Escolha (1-6): ").strip()
            
            if choice == "1":
                new_name = input("\n👤 Digite seu nome: ").strip()
                if new_name:
                    history_db.update_user_profile(name=new_name)
                    print(f"✅ Nome atualizado para: {new_name}")
                    
            elif choice == "2":
                print("\n🎯 Escolha seu nível culinário:")
                print("1. 🔰 Iniciante")
                print("2. 📚 Intermediário")
                print("3. 👨‍🍳 Avançado")
                print("4. 🌟 Profissional")
                
                level_choice = input("➤ Escolha (1-4): ").strip()
                levels = {'1': 'iniciante', '2': 'intermediario', '3': 'avancado', '4': 'profissional'}
                
                if level_choice in levels:
                    history_db.update_user_profile(skill_level=levels[level_choice])
                    print(f"✅ Nível atualizado para: {levels[level_choice]}")
                    
            elif choice == "3":
                print("\n🥗 Gerenciar Restrições Alimentares")
                current_restrictions = json.loads(profile.get('dietary_restrictions', '[]'))
                
                print(f"\nRestrições atuais: {', '.join(current_restrictions) if current_restrictions else 'Nenhuma'}")
                print("\n1. ➕ Adicionar restrição")
                print("2. ➖ Remover restrição")
                print("3. 🗑️ Limpar todas")
                
                rest_choice = input("➤ Escolha (1-3): ").strip()
                
                if rest_choice == "1":
                    available = ['Vegetariano', 'Vegano', 'Sem Glúten', 'Low Carb', 'Diabético', 'Sem Lactose']
                    print("\nRestrições disponíveis:")
                    for i, rest in enumerate(available, 1):
                        print(f"{i}. {rest}")
                    
                    try:
                        rest_idx = int(input("➤ Escolha uma restrição: ").strip()) - 1
                        if 0 <= rest_idx < len(available):
                            new_restriction = available[rest_idx]
                            if new_restriction not in current_restrictions:
                                current_restrictions.append(new_restriction)
                                history_db.update_user_profile(dietary_restrictions=json.dumps(current_restrictions))
                                print(f"✅ {new_restriction} adicionado!")
                            else:
                                print("⚠️ Restrição já existe.")
                    except (ValueError, IndexError):
                        print("❌ Opção inválida!")
                        
                elif rest_choice == "2" and current_restrictions:
                    print("\nRestrições atuais:")
                    for i, rest in enumerate(current_restrictions, 1):
                        print(f"{i}. {rest}")
                    
                    try:
                        rest_idx = int(input("➤ Escolha para remover: ").strip()) - 1
                        if 0 <= rest_idx < len(current_restrictions):
                            removed = current_restrictions.pop(rest_idx)
                            history_db.update_user_profile(dietary_restrictions=json.dumps(current_restrictions))
                            print(f"✅ {removed} removido!")
                    except (ValueError, IndexError):
                        print("❌ Opção inválida!")
                        
                elif rest_choice == "3":
                    confirm = input("\n⚠️ Confirma remoção de todas as restrições? (s/n): ").strip().lower()
                    if confirm == 's':
                        history_db.update_user_profile(dietary_restrictions='[]')
                        print("✅ Todas as restrições removidas!")
                        
            elif choice == "4":
                try:
                    new_time = int(input("\n⏰ Tempo preferido para cozinhar (minutos): ").strip())
                    if new_time > 0:
                        history_db.update_user_profile(preferred_cooking_time=new_time)
                        print(f"✅ Tempo preferido atualizado: {new_time} minutos")
                    else:
                        print("❌ Tempo deve ser maior que 0")
                except ValueError:
                    print("❌ Por favor, digite um número válido.")
                    
            elif choice == "5":
                print("\n💰 Configurar Orçamento:")
                print("1. 💵 Baixo")
                print("2. 💰 Médio")
                print("3. 💎 Alto")
                
                budget_choice = input("➤ Escolha (1-3): ").strip()
                budgets = {'1': 'baixo', '2': 'medio', '3': 'alto'}
                
                if budget_choice in budgets:
                    history_db.update_user_profile(budget_preference=budgets[budget_choice])
                    print(f"✅ Orçamento atualizado para: {budgets[budget_choice]}")
                    
            elif choice == "6":
                break
            else:
                print("❌ Opção inválida!")
                
    except ImportError as e:
        print(f"❌ Erro ao importar módulo de perfil: {e}")
    except Exception as e:
        print(f"❌ Erro no gerenciador de perfil: {e}")

def run_timer_mode():
    """Executa o gerenciador de timers"""
    try:
        from core_logic.timer_manager import timer_manager
        from core_logic import rag_system
        
        clear_screen()
        print("\n⏰ Gerenciador de Timers")
        print("="*30)
        
        while True:
            print("\n1. ⏲️ Criar Timer")
            print("2. 📋 Ver Ativos")
            print("3. ⏹️ Parar Timer")
            print("4. 📖 Extrair de Receita")
            print("5. ⚡ Pré-definidos")
            print("6. 🔙 Voltar")
            
            choice = input("\n➤ Escolha: ").strip()
            
            if choice == "1":
                # Criar timer personalizado
                timer_name = input("\n📝 Nome: ").strip()
                recipe_name = input("📖 Receita (opcional): ").strip()
                step_desc = input("📋 Etapa (opcional): ").strip()
                
                try:
                    duration = int(input("⏱️ Minutos: ").strip())
                    if duration <= 0:
                        print("❌ Duração inválida")
                        continue
                        
                    timer_id = timer_manager.create_timer(
                        timer_name=timer_name,
                        duration_minutes=duration,
                        recipe_name=recipe_name,
                        step_description=step_desc
                    )
                    
                    print(f"\n✅ Timer '{timer_name}' criado! ID: {timer_id}")
                    print(f"⏰ Duração: {duration} minutos")
                    print("🔔 Você será notificado quando terminar.")
                    
                except ValueError:
                    print("❌ Por favor, digite um número válido para a duração.")
                except Exception as e:
                    print(f"❌ Erro ao criar timer: {e}")
                    
            elif choice == "2":
                # Ver timers ativos
                active_timers = timer_manager.get_active_timers()
                
                if not active_timers:
                    print("\n📭 Nenhum timer ativo no momento.")
                else:
                    print("\n⏰ Timers Ativos:")
                    print("-" * 50)
                    for timer in active_timers:
                        print(f"🆔 ID: {timer['id']}")
                        print(f"📝 Nome: {timer['name']}")
                        if timer['recipe']:
                            print(f"📖 Receita: {timer['recipe']}")
                        if timer['step']:
                            print(f"📋 Etapa: {timer['step']}")
                        print(f"⏱️ Tempo restante: {timer['remaining_formatted']}")
                        print(f"🔄 Status: {timer['status']}")
                        print("-" * 30)
                        
            elif choice == "3":
                # Parar timer
                active_timers = timer_manager.get_active_timers()
                
                if not active_timers:
                    print("\n📭 Nenhum timer ativo para parar.")
                else:
                    print("\n⏰ Timers Ativos:")
                    for timer in active_timers:
                        print(f"🆔 {timer['id']}: {timer['name']} - {timer['remaining_formatted']}")
                    
                    try:
                        timer_id = int(input("\n🆔 Digite o ID do timer para parar: ").strip())
                        if timer_manager.stop_timer(timer_id):
                            print(f"\n✅ Timer {timer_id} parado com sucesso!")
                        else:
                            print(f"\n❌ Timer {timer_id} não encontrado.")
                    except ValueError:
                        print("❌ Por favor, digite um número válido.")
                        
            elif choice == "4":
                # Extrair timers de receita
                print("\n📖 Extrair Timers de Receita")
                recipe_text = input("\n📋 Cole o texto da receita:\n").strip()
                
                if recipe_text:
                    print("\n🧠 Analisando receita...")
                    steps_data = rag_system.extract_recipe_steps_with_timers(recipe_text)
                    
                    if steps_data and 'steps_with_timers' in steps_data:
                        print(f"\n📖 Receita: {steps_data.get('recipe_name', 'Sem nome')}")
                        print(f"⏰ Tempo total: {steps_data.get('total_time', 'N/A')} minutos")
                        print("\n📋 Etapas com timers:")
                        
                        for step in steps_data['steps_with_timers']:
                            critical_mark = "🔥" if step.get('is_critical') else "⏲️"
                            print(f"\n{critical_mark} Etapa {step['step_number']}: {step['description']}")
                            print(f"   ⏱️ Timer: {step['timer_minutes']} min - '{step['timer_name']}'")
                            
                            # Opção para criar o timer
                            create = input(f"   ➕ Criar este timer? (s/n): ").strip().lower()
                            if create == 's':
                                timer_id = timer_manager.create_timer(
                                    timer_name=step['timer_name'],
                                    duration_minutes=step['timer_minutes'],
                                    recipe_name=steps_data.get('recipe_name', ''),
                                    step_description=step['description']
                                )
                                print(f"   ✅ Timer criado! ID: {timer_id}")
                        
                        if 'preparation_tips' in steps_data:
                            print("\n💡 Dicas de preparo:")
                            for tip in steps_data['preparation_tips']:
                                print(f"   • {tip}")
                    else:
                        print("\n❌ Não foi possível extrair timers da receita.")
                        
            elif choice == "5":
                # Timers pré-definidos
                presets = timer_manager.list_timer_presets()
                print("\n⚡ Timers Pré-definidos:")
                print("-" * 30)
                
                preset_list = list(presets.items())
                for i, (name, minutes) in enumerate(preset_list, 1):
                    print(f"{i}. {name}: {minutes} min")
                
                try:
                    preset_choice = int(input(f"\n➤ Escolha um preset (1-{len(preset_list)}): ").strip())
                    if 1 <= preset_choice <= len(preset_list):
                        preset_name, preset_duration = preset_list[preset_choice - 1]
                        
                        timer_id = timer_manager.create_timer(
                            timer_name=preset_name,
                            duration_minutes=preset_duration
                        )
                        
                        print(f"\n✅ Timer '{preset_name}' criado! ID: {timer_id}")
                        print(f"⏰ Duração: {preset_duration} minutos")
                    else:
                        print("❌ Opção inválida!")
                except ValueError:
                    print("❌ Por favor, digite um número válido.")
                    
            elif choice == "6":
                break
            else:
                print("❌ Opção inválida!")
                
    except ImportError as e:
        print(f"❌ Erro ao importar timer manager: {e}")
    except Exception as e:
        print(f"❌ Erro no gerenciador de timers: {e}")
def verificar_dependencias():
    """Verifica se os requisitos básicos estão atendidos"""
    # Verifica se a base de dados existe
    chroma_db_file = os.path.join(config.CHROMA_DB_PATH, "chroma.sqlite3")
    if not os.path.exists(chroma_db_file):
        limpar_tela()
        print("❌ Base de receitas não encontrada!")
        print("💡 Para carregar receitas, execute: python pdf_inge.py")
        print("🔄 O sistema funcionará em modo demonstração")
        input("Pressione ENTER para continuar...")
    
    try:
        # Verificações básicas de dependências
        import cv2
        import numpy
        return True
    except ImportError as e:
        print(f"❌ Biblioteca não encontrada: {e}")
        print("🔧 Execute: pip install -r requirements.txt")
        return False

def configurar_limpeza_automatica():
    """Configura o sistema de limpeza automática de imagens"""
    try:
        from core_logic.cleanup_manager import cleanup_manager
        cleanup_manager.start_cleanup_timer()
        print("🧹 Sistema de limpeza automática ativado!")
    except Exception:
        pass  # Não é crítico se não funcionar

def run_filters_mode():
    """Executa o modo de filtros alimentares"""
    try:
        from core_logic import rag_system
        from core_logic.database import history_db
        
        print("\n🥗 Filtros por Restrições Alimentares")
        print("="*50)
        
        # Menu de filtros
        print("\nSelecione suas restrições alimentares:")
        print("1. 🌱 Vegetariano")
        print("2. 🥬 Vegano")
        print("3. 🚫 Sem Glúten")
        print("4. ⚖️ Low Carb")
        print("5. 🍯 Diabético")
        print("6. 🥛 Sem Lactose")
        print("\n0. Continuar com filtros selecionados")
        
        filters = {}
        selected_filters = []
        
        while True:
            choice = input("\n➤ Escolha uma restrição (1-6) ou 0 para continuar: ").strip()
            
            if choice == "1":
                filters['vegetarian'] = True
                selected_filters.append("Vegetariano")
                print("✅ Vegetariano adicionado")
            elif choice == "2":
                filters['vegan'] = True
                selected_filters.append("Vegano")
                print("✅ Vegano adicionado")
            elif choice == "3":
                filters['gluten_free'] = True
                selected_filters.append("Sem Glúten")
                print("✅ Sem Glúten adicionado")
            elif choice == "4":
                filters['low_carb'] = True
                selected_filters.append("Low Carb")
                print("✅ Low Carb adicionado")
            elif choice == "5":
                filters['diabetic_friendly'] = True
                selected_filters.append("Diabético")
                print("✅ Diabético adicionado")
            elif choice == "6":
                filters['lactose_free'] = True
                selected_filters.append("Sem Lactose")
                print("✅ Sem Lactose adicionado")
            elif choice == "0":
                break
            else:
                print("❌ Opção inválida!")
        
        if not filters:
            print("\n⚠️ Nenhum filtro selecionado.")
            return
        
        print(f"\n📋 Filtros selecionados: {', '.join(selected_filters)}")
        
        # Pede ingredientes
        ingredients = input("\n🥕 Digite os ingredientes que você tem (ex: tomate, cebola): ").strip()
        
        if not ingredients:
            print("\n❌ Nenhum ingrediente fornecido.")
            return
        
        print("\n🧠 Buscando receitas que atendem seus filtros...")
        
        # Gera receitas filtradas
        result = rag_system.generate_filtered_recipe_suggestions(ingredients, filters)
        
        print("\n" + "="*80)
        print(result)
        print("="*80)
        
    except Exception as e:
        print(f"❌ Erro ao executar filtros alimentares: {e}")

def run_timer_mode():
    """Executa o gerenciador de timers"""
    try:
        from core_logic.timer_manager import TimerManager
        
        timer_manager = TimerManager()
        
        while True:
            print("\n⏰ Gerenciador de Timers")
            print("="*40)
            
            print("Escolha uma opção:")
            print("1. ⏲️ Criar Timer Novo")
            print("2. 📋 Ver Timers Ativos")
            print("3. ⏹️ Parar Timer")
            print("4. 📖 Extrair Timers de Receita")
            print("5. ⚡ Timers Pré-definidos")
            print("6. 🔙 Voltar ao Menu Principal")
            
            choice = input("\n➤ Escolha (1-6): ").strip()
            
            if choice == "1":
                # Criar novo timer
                name = input("📝 Nome do timer: ").strip()
                if not name:
                    print("❌ Nome não pode estar vazio!")
                    continue
                    
                try:
                    duration = int(input("⏱️ Duração em minutos: ").strip())
                    if duration <= 0:
                        print("❌ Duração deve ser maior que 0!")
                        continue
                except ValueError:
                    print("❌ Duração deve ser um número!")
                    continue
                
                recipe = input("🍳 Nome da receita (opcional): ").strip()
                step = input("📋 Descrição da etapa (opcional): ").strip()
                
                timer_id = timer_manager.create_timer(name, duration, recipe, step)
                print(f"✅ Timer '{name}' criado com ID: {timer_id}")
                
            elif choice == "2":
                # Ver timers ativos
                active_timers = timer_manager.get_active_timers()
                if not active_timers:
                    print("📝 Nenhum timer ativo.")
                else:
                    print("\n📋 Timers Ativos:")
                    for timer in active_timers:
                        print(f"🆔 {timer['timer_id']}: {timer['timer_name']} - {timer['recipe_name']}")
                        
            elif choice == "3":
                # Parar timer
                timer_id = input("🆔 Digite o ID do timer para parar: ").strip()
                if timer_manager.stop_timer(timer_id):
                    print(f"⏹️ Timer {timer_id} parado com sucesso!")
                else:
                    print(f"❌ Timer {timer_id} não encontrado ou já parado.")
                    
            elif choice == "4":
                # Extrair timers de receita
                recipe_text = input("📜 Cole o texto da receita: ").strip()
                if recipe_text:
                    from core_logic.rag_system import extract_recipe_steps_with_timers
                    steps_with_timers = extract_recipe_steps_with_timers(recipe_text)
                    
                    if steps_with_timers.get('steps'):
                        print(f"\n📊 Encontrados {len(steps_with_timers['steps'])} passos com timers:")
                        for i, step in enumerate(steps_with_timers['steps'], 1):
                            print(f"{i}. {step['description']} - ⏰ {step['duration']} min")
                    else:
                        print("❌ Nenhum timer encontrado na receita.")
                        
            elif choice == "5":
                # Timers pré-definidos
                presets = {
                    "🍝 Massa": 8,
                    "🍚 Arroz": 15,
                    "🥚 Ovo cozido": 10,
                    "☕ Café": 5,
                    "🍖 Carne assada": 45,
                }
                
                print("\n⚡ Timers Pré-definidos:")
                for i, (name, duration) in enumerate(presets.items(), 1):
                    print(f"{i}. {name} - {duration} min")
                
                try:
                    preset_choice = int(input("\n➤ Escolha um preset (1-5): ").strip()) - 1
                    preset_items = list(presets.items())
                    if 0 <= preset_choice < len(preset_items):
                        name, duration = preset_items[preset_choice]
                        timer_id = timer_manager.create_timer(name, duration)
                        print(f"✅ Timer '{name}' criado com ID: {timer_id}")
                    else:
                        print("❌ Opção inválida!")
                except ValueError:
                    print("❌ Digite um número válido!")
                    
            elif choice == "6":
                break
            else:
                print("❌ Opção inválida!")
        
    except Exception as e:
        print(f"❌ Erro no gerenciador de timers: {e}")

def run_profile_mode():
    """Alias para run_user_profile() para manter consistência"""
    run_user_profile()

def main():
    """Função principal do sistema"""
    if not verificar_dependencias():
        sys.exit(1)
    
    # Configurar sistema de limpeza automática
    configurar_limpeza_automatica()
    
    while True:
        try:
            mostrar_menu()
            escolha = input("\n🎯 Qual opção você escolhe? ").strip()
            
            if escolha == "1":
                usar_camera_pc()
                
            elif escolha == "2":
                usar_camera_celular()
                
            elif escolha == "3":
                enviar_foto_ingredientes()
                
            elif escolha == "4":
                digitar_ingredientes()
                
            elif escolha == "5":
                falar_ingredientes()
                
            elif escolha == "6":
                filtrar_por_dieta()
                
            elif escolha == "7":
                gerenciar_cronometros()
                
            elif escolha == "8":
                executar_historico()
                
            elif escolha == "9":
                gerenciar_perfil()
                
            elif escolha == "10":
                limpar_tela()
                print("\n" + "="*50)
                print("🍽️ Obrigado por usar o Chef RAG!")
                print("👨‍🍳 Volte sempre que quiser novas receitas!")
                print("="*50)
                break
                
            else:
                print("\n❌ Opção inválida! Por favor, escolha um número de 1 a 10.")
                input("Pressione ENTER para tentar novamente...")
                
        except KeyboardInterrupt:
            limpar_tela()
            print("\n👋 Sistema encerrado pelo usuário.")
            print("🍽️ Até a próxima!")
            break
            
        except Exception as e:
            print(f"\n❌ Ops! Ocorreu um erro inesperado: {e}")
            print("🔧 Tente novamente ou reinicie o sistema.")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()
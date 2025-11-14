#!/usr/bin/env python3
"""
Sistema Chef RAG - Sistema de Análise de Ingredientes e Sugestão de Receitas

Permite ao usuário escolher entre:
1. Webcam - Captura imagens em tempo real da webcam
2. Pasta - Monitor uma pasta para novas imagens
"""

import sys
import os
from core_logic import config
from core_logic.cleanup_manager import setup_image_cleanup

def show_menu():
    """Exibe o menu principal do sistema"""
    print("\n" + "="*60)
    print("🧑‍🍳 CHEF RAG - Sistema de Receitas Inteligente")
    print("="*60)
    print("Escolha uma opção:")
    print()
    print("📸 ANÁLISE DE INGREDIENTES:")
    print("1. 📷 Webcam - Capturar ingredientes em tempo real")
    print("2. 📁 Pasta - Monitorar pasta para novas imagens") 
    print("3. 🎤 Voz - Reconhecer ingredientes por comando de voz")
    print()
    print("🔍 BUSCA ESPECIALIZADA:")
    print("4. 🥗 Filtros Alimentares - Buscar receitas por restrições")
    print("5. ⏰ Timers - Gerenciar cronômetros de receitas")
    print()
    print("📊 DADOS E HISTÓRICO:")
    print("6. 📄 Histórico - Ver análises anteriores")
    print("7. 👤 Perfil - Configurar preferências do usuário")
    print()
    print("8. ❌ Sair")
    print()
    print("="*60)

def run_history_mode():
    """Executa o visualizador de histórico"""
    try:
        from history_viewer import main as history_main
        print("\n🎯 Abrindo visualizador de histórico...")
        history_main()
    except ImportError as e:
        print(f"❌ Erro ao importar visualizador: {e}")
    except Exception as e:
        print(f"❌ Erro no visualizador: {e}")

def run_webcam_mode():
    """Executa o modo webcam"""
    try:
        from webcam import run_webcam_capture
        print("\n🎯 Iniciando modo Webcam...")
        run_webcam_capture()
    except ImportError as e:
        print(f"❌ Erro ao importar módulo webcam: {e}")
    except Exception as e:
        print(f"❌ Erro no modo webcam: {e}")

def run_folder_mode():
    """Executa o modo monitoramento de pasta"""
    try:
        from monitor import start_monitoring
        print("\n🎁 Iniciando monitoramento de pasta...")
        start_monitoring()
    except ImportError as e:
        print(f"❌ Erro ao importar módulo monitor: {e}")
    except Exception as e:
        print(f"❌ Erro no modo pasta: {e}")

def run_voice_mode():
    """Executa o modo reconhecimento de voz"""
    try:
        from core_logic.voice_recognition import voice_recognition
        from core_logic import rag_system
        
        print("\n🎤 Iniciando modo Reconhecimento de Voz...")
        print("="*50)
        
        # Testa microfone
        print("🔧 Verificando microfone...")
        test_result = voice_recognition.test_microphone()
        
        if not test_result['available']:
            print(f"❌ {test_result['message']}")
            print("💡 Verifique se o microfone está conectado e as permissões estão corretas")
            return
        
        print(f"✅ {test_result['message']}")
        print()
        
        # Loop para reconhecimento contínuo
        while True:
            print("-" * 30)
            print("Opções:")
            print("1. 🎙️ Reconhecer ingredientes")
            print("2. ⬅️ Voltar ao menu principal")
            print()
            
            sub_choice = input("➤ Digite sua escolha (1-2): ").strip()
            print()
            
            if sub_choice == "1":
                print("🎤 RECONHECIMENTO DE VOZ")
                print("=" * 30)
                print("💡 Dicas:")
                print("   - Fale claramente: 'Tenho tomate, cebola e alho'")
                print("   - Evite ruídos de fundo")
                print("   - Fale após o sinal")
                print()
                
                input("Pressione ENTER para começar a gravação...")
                print()
                
                # Reconhece ingredientes
                ingredients = voice_recognition.recognize_ingredients(timeout=8, phrase_time_limit=15)
                
                if ingredients:
                    print(f"✅ Ingredientes reconhecidos: {ingredients}")
                    print()
                    
                    # Busca receitas
                    print("🔍 Buscando receitas...")
                    recipes_response = rag_system.find_recipes_by_ingredient(
                        ingredients, 
                        source_mode='voice_terminal'
                    )
                    
                    print()
                    print("📋 SUGESTÕES DE RECEITAS:")
                    print("=" * 40)
                    print(recipes_response)
                    print("=" * 40)
                    
                else:
                    print("❌ Não foi possível reconhecer ingredientes")
                    print("💭 Tente novamente falando mais devagar e claramente")
                
                print()
                input("Pressione ENTER para continuar...")
                
            elif sub_choice == "2":
                break
            else:
                print("❌ Opção inválida! Escolha 1 ou 2.")
                
    except ImportError as e:
        print(f"❌ Erro ao importar reconhecimento de voz: {e}")
        print("💡 Instale as dependências: pip install SpeechRecognition pyaudio")
    except Exception as e:
        print(f"❌ Erro no modo voz: {e}")

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

def check_requirements():
    """Executa o gerenciador de timers"""
    try:
        from core_logic.timer_manager import timer_manager
        from core_logic import rag_system
        
        print("\n⏰ Gerenciador de Timers")
        print("="*40)
        
        while True:
            print("\nEscolha uma opção:")
            print("1. ⏲️ Criar Timer Novo")
            print("2. 📋 Ver Timers Ativos")
            print("3. ⏹️ Parar Timer")
            print("4. 📖 Extrair Timers de Receita")
            print("5. ⚡ Timers Pré-definidos")
            print("6. 🔙 Voltar ao Menu Principal")
            
            choice = input("\n➤ Escolha (1-6): ").strip()
            
            if choice == "1":
                # Criar timer personalizado
                timer_name = input("\n📝 Nome do timer: ").strip()
                recipe_name = input("📖 Nome da receita (opcional): ").strip()
                step_desc = input("📋 Descrição da etapa (opcional): ").strip()
                
                try:
                    duration = int(input("⏱️ Duração em minutos: ").strip())
                    if duration <= 0:
                        print("❌ Duração deve ser maior que 0")
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
    """Verifica se os requisitos básicos estão atendidos"""
    if not config.GOOGLE_API_KEY:
        print("❌ Erro: A chave da API do Google não está configurada.")
        print("Por favor, defina GOOGLE_API_KEY no arquivo .env")
        return False
    
    # Verifica se a base de dados existe
    chroma_db_file = os.path.join(config.CHROMA_DB_PATH, "chroma.sqlite3")
    if not os.path.exists(chroma_db_file):
        print("❌ Base de dados de receitas não encontrada!")
        print("Execute primeiro: python pdf_inge.py")
        return False
    
    return True

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
    if not check_requirements():
        sys.exit(1)
    
    # Configurar sistema de limpeza de imagens
    print("🧹 Configurando sistema de limpeza automática...")
    setup_image_cleanup()
    
    while True:
        try:
            show_menu()
            choice = input("➤ Digite sua escolha (1-8): ").strip()
            
            if choice == "1":
                run_webcam_mode()
            elif choice == "2":
                run_folder_mode()
            elif choice == "3":
                run_voice_mode()
            elif choice == "4":
                run_filters_mode()
            elif choice == "5":
                run_timer_mode()
            elif choice == "6":
                run_history_mode()
            elif choice == "7":
                run_profile_mode()
            elif choice == "8":
                print("\n👋 Obrigado por usar o Chef RAG!")
                break
            else:
                print("❌ Opção inválida! Por favor, escolha 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            break

if __name__ == "__main__":
    main()
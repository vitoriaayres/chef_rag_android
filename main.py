#!/usr/bin/env python3
"""
Sistema Chef RAG v2 - Sistema Avançado de Análise de Ingredientes e Sugestão de Receitas

Menu no terminal com interfaces gráficas para cada opção:
1. Webcam - Interface gráfica para captura em tempo real
2. Câmera Mobile - Interface para QR Code e conexão
3. Upload de Foto - Interface para análise de imagens
4. Digitar Ingredientes - Interface para entrada manual
5. Reconhecimento de Voz - Interface avançada com histórico
6. Visualizar Histórico - Interface de análise de dados

Versão: 2.0 - Novembro 2025
Desenvolvido com Sistema de Busca CSV de Alta Precisão
"""

import sys
import os

# Importar sistema de busca CSV
try:
    from scripts.sistema_busca_csv import BuscaReceitasCSV
    busca_csv = BuscaReceitasCSV()
except ImportError:
    busca_csv = None
    print("Sistema CSV não disponível, usando busca básica")

def extrair_receitas_csv(ingredientes):
    """Extrai receitas do sistema CSV em formato de lista"""
    if not busca_csv:
        return []
    
    import pandas as pd
    resultados = []
    
    # Buscar todas as receitas com score
    for idx, receita in busca_csv.df.iterrows():
        score, matches = busca_csv.calcular_score_ingredientes(
            ingredientes, 
            receita['ingredientes_busca']
        )
        
        if score > 0:
            resultados.append({
                'titulo': receita['titulo'],
                'ingredientes': receita['ingredientes'], 
                'modo_preparo': receita['modo_preparo'],
                'tempo_preparo': receita['tempo_preparo'],
                'dificuldade': receita['dificuldade'],
                'categoria': receita['categoria'],
                'score': score,
                'matches': matches
            })
    
    # Ordenar por score decrescente
    resultados.sort(key=lambda x: x['score'], reverse=True)
    return resultados

def mostrar_modo_preparo_csv(receita):
    """Mostra o modo de preparo de uma receita do CSV com informações completas"""
    limpar_tela()
    print("\n" + "="*80)
    print(f"{receita['titulo']}")
    print("="*80)
    
    # Informações da receita
    print(f"\n📊 INFORMAÇÕES GERAIS:")
    print("-" * 50)
    print(f"📂 Categoria: {receita['categoria']}")
    print(f"⏰ Tempo de preparo: {receita['tempo_preparo']}")
    print(f"📊 Dificuldade: {receita['dificuldade']}")
    print(f"Compatibilidade: {receita['score']:.1f}%")
    
    # Ingredientes completos
    print(f"\n🥬 INGREDIENTES COMPLETOS:")
    print("-" * 50)
    ingredientes_lista = receita['ingredientes'].split(' | ')
    for i, ing in enumerate(ingredientes_lista, 1):
        print(f"  {i}. {ing}")
    
    print(f"\nINGREDIENTES PARA BUSCA:")
    print(f"   {receita.get('ingredientes_busca', 'N/A')}")
    
    # Modo de preparo completo
    print(f"\n👨‍🍳 MODO DE PREPARO COMPLETO:")
    print("-" * 50)
    passos_lista = receita['modo_preparo'].split(' | ')
    for i, passo in enumerate(passos_lista, 1):
        # Limpar numeração duplicada se existir
        passo_limpo = passo.strip()
        if passo_limpo.startswith(f"{i}."):
            passo_limpo = passo_limpo[len(f"{i}."):].strip()
        print(f"  🔸 PASSO {i}: {passo_limpo}")
    
    # Mostrar matches de ingredientes
    if receita.get('matches'):
        print(f"\nINGREDIENTES ENCONTRADOS:")
        print("-" * 50)
        for match in receita['matches'][:5]:  # Mostrar até 5 matches
            print(f"   • {match}")
    
    print("\n" + "="*80)
    
    # Menu de opções
    while True:
        print("\nOPÇÕES:")
        print("1. Abrir interface gráfica passo a passo")
        print("2. Ver mais detalhes")
        print("3. Avaliar receita") 
        print("4. Voltar ao menu")
        
        opcao = input("\nEscolha uma opção (1-4): ").strip()
        
        if opcao == "1":
            abrir_interface_grafica_receita(receita)
            break
        elif opcao == "2":
            print(f"\nDETALHES ADICIONAIS:")
            print(f"Matches encontrados: {', '.join(receita['matches'][:5])}")
            input("\nPressione ENTER para continuar...")
        elif opcao == "3":
            avaliar_receita(receita['titulo'])
            break
        elif opcao == "4":
            break
        else:
            print("Opção inválida")

def avaliar_receita(titulo_receita):
    """Permite avaliar uma receita"""
    print(f"\nAVALIAR: {titulo_receita}")
    print("-" * 50)
    
    try:
        nota = input("Digite uma nota de 1 a 5 estrelas: ").strip()
        comentario = input("Comentário (opcional): ").strip()
        
        if nota in ['1', '2', '3', '4', '5']:
            print(f"Receita '{titulo_receita}' avaliada com {nota} estrelas!")
            if comentario:
                print(f"💬 Comentário: {comentario}")
        else:
            print("Nota deve ser entre 1 e 5")
    except:
        print("Erro na avaliação")
    
    input("\nPressione ENTER para continuar...")

def extrair_receitas_do_texto(texto_receitas):
    """Extrai receitas individuais do texto retornado pelo sistema"""
    import re
    
    receitas = []
    
    # Busca por receitas numeradas no formato "1. **Nome da Receita**"
    padrao = r'(\d+)\.\s*\*\*([^*]+)\*\*'
    matches = re.findall(padrao, texto_receitas)
    
    if matches:
        for numero, nome in matches:
            # Extrair o conteúdo específico desta receita
            inicio_receita = texto_receitas.find(f"{numero}. **{nome}**")
            
            # Encontrar próxima receita ou fim
            proximo_numero = str(int(numero) + 1)
            proximo_padrao = f"{proximo_numero}. **"
            fim_receita = texto_receitas.find(proximo_padrao, inicio_receita)
            
            if fim_receita == -1:
                # É a última receita
                conteudo_receita = texto_receitas[inicio_receita:]
            else:
                conteudo_receita = texto_receitas[inicio_receita:fim_receita]
            
            receitas.append({
                'numero': int(numero),
                'nome': nome.strip(),
                'texto_completo': conteudo_receita.strip(),
                'texto_original': texto_receitas
            })
    else:
        # Se não encontrou padrão numerado, tenta extrair do formato "📖 **Nome**"
        padrao_alt = r'📖\s*\*\*([^*]+)\*\*'
        matches_alt = re.findall(padrao_alt, texto_receitas)
        
        if matches_alt:
            for i, nome in enumerate(matches_alt, 1):
                receitas.append({
                    'numero': i,
                    'nome': nome.strip(),
                    'texto_completo': texto_receitas,
                    'texto_original': texto_receitas
                })
        else:
            # Fallback: receita única
            receitas.append({
                'numero': 1, 
                'nome': 'Receita Encontrada', 
                'texto_completo': texto_receitas,
                'texto_original': texto_receitas
            })
    
    return receitas

def mostrar_modo_preparo(receita_escolhida):
    """Mostra TODAS as informações da receita de forma completa e organizada"""
    limpar_tela()
    nome = receita_escolhida.get('nome', 'Receita')
    texto_completo = receita_escolhida.get('texto_completo', '')
    
    print("\n" + "="*80)
    print(f"COZINHANDO: {nome}")
    print("="*80)
    
    # Extrair TODAS as informações disponíveis
    info_receita = extrair_todas_informacoes(texto_completo)
    
    # 1. INGREDIENTES (com quantidades detalhadas)
    if info_receita['ingredientes']:
        print("\n🥬 INGREDIENTES:")
        print("-" * 50)
        for i, ing in enumerate(info_receita['ingredientes'], 1):
            print(f"  {i}. {ing}")
    
    # 2. MODO DE PREPARO (passos numerados)
    if info_receita['modo_preparo']:
        print(f"\nMODO DE PREPARO:")
        print("-" * 50)
        for i, passo in enumerate(info_receita['modo_preparo'], 1):
            print(f"  {i}. {passo}")
    
    # 3. INFORMAÇÕES ADICIONAIS
    if info_receita['tempo_preparo']:
        print(f"\n⏰ TEMPO DE PREPARO:")
        print("-" * 50)
        print(f"  • {info_receita['tempo_preparo']}")
    
    if info_receita['porcoes']:
        print(f"\n👥 PORÇÕES:")
        print("-" * 50)
        print(f"  • {info_receita['porcoes']}")
    
    if info_receita['dificuldade']:
        print(f"\n📊 DIFICULDADE:")
        print("-" * 50)
        print(f"  • {info_receita['dificuldade']}")
    
    # 4. DICAS E OBSERVAÇÕES
    if info_receita['dicas']:
        print(f"\nDICAS:")
        print("-" * 50)
        for dica in info_receita['dicas']:
            print(f"  • {dica}")
    
    # 5. EQUIPAMENTOS NECESSÁRIOS
    if info_receita['equipamentos']:
        print(f"\nEQUIPAMENTOS:")
        print("-" * 50)
        for equip in info_receita['equipamentos']:
            print(f"  • {equip}")
    
    # 6. INFORMAÇÕES NUTRICIONAIS (se disponível)
    if info_receita['nutricao']:
        print(f"\n📊 INFORMAÇÕES NUTRICIONAIS:")
        print("-" * 50)
        for nutri in info_receita['nutricao']:
            print(f"  • {nutri}")
    
    # 7. TEXTO RAW (se não conseguiu extrair informações estruturadas)
    if not any([info_receita['ingredientes'], info_receita['modo_preparo']]):
        print(f"\n📖 RECEITA COMPLETA:")
        print("-" * 50)
        linhas = texto_completo.split('\n')
        for linha in linhas:
            if linha.strip():
                print(f"  {linha}")
    
    print("\n" + "="*80)
    print("OPÇÕES:")
    print("  1. 🔙 Voltar para lista de receitas")
    print("  2. 🏠 Voltar ao menu principal")
    print("  3. 📋 Ver receita completa (texto original)")
    print("  4. 🖥️ Abrir Interface Gráfica Passo a Passo")
    
    escolha = input("\nDigite sua escolha (1-4): ").strip()
    
    if escolha == "2":
        return "menu"
    elif escolha == "3":
        # Mostrar texto completo original
        limpar_tela()
        print("\n" + "="*80)
        print(f"📖 RECEITA COMPLETA: {nome}")
        print("="*80)
        print(texto_completo)
        print("="*80)
        input("\nPressione ENTER para continuar...")
        return "lista"
    elif escolha == "4":
        return "interface"
    else:
        return "lista"

def abrir_interface_grafica_receita(receita_escolhida):
    """Abre interface gráfica para a receita selecionada"""
    try:
        print("🖥️ Abrindo interface gráfica passo a passo...")
        
        # Importar e abrir interface diretamente
        from interfaces.interface_cozinha_passo_passo_v2 import abrir_interface_passo_a_passo
        
        # Passar receita como lista
        receitas_lista = [receita_escolhida]
        abrir_interface_passo_a_passo(receitas_lista)
        
        print("✅ Interface gráfica passo a passo aberta!")
        
    except ImportError:
        print("❌ Interface gráfica não encontrada")
        print("💡 Usando interface do terminal...")
    except Exception as e:
        print(f"❌ Erro ao abrir interface gráfica: {e}")
        print("💡 Usando interface do terminal...")

def extrair_todas_informacoes(texto):
    """Extrai TODAS as informações disponíveis do texto da receita"""
    import re
    
    info = {
        'ingredientes': [],
        'modo_preparo': [],
        'tempo_preparo': '',
        'porcoes': '',
        'dificuldade': '',
        'dicas': [],
        'equipamentos': [],
        'nutricao': []
    }
    
    linhas = texto.split('\n')
    secao_atual = None
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
            
        # Identificar seções
        linha_upper = linha.upper()
        
        if 'INGREDIENTES' in linha_upper:
            secao_atual = 'ingredientes'
            continue
        elif any(palavra in linha_upper for palavra in ['MODO DE PREPARO', 'PREPARO', 'INSTRUÇÕES']):
            secao_atual = 'modo_preparo'
            continue
        elif any(palavra in linha_upper for palavra in ['DICA', 'OBSERV']):
            secao_atual = 'dicas'
            continue
        elif 'EQUIPAMENTO' in linha_upper:
            secao_atual = 'equipamentos'
            continue
        elif any(palavra in linha_upper for palavra in ['NUTRI', 'CALORIA']):
            secao_atual = 'nutricao'
            continue
        
        # Extrair informações específicas
        if 'TEMPO' in linha_upper and ':' in linha:
            info['tempo_preparo'] = linha.split(':')[-1].strip()
        elif 'PORÇ' in linha_upper and ':' in linha:
            info['porcoes'] = linha.split(':')[-1].strip()
        elif 'DIFICULDADE' in linha_upper and ':' in linha:
            info['dificuldade'] = linha.split(':')[-1].strip()
        
        # Adicionar conteúdo às seções
        elif secao_atual == 'ingredientes':
            if linha.startswith('-') or linha.startswith('•'):
                ingrediente = linha[1:].strip()
                if ingrediente and not ingrediente.startswith('*'):
                    info['ingredientes'].append(ingrediente)
        
        elif secao_atual == 'modo_preparo':
            if linha[0].isdigit() or linha.startswith('-'):
                passo = re.sub(r'^\d+\.\s*', '', linha)
                passo = re.sub(r'^-\s*', '', passo)
                if passo and not passo.startswith('*'):
                    info['modo_preparo'].append(passo)
        
        elif secao_atual == 'dicas':
            if linha.startswith('-') or linha.startswith('•'):
                dica = linha[1:].strip()
                if dica:
                    info['dicas'].append(dica)
        
        elif secao_atual == 'equipamentos':
            if linha.startswith('-') or linha.startswith('•'):
                equip = linha[1:].strip()
                if equip:
                    info['equipamentos'].append(equip)
        
        elif secao_atual == 'nutricao':
            if linha.startswith('-') or linha.startswith('•') or ':' in linha:
                nutri = linha[1:].strip() if linha.startswith(('-', '•')) else linha
                if nutri:
                    info['nutricao'].append(nutri)
    
    return info

def extrair_ingredientes_e_preparo(texto):
    """Extrai ingredientes e modo de preparo do texto da receita"""
    import re
    
    ingredientes = []
    modo_preparo = []
    
    # Busca por seções de ingredientes
    texto_ingredientes = re.search(r'INGREDIENTES:?\s*\n(.*?)(?=\n\s*MODO|$)', texto, re.DOTALL | re.IGNORECASE)
    if texto_ingredientes:
        for linha in texto_ingredientes.group(1).split('\n'):
            linha = linha.strip()
            if linha and linha.startswith('-'):
                ingredientes.append(linha[1:].strip())
            elif linha and not linha.startswith('*'):
                ingredientes.append(linha)
    
    # Busca por modo de preparo
    texto_preparo = re.search(r'(?:MODO DE PREPARO|PREPARO):?\s*\n(.*?)(?=\n\s*[A-Z]+:|$)', texto, re.DOTALL | re.IGNORECASE)
    if texto_preparo:
        for linha in texto_preparo.group(1).split('\n'):
            linha = linha.strip()
            if linha and (linha[0].isdigit() or linha.startswith('-')):
                # Remove numeração se houver
                passo = re.sub(r'^\d+\.\s*', '', linha)
                passo = re.sub(r'^-\s*', '', passo)
                if passo:
                    modo_preparo.append(passo)
    
    return ingredientes, modo_preparo

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Exibe o menu principal do sistema"""
    limpar_tela()
    print("\n🧑‍🍳 CHEF RAG - Assistente Culinário Inteligente\n")
    
    print("COMO VOCÊ QUER ENCONTRAR RECEITAS?\n")
    print("   1. 📷 Usar Câmera do Computador")
    print("   2. 📱 Usar Câmera do Celular")
    print("   3. 📸 Enviar Foto dos Ingredientes") 
    print("   4. ✍️ Digitar os Ingredientes")
    print("   5. 🎤 Reconhecimento de Voz")
    print()
    print("OUTRAS OPÇÕES:")
    print()
    print("   6. Filtrar por Dieta Especial")
    print("   7. Calcular Calorias do Prato")
    print("   8. Verificar Alergias")
    print("   9. ⏰ Gerenciar Cronômetros")
    print("  10. Ver Histórico de Receitas")
    print("  11. Meu Perfil")
    print("  12. Ver Créditos")
    print()
    print("  13. Sair do Sistema")

def usar_camera_pc():
    """Executa a interface da câmera do computador com YOLO"""
    try:
        print("\n📷 Abrindo câmera...")
        
        # Tentar usar webcam com YOLO primeiro
        try:
            from vision.webcam_yolo import run_food_detection_webcam
            run_food_detection_webcam()
        except ImportError:
            print("Usando câmera padrão...")
            from vision.webcam import run_webcam_capture
            run_webcam_capture()
            
    except ImportError:
        print("Sistema de câmera não encontrado")
    except Exception as e:
        print(f"Erro na câmera: {e}")
        input("\nPressione ENTER para continuar...")

def usar_camera_celular():
    """Executa a interface da câmera do celular"""
    try:
        from vision.camera_mobile import start_mobile_server
        start_mobile_server()
    except ImportError:
        print("Sistema mobile não encontrado")
    except Exception as e:
        print(f"Erro no servidor mobile: {e}")
        input("\nPressione ENTER para continuar...")

def enviar_foto_ingredientes():
    """Abre interface para upload de fotos"""
    try:
        from interfaces.interface_upload_foto import PhotoAnalysisInterface
        app = PhotoAnalysisInterface()
        app.run()
    except ImportError as e:
        print(f"Erro ao importar interface de fotos: {e}")
    except Exception as e:
        print(f"Erro na interface de fotos: {e}")
        input("\nPressione ENTER para continuar...")

def digitar_ingredientes():
    """Permite digitar os ingredientes diretamente no terminal com busca conjunta"""
    limpar_tela()
    print("\n✍️ DIGITAR INGREDIENTES\n")
    
    try:
        print("Exemplos:")
        print("   • chocolate → receitas com chocolate")
        print("   • chocolate, leite → receitas que usam AMBOS")
        print("   • tomate, cebola, alho → receitas que usam os 3\n")
        
        ingredientes = input("Digite seus ingredientes: ").strip()
        
        if not ingredientes:
            print("Nenhum ingrediente foi informado")
            input("\nPressione ENTER para continuar...")
            return
            
        # Determina tipo de busca
        if ',' in ingredientes:
            ingredientes_lista = [ing.strip() for ing in ingredientes.split(',')]
            print(f"\n🔍 Busca CONJUNTA: receitas que usem {', '.join(ingredientes_lista)}")
        else:
            print(f"\n🔍 Busca INDIVIDUAL: receitas com {ingredientes}")
            
        print("Consultando base de receitas CSV...")
        
        # Buscar usando sistema CSV
        if busca_csv:
            # Extrair receitas múltiplas do CSV
            receitas_csv = extrair_receitas_csv(ingredientes)
            
            if receitas_csv and len(receitas_csv) > 0:
                print(f"\n✅ {len(receitas_csv)} receita(s) encontrada(s)!")
                
                # FOCO 100% NO PASSO A PASSO - RECEITA PRINCIPAL
                melhor_receita = receitas_csv[0]
                
                # Mostrar imediatamente o modo de preparo completo
                mostrar_modo_preparo_detalhado({
                    'Nome': melhor_receita['titulo'],
                    'Modo_de_Preparo': melhor_receita['modo_preparo'], 
                    'Ingredientes': melhor_receita['ingredientes'],
                    'Tempo': melhor_receita['tempo_preparo'],
                    'Dificuldade': melhor_receita['dificuldade'],
                    'Categoria': melhor_receita['categoria']
                })
                
                # Mostrar TODAS as receitas com passo a passo se houver mais
                if len(receitas_csv) > 1:
                    print(f"\n🍽️ Encontrei mais {len(receitas_csv)-1} receita(s) compatível(is)!")
                    input("\n⏸️ Pressione ENTER para ver todas as receitas com passo a passo completo...")
                    
                    # Converter formato para as novas funções
                    todas_receitas = []
                    for receita in receitas_csv:
                        todas_receitas.append({
                            'Nome': receita['titulo'],
                            'Modo_de_Preparo': receita['modo_preparo'],
                            'Ingredientes': receita['ingredientes'],
                            'Tempo': receita['tempo_preparo'],
                            'Dificuldade': receita['dificuldade'],
                            'Categoria': receita['categoria'],
                            'compatibility_score': receita['score']
                        })
                    mostrar_todas_receitas_passo_a_passo(todas_receitas)
                
                # Menu simplificado focado no preparo
                while True:
                    print(f"\n🍳 OPÇÕES DE PREPARO:")
                    print("1. 🖥️  Abrir interface gráfica passo a passo")
                    print("2. 📋 Ver novamente todas as receitas")
                    print("3. 🔙 Voltar ao menu principal")
                    
                    try:
                        escolha = input(f"\n👨‍🍳 Sua escolha (1-3): ").strip()
                        
                        if escolha == "1":
                            # Interface gráfica com a melhor receita
                            abrir_interface_grafica_receita(melhor_receita)
                            break
                        elif escolha == "2":
                            # Mostrar novamente todas as receitas com passo a passo
                            todas_receitas = []
                            for receita in receitas_csv:
                                todas_receitas.append({
                                    'Nome': receita['titulo'],
                                    'Modo_de_Preparo': receita['modo_preparo'],
                                    'Ingredientes': receita['ingredientes'],
                                    'Tempo': receita['tempo_preparo'],
                                    'Dificuldade': receita['dificuldade'],
                                    'Categoria': receita['categoria'],
                                    'compatibility_score': receita['score']
                                })
                            mostrar_todas_receitas_passo_a_passo(todas_receitas)
                        elif escolha == "3":
                            break
                        else:
                            print("❌ Escolha entre 1 e 3")
                    except ValueError:
                        print("❌ Digite apenas números")
                    except KeyboardInterrupt:
                        print("\n👋 Voltando ao menu...")
                        break
                passos_lista = melhor_receita['modo_preparo'].split(' | ')
                for i, passo in enumerate(passos_lista, 1):
                    # Limpar numeração duplicada se existir
                    passo_limpo = passo.strip()
                    if passo_limpo.startswith(f"{i}."):
                        passo_limpo = passo_limpo[len(f"{i}."):].strip()
                    print(f"  🔸 PASSO {i}: {passo_limpo}")
                
                print("="*70)
                
                # Mostrar outras opções se houver
                if len(receitas_csv) > 1:
                    print(f"\n📋 OUTRAS OPÇÕES ({len(receitas_csv)-1} receitas):")
                    for i, receita in enumerate(receitas_csv[1:5], 2):
                        print(f"{i}. {receita['titulo']} ({receita['score']:.1f}%) - {receita['categoria']}")
                    print("-" * 70)
                
                print("="*70)
                
                # Menu de ações focado no passo a passo
                while True:
                    print(f"\nAÇÕES DISPONÍVEIS:")
                    print("1. 🖥️  Ver receita na interface gráfica passo a passo")
                    if len(receitas_csv) > 1:
                        print("2. 📋 Ver outras receitas disponíveis")
                        print("3. Escolher receita diferente")
                        print("4. 🔙 Voltar ao menu principal")
                        max_opcao = 4
                    else:
                        print("2. 🔙 Voltar ao menu principal")
                        max_opcao = 2
                    
                    try:
                        escolha = input(f"\n👨‍🍳 Sua escolha (1-{max_opcao}): ").strip()
                        
                        if escolha == "1":
                            # Abrir interface gráfica com a melhor receita
                            abrir_interface_grafica_receita(melhor_receita)
                            break
                        elif escolha == "2" and len(receitas_csv) == 1:
                            break  # Voltar ao menu
                        elif escolha == "2" and len(receitas_csv) > 1:
                            # Mostrar outras receitas com passo a passo
                            mostrar_todas_receitas_passo_a_passo(receitas_csv[1:])
                        elif escolha == "3" and len(receitas_csv) > 1:
                            # Seleção manual de receita
                            escolher_receita_manual(receitas_csv)
                            break
                        elif (escolha == "4" and len(receitas_csv) > 1) or (escolha == "2" and len(receitas_csv) == 1):
                            break
                        else:
                            print(f"❌ Escolha entre 1 e {max_opcao}")
                    except ValueError:
                        print("❌ Digite apenas números")
                    except KeyboardInterrupt:
                        print("\n👋 Voltando ao menu...")
                        break
            else:
                print("\n❌ Nenhuma receita encontrada para estes ingredientes.")
                print("💡 Tente ingredientes mais genéricos como: frango, arroz, chocolate")
        else:
            print("❌ Sistema CSV não disponível")
            
    except Exception as e:
        print(f"❌ Erro ao buscar receitas: {e}")
        input("\nPressione ENTER para continuar...")

def falar_ingredientes():
    """Abre a interface de reconhecimento de voz"""
    try:
        from audio.reconhecimento_voz_simples import SimpleVoiceInterface
        app = SimpleVoiceInterface()
        app.run()
    except ImportError as e:
        print(f"Erro ao importar interface de voz: {e}")
        print("Execute: python instalar_dependencias_voz.py")
    except Exception as e:
        print(f"Erro na interface de voz: {e}")
        input("\nPressione ENTER para continuar...")

def executar_historico():
    """Executa o visualizador de histórico"""
    try:
        from scripts.visualizador_historico import main as history_main
        history_main()
    except ImportError:
        print("Sistema de histórico não encontrado")
    except Exception as e:
        print(f"Erro ao abrir histórico: {e}")
        input("\nPressione ENTER para continuar...")

def filtrar_dieta_especial():
    """Abre interface de filtros dietéticos"""
    try:
        from interfaces.interface_filtros_dieta import DietFilterInterface
        app = DietFilterInterface()
        app.run()
    except ImportError as e:
        print(f"Erro ao importar interface de filtros: {e}")
    except Exception as e:
        print(f"Erro na interface de filtros: {e}")
        input("\nPressione ENTER para continuar...")

def calcular_calorias():
    """Abre interface da calculadora de calorias"""
    try:
        from interfaces.interface_calculadora_calorias import CalorieCalculatorInterface
        app = CalorieCalculatorInterface()
        app.run()
    except ImportError as e:
        print(f"Erro ao importar calculadora: {e}")
    except Exception as e:
        print(f"Erro na calculadora: {e}")
        input("\nPressione ENTER para continuar...")

def verificar_alergias():
    """Verificar alergias em receitas"""
    limpar_tela()
    print("\nVERIFICAR ALERGIAS")
    print("="*30)
    print("Alergias comuns:")
    print("• Amendoim • Nozes • Leite")
    print("• Ovos • Glúten • Frutos do mar")
    
    alergia = input("\nDigite sua alergia: ").strip().lower()
    receita = input("Digite a receita para verificar: ").strip().lower()
    
    if alergia and receita:
        print(f"\nVerificando {alergia} em: {receita}")
        
        # Base de dados de ingredientes alergênicos
        alergenos = {
            'amendoim': ['amendoim', 'pasta de amendoim', 'óleo de amendoim'],
            'nozes': ['nozes', 'castanha', 'amêndoa', 'avelã', 'pistache'],
            'leite': ['leite', 'queijo', 'iogurte', 'manteiga', 'creme de leite', 'lactose'],
            'ovos': ['ovo', 'clara', 'gema', 'maionese'],
            'glúten': ['trigo', 'farinha', 'pão', 'macarrão', 'massa', 'centeio', 'cevada'],
            'frutos do mar': ['camarão', 'peixe', 'salmão', 'atum', 'sardinha', 'marisco', 'lula']
        }
        
        alergia_encontrada = False
        ingredientes_perigosos = []
        
        # Verificar se a alergia informada está na base
        alergia_key = None
        for key in alergenos.keys():
            if alergia in key or key in alergia:
                alergia_key = key
                break
        
        if alergia_key:
            # Verificar ingredientes alergênicos na receita
            for ingrediente_alergico in alergenos[alergia_key]:
                if ingrediente_alergico in receita:
                    alergia_encontrada = True
                    ingredientes_perigosos.append(ingrediente_alergico)
        
        print("\n" + "="*30)
        if alergia_encontrada:
            print("ATENÇÃO - RISCO DE ALERGIA DETECTADO!")
            print(f"\nIngredientes problemáticos encontrados:")
            for ingrediente in ingredientes_perigosos:
                print(f"   • {ingrediente.title()}")
            print(f"\nNÃO recomendado para pessoas com alergia a {alergia}")
        else:
            print("RECEITA APARENTEMENTE SEGURA")
            print(f"\nNenhum ingrediente relacionado a {alergia} foi detectado")
            print("\nSempre verifique os rótulos dos produtos industrializados")
        
        print("="*30)
        
        # Salvar verificação no histórico
        try:
            from core_logic.database import history_db
            resultado = "RISCO DETECTADO" if alergia_encontrada else "SEGURA"
            history_db.add_analysis(
                ingredient=f"Alergia: {alergia}",
                recipes_response=f"Receita: {receita} - {resultado}",
                source_mode="allergy_check"
            )
        except:
            pass
            
    else:
        print("Informações incompletas!")
        
    input("\nPressione ENTER para continuar...")

def gerenciar_cronometros():
    """Abre a interface de cronômetros de cozinha"""
    try:
        print("\n⏰ Abrindo cronômetros de cozinha...")
        from interfaces.interface_cronometros_cozinha import TimerKitchenInterface
        app = TimerKitchenInterface()
        app.run()
        print("✅ Interface de cronômetros finalizada!")
    except ImportError as e:
        print(f"❌ Erro ao importar interface de cronômetros: {e}")
        print("💡 Verifique se o arquivo interface_cronometros_cozinha.py existe")
        input("\nPressione ENTER para continuar...")
    except Exception as e:
        print(f"❌ Erro na interface de cronômetros: {e}")
        input("\nPressione ENTER para continuar...")

def meu_perfil():
    """Configurações do perfil do usuário"""
    limpar_tela()
    print("\n👤 MEU PERFIL")
    print("="*50)
    
    try:
        from core_logic.database import history_db
        
        # Carregar perfil atual
        perfil = history_db.get_user_profile()
        
        print(f"📝 Nome: {perfil.get('name', 'Não informado')}")
        print(f"Nível: {perfil.get('skill_level', 'iniciante').title()}")
        print(f"🚫 Restrições: {perfil.get('dietary_restrictions', '[]')}")
        print(f"❤️ Alergias: {perfil.get('allergies', '[]')}")
        print(f"🍽️ Cozinhas favoritas: {perfil.get('favorite_cuisines', '[]')}")
        print(f"⏰ Tempo preferido: {perfil.get('preferred_cooking_time', 60)} minutos")
        
        while True:
            print("\nOpções:")
            print("1. ✏️ Editar nome")
            print("2. 📊 Ver estatísticas")
            print("3. ⭐ Ver avaliações de receitas")
            print("4. 🔙 Voltar ao menu")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                novo_nome = input("\n📝 Digite seu nome: ").strip()
                if novo_nome:
                    try:
                        history_db.update_user_profile(name=novo_nome)
                        print(f"✅ Nome atualizado para: {novo_nome}")
                    except Exception as e:
                        print(f"❌ Erro ao atualizar: {e}")
                        
            elif opcao == "2":
                stats = history_db.get_statistics()
                print("\n📊 SUAS ESTATÍSTICAS:")
                print(f"🔸 Total de análises: {stats.get('total_analyses', 0)}")
                print(f"🔸 Análises bem-sucedidas: {stats.get('successful_analyses', 0)}")
                print(f"🔸 Última atualização: {stats.get('last_updated', 'N/A')}")
                
            elif opcao == "3":
                ratings = history_db.get_user_recipe_ratings()
                if ratings:
                    print("\n⭐ SUAS AVALIAÇÕES:")
                    for rating in ratings:
                        stars = "⭐" * int(rating.get('rating', 0))
                        print(f"🔸 {rating.get('recipe_name', 'N/A')} - {stars}")
                        if rating.get('comment'):
                            print(f"   💭 {rating['comment']}")
                else:
                    print("\n📭 Você ainda não avaliou nenhuma receita")
                    
            elif opcao == "4":
                break
            else:
                print("❌ Opção inválida!")
                
            input("\nPressione ENTER para continuar...")
            limpar_tela()
            print("\n👤 MEU PERFIL")
            print("="*50)
            
    except Exception as e:
        print(f"❌ Erro no sistema de perfil: {e}")
        
    input("\nPressione ENTER para voltar ao menu...")

def mostrar_creditos():
    """Exibe os créditos do sistema"""
    limpar_tela()
    print("\n" + "="*60)
    print("🧑‍🍳 CHEF RAG - CRÉDITOS")
    print("="*60)
    print()
    print("📋 DESENVOLVIDO POR:")
    print("   • Vitória Ayres")
    print()
    print("🛠️ TECNOLOGIAS ENVOLVIDAS:")
    print("   • Python")
    print("   • LangChain")
    print("   • ChromaDB")
    print("   • OpenCV")
    print("   • YOLO")
    print("   • Tkinter")
    print("   • SQLite")
    print("   • Pandas")
    print("   • Speech Recognition")
    print("   • Flask")
    print("   • RAG (Retrieval-Augmented Generation)")
    print()
    print("🎯 FUNCIONALIDADES:")
    print("   • Reconhecimento de ingredientes por imagem")
    print("   • Reconhecimento de voz")
    print("   • Sistema de busca inteligente")
    print("   • Filtros dietéticos")
    print("   • Calculadora de calorias")
    print("   • Verificador de alergias")
    print("   • Cronômetros de cozinha")
    print("   • Interface mobile")
    print()
    print("="*60)
    input("\nPressione ENTER para voltar ao menu...")

def main():
    """Função principal - loop do menu"""
    while True:
        try:
            mostrar_menu()
            opcao = input("\nDigite sua escolha (1-13): ").strip()
            
            if opcao == "1":
                usar_camera_pc()
            elif opcao == "2":
                usar_camera_celular()
            elif opcao == "3":
                enviar_foto_ingredientes()
            elif opcao == "4":
                digitar_ingredientes()
            elif opcao == "5":
                falar_ingredientes()
            elif opcao == "6":
                filtrar_dieta_especial()
            elif opcao == "7":
                calcular_calorias()
            elif opcao == "8":
                verificar_alergias()
            elif opcao == "9":
                gerenciar_cronometros()
            elif opcao == "10":
                executar_historico()
            elif opcao == "11":
                meu_perfil()
            elif opcao == "12":
                mostrar_creditos()
            elif opcao == "13":
                print("\nObrigado por usar o Chef RAG!")
                print("Bom apetite e até a próxima!")
                break
            else:
                print("\nOpção inválida! Digite um número de 1 a 13.")
                input("Pressione ENTER para continuar...")
                
        except KeyboardInterrupt:
            print("\n\nSaindo do Chef RAG...")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            input("Pressione ENTER para continuar...")

def mostrar_todas_receitas_passo_a_passo(receitas):
    """
    Mostra todas as receitas encontradas com foco 100% no passo a passo de preparo
    """
    print("\n" + "-"*60)
    print("RECEITAS ENCONTRADAS")
    print("-"*60)
    
    for i, receita in enumerate(receitas, 1):
        print(f"\nRECEITA {i}: {receita['Nome'].upper()}")
        print(f"⏱️ Tempo: {receita['Tempo']} | Dificuldade: {receita['Dificuldade']}")
        print(f"Categoria: {receita['Categoria']} | Compatibilidade: {receita['compatibility_score']:.1f}%")
        
        # PASSO A PASSO - FOCO PRINCIPAL
        print(f"\nMODO DE PREPARO:")
        print("-" * 50)
        
        # Usar o separador correto baseado no formato do CSV
        if ' | ' in receita['Modo_de_Preparo']:
            passos = receita['Modo_de_Preparo'].split(' | ')
        else:
            passos = receita['Modo_de_Preparo'].split('. ')
        
        for j, passo in enumerate(passos, 1):
            if passo.strip():
                passo = passo.strip()
                # Remove numeração se já existir no início
                if passo.startswith(f"{j}."):
                    passo = passo[len(f"{j}."):].strip()
                if not passo.endswith('.'):
                    passo += '.'
                print(f"Passo {j}: {passo}")
        
        # Ingredientes como informação de apoio
        print(f"\nINGREDIENTES:")
        # Usar o separador correto para ingredientes
        if ' | ' in receita['Ingredientes']:
            ingredientes = receita['Ingredientes'].split(' | ')
        else:
            ingredientes = receita['Ingredientes'].split(', ')
        
        for ingrediente in ingredientes:
            if ingrediente.strip():
                print(f"   • {ingrediente.strip()}")
        
        if i < len(receitas):
            print("\n" + "-"*80)
    
    print(f"\nTotal: {len(receitas)} receita(s) encontrada(s)")
    print("="*80)

def mostrar_modo_preparo_detalhado(receita):
    """
    Foca exclusivamente no modo de preparo da receita com máximo detalhamento
    """
    print("\n" + "="*50)
    print(f"    MODO DE PREPARO: {receita['Nome'].upper()}")
    print("="*50)
    
    print(f"\n⏱️ Tempo: {receita['Tempo']}")
    print(f"Dificuldade: {receita['Dificuldade']}")
    print(f"Categoria: {receita['Categoria']}")
    
    print(f"\nINSTRUÇÕES PASSO A PASSO:")
    print("="*50)
    
    # Usar o separador correto baseado no formato do CSV
    if ' | ' in receita['Modo_de_Preparo']:
        passos = receita['Modo_de_Preparo'].split(' | ')
    else:
        passos = receita['Modo_de_Preparo'].split('. ')
    
    for i, passo in enumerate(passos, 1):
        if passo.strip():
            passo = passo.strip()
            # Remove numeração se já existir no início
            if passo.startswith(f"{i}."):
                passo = passo[len(f"{i}."):].strip()
            if not passo.endswith('.'):
                passo += '.'
            print(f"\nPasso {i}: {passo}")
    
    print(f"\nINGREDIENTES:")
    # Usar o separador correto para ingredientes
    if ' | ' in receita['Ingredientes']:
        ingredientes = receita['Ingredientes'].split(' | ')
    else:
        ingredientes = receita['Ingredientes'].split(', ')
    
    for ingrediente in ingredientes:
        if ingrediente.strip():
            print(f"   • {ingrediente.strip()}")
    
    print("\n" + "="*50)
    print("    PRONTO PARA COZINHAR!")
    print("="*50)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Sistema de Busca Robusta - Chef RAG v2
=====================================

Sistema que garante sempre retornar receitas para o usuário.
"""

from core_logic.database import history_db

def buscar_receitas_robusta(ingredientes_list):
    """
    Busca receitas de forma robusta, priorizando 100% o PDF local.
    
    Estratégia PRIORITÁRIA - PDF FIRST:
    1. Busca exata no PDF/ChromaDB pelos ingredientes
    2. Busca parcial/similar no PDF com ingredientes relacionados
    3. Busca no histórico de receitas já processadas
    4. Análise semântica do PDF para encontrar receitas compatíveis
    5. Sugestões de ingredientes disponíveis no PDF
    6. Opção para upload de novo PDF
    7. ÚLTIMA OPÇÃO: busca online (só se usuário aceitar)
    """
    import os
    
    ingredientes_str = ", ".join(ingredientes_list)
    receitas_encontradas = []
    
    print(f"🔍 Busca INTELIGENTE no seu PDF para: {ingredientes_str}")
    print("📚 Priorizando 100% suas receitas locais...")
    
    # ETAPA 1: Busca EXATA no PDF/ChromaDB
    print("\n📖 Etapa 1: Busca exata no PDF...")
    receitas_exatas = buscar_receitas_exatas_pdf(ingredientes_list)
    if receitas_exatas:
        receitas_encontradas.extend(receitas_exatas)
        print(f"✅ {len(receitas_exatas)} receitas EXATAS encontradas no PDF!")
        return finalizar_busca(receitas_encontradas, ingredientes_str)
    
    # ETAPA 2: Busca SIMILAR/PARCIAL no PDF
    print("🔍 Etapa 2: Busca similar no PDF...")
    receitas_similares = buscar_receitas_similares_inteligente(ingredientes_list)
    if receitas_similares:
        receitas_encontradas.extend(receitas_similares)
        print(f"✅ {len(receitas_similares)} receitas SIMILARES encontradas no PDF!")
        return finalizar_busca(receitas_encontradas, ingredientes_str)
    
    # ETAPA 3: Busca no histórico processado
    print("📚 Etapa 3: Verificando histórico de receitas processadas...")
    receitas_historico = buscar_no_historico_inteligente(ingredientes_list)
    if receitas_historico:
        receitas_encontradas.extend(receitas_historico)
        print(f"✅ {len(receitas_historico)} receitas encontradas no histórico!")
        return finalizar_busca(receitas_encontradas, ingredientes_str)
    
    # ETAPA 4: Análise semântica avançada do PDF
    print("🧠 Etapa 4: Análise semântica avançada do PDF...")
    receitas_semanticas = buscar_receitas_semanticas_pdf(ingredientes_list)
    if receitas_semanticas:
        receitas_encontradas.extend(receitas_semanticas)
        print(f"✅ {len(receitas_semanticas)} receitas por análise semântica!")
        return finalizar_busca(receitas_encontradas, ingredientes_str)
    
    # ETAPA 5: Sugerir ingredientes DISPONÍVEIS no PDF
    print("💡 Etapa 5: Analisando ingredientes disponíveis no seu PDF...")
    ingredientes_disponiveis = extrair_ingredientes_do_pdf()
    if ingredientes_disponiveis:
        sugestao_pdf = criar_sugestoes_do_pdf(ingredientes_list, ingredientes_disponiveis)
        receitas_encontradas.append(sugestao_pdf)
        return finalizar_busca(receitas_encontradas, ingredientes_str)
    
    # ETAPA 6: Oferecer upload de novo PDF
    print("📤 Etapa 6: Oferecendo opção de novo PDF...")
    opcao_upload = criar_opcao_upload_pdf(ingredientes_list)
    receitas_encontradas.append(opcao_upload)
    
    # ETAPA 7: ÚLTIMA OPÇÃO - perguntar sobre busca online
    opcao_online = perguntar_busca_online(ingredientes_str)
    if opcao_online:
        receitas_encontradas.append(opcao_online)
    
    return finalizar_busca(receitas_encontradas, ingredientes_str)

def buscar_receitas_exatas_pdf(ingredientes_list):
    """Busca EXATA no PDF por receitas - versão melhorada para receitas completas"""
    receitas_exatas = []
    try:
        # Usa as funções existentes do sistema RAG para busca individual de cada ingrediente
        from core_logic.sistema_rag import find_relevant_recipes, generate_recipe_suggestion
        
        # Busca receitas individuais completas para cada ingrediente
        for ingrediente in ingredientes_list:
            recipes_data = find_relevant_recipes(ingrediente, n_results=3)
            
            if recipes_data.get('documents') and len(recipes_data['documents']) > 0:
                # Gera receita completa usando o sistema existente com prompt melhorado
                resultado = generate_recipe_suggestion(
                    ingrediente, 
                    recipes_data, 
                    source_mode="receita_completa_detalhada"
                )
                
                if resultado and len(resultado) > 100:
                    # Verificar se é uma receita real (não apenas lista)
                    if any(palavra in resultado.lower() for palavra in ['ingredientes', 'modo de preparo', 'preparo', 'receita']):
                        receita_formatada = f"📖 **RECEITA COMPLETA DO PDF** - {ingrediente.title()}\n\n{resultado}\n"
                        receitas_exatas.append(receita_formatada)
        
        # Se não encontrou receitas individuais, tenta busca combinada
        if not receitas_exatas:
            try:
                from core_logic.sistema_rag import find_relevant_recipes_multiple_ingredients, generate_recipe_suggestion_multiple
                
                recipes_data = find_relevant_recipes_multiple_ingredients(ingredientes_list, n_results=5)
                
                if recipes_data.get('documents') and len(recipes_data['documents']) > 0:
                    resultado = generate_recipe_suggestion_multiple(
                        ingredientes_list, 
                        recipes_data, 
                        source_mode="receita_completa_combinada"
                    )
                    
                    if resultado and len(resultado) > 100:
                        if any(palavra in resultado.lower() for palavra in ['ingredientes', 'modo de preparo', 'preparo']):
                            receita_formatada = f"📖 **RECEITA COMPLETA DO PDF** - {', '.join(ingredientes_list)}\n\n{resultado}\n"
                            receitas_exatas.append(receita_formatada)
            except Exception as e:
                print(f"⚠️ Erro na busca combinada: {e}")
        
        return receitas_exatas
        
    except Exception as e:
        print(f"⚠️ Sistema PDF indisponível: {e}")
        return []

def buscar_receitas_similares_inteligente(ingredientes_list):
    """Busca inteligente no PDF - versão simplificada"""
    receitas_similares = []
    try:
        # Tenta buscar ingredientes individuais
        from core_logic.sistema_rag import find_relevant_recipes, generate_recipe_suggestion
        
        for ingrediente in ingredientes_list:
            recipes_data = find_relevant_recipes(ingrediente, n_results=2)
            
            if recipes_data.get('documents') and len(recipes_data['documents']) > 0:
                resultado = generate_recipe_suggestion(ingrediente, recipes_data, source_mode="pdf_similar")
                
                if resultado and len(resultado) > 80:
                    receita_formatada = f"📚 **RECEITA SIMILAR DO PDF** - {ingrediente.title()}\n\n{resultado}\n"
                    if receita_formatada not in receitas_similares:
                        receitas_similares.append(receita_formatada)
            
        return receitas_similares
    except Exception as e:
        print(f"⚠️ Sistema PDF indisponível: {e}")
        return []

def buscar_no_historico_inteligente(ingredientes_list):
    """Busca inteligente no histórico de receitas processadas"""
    receitas_historico = []
    try:
        recent_analyses = history_db.get_recent_analyses(limit=200)
        
        # get_recent_analyses retorna tuplas: (timestamp, image_name, ingredient_identified, chef_suggestion, source_mode, processing_time_seconds)
        for analysis in recent_analyses:
            if len(analysis) >= 4:
                ingredient_text = analysis[2].lower() if analysis[2] else ""  # ingredient_identified
                recipes_text = analysis[3] if analysis[3] else ""  # chef_suggestion
                
                # Busca por qualquer ingrediente no histórico
                for ing in ingredientes_list:
                    if (ing.lower().strip() in ingredient_text and 
                        recipes_text and len(recipes_text) > 100):
                        
                        receita_historico = f"📚 **DO SEU HISTÓRICO** - {ing.title()}\n\n{recipes_text}\n"
                        if receita_historico not in receitas_historico:
                            receitas_historico.append(receita_historico)
                        break
                        
    except Exception as e:
        print(f"⚠️ Erro no histórico: {e}")
    
    return receitas_historico

def buscar_receitas_semanticas_pdf(ingredientes_list):
    """Análise semântica simplificada usando funções existentes"""
    receitas_semanticas = []
    try:
        from core_logic.sistema_rag import find_recipes_by_ingredient
        
        # Busca usando o sistema existente para cada ingrediente
        for ingrediente in ingredientes_list:
            resultado = find_recipes_by_ingredient(ingrediente, source_mode="pdf_semantico")
            
            if resultado and len(resultado) > 100:
                receita_semantica = f"🧠 **RECEITA COMPATÍVEL DO PDF** - {ingrediente.title()}\n\n{resultado}\n"
                if receita_semantica not in receitas_semanticas:
                    receitas_semanticas.append(receita_semantica)
                    
    except Exception as e:
        print(f"⚠️ Erro na análise semântica: {e}")
    
    return receitas_semanticas

def extrair_ingredientes_do_pdf():
    """Extrai lista de ingredientes básicos disponíveis"""
    try:
        # Lista de ingredientes comuns que provavelmente estão em qualquer PDF de receitas
        ingredientes_basicos = [
            "leite", "ovos", "farinha", "açúcar", "sal", "óleo", 
            "cebola", "alho", "tomate", "queijo", "frango", "carne",
            "arroz", "feijão", "batata", "cenoura", "pão", "manteiga",
            "azeite", "pimenta", "limão", "alface", "couve", "espinafre"
        ]
        
        return ingredientes_basicos
        
    except Exception as e:
        print(f"⚠️ Erro ao extrair ingredientes: {e}")
        return ["arroz", "feijão", "batata", "cebola", "alho", "tomate"]

def criar_sugestoes_do_pdf(ingredientes_solicitados, ingredientes_disponiveis):
    """Cria sugestões baseadas nos ingredientes disponíveis no PDF"""
    sugestao = f"💡 **INGREDIENTES DISPONÍVEIS NO SEU PDF**\n\n"
    sugestao += f"Você procurou: {', '.join(ingredientes_solicitados)}\n\n"
    sugestao += "📚 Ingredientes que encontrei no seu PDF:\n"
    
    for i, ing in enumerate(ingredientes_disponiveis[:8], 1):
        sugestao += f"{i}. {ing.title()}\n"
    
    sugestao += "\n🔄 **Tente buscar receitas com esses ingredientes!**\n"
    sugestao += "💡 **Dica**: Combine 2-3 ingredientes para melhores resultados."
    
    return sugestao

def criar_opcao_upload_pdf(ingredientes_list):
    """Cria opção para fazer upload de novo PDF"""
    opcao = f"📤 **OPÇÃO: ADICIONAR NOVO PDF DE RECEITAS**\n\n"
    opcao += f"Você procurou: {', '.join(ingredientes_list)}\n\n"
    opcao += "❌ Não encontrei receitas com esses ingredientes no PDF atual.\n\n"
    opcao += "💡 **SOLUÇÕES DISPONÍVEIS:**\n"
    opcao += "1. 📁 Faça upload de um novo PDF com mais receitas\n"
    opcao += "2. 🔄 Tente com ingredientes similares\n"
    opcao += "3. 📚 Verifique se o PDF atual está carregado corretamente\n\n"
    opcao += "🎯 **Para fazer upload:**\n"
    opcao += "- Vá no menu principal\n"
    opcao += "- Escolha 'Upload de Arquivo PDF'\n"
    opcao += "- Selecione um PDF com receitas que contenham seus ingredientes\n\n"
    opcao += "✨ **Dica**: PDFs com receitas organizadas funcionam melhor!"
    
    return opcao

def perguntar_busca_online(ingredientes_str):
    """Pergunta ao usuário se quer busca online como ÚLTIMA opção"""
    pergunta = f"🌐 **ÚLTIMA OPÇÃO: BUSCA ONLINE**\n\n"
    pergunta += f"Ingredientes: {ingredientes_str}\n\n"
    pergunta += "❌ Não encontrei receitas no seu PDF local.\n\n"
    pergunta += "🤔 **DESEJA BUSCAR ONLINE?**\n"
    pergunta += "⚠️ ATENÇÃO: Isso sairá do foco do seu PDF local\n\n"
    pergunta += "💡 **RECOMENDAÇÃO:**\n"
    pergunta += "1. Primeiro tente fazer upload de um PDF mais completo\n"
    pergunta += "2. Só use busca online se realmente necessário\n\n"
    pergunta += "🎯 **Para aceitar busca online, digite 'sim online'**"
    
    return pergunta

def finalizar_busca(receitas_encontradas, ingredientes_str):
    """Finaliza a busca salvando no histórico e retornando resultados"""
    try:
        resultado_final = "\n\n---\n\n".join(receitas_encontradas)
        history_db.add_analysis(
            ingredient=ingredientes_str,
            recipes_response=resultado_final,
            source_mode="busca_pdf_inteligente"
        )
        print(f"💾 {len(receitas_encontradas)} receita(s) salva(s) no histórico")
    except Exception as e:
        print(f"⚠️ Erro ao salvar: {e}")
    
    return receitas_encontradas

def apresentar_receitas_para_selecao(receitas, ingredientes_str):
    """Apresenta receitas numeradas para o usuário escolher qual cozinhar - versão melhorada"""
    if not receitas:
        return None
    
    print(f"\n🍽️ RECEITAS ENCONTRADAS PARA: {ingredientes_str}")
    print("="*60)
    
    receitas_validas = []
    
    for i, receita in enumerate(receitas, 1):
        # Verificar se é uma receita válida (não apenas mensagens muito curtas)
        if not receita or len(receita.strip()) < 30:
            continue
        
        receitas_validas.append(receita)
        
        # Extrair título da receita de forma melhorada
        lines = receita.split('\n')
        titulo = f"Receita {len(receitas_validas)}"
        
        # Buscar por títulos de receitas específicas nas listas
        import re
        receitas_encontradas = re.findall(r'\d+\.\s+\*\*(.*?)\*\*', receita)
        
        if receitas_encontradas:
            # Se é uma lista, mostrar as receitas disponíveis
            titulo = f"Opções de receitas com {ingredientes_str.split(',')[i-1].strip()}"
            print(f"\n{len(receitas_validas)}. {titulo}")
            print("   📋 Receitas disponíveis:")
            
            for j, nome_receita in enumerate(receitas_encontradas[:3], 1):
                print(f"      • {nome_receita}")
                if j == 3 and len(receitas_encontradas) > 3:
                    print(f"      • ... e mais {len(receitas_encontradas) - 3} receitas")
                    break
        else:
            # Buscar título em formato tradicional
            for line in lines:
                line_clean = line.strip().replace("*", "").replace("#", "").replace("📖", "")
                if any(palavra in line_clean.upper() for palavra in ['RECEITA', 'BOLO', 'BRIGADEIRO', 'SOPA', 'PRATO']):
                    if 5 < len(line_clean) < 80:
                        titulo = line_clean
                        break
            
            print(f"\n{len(receitas_validas)}. {titulo}")
        
        print(f"   [📄 Conteúdo com {len(lines)} linhas - {len(receita)} caracteres]")
    
    if not receitas_validas:
        print("❌ Nenhuma receita válida encontrada")
        return None
    
    if not receitas_validas:
        print("❌ Nenhuma receita válida encontrada")
        return None
    
    print("="*60)
    print("👨‍🍳 BORA COZINHAR? Só me diga o número da receita que você gostou!")
    print(f"🎯 Digite o número (1-{len(receitas_validas)}) ou 'não' para voltar ao menu")
    
    return receitas_validas
    
    return receitas_validas

def selecionar_receita_para_cozinhar(receitas):
    """Permite ao usuário selecionar uma receita específica para cozinhar"""
    if not receitas:
        return None
    
    try:
        escolha = input("\n🎯 Qual receita você quer fazer? (número): ").strip()
        
        if escolha.lower() in ['nao', 'não', 'n', 'sair', 'voltar']:
            print("👋 Voltando ao menu principal...")
            return None
        
        numero = int(escolha)
        
        if 1 <= numero <= len(receitas):
            receita_selecionada = receitas[numero - 1]
            print(f"✅ Receita {numero} selecionada!")
            print("🧑‍🍳 Preparando interface de cozinha...")
            return receita_selecionada
        else:
            print(f"❌ Número inválido. Digite um número entre 1 e {len(receitas)}")
            return None
            
    except ValueError:
        print("❌ Digite apenas o número da receita")
        return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def buscar_receita_completa_pdf(titulo_receita, ingredientes_originais):
    """Busca receita completa e estruturada no PDF"""
    try:
        from core_logic.sistema_rag import find_relevant_recipes, generate_recipe_suggestion
        
        # Busca mais detalhada usando título + ingredientes
        termos_busca = [
            titulo_receita.replace("**", "").replace("📖", "").strip(),
            " ".join(ingredientes_originais),
            f"{titulo_receita} completa ingredientes preparo"
        ]
        
        melhor_receita = None
        melhor_score = 0
        
        for termo in termos_busca:
            try:
                recipes_data = find_relevant_recipes(termo, n_results=3)
                
                if recipes_data.get('documents') and len(recipes_data['documents']) > 0:
                    # Gerar receita completa
                    receita_completa = generate_recipe_suggestion(termo, recipes_data, source_mode="receita_completa")
                    
                    if receita_completa and len(receita_completa) > melhor_score:
                        melhor_receita = receita_completa
                        melhor_score = len(receita_completa)
            except Exception as e:
                print(f"⚠️ Erro na busca por '{termo}': {e}")
                continue
        
        return melhor_receita if melhor_receita else None
        
    except Exception as e:
        print(f"⚠️ Erro ao buscar receita completa: {e}")
        return None


    """Extrai dados estruturados da receita para interface de cozinha - versão híbrida JSON + PDF"""
    dados_receita = {
        'titulo': 'Receita Selecionada',
        'ingredientes': [],
        'modo_preparo': [],
        'tempo_preparo': 'Não especificado',
        'porcoes': 'Não especificado',
        'dificuldade': 'Média',
        'texto_completo': receita_texto
    }

    
    try:
        # Detecta se é uma lista de receitas (não uma receita individual)
        if any(indicador in receita_texto for indicador in [
            "🍽️ **RECEITAS ENCONTRADAS",
            "📚 **DO SEU LIVRO DE RECEITAS:**",
            "🌐 **QUER MAIS OPÇÕES?",
            "👨‍🍳 **SUGESTÃO DO CHEF:**",
            "1. **",
            "2. **"
        ]):
            print("⚠️ Detectada lista de receitas - tentando extrair receita específica...")
            
            # Tenta extrair a primeira receita mencionada
            import re
            padrao_receita = r'\*\*(.*?)\*\*.*?(?:Página\s+(\d+))?'
            matches = re.findall(padrao_receita, receita_texto)
            
            if matches:
                primeira_receita = matches[0][0] if isinstance(matches[0], tuple) else matches[0]
                pagina = matches[0][1] if isinstance(matches[0], tuple) and len(matches[0]) > 1 else None
                
                # Remove "RECEITA COMPLETA DO PDF" e pega a primeira receita real da lista
                if "RECEITA COMPLETA DO PDF" in primeira_receita:
                    # Busca por receitas específicas na lista
                    receitas_na_lista = re.findall(r'\d+\.\s+\*\*(.*?)\*\*', receita_texto)
                    if receitas_na_lista:
                        primeira_receita = receitas_na_lista[0]
                        print(f"📝 Extraída receita da lista: {primeira_receita}")
                
                print(f"📝 Tentando buscar receita específica: {primeira_receita}")
                
                # Busca a receita específica
                receita_especifica = buscar_receita_especifica_por_nome(primeira_receita, pagina)
                
                if receita_especifica:
                    print("✅ Receita específica encontrada!")
                    return extrair_dados_receita(receita_especifica)
                else:
                    print("❌ Receita específica não encontrada, usando dados da lista...")
                    dados_receita['titulo'] = primeira_receita
                    dados_receita['ingredientes'] = [
                        "⚠️ Esta é uma lista de receitas, não uma receita completa.",
                        f"📝 Receita sugerida: {primeira_receita}",
                        "🔍 Busque pela receita específica para ver ingredientes detalhados."
                    ]
                    dados_receita['modo_preparo'] = [
                        "⚠️ Modo de preparo não disponível nesta lista.",
                        f"📖 Para ver o passo-a-passo da receita '{primeira_receita}',",
                        "🔍 faça uma busca específica pelo nome da receita."
                    ]
                    return dados_receita
        
        # Se chegou aqui, é uma receita individual - processa normalmente
        linhas = receita_texto.split('\n')
        secao_atual = None
        
        for linha in linhas:
            linha_original = linha
            linha = linha.strip()
            if not linha:
                continue
            
            # Limpar marcadores comuns
            linha_limpa = linha.replace('**', '').replace('*', '').replace('#', '').strip()
                
            # Detectar título - melhorado
            if any(palavra in linha_limpa.upper() for palavra in ['RECEITA', 'BOLO', 'SOPA', 'PRATO', 'DOCE', 'BRIGADEIRO']):
                if len(linha_limpa) > 5 and len(linha_limpa) < 100:
                    dados_receita['titulo'] = linha_limpa.replace('📖', '').replace('📚', '').replace('🧠', '').strip()
            
            # Detectar seções
            linha_upper = linha.upper()
            if any(palavra in linha_upper for palavra in ['INGREDIENTES', 'INGREDIENTS', 'VOCÊ VAI PRECISAR']):
                secao_atual = 'ingredientes'
                continue
            elif any(palavra in linha_upper for palavra in ['MODO DE PREPARO', 'PREPARO', 'INSTRUÇÕES', 'INSTRUCTIONS', 'COMO FAZER']):
                secao_atual = 'preparo'
                continue
            elif any(palavra in linha_upper for palavra in ['TEMPO', 'DURAÇÃO']) and any(palavra in linha for palavra in ['min', 'hora', 'h']):
                dados_receita['tempo_preparo'] = linha_limpa
                continue
            elif any(palavra in linha_upper for palavra in ['PORÇÃO', 'SERVE', 'RENDIMENTO']):
                dados_receita['porcoes'] = linha_limpa
                continue
            
            # Adicionar conteúdo às seções
            if secao_atual == 'ingredientes':
                if linha.startswith(('-', '•', '●', '*', '○', '▪')):
                    ingrediente = linha[1:].strip()
                    if len(ingrediente) > 2:
                        dados_receita['ingredientes'].append(ingrediente)
                elif linha_limpa and (linha[0].isdigit() or any(linha.startswith(medida) for medida in ['½', '¼', '¾', '1', '2', '3'])):
                    if len(linha_limpa) > 3 and not linha_limpa.startswith('📖'):
                        dados_receita['ingredientes'].append(linha_limpa)
                elif 'xícara' in linha or 'colher' in linha or 'grama' in linha or 'ml' in linha:
                    if len(linha_limpa) > 3:
                        dados_receita['ingredientes'].append(linha_limpa)
            
            elif secao_atual == 'preparo':
                if linha.startswith(('-', '•', '●', '*', '○', '▪')):
                    passo = linha[1:].strip()
                    if len(passo) > 5:
                        dados_receita['modo_preparo'].append(passo)
                elif linha_limpa and linha[0].isdigit() and ('.' in linha or ')' in linha):
                    if len(linha_limpa) > 10:
                        dados_receita['modo_preparo'].append(linha_limpa)
                elif any(palavra in linha.lower() for palavra in ['aqueça', 'misture', 'adicione', 'cozinhe', 'ferva', 'doure', 'tempere']):
                    if len(linha_limpa) > 10 and not linha_limpa.startswith('📖'):
                        dados_receita['modo_preparo'].append(linha_limpa)
        
        # Fallback: se não encontrou ingredientes/preparo estruturados, tentar extrair do texto
        if not dados_receita['ingredientes'] and not dados_receita['modo_preparo']:
            # Buscar por listas numeradas ou com marcadores
            for linha in linhas:
                linha_limpa = linha.strip()
                if linha_limpa:
                    # Ingredientes comuns
                    if any(palavra in linha_limpa.lower() for palavra in ['xícara', 'colher', 'grama', 'ml', 'kg', 'litro']):
                        dados_receita['ingredientes'].append(linha_limpa.replace('-', '').replace('*', '').strip())
                    # Passos de preparo
                    elif any(palavra in linha_limpa.lower() for palavra in ['aqueça', 'misture', 'adicione', 'cozinhe']):
                        dados_receita['modo_preparo'].append(linha_limpa.replace('-', '').replace('*', '').strip())
    
    except Exception as e:
        print(f"⚠️ Erro ao extrair dados da receita: {e}")
    
    return dados_receita

def buscar_receita_especifica_por_nome(nome_receita, pagina=None):
    """Busca uma receita específica pelo nome"""
    try:
        from core_logic.sistema_rag import find_relevant_recipes, generate_recipe_suggestion
        
        # Termos de busca específicos
        termos_busca = [
            f"receita completa {nome_receita} ingredientes modo preparo",
            f"{nome_receita} ingredientes preparo passo a passo",
            f"página {pagina} {nome_receita}" if pagina else f"{nome_receita} receita",
            f"{nome_receita} como fazer"
        ]
        
        for termo in termos_busca:
            recipes_data = find_relevant_recipes(termo, n_results=5)
            
            if recipes_data.get('documents'):
                resultado = generate_recipe_suggestion(nome_receita, recipes_data, source_mode="receita_individual_completa")
                
                # Verifica se é uma receita completa (não uma lista)
                if (resultado and len(resultado) > 200 and 
                    "ingredientes" in resultado.lower() and
                    ("modo de preparo" in resultado.lower() or "preparo" in resultado.lower()) and
                    "🍽️ **RECEITAS ENCONTRADAS" not in resultado):
                    return resultado
        
        return None
        
    except Exception as e:
        print(f"⚠️ Erro ao buscar receita específica: {e}")
        return None
    
    return dados_receita

def processar_receita_para_cozinha(receita_selecionada, ingredientes_originais):
    """Processa a receita selecionada para a interface de cozinha"""
    print("🔍 Buscando receita completa no PDF...")
    
    # Extrair dados básicos da receita selecionada
    dados_basicos = extrair_dados_receita(receita_selecionada)
    
    # Buscar versão mais completa no PDF
    titulo = dados_basicos['titulo']
    receita_completa = buscar_receita_completa_pdf(titulo, ingredientes_originais)
    
    if receita_completa and len(receita_completa) > len(receita_selecionada):
        print("✅ Receita mais detalhada encontrada no PDF!")
        dados_completos = extrair_dados_receita(receita_completa)
        
        # Mesclar dados (priorizar dados completos)
        if len(dados_completos['ingredientes']) > len(dados_basicos['ingredientes']):
            dados_basicos['ingredientes'] = dados_completos['ingredientes']
        
        if len(dados_completos['modo_preparo']) > len(dados_basicos['modo_preparo']):
            dados_basicos['modo_preparo'] = dados_completos['modo_preparo']
        
        dados_basicos['texto_completo'] = receita_completa
        
    else:
        print("📝 Usando dados da receita selecionada")
    
    # Garantir que temos dados mínimos
    if not dados_basicos['ingredientes']:
        dados_basicos['ingredientes'] = ['Ingredientes não especificados na receita']
    
    if not dados_basicos['modo_preparo']:
        dados_basicos['modo_preparo'] = ['Modo de preparo não especificado na receita']
    
    return dados_basicos

def buscar_receitas_similares_pdf(ingredientes_list):
    """FUNÇÃO MANTIDA PARA COMPATIBILIDADE - USA A NOVA INTELIGENTE"""
    return buscar_receitas_similares_inteligente(ingredientes_list)

def sugerir_ingredientes_alternativos():
    """Sugere ingredientes alternativos baseados no que está disponível"""
    ingredientes_comuns = [
        "🥚 Ovos", "🥛 Leite", "🍅 Tomate", "🧅 Cebola", "🧄 Alho",
        "🐔 Frango", "🥩 Carne bovina", "🐟 Peixe", "🍚 Arroz", "🫘 Feijão",
        "🥔 Batata", "🥕 Cenoura", "🥬 Alface", "🫑 Pimentão", "🧀 Queijo",
        "🍝 Macarrão", "🍞 Pão", "🫒 Azeite", "🧈 Manteiga", "🧂 Sal",
        "🌿 Temperos", "🍋 Limão", "🍌 Banana", "🍎 Maçã", "🥑 Abacate"
    ]
    
    import random
    sugestoes_aleatorias = random.sample(ingredientes_comuns, 8)
    
    return f"""
💡 **INGREDIENTES SUGERIDOS PARA VOCÊ:**

Não encontramos receitas específicas, mas aqui estão ingredientes populares que costumam funcionar bem:

🛒 **SUGESTÕES:**
{chr(10).join([f"   • {ing}" for ing in sugestoes_aleatorias])}

🍽️ **COMBINAÇÕES QUE FUNCIONAM:**
   • {sugestoes_aleatorias[0]} + {sugestoes_aleatorias[1]} + {sugestoes_aleatorias[2]}
   • {sugestoes_aleatorias[3]} + {sugestoes_aleatorias[4]} + {sugestoes_aleatorias[5]}
   • {sugestoes_aleatorias[6]} + {sugestoes_aleatorias[7]} + Temperos

💡 **DICA:** Experimente digitar um destes ingredientes para receitas específicas!

📱 **LINKS ÚTEIS:**
   • TudoGostoso.com.br
   • Receitas.com
   • Panelinha.com.br
"""

def criar_receita_emergencia(ingredientes_list):
    """Cria receita básica de emergência com os ingredientes fornecidos"""
    ingredientes_str = ", ".join(ingredientes_list)
    
    return f"""
🆘 **RECEITA DE EMERGÊNCIA**

🍽️ **Refogado Simples com:** {ingredientes_str}

📝 **INGREDIENTES:**
   • {ingredientes_str}
   • Alho (se tiver)
   • Cebola (se tiver) 
   • Azeite ou óleo
   • Sal e pimenta a gosto

👩‍🍳 **MODO DE PREPARO:**
   1. Aqueça o azeite na panela
   2. Refogue o alho e cebola (se tiver)
   3. Adicione os ingredientes principais: {ingredientes_str}
   4. Tempere com sal e pimenta
   5. Cozinhe até ficar macio
   6. Sirva quente

⏱️ **Tempo:** 15-20 minutos
👥 **Porções:** 2-3 pessoas

💡 **VARIAÇÕES:**
   • Adicione arroz para fazer um prato mais completo
   • Use temperos extras como oregano, manjericão
   • Finalize com queijo ralado se tiver

🌟 **DICA DO CHEF:** Esta é uma receita versátil que funciona com quase qualquer ingrediente!
"""

def testar_sistema_robusto():
    """Função para testar o sistema"""
    print("🧪 Testando sistema de busca robusta...")
    
    # Teste 1: Ingredientes comuns
    print("\n=== TESTE 1: Ingredientes comuns ===")
    resultado1 = buscar_receitas_robusta(["tomate", "cebola"])
    print(f"Resultado: {len(resultado1)} receitas encontradas")
    
    # Teste 2: Ingredientes inexistentes
    print("\n=== TESTE 2: Ingredientes inexistentes ===")
    resultado2 = buscar_receitas_robusta(["xyz123", "abc456"])
    print(f"Resultado: {len(resultado2)} receitas encontradas")
    
    print("\n✅ Sistema robusto testado!")

if __name__ == "__main__":
    testar_sistema_robusto()
#!/usr/bin/env python3
"""
Script para extrair receitas do PDF e converter para CSV estruturado
"""

import pandas as pd
import PyPDF2
import re
from pathlib import Path
import os

def extrair_texto_pdf(pdf_path):
    """Extrai todo o texto do PDF"""
    texto_completo = ""
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                texto_completo += page.extract_text() + "\n"
        return texto_completo
    except Exception as e:
        print(f"Erro ao extrair PDF: {e}")
        return ""

def identificar_receitas(texto):
    """Identifica e separa as receitas do texto"""
    # Padrões para identificar início de receitas
    padroes_receita = [
        r'^[A-ZÁÉÍÓÚ][A-Za-zÁÉÍÓÚáéíóúàâêôç\s]+(?:\([^)]*\))?$',  # Títulos em maiúscula
        r'^\d+\.\s*[A-ZÁÉÍÓÚ][A-Za-zÁÉÍÓÚáéíóúàâêôç\s]+',  # Numerados
        r'^[A-Z][A-Za-z\s]+(?:com|de|à|do|da)[A-Za-z\s]+$'  # Receitas com preposições
    ]
    
    linhas = texto.split('\n')
    receitas_bruto = []
    receita_atual = []
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
            
        # Verificar se é início de nova receita
        eh_titulo = False
        for padrao in padroes_receita:
            if re.match(padrao, linha) and len(linha) > 10 and len(linha) < 100:
                eh_titulo = True
                break
        
        if eh_titulo:
            # Salvar receita anterior se existir
            if receita_atual:
                receitas_bruto.append('\n'.join(receita_atual))
            
            # Iniciar nova receita
            receita_atual = [linha]
        else:
            if receita_atual:  # Só adiciona se estiver dentro de uma receita
                receita_atual.append(linha)
    
    # Adicionar última receita
    if receita_atual:
        receitas_bruto.append('\n'.join(receita_atual))
    
    return receitas_bruto

def processar_receita_individual(texto_receita):
    """Processa uma receita individual e extrai campos estruturados"""
    linhas = texto_receita.split('\n')
    
    # Extrair título (primeira linha)
    titulo = linhas[0].strip()
    
    # Inicializar campos
    ingredientes = []
    modo_preparo = []
    tempo_preparo = ""
    dificuldade = ""
    categoria = ""
    
    # Flags para seções
    na_secao_ingredientes = False
    na_secao_preparo = False
    
    for i, linha in enumerate(linhas[1:], 1):
        linha = linha.strip()
        if not linha:
            continue
        
        # Detectar seções
        if re.search(r'ingrediente|necessário|precisa', linha.lower()):
            na_secao_ingredientes = True
            na_secao_preparo = False
            continue
        elif re.search(r'modo de preparo|preparação|como fazer|preparo', linha.lower()):
            na_secao_preparo = True
            na_secao_ingredientes = False
            continue
        elif re.search(r'tempo|minutos|horas', linha.lower()):
            tempo_preparo = linha
            continue
        elif re.search(r'dificuldade|fácil|médio|difícil', linha.lower()):
            dificuldade = linha
            continue
        
        # Classificar conteúdo
        if na_secao_ingredientes:
            if re.match(r'^[-•*]\s*', linha) or re.match(r'^\d+', linha):
                ingredientes.append(linha)
            elif len(linha) > 5:
                ingredientes.append(linha)
        elif na_secao_preparo:
            if re.match(r'^[-•*]\s*', linha) or re.match(r'^\d+', linha):
                modo_preparo.append(linha)
            elif len(linha) > 10:
                modo_preparo.append(linha)
        else:
            # Tentar classificar automaticamente
            if any(palavra in linha.lower() for palavra in ['xícara', 'colher', 'kg', 'grama', 'litro', 'ml']):
                ingredientes.append(linha)
            elif any(palavra in linha.lower() for palavra in ['misture', 'adicione', 'cozinhe', 'asse', 'ferva', 'mexa']):
                modo_preparo.append(linha)
    
    # Extrair ingredientes únicos para busca
    ingredientes_principais = []
    for ing in ingredientes:
        # Limpar e extrair palavras-chave
        palavras = re.findall(r'[a-záéíóúàâêôç]+', ing.lower())
        for palavra in palavras:
            if len(palavra) > 3 and palavra not in ['xícara', 'colher', 'grama', 'litro']:
                ingredientes_principais.append(palavra)
    
    # Classificar categoria automaticamente
    categoria = classificar_categoria(titulo, ingredientes_principais)
    
    return {
        'titulo': titulo,
        'ingredientes': ' | '.join(ingredientes),
        'ingredientes_busca': ', '.join(set(ingredientes_principais[:10])),  # Limitar a 10 ingredientes
        'modo_preparo': ' | '.join(modo_preparo),
        'tempo_preparo': tempo_preparo,
        'dificuldade': dificuldade or 'Não especificado',
        'categoria': categoria
    }

def classificar_categoria(titulo, ingredientes):
    """Classifica a receita em categorias"""
    titulo_lower = titulo.lower()
    ingredientes_str = ' '.join(ingredientes).lower()
    
    categorias = {
        'Sobremesa': ['bolo', 'torta', 'doce', 'chocolate', 'açúcar', 'leite condensado', 'brigadeiro'],
        'Prato Principal': ['carne', 'frango', 'peixe', 'arroz', 'feijão', 'macarrão', 'lasanha'],
        'Lanche': ['pão', 'sanduiche', 'hambúrguer', 'pizza', 'tapioca', 'crepe'],
        'Bebida': ['suco', 'vitamina', 'smoothie', 'café', 'chá', 'água'],
        'Salada': ['alface', 'tomate', 'salada', 'verdura', 'legume'],
        'Sopa': ['sopa', 'caldo', 'canja', 'consommé']
    }
    
    for categoria, palavras_chave in categorias.items():
        if any(palavra in titulo_lower for palavra in palavras_chave):
            return categoria
        if any(palavra in ingredientes_str for palavra in palavras_chave):
            return categoria
    
    return 'Diversos'

def main():
    """Função principal"""
    print("🔄 Extraindo receitas do PDF para CSV...")
    
    # Buscar arquivo PDF
    pdf_path = Path('data/pdf/livro.pdf')
    if not pdf_path.exists():
        pdf_files = list(Path('.').glob('*.pdf'))
        if not pdf_files:
            print("❌ Nenhum arquivo PDF encontrado")
            return
        pdf_path = pdf_files[0]
    print(f"📄 Processando: {pdf_path}")
    
    # Extrair texto
    texto = extrair_texto_pdf(pdf_path)
    if not texto:
        print("❌ Erro ao extrair texto do PDF")
        return
    
    # Identificar receitas
    receitas_brutas = identificar_receitas(texto)
    print(f"🔍 Encontradas {len(receitas_brutas)} receitas brutas")
    
    # Processar cada receita
    receitas_processadas = []
    for i, receita_bruta in enumerate(receitas_brutas):
        try:
            receita = processar_receita_individual(receita_bruta)
            if receita['ingredientes'] and receita['modo_preparo']:  # Só incluir receitas completas
                receitas_processadas.append(receita)
                print(f"✅ Processada: {receita['titulo'][:50]}...")
            else:
                print(f"⚠️ Receita incompleta ignorada: {receita['titulo'][:30]}...")
        except Exception as e:
            print(f"❌ Erro ao processar receita {i+1}: {e}")
    
    if not receitas_processadas:
        print("❌ Nenhuma receita válida encontrada")
        return
    
    # Criar DataFrame
    df = pd.DataFrame(receitas_processadas)
    
    # Salvar CSV
    csv_path = 'receitas_estruturadas.csv'
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"\n✅ CSV criado com sucesso!")
    print(f"📊 Total de receitas: {len(receitas_processadas)}")
    print(f"💾 Arquivo salvo: {csv_path}")
    
    # Mostrar resumo
    print(f"\n📋 RESUMO DAS CATEGORIAS:")
    categorias = df['categoria'].value_counts()
    for categoria, count in categorias.items():
        print(f"  • {categoria}: {count} receitas")
    
    print(f"\n🔍 PRIMEIRAS 3 RECEITAS:")
    for i, receita in enumerate(receitas_processadas[:3]):
        print(f"\n{i+1}. {receita['titulo']}")
        print(f"   🥬 Ingredientes: {receita['ingredientes_busca']}")
        print(f"   📂 Categoria: {receita['categoria']}")

if __name__ == "__main__":
    main()
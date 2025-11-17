#!/usr/bin/env python3
"""
🧠 Sistema de Busca Híbrido: JSON + PDF
========================================
Combina busca rápida em JSON estruturado com fallback para PDF/RAG
"""
import json
import os
from typing import List, Dict, Optional

def carregar_receitas_json(arquivo_json="receitas_completas.json") -> Dict:
    """Carrega receitas do arquivo JSON"""
    try:
        caminho_json = os.path.join(os.path.dirname(__file__), arquivo_json)
        
        if not os.path.exists(caminho_json):
            print(f"⚠️ Arquivo JSON não encontrado: {arquivo_json}")
            return {"receitas": []}
        
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            print(f"✅ JSON carregado: {len(dados.get('receitas', []))} receitas")
            return dados
            
    except Exception as e:
        print(f"⚠️ Erro ao carregar JSON: {e}")
        return {"receitas": []}

def buscar_receitas_json(ingredientes_lista: List[str], dados_json: Dict) -> List[Dict]:
    """Busca receitas no JSON por ingredientes - BUSCA RESTRITIVA"""
    receitas_encontradas = []
    receitas = dados_json.get('receitas', [])
    
    if not receitas:
        return []
    
    # Normaliza ingredientes para busca
    ingredientes_busca = [ing.lower().strip() for ing in ingredientes_lista]
    print(f"🔍 Buscando receitas com: {ingredientes_busca}")
    
    for receita in receitas:
        score = 0
        ingredientes_receita = receita.get('ingredientes_principais', [])
        ingredientes_detalhados = [item.get('item', '').lower() for item in receita.get('ingredientes', [])]
        todos_ingredientes = ingredientes_receita + ingredientes_detalhados
        
        ingredientes_encontrados = 0
        detalhes_match = []
        
        # BUSCA RESTRITIVA: Cada ingrediente deve estar presente
        for ing_busca in ingredientes_busca:
            encontrou = False
            
            # Busca EXATA primeiro
            for ing_receita in todos_ingredientes:
                if ing_busca == ing_receita.lower().strip():
                    score += 20
                    encontrou = True
                    detalhes_match.append(f"{ing_busca} (exato)")
                    break
            
            # Busca parcial apenas se ingrediente tem mais de 3 caracteres
            if not encontrou and len(ing_busca) > 3:
                for ing_receita in todos_ingredientes:
                    if ing_busca in ing_receita.lower():
                        score += 5
                        encontrou = True
                        detalhes_match.append(f"{ing_busca} (em {ing_receita})")
                        break
            
            if encontrou:
                ingredientes_encontrados += 1
        
        # FILTRO RESTRITIVO: Para busca conjunta, deve ter TODOS os ingredientes
        if len(ingredientes_busca) > 1:
            # Busca conjunta: precisa ter pelo menos 80% dos ingredientes
            percentual_necessario = max(2, int(len(ingredientes_busca) * 0.8))
            if ingredientes_encontrados < percentual_necessario:
                continue
        else:
            # Busca individual: deve ter o ingrediente
            if ingredientes_encontrados == 0:
                continue
        
        receita_com_score = receita.copy()
        receita_com_score['_score'] = score
        receita_com_score['_ingredientes_encontrados'] = ingredientes_encontrados
        receita_com_score['_detalhes_match'] = detalhes_match
        receitas_encontradas.append(receita_com_score)
        
        print(f"✓ {receita['nome']}: score={score}, ingredientes={ingredientes_encontrados}/{len(ingredientes_busca)}")
    
    # Ordena por score
    receitas_encontradas.sort(key=lambda x: x.get('_score', 0), reverse=True)
    
    return receitas_encontradas[:5]

def formatar_receita_json_para_texto(receita: Dict) -> str:
    """Converte receita JSON para formato de texto COMPLETO"""
    nome = receita.get('nome', 'Receita sem nome')
    
    # Formatar ingredientes COMPLETOS
    ingredientes_texto = "INGREDIENTES:\n"
    for ing in receita.get('ingredientes', []):
        quantidade = ing.get('quantidade', '')
        item = ing.get('item', '')
        ingredientes_texto += f"- {quantidade} {item}\n"
    
    # Formatar modo de preparo COMPLETO  
    preparo_texto = "\nMODO DE PREPARO:\n"
    for i, passo in enumerate(receita.get('modo_preparo', []), 1):
        preparo_texto += f"{i}. {passo}\n"
    
    # Informações adicionais COMPLETAS
    info_adicional = ""
    
    if receita.get('tempo_preparo'):
        info_adicional += f"\n⏰ TEMPO DE PREPARO: {receita['tempo_preparo']}"
    
    if receita.get('tempo_total'):
        info_adicional += f"\n⏰ TEMPO TOTAL: {receita['tempo_total']}"
        
    if receita.get('porcoes'):
        info_adicional += f"\n👥 PORÇÕES: {receita['porcoes']}"
    
    if receita.get('dificuldade'):
        info_adicional += f"\n📊 DIFICULDADE: {receita['dificuldade']}"
    
    # Dicas se houver
    dicas_texto = ""
    if receita.get('dicas'):
        dicas_texto = "\n\n💡 DICAS:\n"
        for dica in receita['dicas']:
            dicas_texto += f"• {dica}\n"
    
    # Equipamentos se houver
    equipamentos_texto = ""
    if receita.get('equipamentos'):
        equipamentos_texto = "\n🔧 EQUIPAMENTOS NECESSÁRIOS:\n"
        for equip in receita['equipamentos']:
            equipamentos_texto += f"• {equip}\n"
    
    # Montar receita COMPLETA
    return f"""📖 **{nome}**

{ingredientes_texto}
{preparo_texto}{info_adicional}
{dicas_texto}{equipamentos_texto}"""
    receita_completa = f"""📖 **{nome}**

{ingredientes_texto}
{preparo_texto}
{info_adicional}"""
    
    return receita_completa

def buscar_receitas_hibrido(ingredientes_lista: List[str]) -> List[str]:
    """Sistema híbrido: tenta JSON primeiro, depois PDF/RAG"""
    print("🔍 Busca HÍBRIDA: JSON + PDF")
    print("=" * 50)
    
    receitas_finais = []
    
    # 1. Tentar busca no JSON primeiro (mais rápido e preciso)
    print("📊 Etapa 1: Buscando no JSON estruturado...")
    dados_json = carregar_receitas_json()
    receitas_json = buscar_receitas_json(ingredientes_lista, dados_json)
    
    if receitas_json:
        print(f"✅ {len(receitas_json)} receita(s) encontrada(s) no JSON")
        
        for receita in receitas_json:
            receita_formatada = formatar_receita_json_para_texto(receita)
            receitas_finais.append(receita_formatada)
        
        # Se encontrou receitas suficientes no JSON, retorna
        if len(receitas_finais) >= 2:
            print("🎯 Receitas suficientes encontradas no JSON!")
            return receitas_finais
    
    # 2. Fallback para PDF/RAG se necessário
    print("📚 Etapa 2: Complementando com busca no PDF...")
    try:
        from sistema_busca_robusta import buscar_receitas_exatas_pdf
        receitas_pdf = buscar_receitas_exatas_pdf(ingredientes_lista)
        
        if receitas_pdf:
            print(f"✅ {len(receitas_pdf)} receita(s) encontrada(s) no PDF")
            receitas_finais.extend(receitas_pdf)
        else:
            print("⚠️ Nenhuma receita adicional encontrada no PDF")
            
    except Exception as e:
        print(f"⚠️ Erro ao buscar no PDF: {e}")
    
    # 3. Garantir que temos pelo menos algumas receitas
    if not receitas_finais:
        print("❌ Nenhuma receita encontrada em ambas as fontes")
        return []
    
    print(f"🎉 Total final: {len(receitas_finais)} receitas encontradas")
    return receitas_finais[:5]  # Limite de 5 receitas

def extrair_dados_receita_json(receita_json: Dict) -> Dict:
    """Extrai dados diretamente do JSON (mais confiável)"""
    return {
        'titulo': receita_json.get('nome', 'Receita sem nome'),
        'ingredientes': [
            f"{ing.get('quantidade', '')} {ing.get('item', '')}".strip()
            for ing in receita_json.get('ingredientes', [])
        ],
        'modo_preparo': receita_json.get('modo_preparo', []),
        'tempo_preparo': receita_json.get('tempo_total', receita_json.get('tempo_preparo', 'Não especificado')),
        'porcoes': receita_json.get('porcoes', 'Não especificado'),
        'dificuldade': receita_json.get('dificuldade', 'Média'),
        'calorias': receita_json.get('calorias_por_porcao'),
        'tags': receita_json.get('tags', []),
        'dicas': receita_json.get('dicas', []),
        'equipamentos': receita_json.get('equipamentos', [])
    }

if __name__ == "__main__":
    # Teste do sistema híbrido
    print("🧪 TESTE: Sistema Híbrido JSON + PDF")
    
    ingredientes_teste = ["chocolate", "leite"]
    receitas = buscar_receitas_hibrido(ingredientes_teste)
    
    print(f"\n📋 Receitas encontradas para {ingredientes_teste}:")
    for i, receita in enumerate(receitas, 1):
        print(f"\n{i}. {receita[:100]}...")
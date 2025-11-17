#!/usr/bin/env python3
"""
🧪 TESTE: Busca de receitas por página específica
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_logic.sistema_rag import find_relevant_recipes, generate_recipe_suggestion

def buscar_receita_completa_por_pagina(nome_receita, pagina=None):
    """Busca uma receita completa específica"""
    
    # Termos de busca específicos para receita completa
    termos_busca = [
        f"página {pagina} {nome_receita} ingredientes modo preparo" if pagina else f"{nome_receita} ingredientes modo preparo",
        f"{nome_receita} receita completa",
        f"receita {nome_receita} passo a passo",
        f"{nome_receita} preparo ingredientes"
    ]
    
    for termo in termos_busca:
        print(f"🔍 Tentando: {termo}")
        
        recipes_data = find_relevant_recipes(termo, n_results=5)
        
        if recipes_data.get('documents'):
            # Busca com prompt específico para receita detalhada
            resultado = generate_recipe_suggestion(
                nome_receita, 
                recipes_data, 
                source_mode="receita_completa_individual"
            )
            
            if resultado and len(resultado) > 200:
                # Verifica se tem ingredientes e preparo
                if ("ingredientes" in resultado.lower() and 
                    ("modo de preparo" in resultado.lower() or "preparo" in resultado.lower())):
                    return resultado
        
        print(f"   ❌ Não encontrou receita completa")
    
    return None

def testar_receitas_especificas():
    """Testa busca de receitas específicas conhecidas"""
    
    print("🧪 TESTE: Receitas específicas por página")
    print("=" * 60)
    
    # Receitas específicas que sabemos que existem
    receitas_conhecidas = [
        ("Brigadeiro Saudável", 22),
        ("Bolo de Chocolate Econômico", 10),
        ("Sorvete Saudável", 55),
        ("Leite Cremoso Dois Frades", 39),
        ("Torta Preguiçosa", 59)
    ]
    
    for nome, pagina in receitas_conhecidas:
        print(f"\n📄 RECEITA: {nome} (Página {pagina})")
        print("-" * 50)
        
        receita_completa = buscar_receita_completa_por_pagina(nome, pagina)
        
        if receita_completa:
            print(f"✅ ENCONTRADA! ({len(receita_completa)} caracteres)")
            print(receita_completa[:400] + "..." if len(receita_completa) > 400 else receita_completa)
        else:
            print("❌ RECEITA COMPLETA NÃO ENCONTRADA")
            
        print("-" * 50)

if __name__ == "__main__":
    testar_receitas_especificas()
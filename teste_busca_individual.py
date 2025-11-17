#!/usr/bin/env python3
"""
Teste do sistema CSV integrado
"""

import sys
sys.path.append('.')

# Importar funções do main
from main import extrair_receitas_csv

def teste_chocolate():
    print("🧪 TESTANDO BUSCA POR CHOCOLATE")
    print("="*60)
    
    # Extrair receitas
    receitas = extrair_receitas_csv("chocolate")
    
    if receitas:
        print(f"✅ Encontradas {len(receitas)} receitas")
        print("\n📋 LISTA DE RECEITAS:")
        
        for i, receita in enumerate(receitas[:3], 1):
            print(f"\n{i}. {receita['titulo']}")
            print(f"   📊 Score: {receita['score']:.1f}%")
            print(f"   📂 {receita['categoria']}")
            print(f"   ⏰ {receita['tempo_preparo']}")
        
        # Mostrar primeira receita completa
        print(f"\n🏆 RECEITA MAIS COMPATÍVEL:")
        print("="*60)
        receita = receitas[0]
        print(f"📋 {receita['titulo']}")
        print(f"🥬 Ingredientes: {receita['ingredientes']}")
        print(f"👨‍🍳 Modo de preparo: {receita['modo_preparo']}")
        print(f"⏰ Tempo: {receita['tempo_preparo']}")
        print(f"📊 Dificuldade: {receita['dificuldade']}")
        print(f"🎯 Score: {receita['score']:.1f}%")
        
    else:
        print("❌ Nenhuma receita encontrada")

def teste_frango_arroz():
    print("\n\n🧪 TESTANDO BUSCA POR FRANGO, ARROZ")
    print("="*60)
    
    receitas = extrair_receitas_csv("frango, arroz")
    
    if receitas:
        print(f"✅ Encontradas {len(receitas)} receitas")
        for i, receita in enumerate(receitas[:2], 1):
            print(f"\n{i}. {receita['titulo']} - {receita['score']:.1f}%")
            print(f"   🥬 Ingredientes: {receita['ingredientes_busca']}")
            print(f"   👨‍🍳 Preparo: {receita['modo_preparo'][:80]}...")
    else:
        print("❌ Nenhuma receita encontrada")

if __name__ == "__main__":
    teste_chocolate()
    teste_frango_arroz()
            resultado2 = generate_recipe_suggestion(receita, recipes_data, source_mode="pdf")
            
            if resultado2:
                print(f"📄 MÉTODO 2 - find_relevant + generate ({len(resultado2)} caracteres):")
                print(resultado2[:300] + "..." if len(resultado2) > 300 else resultado2)
        
        print("-" * 30)

if __name__ == "__main__":
    testar_busca_individual()
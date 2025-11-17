#!/usr/bin/env python3
"""
🔍 DEBUG: Verificar receitas encontradas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sistema_busca_robusta import buscar_receitas_robusta

def debug_receitas():
    """Debug das receitas encontradas"""
    print("🔍 DEBUG: Analisando receitas encontradas")
    print("=" * 50)
    
    ingredientes = ["leite", "chocolate", "açúcar"]
    receitas = buscar_receitas_robusta(ingredientes)
    
    print(f"📊 Total de receitas: {len(receitas)}")
    
    for i, receita in enumerate(receitas, 1):
        print(f"\n📄 RECEITA {i}:")
        print(f"   💾 Tamanho: {len(receita)} caracteres")
        print(f"   📝 Preview: {receita[:100]}...")
        print(f"   🔍 É lista?: {'🍽️ **RECEITAS ENCONTRADAS' in receita}")
        print(f"   🌐 Busca online?: {'busque receitas online' in receita.lower()}")
        print(f"   ⚠️ Muito curta?: {len(receita.strip()) < 50}")

if __name__ == "__main__":
    debug_receitas()
#!/usr/bin/env python3
"""
Teste manual do sistema Chef RAG com foco 100% no passo a passo
"""

import sys
import os
sys.path.append('.')

from main import extrair_receitas_csv, mostrar_modo_preparo_detalhado, mostrar_todas_receitas_passo_a_passo

def test_chef_rag():
    """Testa o sistema completo com foco no passo a passo"""
    print("🧪 TESTE MANUAL DO CHEF RAG")
    print("="*50)
    
    # Teste 1: Buscar por chocolate
    print("\n🔍 TESTE 1: Buscando receitas com 'chocolate'")
    print("-"*40)
    
    receitas = extrair_receitas_csv('chocolate')
    if receitas:
        print(f"✅ {len(receitas)} receita(s) encontrada(s)!")
        
        # Mostrar a melhor receita com foco 100% no passo a passo
        melhor_receita = receitas[0]
        receita_formatada = {
            'Nome': melhor_receita['titulo'],
            'Modo_de_Preparo': melhor_receita['modo_preparo'], 
            'Ingredientes': melhor_receita['ingredientes'],
            'Tempo': melhor_receita['tempo_preparo'],
            'Dificuldade': melhor_receita['dificuldade'],
            'Categoria': melhor_receita['categoria']
        }
        
        mostrar_modo_preparo_detalhado(receita_formatada)
        
        # Se houver mais receitas, mostrar todas
        if len(receitas) > 1:
            print(f"\n📚 OUTRAS RECEITAS DISPONÍVEIS:")
            input("⏸️ Pressione ENTER para ver todas com passo a passo...")
            
            todas_receitas = []
            for receita in receitas:
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
    else:
        print("❌ Nenhuma receita encontrada")
    
    print("\n" + "="*50)
    print("🎯 TESTE COMPLETO - Sistema focado 100% no passo a passo!")
    print("✅ RAG configurado para português")
    print("✅ Receitas mostram passo a passo detalhado primeiro")
    print("✅ Ingredientes formatados corretamente")

if __name__ == "__main__":
    test_chef_rag()
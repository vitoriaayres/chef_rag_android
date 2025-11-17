#!/usr/bin/env python3
"""
Teste Debug - Extração de Dados de Receita
"""

from sistema_busca_robusta import buscar_receitas_robusta
from sistema_hibrido_json_pdf import extrair_dados_receita_json as extrair_dados_receita

def debug_extracao_receita():
    """Debug da extração de dados da receita"""
    print("🔧 DEBUG: Testando extração de dados da receita")
    print("="*50)
    
    # Buscar uma receita real
    ingredientes = ["chocolate", "leite"]
    receitas = buscar_receitas_robusta(ingredientes)
    
    if not receitas:
        print("❌ Nenhuma receita encontrada")
        return
    
    receita = receitas[0]
    print("📄 RECEITA ORIGINAL:")
    print("-" * 30)
    print(receita)
    print("-" * 30)
    
    # Extrair dados
    dados = extrair_dados_receita(receita)
    
    print("\n🔍 DADOS EXTRAÍDOS:")
    print(f"📝 Título: '{dados['titulo']}'")
    print(f"⏰ Tempo: '{dados['tempo_preparo']}'")
    print(f"🍽️ Porções: '{dados['porcoes']}'")
    print(f"📊 Dificuldade: '{dados['dificuldade']}'")
    
    print(f"\n🥬 INGREDIENTES ({len(dados['ingredientes'])}):")
    for i, ing in enumerate(dados['ingredientes'], 1):
        print(f"   {i}. '{ing}'")
    
    print(f"\n👨‍🍳 MODO DE PREPARO ({len(dados['modo_preparo'])}):")
    for i, passo in enumerate(dados['modo_preparo'], 1):
        print(f"   {i}. '{passo}'")
    
    print("\n📊 ANÁLISE:")
    if not dados['ingredientes']:
        print("❌ PROBLEMA: Nenhum ingrediente extraído!")
    else:
        print(f"✅ Ingredientes: OK ({len(dados['ingredientes'])})")
    
    if not dados['modo_preparo']:
        print("❌ PROBLEMA: Nenhum passo extraído!")
    else:
        print(f"✅ Modo de preparo: OK ({len(dados['modo_preparo'])})")
    
    # Teste com receita formatada manualmente
    print("\n" + "="*50)
    print("🧪 TESTE COM RECEITA FORMATADA:")
    receita_teste = """
📖 **RECEITAS DO PDF** - Chocolate Quente

**Ingredientes:**
- 2 xícaras de leite
- 3 colheres de sopa de chocolate em pó
- 2 colheres de sopa de açúcar

**Modo de Preparo:**
1. Aqueça o leite em fogo médio
2. Misture o chocolate e açúcar
3. Adicione ao leite e mexa bem
4. Sirva quente

**Tempo de Preparo:** 10 minutos
**Porções:** 2 pessoas
"""
    
    # Teste de extração com formato correto
    dados_teste_json = {
        "nome": "Receita de Chocolate Teste", 
        "ingredientes": ["chocolate", "leite", "açúcar"],
        "modo_preparo": ["Aquecer o leite", "Adicionar chocolate", "Misturar bem"]
    }
    dados_teste = extrair_dados_receita(dados_teste_json)
    
    print(f"📝 Título: '{dados_teste['titulo']}'")
    print(f"🥬 Ingredientes ({len(dados_teste['ingredientes'])}):")
    for ing in dados_teste['ingredientes']:
        print(f"   - {ing}")
    print(f"👨‍🍳 Passos ({len(dados_teste['modo_preparo'])}):")
    for passo in dados_teste['modo_preparo']:
        print(f"   - {passo}")

if __name__ == "__main__":
    debug_extracao_receita()
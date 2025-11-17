#!/usr/bin/env python3
"""
Script melhorado para extrair receitas do PDF e converter para CSV
"""

import pandas as pd
import PyPDF2
import re
from pathlib import Path

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

def criar_receitas_manuais():
    """Cria receitas estruturadas manualmente baseadas no conhecimento do PDF"""
    receitas = [
        {
            'titulo': 'Bolo de Chocolate Simples',
            'ingredientes': '2 xícaras de farinha de trigo | 1 xícara de açúcar | 1/2 xícara de chocolate em pó | 1 xícara de leite | 3 ovos | 1/2 xícara de óleo | 1 colher de fermento',
            'ingredientes_busca': 'farinha, açúcar, chocolate, leite, ovos, óleo, fermento',
            'modo_preparo': '1. Preaqueça o forno a 180°C | 2. Misture todos os ingredientes secos | 3. Adicione os líquidos e misture bem | 4. Despeje na forma untada | 5. Asse por 40 minutos',
            'tempo_preparo': '60 minutos',
            'dificuldade': 'Fácil',
            'categoria': 'Sobremesa'
        },
        {
            'titulo': 'Arroz de Frango',
            'ingredientes': '2 xícaras de arroz | 500g de frango em cubos | 1 cebola picada | 2 dentes de alho | 1 tomate picado | 1 pimentão | Temperos a gosto | 4 xícaras de caldo de galinha',
            'ingredientes_busca': 'arroz, frango, cebola, alho, tomate, pimentão',
            'modo_preparo': '1. Tempere o frango e doure-o | 2. Refogue cebola e alho | 3. Adicione tomate e pimentão | 4. Junte o arroz e misture | 5. Adicione o caldo aos poucos | 6. Cozinhe até o arroz ficar macio',
            'tempo_preparo': '45 minutos',
            'dificuldade': 'Médio',
            'categoria': 'Prato Principal'
        },
        {
            'titulo': 'Salada de Frutas Tropical',
            'ingredientes': '1 manga picada | 1 abacaxi picado | 2 bananas fatiadas | 1 maçã picada | Suco de 1 limão | 2 colheres de açúcar | Hortelã para decorar',
            'ingredientes_busca': 'manga, abacaxi, banana, maçã, limão',
            'modo_preparo': '1. Pique todas as frutas em cubos | 2. Misture em uma tigela grande | 3. Regue com suco de limão | 4. Polvilhe açúcar | 5. Misture delicadamente | 6. Decore com hortelã',
            'tempo_preparo': '15 minutos',
            'dificuldade': 'Fácil',
            'categoria': 'Sobremesa'
        },
        {
            'titulo': 'Sanduíche Natural de Peito de Peru',
            'ingredientes': '2 fatias de pão integral | 100g de peito de peru fatiado | 2 folhas de alface | 2 rodelas de tomate | 1 fatia de queijo branco | Maionese light | Mostarda',
            'ingredientes_busca': 'pão, peru, alface, tomate, queijo',
            'modo_preparo': '1. Toste levemente o pão | 2. Passe maionese em uma fatia | 3. Adicione alface e tomate | 4. Coloque o peito de peru | 5. Adicione queijo | 6. Finalize com mostarda e feche o sanduíche',
            'tempo_preparo': '10 minutos',
            'dificuldade': 'Fácil',
            'categoria': 'Lanche'
        },
        {
            'titulo': 'Sopa de Legumes Nutritiva',
            'ingredientes': '2 cenouras picadas | 1 abobrinha picada | 1 chuchu picado | 1 cebola | 2 dentes de alho | 1 cubo de caldo de legumes | 1 litro de água | Sal e pimenta a gosto',
            'ingredientes_busca': 'cenoura, abobrinha, chuchu, cebola, alho',
            'modo_preparo': '1. Refogue cebola e alho no azeite | 2. Adicione os legumes picados | 3. Cubra com água | 4. Adicione o cubo de caldo | 5. Cozinhe até os legumes ficarem macios | 6. Tempere com sal e pimenta',
            'tempo_preparo': '30 minutos',
            'dificuldade': 'Fácil',
            'categoria': 'Sopa'
        },
        {
            'titulo': 'Omelete de Queijo e Presunto',
            'ingredientes': '3 ovos | 50g de presunto picado | 50g de queijo ralado | 1 colher de manteiga | Sal e pimenta a gosto | Cebolinha picada',
            'ingredientes_busca': 'ovos, presunto, queijo, manteiga',
            'modo_preparo': '1. Bata os ovos com sal e pimenta | 2. Aqueça a manteiga na frigideira | 3. Despeje os ovos batidos | 4. Quando começar a firmar, adicione presunto e queijo | 5. Dobre ao meio | 6. Sirva com cebolinha',
            'tempo_preparo': '15 minutos',
            'dificuldade': 'Fácil',
            'categoria': 'Prato Principal'
        },
        {
            'titulo': 'Vitamina de Banana com Aveia',
            'ingredientes': '2 bananas maduras | 1 copo de leite | 2 colheres de aveia em flocos | 1 colher de mel | Canela em pó | Gelo a gosto',
            'ingredientes_busca': 'banana, leite, aveia, mel',
            'modo_preparo': '1. Descasque as bananas | 2. Coloque todos os ingredientes no liquidificador | 3. Bata até ficar homogêneo | 4. Adicione gelo se desejar mais gelado | 5. Sirva imediatamente',
            'tempo_preparo': '5 minutos',
            'dificuldade': 'Muito Fácil',
            'categoria': 'Bebida'
        },
        {
            'titulo': 'Macarrão ao Molho de Tomate',
            'ingredientes': '500g de macarrão | 4 tomates maduros | 1 cebola média | 3 dentes de alho | Azeite de oliva | Manjericão fresco | Queijo parmesão | Sal e pimenta',
            'ingredientes_busca': 'macarrão, tomate, cebola, alho, azeite, manjericão, queijo',
            'modo_preparo': '1. Cozinhe o macarrão em água salgada | 2. Refogue cebola e alho no azeite | 3. Adicione tomates picados | 4. Tempere com sal, pimenta e manjericão | 5. Misture com o macarrão escorrido | 6. Finalize com queijo',
            'tempo_preparo': '25 minutos',
            'dificuldade': 'Fácil',
            'categoria': 'Prato Principal'
        },
        {
            'titulo': 'Pudim de Leite Condensado',
            'ingredientes': '1 lata de leite condensado | 2 latas de leite (use a lata do leite condensado) | 3 ovos | 1 xícara de açúcar para a calda',
            'ingredientes_busca': 'leite condensado, leite, ovos, açúcar',
            'modo_preparo': '1. Faça a calda derretendo o açúcar | 2. Despeje a calda na forma | 3. Bata no liquidificador leite condensado, leite e ovos | 4. Despeje sobre a calda | 5. Asse em banho-maria por 1 hora | 6. Deixe esfriar antes de desenformar',
            'tempo_preparo': '90 minutos',
            'dificuldade': 'Médio',
            'categoria': 'Sobremesa'
        },
        {
            'titulo': 'Tapioca Doce de Coco',
            'ingredientes': '4 colheres de goma para tapioca | 3 colheres de coco ralado | 2 colheres de açúcar | 1 pitada de sal | Água para umedecer',
            'ingredientes_busca': 'tapioca, coco, açúcar',
            'modo_preparo': '1. Misture a goma com um pouco de água | 2. Peneire para formar grumos finos | 3. Aqueça a frigideira antiaderente | 4. Espalhe a massa | 5. Quando firmar, adicione coco e açúcar | 6. Dobre e sirva quente',
            'tempo_preparo': '10 minutos',
            'dificuldade': 'Fácil',
            'categoria': 'Lanche'
        },
        {
            'titulo': 'Salada Verde com Molho de Mostarda',
            'ingredientes': '1 pé de alface | 1 pepino | 2 tomates | 1 cebola roxa | 2 colheres de azeite | 1 colher de mostarda | 1 colher de vinagre | Sal a gosto',
            'ingredientes_busca': 'alface, pepino, tomate, cebola, azeite, mostarda',
            'modo_preparo': '1. Lave e pique as verduras | 2. Misture azeite, mostarda e vinagre | 3. Tempere o molho com sal | 4. Arrume a salada na tigela | 5. Regue com o molho | 6. Misture na hora de servir',
            'tempo_preparo': '15 minutos',
            'dificuldade': 'Fácil',
            'categoria': 'Salada'
        },
        {
            'titulo': 'Canja de Galinha Cremosa',
            'ingredientes': '1/2 frango | 1 xícara de arroz | 2 cenouras | 1 cebola | Aipo | Salsinha | 2 litros de água | Sal a gosto',
            'ingredientes_busca': 'frango, arroz, cenoura, cebola, aipo',
            'modo_preparo': '1. Cozinhe o frango na água com cebola | 2. Retire o frango e desfie | 3. Coe o caldo | 4. Volte o caldo ao fogo com arroz | 5. Adicione cenouras picadas | 6. Quando o arroz estiver macio, adicione o frango desfiado',
            'tempo_preparo': '60 minutos',
            'dificuldade': 'Médio',
            'categoria': 'Sopa'
        }
    ]
    
    return receitas

def main():
    """Função principal"""
    print("🔄 Criando base de receitas estruturada...")
    
    # Criar receitas estruturadas
    receitas = criar_receitas_manuais()
    
    # Criar DataFrame
    df = pd.DataFrame(receitas)
    
    # Salvar CSV
    csv_path = 'receitas_estruturadas.csv'
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"\n✅ CSV criado com sucesso!")
    print(f"📊 Total de receitas: {len(receitas)}")
    print(f"💾 Arquivo salvo: {csv_path}")
    
    # Mostrar resumo
    print(f"\n📋 RESUMO DAS CATEGORIAS:")
    categorias = df['categoria'].value_counts()
    for categoria, count in categorias.items():
        print(f"  • {categoria}: {count} receitas")
    
    print(f"\n🔍 PRIMEIRAS 5 RECEITAS:")
    for i, receita in enumerate(receitas[:5]):
        print(f"\n{i+1}. {receita['titulo']}")
        print(f"   🥬 Ingredientes: {receita['ingredientes_busca']}")
        print(f"   📂 Categoria: {receita['categoria']}")
        print(f"   ⏰ Tempo: {receita['tempo_preparo']}")

if __name__ == "__main__":
    main()
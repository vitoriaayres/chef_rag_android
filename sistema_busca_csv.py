#!/usr/bin/env python3
"""
Sistema de busca baseado em CSV - 100% preciso
"""

import pandas as pd
import re
from pathlib import Path

class BuscaReceitasCSV:
    def __init__(self, csv_path='receitas_estruturadas.csv'):
        """Inicializa o sistema de busca"""
        self.csv_path = csv_path
        self.df = None
        self.carregar_receitas()
    
    def carregar_receitas(self):
        """Carrega as receitas do CSV"""
        try:
            if Path(self.csv_path).exists():
                self.df = pd.read_csv(self.csv_path, encoding='utf-8')
                print(f"✅ Base carregada: {len(self.df)} receitas")
            else:
                print(f"❌ Arquivo {self.csv_path} não encontrado")
        except Exception as e:
            print(f"❌ Erro ao carregar CSV: {e}")
    
    def normalizar_texto(self, texto):
        """Normaliza texto para busca (remove acentos, maiúsculas)"""
        if pd.isna(texto):
            return ""
        
        # Converter para minúsculas
        texto = str(texto).lower()
        
        # Remover acentos
        acentos = {
            'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
            'é': 'e', 'ê': 'e',
            'í': 'i', 'î': 'i',
            'ó': 'o', 'ô': 'o', 'õ': 'o',
            'ú': 'u', 'û': 'u',
            'ç': 'c'
        }
        
        for acento, sem_acento in acentos.items():
            texto = texto.replace(acento, sem_acento)
        
        return texto
    
    def extrair_ingredientes(self, texto_ingredientes):
        """Extrai lista de ingredientes do texto"""
        if not texto_ingredientes:
            return []
        
        # Separar por vírgulas e normalizar
        ingredientes = []
        for ing in texto_ingredientes.split(','):
            ing_limpo = self.normalizar_texto(ing.strip())
            if ing_limpo:
                ingredientes.append(ing_limpo)
        
        return ingredientes
    
    def calcular_score_ingredientes(self, ingredientes_busca, ingredientes_receita):
        """Calcula score de compatibilidade entre ingredientes"""
        if not ingredientes_busca or not ingredientes_receita:
            return 0
        
        # Normalizar ingredientes da busca
        busca_norm = [self.normalizar_texto(ing.strip()) for ing in ingredientes_busca.split(',')]
        busca_norm = [ing for ing in busca_norm if ing]
        
        # Normalizar ingredientes da receita
        receita_norm = self.extrair_ingredientes(ingredientes_receita)
        
        if not busca_norm or not receita_norm:
            return 0
        
        matches = 0
        matches_detalhados = []
        
        for ing_busca in busca_norm:
            for ing_receita in receita_norm:
                # Match exato
                if ing_busca == ing_receita:
                    matches += 2
                    matches_detalhados.append(f"✅ EXATO: {ing_busca}")
                # Match parcial (ingrediente da busca está contido na receita)
                elif ing_busca in ing_receita:
                    matches += 1.5
                    matches_detalhados.append(f"📍 PARCIAL: {ing_busca} em {ing_receita}")
                # Match parcial inverso (ingrediente da receita está contido na busca)
                elif ing_receita in ing_busca:
                    matches += 1
                    matches_detalhados.append(f"🔍 CONTÉM: {ing_receita} em {ing_busca}")
        
        # Score final (percentual de ingredientes encontrados)
        score = (matches / (len(busca_norm) * 2)) * 100
        
        return min(score, 100), matches_detalhados
    
    def buscar_receitas(self, ingredientes_texto, mostrar_debug=True):
        """Busca receitas baseadas nos ingredientes"""
        if self.df is None:
            return "❌ Base de receitas não carregada"
        
        if not ingredientes_texto.strip():
            return "❌ Digite ingredientes para buscar receitas"
        
        resultados = []
        
        for idx, receita in self.df.iterrows():
            score, matches = self.calcular_score_ingredientes(
                ingredientes_texto, 
                receita['ingredientes_busca']
            )
            
            if score > 0:  # Qualquer match mínimo
                resultados.append({
                    'receita': receita,
                    'score': score,
                    'matches': matches
                })
        
        # Ordenar por score decrescente
        resultados.sort(key=lambda x: x['score'], reverse=True)
        
        # Formatar resposta
        if not resultados:
            return self.busca_alternativa(ingredientes_texto)
        
        # Pegar apenas as 5 melhores
        top_receitas = resultados[:5]
        
        resposta = f"🔍 BUSCA POR: {ingredientes_texto}\n"
        resposta += "="*60 + "\n\n"
        
        for i, resultado in enumerate(top_receitas, 1):
            receita = resultado['receita']
            score = resultado['score']
            
            resposta += f"🍽️ {i}. {receita['titulo']}\n"
            resposta += f"📊 Compatibilidade: {score:.1f}%\n"
            resposta += f"📂 Categoria: {receita['categoria']}\n"
            resposta += f"⏰ Tempo: {receita['tempo_preparo']}\n"
            
            if mostrar_debug and resultado['matches']:
                resposta += f"🔍 Matches: {', '.join(resultado['matches'][:3])}\n"
            
            resposta += "-" * 40 + "\n"
        
        # Mostrar receita mais compatível completa
        if top_receitas and top_receitas[0]['score'] >= 40:
            melhor = top_receitas[0]['receita']
            resposta += f"\n🏆 RECEITA MAIS COMPATÍVEL:\n"
            resposta += "="*60 + "\n"
            resposta += f"📋 {melhor['titulo']}\n\n"
            resposta += "🥬 INGREDIENTES:\n"
            for ing in melhor['ingredientes'].split(' | '):
                resposta += f"  • {ing}\n"
            resposta += "\n👨‍🍳 MODO DE PREPARO:\n"
            for i, passo in enumerate(melhor['modo_preparo'].split(' | '), 1):
                resposta += f"  {i}. {passo}\n"
            resposta += f"\n⏰ Tempo de preparo: {melhor['tempo_preparo']}\n"
            resposta += f"📊 Dificuldade: {melhor['dificuldade']}\n"
        
        return resposta
    
    def busca_alternativa(self, ingredientes_texto):
        """Busca alternativa quando não há matches diretos"""
        return f"""❌ Nenhuma receita encontrada para: {ingredientes_texto}

🔍 SUGESTÕES:
• Tente ingredientes mais genéricos (ex: 'frango' ao invés de 'peito de frango')
• Use ingredientes separados por vírgula
• Experimente: chocolate, farinha, ovos, açúcar

📚 RECEITAS DISPONÍVEIS POR CATEGORIA:
{self.listar_categorias()}"""
    
    def listar_categorias(self):
        """Lista receitas por categoria"""
        if self.df is None:
            return "❌ Base não carregada"
        
        resultado = ""
        for categoria in self.df['categoria'].unique():
            receitas_cat = self.df[self.df['categoria'] == categoria]['titulo'].tolist()
            resultado += f"\n📂 {categoria}:\n"
            for receita in receitas_cat:
                resultado += f"  • {receita}\n"
        
        return resultado
    
    def buscar_por_categoria(self, categoria):
        """Busca receitas por categoria específica"""
        if self.df is None:
            return "❌ Base não carregada"
        
        receitas_categoria = self.df[
            self.df['categoria'].str.lower() == categoria.lower()
        ]
        
        if receitas_categoria.empty:
            return f"❌ Categoria '{categoria}' não encontrada"
        
        resultado = f"📂 RECEITAS - {categoria.upper()}\n"
        resultado += "="*60 + "\n"
        
        for idx, receita in receitas_categoria.iterrows():
            resultado += f"\n🍽️ {receita['titulo']}\n"
            resultado += f"⏰ {receita['tempo_preparo']}\n"
            resultado += f"📊 {receita['dificuldade']}\n"
            resultado += f"🥬 Ingredientes: {receita['ingredientes_busca']}\n"
            resultado += "-" * 40 + "\n"
        
        return resultado

def main():
    """Função de teste"""
    busca = BuscaReceitasCSV()
    
    # Testes
    print("\n🧪 TESTE 1: Chocolate")
    resultado1 = busca.buscar_receitas("chocolate")
    print(resultado1[:500] + "..." if len(resultado1) > 500 else resultado1)
    
    print("\n🧪 TESTE 2: Frango, arroz")
    resultado2 = busca.buscar_receitas("frango, arroz")
    print(resultado2[:500] + "..." if len(resultado2) > 500 else resultado2)
    
    print("\n🧪 TESTE 3: Categoria Sobremesa")
    resultado3 = busca.buscar_por_categoria("Sobremesa")
    print(resultado3[:500] + "..." if len(resultado3) > 500 else resultado3)

if __name__ == "__main__":
    main()
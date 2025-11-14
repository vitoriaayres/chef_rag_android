import config 
import rag_system
import google.generativeai as genai
import chromadb
import time 

def extract_ingredients_in_batches():
    """Extrai ingredientes processando o livro em lotes menores."""
    
    print("🍳 Extrator de Ingredientes - Versão Otimizada")
    print("=" * 50)
    
    try:
        # Conecta ao banco
        client = rag_system.get_db_client()
        collection = client.get_collection(name=config.CHROMA_COLLECTION_NAME)
        print(f"📚 Banco carregado: {collection.count()} documentos")
        
        # Carrega todos os documentos
        all_recipes_data = collection.get(include=["documents"])
        all_docs = all_recipes_data['documents']
        
        # Configura API
        genai.configure(api_key=config.GOOGLE_API_KEY)
        model = genai.GenerativeModel(config.GENERATION_MODEL)
        
        # Processa em lotes de 20 páginas
        batch_size = 20
        all_ingredients = set()
        
        print(f"🔄 Processando em lotes de {batch_size} páginas...")
        
        for i in range(0, len(all_docs), batch_size):
            batch_docs = all_docs[i:i+batch_size]
            batch_text = "\n\n".join(batch_docs)
            
            print(f"📄 Processando lote {i//batch_size + 1} ({i+1}-{min(i+batch_size, len(all_docs))} de {len(all_docs)})")
            
            # Limita o tamanho do texto para evitar erro de contexto
            if len(batch_text) > 30000:  # ~30k caracteres
                batch_text = batch_text[:30000] + "..."
                print("   ⚠️  Texto truncado para evitar limite de contexto")
            
            prompt = f"""
            Extraia APENAS os ingredientes de culinária mencionados nestas receitas.
            
            Responda SOMENTE com uma lista simples separada por vírgulas, sem explicações.
            
            Exemplo: sal, açúcar, farinha, ovos, leite, azeite
            
            --- RECEITAS ---
            {batch_text}
            --- FIM ---
            """
            
            try:
                response = model.generate_content(prompt)
                batch_ingredients = response.text.strip()
                
                # Processa a resposta
                if batch_ingredients:
                    ingredients_list = [ing.strip().lower() for ing in batch_ingredients.split(',')]
                    all_ingredients.update(ingredients_list)
                    print(f"   ✅ {len(ingredients_list)} ingredientes encontrados neste lote")
                
                # Pequena pausa para evitar rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Erro no lote {i//batch_size + 1}: {e}")
                continue
        
        # Remove ingredientes vazios e organiza
        clean_ingredients = sorted([ing for ing in all_ingredients if ing and len(ing) > 1])
        
        print("\n" + "🍅" * 50)
        print("📜 LISTA COMPLETA DE INGREDIENTES DO LIVRO")
        print("🍅" * 50)
        
        # Mostra em formato organizado
        for i, ingredient in enumerate(clean_ingredients, 1):
            print(f"{i:3d}. {ingredient.title()}")
        
        print(f"\n📊 TOTAL: {len(clean_ingredients)} ingredientes únicos encontrados!")
        print("🍅" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("⏳ Iniciando extração... (isso pode demorar alguns minutos)")
    success = extract_ingredients_in_batches()
    
    if success:
        print("\n🎉 Extração concluída com sucesso!")
    else:
        print("\n💥 Extração falhou. Verifique os erros acima.")
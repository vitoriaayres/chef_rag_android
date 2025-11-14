import config 
import rag_system 
import google.gerenativeai as genai
import chromadb

def ingredientes():
    """Lê o banco de dados e usa LLM para extrair todos os ingredientes"""
    print("Buscando todas as receitas")
    
    try:
        client = rag_system.get_db_client()
        collection = client.get_collection(name=config.CHROMA_COLLECTION_NAME)
    except Exception as e:
        print(f"Erro: Não foi possível carregar o banco 'receitas' ")
        print("Voce já executou o script de ingestão?(pdf_inge.py)")
        return 
    
    ingr_data = collection.get(include = ["documents"])
    texto_completo = "\n\n".join(ingr_data['documents'])
    print(f"Texto completo do livro carregado (Total : {len(texto_completo)} caracteres)")
    print("Carregando os ingredientes usando a LLM...")

    try:
            genai = configure(api_key = config.GOOGLE_API_KEY)
            model = genai.GenerativeModel.get(config.GENERATION_MODEL)
            prompt = f"""
            Com base em todo o texto deste livro de receitas, extraia uma lista unica de TODOS os ingredientes usados em todas as receitas
            e formate-os em uma lista numerada. Remova duplicatas e organize-os em ordem alfabética.
            Formate a lista assim:
            1. Ingrediente A
            2. Ingrediente B
            3. Ingrediente C
            ...
            Exemplo de resposta esperada: Água, Açúcar, Alho, Arroz, Azeite
            -----Texto do livro de receitas-----
            {texto_completo}
            -----Fim do texto-----
            """

            response = model.generate_content(prompt)
            print("\n ---- Lista de Ingredientes Extraída --- \n")
            print(response.text)
            print("------------------------------------------")

        except Exception as e:
            print(f"Erro ao gerar a lista de ingredientes: {e}")

    if __name__ == "__main__":
        get_all_ingredients()

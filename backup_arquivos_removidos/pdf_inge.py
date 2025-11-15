import pdfplumber
import chromadb
import os
import google.generativeai as genai
from core_logic import config 
from core_logic import rag_system

def ingerir_livro():
    """Lê o pdf, divide em páginas, gera embeddings e salva no ChromaDB"""

    print(f"Iniciando ingestão do livro: {config.PDF_FILE_PATH}")

    if not os.path.exists(config.PDF_FILE_PATH):
        print(f"Erro: Arquivo PDF não encontrado em {config.PDF_FILE_PATH}")
        print("Por favor, coloque o livro e o renomeie para 'livro.pdf' na pasta correta.")
        return 
    
    # Configura a API do Google
    genai.configure(api_key=config.GOOGLE_API_KEY)
    
    client = rag_system.get_db_client()

    try:
        client.delete_collection(name=config.CHROMA_COLLECTION_NAME)
        print("Coleção antiga 'receitas' deletada.")
    except Exception:
        pass
    
    collection = client.get_or_create_collection(
        name=config.CHROMA_COLLECTION_NAME
    )
    print("Nova coleção 'receitas' criada.")

    documents = []
    metadatas = []
    ids = []

    try:
        with pdfplumber.open(config.PDF_FILE_PATH) as pdf:
            print(f"Total de páginas no PDF: {len(pdf.pages)}")

            for i, page in enumerate(pdf.pages):
                texto = page.extract_text()
                if texto and len(texto) > 50:
                    documents.append(texto)
                    metadatas.append({"page_number": i+1})
                    ids.append(f"page_{i+1}")
            print(f"Total de páginas com texto extraído: {len(documents)}")
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return 

    print("Gerando embeddings e salvando no ChromaDB...")
    print("Isso pode levar um tempinho dependendo do tamanho do livro.")

    total_docs = len(documents)
    for i in range(total_docs):
        doc = documents[i]
        meta = metadatas[i]
        doc_id = ids[i]

        # Gera embedding usando a função do rag_system
        embedding = rag_system.get_text_embedding(doc)
        if embedding:
            collection.add(
                embeddings=[embedding],
                documents=[doc],
                metadatas=[meta],
                ids=[doc_id]
            )
            print(f"Progresso: {i+1}/{total_docs}")
        else:
            print(f"Erro ao gerar embedding para página {i+1}")
    
    print("\n✅ Ingestão do livro de receitas concluída!")
    print(f"Total de receitas (páginas) salvas no banco: {collection.count()}")

if __name__ == "__main__":
    ingerir_livro()
    
"""
Sistema RAG Avançado usando LangChain para Chef RAG
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain_community.document_loaders import PyPDFLoader, JSONLoader, WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.retrievers import MultiQueryRetriever, BM25Retriever, EnsembleRetriever
from langchain_core.documents import Document
import os
import json
from pathlib import Path
from typing import List, Dict, Any

class AdvancedRAGSystem:
    """Sistema RAG avançado para Chef RAG usando LangChain"""
    
    def __init__(self, openai_api_key: str = None):
        """Inicializa o sistema RAG avançado"""
        self.openai_api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
        
        # Configurar diretórios
        self.data_dir = Path("data")
        self.vector_store_dir = self.data_dir / "chroma_advanced"
        
        # Inicializar componentes
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        self.memory = None
        
        self._setup_rag_system()
    
    def _setup_rag_system(self):
        """Configura o sistema RAG"""
        try:
            # Carregar ou criar vector store
            self._setup_vectorstore()
            
            # Configurar retrievers avançados
            self._setup_advanced_retriever()
            
            # Configurar memory
            self._setup_memory()
            
            # Criar chains
            self._setup_chains()
            
            print("✅ Sistema RAG avançado configurado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao configurar RAG: {e}")
    
    def _setup_vectorstore(self):
        """Configura o vector store"""
        try:
            # Tentar carregar vector store existente
            if self.vector_store_dir.exists():
                self.vectorstore = Chroma(
                    persist_directory=str(self.vector_store_dir),
                    embedding_function=self.embeddings
                )
                print("📚 Vector store existente carregado")
            else:
                # Criar novo vector store
                self._create_vectorstore()
                
        except Exception as e:
            print(f"❌ Erro no vector store: {e}")
            self._create_empty_vectorstore()
    
    def _create_vectorstore(self):
        """Cria um novo vector store com dados"""
        print("🔄 Criando novo vector store...")
        
        # Carregar documentos de diferentes fontes
        documents = []
        
        # 1. Carregar PDFs de receitas
        documents.extend(self._load_pdf_documents())
        
        # 2. Carregar dados JSON existentes
        documents.extend(self._load_json_documents())
        
        # 3. Criar documentos de receitas padrão
        documents.extend(self._create_default_recipes())
        
        if documents:
            # Dividir documentos em chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
            )
            
            splits = text_splitter.split_documents(documents)
            
            # Criar vector store
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=str(self.vector_store_dir)
            )
            
            self.vectorstore.persist()
            print(f"✅ Vector store criado com {len(splits)} chunks")
        else:
            self._create_empty_vectorstore()
    
    def _create_empty_vectorstore(self):
        """Cria um vector store vazio"""
        self.vectorstore = Chroma(
            persist_directory=str(self.vector_store_dir),
            embedding_function=self.embeddings
        )
        print("📝 Vector store vazio criado")
    
    def _load_pdf_documents(self) -> List[Document]:
        """Carrega documentos PDF"""
        documents = []
        pdf_dir = self.data_dir / "pdf"
        
        if pdf_dir.exists():
            for pdf_file in pdf_dir.glob("*.pdf"):
                try:
                    loader = PyPDFLoader(str(pdf_file))
                    docs = loader.load()
                    
                    # Adicionar metadados
                    for doc in docs:
                        doc.metadata.update({
                            "source": "pdf",
                            "filename": pdf_file.name,
                            "type": "recipe_book"
                        })
                    
                    documents.extend(docs)
                    print(f"📄 PDF carregado: {pdf_file.name}")
                    
                except Exception as e:
                    print(f"❌ Erro ao carregar {pdf_file.name}: {e}")
        
        return documents
    
    def _load_json_documents(self) -> List[Document]:
        """Carrega documentos JSON existentes"""
        documents = []
        
        # Carregar receitas do banco de dados existente
        try:
            from core_logic.database import get_all_recipes
            recipes = get_all_recipes()
            
            for recipe in recipes:
                content = f"""
                Título: {recipe.get('title', 'Sem título')}
                Ingredientes: {', '.join(recipe.get('ingredients', []))}
                Instruções: {recipe.get('instructions', 'Sem instruções')}
                Tempo de Preparo: {recipe.get('prep_time', 'Não especificado')}
                Dificuldade: {recipe.get('difficulty', 'Média')}
                Categoria: {recipe.get('category', 'Geral')}
                """
                
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": "database",
                        "recipe_id": recipe.get('id'),
                        "title": recipe.get('title'),
                        "category": recipe.get('category'),
                        "difficulty": recipe.get('difficulty')
                    }
                )
                documents.append(doc)
            
            print(f"🗃️ Receitas do banco carregadas: {len(documents)}")
            
        except Exception as e:
            print(f"❌ Erro ao carregar do banco: {e}")
        
        return documents
    
    def _create_default_recipes(self) -> List[Document]:
        """Cria receitas padrão para o sistema"""
        default_recipes = [
            {
                "title": "Omelete Simples",
                "ingredients": ["ovos", "sal", "azeite", "queijo"],
                "instructions": "Bata os ovos, tempere com sal, aqueça o azeite na frigideira, despeje os ovos, adicione queijo e dobre.",
                "prep_time": "10 minutos",
                "difficulty": "Fácil",
                "category": "Café da manhã"
            },
            {
                "title": "Salada de Tomate",
                "ingredients": ["tomate", "cebola", "azeite", "vinagre", "sal"],
                "instructions": "Corte os tomates e cebola, tempere com azeite, vinagre e sal.",
                "prep_time": "5 minutos",
                "difficulty": "Fácil",
                "category": "Salada"
            },
            {
                "title": "Frango Grelhado",
                "ingredients": ["frango", "alho", "limão", "sal", "pimenta"],
                "instructions": "Tempere o frango com alho, limão, sal e pimenta. Grelhe até dourar.",
                "prep_time": "30 minutos",
                "difficulty": "Médio",
                "category": "Prato principal"
            }
        ]
        
        documents = []
        for recipe in default_recipes:
            content = f"""
            Título: {recipe['title']}
            Ingredientes: {', '.join(recipe['ingredients'])}
            Instruções: {recipe['instructions']}
            Tempo de Preparo: {recipe['prep_time']}
            Dificuldade: {recipe['difficulty']}
            Categoria: {recipe['category']}
            """
            
            doc = Document(
                page_content=content,
                metadata={
                    "source": "default",
                    "title": recipe['title'],
                    "category": recipe['category'],
                    "difficulty": recipe['difficulty']
                }
            )
            documents.append(doc)
        
        print(f"📝 Receitas padrão criadas: {len(documents)}")
        return documents
    
    def _setup_advanced_retriever(self):
        """Configura retriever avançado com multiple query"""
        try:
            if self.vectorstore:
                # Retriever vetorial básico
                vector_retriever = self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 4}
                )
                
                # Multi-query retriever para diferentes perspectivas
                self.retriever = MultiQueryRetriever.from_llm(
                    retriever=vector_retriever,
                    llm=self.llm
                )
                
                print("🔍 Retriever avançado configurado")
            
        except Exception as e:
            print(f"❌ Erro no retriever: {e}")
            # Fallback para retriever simples
            if self.vectorstore:
                self.retriever = self.vectorstore.as_retriever()
    
    def _setup_memory(self):
        """Configura sistema de memória"""
        try:
            # Usar ConversationSummaryBufferMemory para eficiência
            self.memory = ConversationSummaryBufferMemory(
                llm=self.llm,
                memory_key="chat_history",
                return_messages=True,
                max_token_limit=1000
            )
            
            print("🧠 Memória configurada")
            
        except Exception as e:
            print(f"❌ Erro na memória: {e}")
            # Fallback para memória simples
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
    
    def _setup_chains(self):
        """Configura chains de processamento"""
        try:
            # Template personalizado para culinária
            template = """
            Você é um chef especialista em culinária brasileira e internacional.
            Use o contexto fornecido para responder sobre receitas, ingredientes e técnicas culinárias.
            
            Contexto: {context}
            Histórico da conversa: {chat_history}
            Pergunta: {question}
            
            Instruções:
            - Forneça receitas detalhadas com ingredientes e modo de preparo
            - Sugira substituições para ingredientes quando apropriado
            - Inclua dicas de preparo e apresentação
            - Considere restrições alimentares mencionadas
            - Se não souber algo, seja honesto
            
            Resposta detalhada:
            """
            
            prompt = PromptTemplate(
                template=template,
                input_variables=["context", "chat_history", "question"]
            )
            
            # Chain conversacional com retrieval
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.retriever,
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": prompt},
                return_source_documents=True,
                verbose=True
            )
            
            print("🔗 Chains configuradas")
            
        except Exception as e:
            print(f"❌ Erro nas chains: {e}")
    
    def query_recipes(self, question: str) -> Dict[str, Any]:
        """Faz query no sistema RAG"""
        try:
            if not self.qa_chain:
                return {"answer": "Sistema RAG não configurado", "sources": []}
            
            result = self.qa_chain({"question": question})
            
            return {
                "answer": result["answer"],
                "sources": [doc.metadata for doc in result.get("source_documents", [])]
            }
            
        except Exception as e:
            return {
                "answer": f"Erro na consulta: {str(e)}",
                "sources": []
            }
    
    def add_recipe_document(self, title: str, ingredients: List[str], 
                          instructions: str, metadata: Dict = None) -> bool:
        """Adiciona nova receita ao vector store"""
        try:
            content = f"""
            Título: {title}
            Ingredientes: {', '.join(ingredients)}
            Instruções: {instructions}
            """
            
            doc_metadata = {
                "source": "user_added",
                "title": title,
                "timestamp": str(pd.Timestamp.now())
            }
            
            if metadata:
                doc_metadata.update(metadata)
            
            doc = Document(page_content=content, metadata=doc_metadata)
            
            if self.vectorstore:
                self.vectorstore.add_documents([doc])
                self.vectorstore.persist()
                print(f"✅ Receita adicionada: {title}")
                return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar receita: {e}")
        
        return False
    
    def get_similar_recipes(self, ingredients: List[str], k: int = 3) -> List[Dict]:
        """Busca receitas similares baseadas em ingredientes"""
        try:
            query = f"receitas com {', '.join(ingredients)}"
            
            if self.vectorstore:
                docs = self.vectorstore.similarity_search(query, k=k)
                
                results = []
                for doc in docs:
                    results.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "similarity_score": doc.metadata.get("score", 0)
                    })
                
                return results
            
        except Exception as e:
            print(f"❌ Erro na busca de similares: {e}")
        
        return []

# Instância global
advanced_rag = None

def get_advanced_rag_system():
    """Retorna instância do sistema RAG avançado"""
    global advanced_rag
    if advanced_rag is None:
        from core_logic.config import OPENAI_API_KEY
        advanced_rag = AdvancedRAGSystem(openai_api_key=OPENAI_API_KEY)
    return advanced_rag

def query_with_langchain_rag(question: str) -> str:
    """Interface simplificada para consultas RAG"""
    rag_system = get_advanced_rag_system()
    result = rag_system.query_recipes(question)
    return result.get("answer", "Erro na consulta")
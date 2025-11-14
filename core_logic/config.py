import os
from dotenv import load_dotenv

load_dotenv()

# Configuração principal: OpenAI
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Verificar configuração
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

ACTIVE_PROVIDER = "openai"
print(f"🤖 Usando provedor de IA: {ACTIVE_PROVIDER.upper()}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FILE_PATH = os.path.join(BASE_DIR, "..", "data", "pdf", "livro.pdf")
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
MONITORED_FOLDER = os.path.join(BASE_DIR, "imagens_para_monitorar")
IMAGE_WATCH_FOLDER = os.path.join(BASE_DIR, "..", "data", "imagens")
CHROMA_COLLECTION_NAME = "receitas"

# Configurações OpenAI
EMBEDDING_MODEL = "text-embedding-3-small"
VISION_MODEL = "gpt-4o-mini"
MODEL_NAME = "gpt-4o-mini"
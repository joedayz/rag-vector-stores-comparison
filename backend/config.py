"""
Configuración unificada para el proyecto RAG
Soporta múltiples vector stores: FAISS, Pinecone, Weaviate
"""
import os
from dotenv import load_dotenv
from enum import Enum
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

class VectorStoreType(str, Enum):
    """Tipos de vector stores soportados"""
    FAISS = "faiss"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"

# Vector store seleccionado (por defecto FAISS)
VECTOR_STORE_TYPE = VectorStoreType(
    os.getenv("VECTOR_STORE_TYPE", "faiss").lower()
)

# Configuración común
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Configuración del servidor
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))

# Configuración específica por vector store
PINECONE_API_KEY = None
PINECONE_ENVIRONMENT = None
PINECONE_INDEX_NAME = None

WEAVIATE_URL = None
WEAVIATE_API_KEY = None
WEAVIATE_INDEX_NAME = None

FAISS_VECTORSTORE_PATH = Path("./vector_stores_data/faiss")

# Cargar configuración según el vector store seleccionado
if VECTOR_STORE_TYPE == VectorStoreType.PINECONE:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "afp-chatbot")
    
    if not PINECONE_API_KEY:
        raise ValueError(
            "PINECONE_API_KEY no está configurada. "
            "Configura tu API key en el archivo .env"
        )

elif VECTOR_STORE_TYPE == VectorStoreType.WEAVIATE:
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")
    WEAVIATE_INDEX_NAME = os.getenv("WEAVIATE_INDEX_NAME", "AFP_Chatbot")
    
    if not WEAVIATE_URL:
        raise ValueError(
            "WEAVIATE_URL no está configurada. "
            "Configura la URL de Weaviate en el archivo .env"
        )

# Validar que la API key de OpenAI esté configurada (opcional)
if not OPENAI_API_KEY:
    print("⚠️  Warning: OPENAI_API_KEY no está configurada. Algunas funcionalidades pueden no estar disponibles.")


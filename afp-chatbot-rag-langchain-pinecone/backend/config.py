import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de OpenAI (opcional, solo para fallback)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Configuración de Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "afp-chatbot")

# Configuración del servidor
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))

# Validar que la API key de Pinecone esté configurada
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY no está configurada. Por favor, configura tu API key de Pinecone en el archivo .env")

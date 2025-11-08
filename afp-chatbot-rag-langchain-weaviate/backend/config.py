import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de OpenAI (opcional, solo para fallback)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Configuración de Weaviate
# Para Weaviate Cloud: usar WEAVIATE_URL con formato https://cluster-id.weaviate.network
# Para Weaviate local: usar http://localhost:8080
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")  # Opcional para Weaviate Cloud
WEAVIATE_INDEX_NAME = os.getenv("WEAVIATE_INDEX_NAME", "AFP_Chatbot")

# Configuración del servidor
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))

# Validar que la URL de Weaviate esté configurada
if not WEAVIATE_URL:
    raise ValueError("WEAVIATE_URL no está configurada. Por favor, configura la URL de Weaviate en el archivo .env")

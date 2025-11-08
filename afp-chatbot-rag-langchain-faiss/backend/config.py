import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuración del servidor
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))

# Validar que la API key esté configurada
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está configurada. Por favor, configura tu API key en el archivo .env")

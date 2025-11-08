# main.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_weaviate import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import weaviate
from weaviate.classes.init import Auth
from openai import OpenAI
from pydantic import BaseModel
from config import OPENAI_API_KEY, WEAVIATE_URL, WEAVIATE_API_KEY, WEAVIATE_INDEX_NAME
import os

app = FastAPI(title="AI Chatbot")

# Configura CORS si vas a llamar desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Inicializa cliente de OpenAI (opcional, solo para fallback)
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

# Conecta a Weaviate
weaviate_client = None
vectordb = None
try:
    # Crear cliente de Weaviate
    if WEAVIATE_API_KEY:
        # Para Weaviate Cloud - la URL debe ser sin https://
        cluster_url = WEAVIATE_URL.replace("https://", "").replace("http://", "")
        weaviate_client = weaviate.connect_to_weaviate_cloud(
            cluster_url=cluster_url,
            auth_credentials=Auth.api_key(WEAVIATE_API_KEY)
        )
    else:
        # Para Weaviate local
        host = WEAVIATE_URL.replace("http://", "").replace("https://", "").split(":")[0]
        weaviate_client = weaviate.connect_to_local(host=host)
    
    if weaviate_client.is_ready():
        vectordb = WeaviateVectorStore(
            client=weaviate_client,
            index_name=WEAVIATE_INDEX_NAME,
            embedding=embeddings,
            text_key="text"
        )
        print(f"Conectado exitosamente a Weaviate (clase: {WEAVIATE_INDEX_NAME})")
    else:
        raise Exception("Weaviate no está listo")
except Exception as e:
    print(f"Warning: No se pudo conectar a Weaviate: {e}")
    if weaviate_client:
        weaviate_client.close()
    vectordb = None

# Modelo para las consultas AFP
class AFPQuery(BaseModel):
    question: str

@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servidor está funcionando."""
    return {"message": "Servidor AFP Chatbot Perú funcionando correctamente - Información local sobre el 4to retiro de AFP"}

@app.post("/afp-query")
async def afp_query(query: AFPQuery):
    """
    Endpoint para consultas sobre el cuarto retiro de AFP usando información local.
    """
    try:
        if vectordb is None:
            raise HTTPException(status_code=503, detail="Vectorstore no disponible. Verifica tu conexión a Weaviate y ejecuta primero el script ingest.py")
        
        # Buscar información relevante en Weaviate
        docs = vectordb.similarity_search(query.question, k=3)
        
        if not docs:
            return {
                "answer": "No se encontró información específica sobre tu consulta en nuestra base de datos local. Por favor, contacta directamente con tu AFP o la Superintendencia de Banca, Seguros y AFP (SBS).",
                "question": query.question,
                "source": "No se encontraron documentos relevantes"
            }
        
        # Combinar la información encontrada
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Crear una respuesta basada en el contexto local
        answer = f"""Basándome en la información oficial disponible sobre el 4to retiro de AFP en Perú:

{context}

Información adicional importante:
- El retiro es de hasta 4 UIT (S/ 21,400)
- El proceso inicia el 21 de octubre de 2025
- Las fechas dependen del último dígito de tu DNI
- Hay una ventana libre del 4 de diciembre 2025 al 18 de enero 2026

Para consultas específicas sobre tu caso particular, te recomiendo contactar directamente con tu AFP o visitar la página de la SBS: https://servicios.sbs.gob.pe/ReporteSituacionPrevisional"""
        
        return {
            "answer": answer,
            "question": query.question,
            "source": "Información local del archivo data1.txt"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {str(e)}")

@app.get("/search")
async def search(query: str = Query(..., description="Consulta a buscar")):
    """
    Busca los documentos más relevantes para la query usando Weaviate.
    """
    if vectordb is None:
        raise HTTPException(status_code=503, detail="Vectorstore no disponible. Verifica tu conexión a Weaviate")
    
    # Devuelve solo el top 1 documento
    docs = vectordb.similarity_search(query, k=1)
    
    # Extrae el contenido del documento
    results = [doc.page_content for doc in docs]
    
    return {"results": results}

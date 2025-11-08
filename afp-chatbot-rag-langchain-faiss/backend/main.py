# main.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path
from openai import OpenAI
from pydantic import BaseModel
from config import OPENAI_API_KEY
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

# Carpeta del vectorstore
VECTORSTORE_PATH = Path("./vector_store")

# Inicializa embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Inicializa cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Carga FAISS vectorstore (opcional, para búsquedas en documentos)
try:
    vectordb = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings=embeddings,
        allow_dangerous_deserialization=True  # seguro si el vectorstore es tuyo
    )
except Exception as e:
    print(f"Warning: No se pudo cargar el vectorstore: {e}")
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
            raise HTTPException(status_code=503, detail="Vectorstore no disponible. Ejecuta primero el script ingest.py")
        
        # Buscar información relevante en el vectorstore local
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
    Busca los documentos más relevantes para la query usando FAISS.
    """
    if vectordb is None:
        raise HTTPException(status_code=503, detail="Vectorstore no disponible")
    
    # Devuelve solo el top 1 documento
    docs = vectordb.similarity_search(query, k=1)
    
    # Extrae el contenido del documento
    results = [doc.page_content for doc in docs]
    
    return {"results": results}

"""
FastAPI application unificada para RAG con múltiples vector stores
Soporta FAISS, Pinecone y Weaviate
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import VECTOR_STORE_TYPE, OPENAI_API_KEY
from vector_stores import get_vector_store
from openai import OpenAI

app = FastAPI(title="AI Chatbot - RAG Comparison")

# Configura CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar vector store según configuración
try:
    vectordb = get_vector_store()
    print(f"✅ Vector store '{VECTOR_STORE_TYPE.value}' inicializado correctamente")
except Exception as e:
    print(f"❌ Error inicializando vector store: {e}")
    vectordb = None

# Inicializar cliente de OpenAI (opcional)
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

# Modelo para las consultas
class AFPQuery(BaseModel):
    question: str

@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servidor está funcionando"""
    return {
        "message": "Servidor AFP Chatbot Perú funcionando correctamente",
        "vector_store": VECTOR_STORE_TYPE.value,
        "status": "ok"
    }

@app.post("/afp-query")
async def afp_query(query: AFPQuery):
    """
    Endpoint para consultas sobre el cuarto retiro de AFP
    """
    try:
        if vectordb is None:
            raise HTTPException(
                status_code=503,
                detail=f"Vectorstore no disponible. Verifica tu configuración de {VECTOR_STORE_TYPE.value} y ejecuta primero 'python ingest.py'"
            )
        
        # Buscar información relevante en el vectorstore
        docs = vectordb.similarity_search(query.question, k=3)
        
        if not docs:
            return {
                "answer": "No se encontró información específica sobre tu consulta en nuestra base de datos. Por favor, contacta directamente con tu AFP o la Superintendencia de Banca, Seguros y AFP (SBS).",
                "question": query.question,
                "source": "No se encontraron documentos relevantes",
                "vector_store": VECTOR_STORE_TYPE.value
            }
        
        # Combinar la información encontrada
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Crear una respuesta basada en el contexto
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
            "source": f"Información del archivo data1.txt (Vector Store: {VECTOR_STORE_TYPE.value})",
            "vector_store": VECTOR_STORE_TYPE.value
        }
        
    except ValueError as e:
        # Errores de configuración o vectorstore no disponible
        raise HTTPException(
            status_code=503,
            detail=f"Error de configuración: {str(e)}. Verifica tu configuración de {VECTOR_STORE_TYPE.value} y ejecuta 'python ingest.py' primero."
        )
    except Exception as e:
        # Otros errores
        import traceback
        error_detail = f"Error al procesar la consulta: {str(e)}"
        print(f"❌ Error completo: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/search")
async def search(query: str = Query(..., description="Consulta a buscar")):
    """
    Busca los documentos más relevantes para la query
    """
    if vectordb is None:
        raise HTTPException(
            status_code=503,
            detail=f"Vectorstore no disponible. Verifica tu configuración de {VECTOR_STORE_TYPE.value}"
        )
    
    # Devuelve solo el top 1 documento
    docs = vectordb.similarity_search(query, k=1)
    
    # Extrae el contenido del documento
    results = [doc.page_content for doc in docs]
    
    return {
        "results": results,
        "vector_store": VECTOR_STORE_TYPE.value
    }

@app.get("/health")
async def health():
    """Endpoint de health check"""
    return {
        "status": "healthy" if vectordb is not None else "unhealthy",
        "vector_store": VECTOR_STORE_TYPE.value,
        "vector_store_available": vectordb.is_available() if vectordb else False
    }


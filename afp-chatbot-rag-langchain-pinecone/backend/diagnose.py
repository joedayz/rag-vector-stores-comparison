"""
Script de diagnóstico para verificar el vectorstore de Pinecone
Este script permite verificar que los datos se cargaron correctamente en Pinecone
y probar búsquedas en el índice.
"""
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME
import os

# Configurar la API key de Pinecone como variable de entorno para langchain-pinecone
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Inicializa embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Conecta a Pinecone
try:
    print("🔌 Conectando a Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Verificar que el índice existe
    index_names = [index.name for index in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in index_names:
        print(f"❌ ERROR: El índice '{PINECONE_INDEX_NAME}' no existe en Pinecone")
        print(f"   Ejecuta 'python ingest.py' para crear el índice y cargar los datos")
        exit(1)
    
    print(f"✅ Índice '{PINECONE_INDEX_NAME}' encontrado")
    
    # Obtener estadísticas del índice
    index = pc.Index(PINECONE_INDEX_NAME)
    stats = index.describe_index_stats()
    total_vectors = stats.get('total_vector_count', 0)
    dimension = stats.get('dimension', 'N/A')
    
    print(f"📊 Estadísticas del índice:")
    print(f"   Total de vectores: {total_vectors}")
    print(f"   Dimensiones: {dimension}\n")
    
    # Conecta al vectorstore de Pinecone
    vectordb = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )
    
    print("✅ Conectado exitosamente a Pinecone\n")
    
    # Prueba de búsqueda
    query = "¿cuando se pierde el fraccionamiento?"
    print(f"🔍 Realizando búsqueda: '{query}'\n")
    results = vectordb.similarity_search(query, k=5)
    
    print(f"📋 Resultados de búsqueda ({len(results)} encontrados):\n")
    for i, res in enumerate(results, 1):
        print(f"--- Resultado {i} ---")
        print(f"{res.page_content}\n")
    
    # Prueba adicional con otra consulta
    query2 = "¿Cuándo puedo retirar mi AFP si mi DNI termina en 5?"
    print(f"🔍 Realizando búsqueda adicional: '{query2}'\n")
    results2 = vectordb.similarity_search(query2, k=3)
    
    print(f"📋 Resultados de búsqueda ({len(results2)} encontrados):\n")
    for i, res in enumerate(results2, 1):
        print(f"--- Resultado {i} ---")
        print(f"{res.page_content}\n")
    
    print("✅ Diagnóstico completado exitosamente!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nPosibles causas:")
    print("  1. API key de Pinecone incorrecta")
    print("  2. El índice no existe (ejecuta 'python ingest.py')")
    print("  3. Problemas de conexión a internet")
    print("  4. La región/environment no es correcta")
    exit(1)

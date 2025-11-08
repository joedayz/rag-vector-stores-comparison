"""
Script de diagnóstico para verificar el vectorstore de Weaviate
Este script permite verificar que los datos se cargaron correctamente en Weaviate
y probar búsquedas en la clase.
"""
from langchain_weaviate import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import weaviate
from weaviate.classes.init import Auth
from config import WEAVIATE_URL, WEAVIATE_API_KEY, WEAVIATE_INDEX_NAME
import os

# Inicializa embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Conecta a Weaviate
try:
    print("🔌 Conectando a Weaviate...")
    
    # Conectar para verificar que la clase existe
    if WEAVIATE_API_KEY:
        # Para Weaviate Cloud - la URL debe ser sin https://
        cluster_url = WEAVIATE_URL.replace("https://", "").replace("http://", "")
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=cluster_url,
            auth_credentials=Auth.api_key(WEAVIATE_API_KEY)
        )
    else:
        # Para Weaviate local
        host = WEAVIATE_URL.replace("http://", "").replace("https://", "").split(":")[0]
        client = weaviate.connect_to_local(host=host)
    
    # Verificar conexión
    if not client.is_ready():
        print("❌ ERROR: Weaviate no está listo")
        client.close()
        exit(1)
    
    # Verificar que la clase existe
    collections = client.collections.list_all()
    collection_names = list(collections.keys()) if collections else []
    
    if WEAVIATE_INDEX_NAME not in collection_names:
        print(f"❌ ERROR: La clase '{WEAVIATE_INDEX_NAME}' no existe en Weaviate")
        print(f"   Ejecuta 'python ingest.py' para crear la clase y cargar los datos")
        client.close()
        exit(1)
    
    print(f"✅ Clase '{WEAVIATE_INDEX_NAME}' encontrada")
    
    # Obtener estadísticas de la clase
    collection = client.collections.get(WEAVIATE_INDEX_NAME)
    count_result = collection.query.fetch_objects(limit=1, return_metadata=weaviate.classes.query.MetadataQuery(count=True))
    count = count_result.total if hasattr(count_result, 'total') else 0
    
    print(f"📊 Estadísticas de la clase:")
    print(f"   Total de objetos: {count}\n")
    
    client.close()
    
    # Conecta al vectorstore de Weaviate usando langchain
    # Reusar el cliente que ya creamos
    if WEAVIATE_API_KEY:
        # Para Weaviate Cloud - la URL debe ser sin https://
        cluster_url = WEAVIATE_URL.replace("https://", "").replace("http://", "")
        langchain_client = weaviate.connect_to_weaviate_cloud(
            cluster_url=cluster_url,
            auth_credentials=Auth.api_key(WEAVIATE_API_KEY)
        )
    else:
        # Para Weaviate local
        host = WEAVIATE_URL.replace("http://", "").replace("https://", "").split(":")[0]
        langchain_client = weaviate.connect_to_local(host=host)
    
    vectordb = WeaviateVectorStore(
        client=langchain_client,
        index_name=WEAVIATE_INDEX_NAME,
        embedding=embeddings,
        text_key="text"
    )
    
    print("✅ Conectado exitosamente a Weaviate\n")
    
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
    print("  1. URL de Weaviate incorrecta")
    print("  2. La clase no existe (ejecuta 'python ingest.py')")
    print("  3. Problemas de conexión a internet")
    print("  4. Weaviate no está corriendo (si es local)")
    print("  5. API key incorrecta (si es Weaviate Cloud)")
    print("\nPara Weaviate local, asegúrate de que esté corriendo:")
    print("  docker run -d -p 8080:8080 semitechnologies/weaviate:latest")
    exit(1)

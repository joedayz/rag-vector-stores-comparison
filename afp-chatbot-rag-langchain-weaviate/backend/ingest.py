from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_weaviate import WeaviateVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import weaviate
from weaviate.classes.init import Auth
from config import WEAVIATE_URL, WEAVIATE_API_KEY, WEAVIATE_INDEX_NAME
import os

# Carpeta de documentos
docs_path = Path("./data")

# Cargar todos los documentos .txt
docs = []
for file in docs_path.glob("*.txt"):
    loader = TextLoader(str(file))
    docs.extend(loader.load())

# Dividir documentos en chunks para mejorar búsqueda
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(docs)

# Inicializar embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Conectar a Weaviate
print(f"Conectando a Weaviate en {WEAVIATE_URL}...")

try:
    # Crear cliente de Weaviate
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
    if client.is_ready():
        print("✅ Conexión exitosa a Weaviate")
    else:
        raise Exception("No se pudo conectar a Weaviate")
    
    # Crear vectorstore en Weaviate a partir de los documentos
    # Weaviate creará la clase automáticamente si no existe
    vectordb = WeaviateVectorStore.from_documents(
        documents=split_docs,
        embedding=embeddings,
        client=client,
        index_name=WEAVIATE_INDEX_NAME,
        text_key="text"
    )
    
    # Cerrar el cliente
    client.close()
    
except Exception as e:
    print(f"❌ Error al conectar a Weaviate: {e}")
    raise

print(f"✅ Vectorstore generado y guardado en Weaviate (clase: {WEAVIATE_INDEX_NAME})")
print(f"Total de documentos procesados: {len(split_docs)}")

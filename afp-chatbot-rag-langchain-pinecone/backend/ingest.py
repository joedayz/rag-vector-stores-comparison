from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME
import os

# Configurar la API key de Pinecone como variable de entorno para langchain-pinecone
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

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

# Inicializar Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Verificar si el índice existe, si no, crearlo
index_names = [index.name for index in pc.list_indexes()]
if PINECONE_INDEX_NAME not in index_names:
    print(f"Creando índice {PINECONE_INDEX_NAME} en Pinecone...")
    # Dimensiones del modelo all-MiniLM-L6-v2
    # Extraer la región correcta (remover el sufijo -aws si existe)
    region = PINECONE_ENVIRONMENT.replace("-aws", "").replace("-gcp", "")
    
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,  # Dimensiones del embedding model
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=region)
    )
    print(f"Índice {PINECONE_INDEX_NAME} creado exitosamente")
else:
    print(f"Usando índice existente {PINECONE_INDEX_NAME}")

# Crear vectorstore en Pinecone a partir de los documentos
# La API key se lee automáticamente de la variable de entorno PINECONE_API_KEY
vectordb = PineconeVectorStore.from_documents(
    documents=split_docs,
    embedding=embeddings,
    index_name=PINECONE_INDEX_NAME
)

print(f"Vectorstore generado y guardado en Pinecone (índice: {PINECONE_INDEX_NAME})")
print(f"Total de documentos procesados: {len(split_docs)}")

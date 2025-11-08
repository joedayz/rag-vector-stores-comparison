"""
Script unificado para ingerir documentos en el vector store configurado
Soporta FAISS, Pinecone y Weaviate
"""
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from config import VECTOR_STORE_TYPE, EMBEDDING_MODEL
from vector_stores import get_vector_store

def main():
    """Función principal para ingerir documentos"""
    print("="*60)
    print(f"🚀 Iniciando ingest con {VECTOR_STORE_TYPE.value.upper()}")
    print("="*60)
    
    # Carpeta de documentos
    docs_path = Path("./data")
    
    if not docs_path.exists():
        print(f"❌ Error: La carpeta {docs_path} no existe")
        return
    
    # Cargar todos los documentos .txt
    print("\n📄 Cargando documentos...")
    docs = []
    for file in docs_path.glob("*.txt"):
        print(f"   - Cargando {file.name}")
        loader = TextLoader(str(file))
        docs.extend(loader.load())
    
    if not docs:
        print(f"❌ No se encontraron archivos .txt en {docs_path}")
        return
    
    print(f"✅ {len(docs)} documento(s) cargado(s)")
    
    # Dividir documentos en chunks para mejorar búsqueda
    print("\n✂️  Dividiendo documentos en chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(docs)
    print(f"✅ {len(split_docs)} chunk(s) creado(s)")
    
    # Inicializar embeddings
    print(f"\n🔧 Inicializando embeddings ({EMBEDDING_MODEL})...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    print("✅ Embeddings inicializados")
    
    # Crear vectorstore según configuración
    print(f"\n📦 Creando vectorstore en {VECTOR_STORE_TYPE.value.upper()}...")
    try:
        vectordb = get_vector_store()
        vectordb.from_documents(split_docs, embeddings)
        print(f"\n✅ ¡Ingest completado exitosamente!")
        print(f"   Vector Store: {VECTOR_STORE_TYPE.value.upper()}")
        print(f"   Total de documentos procesados: {len(split_docs)}")
    except Exception as e:
        print(f"\n❌ Error durante el ingest: {e}")
        raise

if __name__ == "__main__":
    main()


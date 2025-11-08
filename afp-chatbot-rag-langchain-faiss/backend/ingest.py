from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Carpeta de documentos y vectorstore
docs_path = Path("./data")
vectorstore_path = Path("./vector_store")

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

# Crear vectorstore a partir de los documentos
vectordb = FAISS.from_documents(split_docs, embeddings)

# Guardar vectorstore localmente
vectordb.save_local(vectorstore_path)
print(f"Vectorstore generado y guardado en {vectorstore_path}")

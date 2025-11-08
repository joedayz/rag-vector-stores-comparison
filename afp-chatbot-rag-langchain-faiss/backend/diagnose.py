from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings  # usa la versión correcta

vectorstore_path = "./vector_store"

# Inicializa embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Carga el vectorstore con deserialización peligrosa permitida
vectordb = FAISS.load_local(
    vectorstore_path,
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)

# Imprime documentos
print(f"Documentos indexados: {len(vectordb.docstore._dict)}\n")
for i, doc_id in enumerate(vectordb.docstore._dict):
    print(f"Doc {i+1}: {vectordb.docstore._dict[doc_id].page_content}\n")

# Prueba de búsqueda
query = "¿cuando se pierde el fraccionamiento?"
results = vectordb.similarity_search(query, k=5)
print("Resultados de búsqueda:")
for i, res in enumerate(results):
    print(f"{i+1}: {res.page_content}\n")

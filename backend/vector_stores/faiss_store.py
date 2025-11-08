"""
Implementación de FAISS vector store
"""
from pathlib import Path
from typing import List
from langchain_community.vectorstores.faiss import FAISS
from langchain.schema import Document
from .base import VectorStoreBase
from config import FAISS_VECTORSTORE_PATH, EMBEDDING_MODEL
from langchain_huggingface import HuggingFaceEmbeddings

class FAISSVectorStore(VectorStoreBase):
    """Implementación de vector store usando FAISS (local)"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vectordb = None
        self._load()
    
    def _load(self):
        """Carga el vectorstore desde disco"""
        try:
            if FAISS_VECTORSTORE_PATH.exists():
                self.vectordb = FAISS.load_local(
                    str(FAISS_VECTORSTORE_PATH),
                    embeddings=self.embeddings,
                    allow_dangerous_deserialization=True
                )
            else:
                print(f"⚠️  Vectorstore no encontrado en {FAISS_VECTORSTORE_PATH}")
                print("   Ejecuta 'python ingest.py' para crear el vectorstore")
        except Exception as e:
            print(f"⚠️  Error cargando vectorstore FAISS: {e}")
            self.vectordb = None
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Busca documentos similares"""
        if self.vectordb is None:
            raise ValueError("Vectorstore no disponible. Ejecuta 'python ingest.py' primero.")
        return self.vectordb.similarity_search(query, k=k)
    
    def from_documents(self, documents: List[Document], embeddings=None) -> None:
        """Crea el vectorstore a partir de documentos"""
        if embeddings is None:
            embeddings = self.embeddings
        
        # Crear directorio si no existe
        FAISS_VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
        
        # Crear vectorstore
        self.vectordb = FAISS.from_documents(documents, embeddings)
        
        # Guardar localmente
        self.vectordb.save_local(str(FAISS_VECTORSTORE_PATH))
        print(f"✅ Vectorstore FAISS guardado en {FAISS_VECTORSTORE_PATH}")
    
    def is_available(self) -> bool:
        """Verifica si el vectorstore está disponible"""
        return self.vectordb is not None


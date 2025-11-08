"""
Implementación de Pinecone vector store
"""
import os
from typing import List
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from .base import VectorStoreBase
from config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    EMBEDDING_MODEL
)
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

class PineconeVectorStore(VectorStoreBase):
    """Implementación de vector store usando Pinecone (cloud)"""
    
    def __init__(self):
        # Configurar API key como variable de entorno
        os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
        
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vectordb = None
        self._connect()
    
    def _connect(self):
        """Conecta a Pinecone"""
        try:
            self.vectordb = PineconeVectorStore(
                index_name=PINECONE_INDEX_NAME,
                embedding=self.embeddings
            )
            print(f"✅ Conectado a Pinecone (índice: {PINECONE_INDEX_NAME})")
        except Exception as e:
            print(f"⚠️  Error conectando a Pinecone: {e}")
            self.vectordb = None
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Busca documentos similares"""
        if self.vectordb is None:
            raise ValueError("No se pudo conectar a Pinecone. Verifica tu configuración.")
        return self.vectordb.similarity_search(query, k=k)
    
    def from_documents(self, documents: List[Document], embeddings=None) -> None:
        """Crea el vectorstore a partir de documentos"""
        if embeddings is None:
            embeddings = self.embeddings
        
        # Verificar si el índice existe, si no, crearlo
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index_names = [index.name for index in pc.list_indexes()]
        
        if PINECONE_INDEX_NAME not in index_names:
            print(f"📦 Creando índice {PINECONE_INDEX_NAME} en Pinecone...")
            # Dimensiones del modelo all-MiniLM-L6-v2
            region = os.getenv("PINECONE_ENVIRONMENT", "us-east-1").replace("-aws", "").replace("-gcp", "")
            
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=384,  # Dimensiones del embedding model
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=region)
            )
            print(f"✅ Índice {PINECONE_INDEX_NAME} creado exitosamente")
        else:
            print(f"✅ Usando índice existente {PINECONE_INDEX_NAME}")
        
        # Crear vectorstore en Pinecone
        self.vectordb = PineconeVectorStore.from_documents(
            documents=documents,
            embedding=embeddings,
            index_name=PINECONE_INDEX_NAME
        )
        print(f"✅ Vectorstore Pinecone creado (índice: {PINECONE_INDEX_NAME})")
    
    def is_available(self) -> bool:
        """Verifica si el vectorstore está disponible"""
        return self.vectordb is not None


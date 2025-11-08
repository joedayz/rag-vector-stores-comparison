"""
Implementación de Weaviate vector store
"""
from typing import List
from langchain_weaviate import WeaviateVectorStore as LangChainWeaviateVectorStore
from langchain_core.documents import Document
from .base import VectorStoreBase
from config import (
    WEAVIATE_URL,
    WEAVIATE_API_KEY,
    WEAVIATE_INDEX_NAME,
    EMBEDDING_MODEL
)
from langchain_huggingface import HuggingFaceEmbeddings
import weaviate
from weaviate.classes.init import Auth

class WeaviateVectorStore(VectorStoreBase):
    """Implementación de vector store usando Weaviate (cloud o local)"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vectordb = None
        self.client = None
        self._connect()
    
    def _connect(self):
        """Conecta a Weaviate"""
        try:
            # Crear cliente de Weaviate
            if WEAVIATE_API_KEY:
                # Para Weaviate Cloud
                cluster_url = WEAVIATE_URL.replace("https://", "").replace("http://", "")
                self.client = weaviate.connect_to_weaviate_cloud(
                    cluster_url=cluster_url,
                    auth_credentials=Auth.api_key(WEAVIATE_API_KEY)
                )
            else:
                # Para Weaviate local
                host = WEAVIATE_URL.replace("http://", "").replace("https://", "").split(":")[0]
                self.client = weaviate.connect_to_local(host=host)
            
            if self.client.is_ready():
                self.vectordb = LangChainWeaviateVectorStore(
                    client=self.client,
                    index_name=WEAVIATE_INDEX_NAME,
                    embedding=self.embeddings,
                    text_key="text"
                )
                print(f"✅ Conectado a Weaviate (clase: {WEAVIATE_INDEX_NAME})")
            else:
                raise Exception("Weaviate no está listo")
        except Exception as e:
            print(f"⚠️  Error conectando a Weaviate: {e}")
            self.vectordb = None
            if self.client:
                self.client.close()
                self.client = None
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Busca documentos similares"""
        if self.vectordb is None:
            raise ValueError("No se pudo conectar a Weaviate. Verifica tu configuración.")
        return self.vectordb.similarity_search(query, k=k)
    
    def from_documents(self, documents: List[Document], embeddings=None) -> None:
        """Crea el vectorstore a partir de documentos"""
        if embeddings is None:
            embeddings = self.embeddings
        
        # Asegurar que el cliente esté conectado
        if self.client is None or not self.client.is_ready():
            self._connect()
        
        if self.vectordb is None:
            raise ValueError("No se pudo conectar a Weaviate")
        
        # Crear vectorstore en Weaviate
        self.vectordb = LangChainWeaviateVectorStore.from_documents(
            documents=documents,
            embedding=embeddings,
            client=self.client,
            index_name=WEAVIATE_INDEX_NAME,
            text_key="text"
        )
        print(f"✅ Vectorstore Weaviate creado (clase: {WEAVIATE_INDEX_NAME})")
    
    def is_available(self) -> bool:
        """Verifica si el vectorstore está disponible"""
        return self.vectordb is not None and self.client is not None and self.client.is_ready()
    
    def __del__(self):
        """Cierra la conexión al destruir el objeto"""
        if self.client:
            self.client.close()


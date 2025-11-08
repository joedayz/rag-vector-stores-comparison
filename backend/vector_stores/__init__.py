"""
Módulo de vector stores
Factory pattern para crear instancias de vector stores según configuración
"""
from .base import VectorStoreBase
from .faiss_store import FAISSVectorStore
from .pinecone_store import PineconeVectorStore
from .weaviate_store import WeaviateVectorStore
from config import VECTOR_STORE_TYPE, VectorStoreType

def get_vector_store():
    """
    Factory function para obtener el vector store configurado
    
    Returns:
        VectorStoreBase: Instancia del vector store configurado
        
    Raises:
        ValueError: Si el tipo de vector store no es soportado
    """
    if VECTOR_STORE_TYPE == VectorStoreType.FAISS:
        return FAISSVectorStore()
    elif VECTOR_STORE_TYPE == VectorStoreType.PINECONE:
        return PineconeVectorStore()
    elif VECTOR_STORE_TYPE == VectorStoreType.WEAVIATE:
        return WeaviateVectorStore()
    else:
        raise ValueError(f"Vector store type '{VECTOR_STORE_TYPE}' no soportado")

__all__ = [
    "VectorStoreBase",
    "FAISSVectorStore",
    "PineconeVectorStore",
    "WeaviateVectorStore",
    "get_vector_store",
]


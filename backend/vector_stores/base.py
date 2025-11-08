"""
Clase base abstracta para vector stores
Define la interfaz común que todos los vector stores deben implementar
"""
from abc import ABC, abstractmethod
from typing import List, Any
from langchain.schema import Document

class VectorStoreBase(ABC):
    """Clase base abstracta para vector stores"""
    
    @abstractmethod
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """
        Busca documentos similares a la query
        
        Args:
            query: Texto de búsqueda
            k: Número de resultados a retornar
            
        Returns:
            Lista de documentos similares
        """
        pass
    
    @abstractmethod
    def from_documents(self, documents: List[Document], embeddings) -> None:
        """
        Crea el vector store a partir de documentos
        
        Args:
            documents: Lista de documentos a indexar
            embeddings: Modelo de embeddings a usar
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica si el vector store está disponible
        
        Returns:
            True si está disponible, False en caso contrario
        """
        pass


"""
Script simple para probar FAISS
"""
import sys
from pathlib import Path

# Agregar el backend al path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from vector_stores import get_vector_store
from config import VECTOR_STORE_TYPE

def test_faiss():
    """Prueba FAISS"""
    print("="*60)
    print("🧪 Probando FAISS")
    print("="*60)
    
    # Verificar que esté configurado como FAISS
    if VECTOR_STORE_TYPE.value != "faiss":
        print(f"❌ Error: VECTOR_STORE_TYPE está configurado como '{VECTOR_STORE_TYPE.value}'")
        print("   Cambia VECTOR_STORE_TYPE=faiss en backend/.env")
        return False
    
    try:
        # Obtener vector store
        print("\n📦 Cargando vector store FAISS...")
        vectordb = get_vector_store()
        
        if not vectordb.is_available():
            print("❌ Error: Vectorstore no disponible")
            print("   Ejecuta 'python ingest.py' primero en backend/")
            return False
        
        print("✅ Vectorstore cargado correctamente")
        
        # Probar búsqueda
        print("\n🔍 Probando búsqueda...")
        test_query = "¿Cuándo inicia el cuarto retiro de AFP?"
        print(f"   Query: '{test_query}'")
        
        docs = vectordb.similarity_search(test_query, k=3)
        
        print(f"✅ Búsqueda exitosa: {len(docs)} resultados encontrados")
        
        if docs:
            print("\n📄 Primer resultado:")
            print(f"   {docs[0].page_content[:200]}...")
        
        print("\n✅ FAISS funciona correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_faiss()


"""
Script simple para probar Weaviate
"""
import sys
from pathlib import Path

# Agregar el backend al path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from vector_stores import get_vector_store
from config import VECTOR_STORE_TYPE

def test_weaviate():
    """Prueba Weaviate"""
    print("="*60)
    print("🧪 Probando Weaviate")
    print("="*60)
    
    # Verificar que esté configurado como Weaviate
    if VECTOR_STORE_TYPE.value != "weaviate":
        print(f"❌ Error: VECTOR_STORE_TYPE está configurado como '{VECTOR_STORE_TYPE.value}'")
        print("   Cambia VECTOR_STORE_TYPE=weaviate en backend/.env")
        return False
    
    try:
        # Obtener vector store
        print("\n📦 Conectando a Weaviate...")
        vectordb = get_vector_store()
        
        if not vectordb.is_available():
            print("❌ Error: No se pudo conectar a Weaviate")
            print("   Verifica tu WEAVIATE_URL en backend/.env")
            print("   Para local: Asegúrate de que Docker esté corriendo")
            print("   Ejecuta 'python ingest.py' primero si no has ingerido datos")
            return False
        
        print("✅ Conectado a Weaviate correctamente")
        
        # Probar búsqueda
        print("\n🔍 Probando búsqueda...")
        test_query = "¿Cómo sé cuándo me toca retirar según mi DNI?"
        print(f"   Query: '{test_query}'")
        
        docs = vectordb.similarity_search(test_query, k=3)
        
        print(f"✅ Búsqueda exitosa: {len(docs)} resultados encontrados")
        
        if docs:
            print("\n📄 Primer resultado:")
            print(f"   {docs[0].page_content[:200]}...")
        
        print("\n✅ Weaviate funciona correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_weaviate()


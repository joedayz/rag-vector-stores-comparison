"""
Script simple para probar Pinecone
"""
import sys
from pathlib import Path

# Agregar el backend al path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from vector_stores import get_vector_store
from config import VECTOR_STORE_TYPE

def test_pinecone():
    """Prueba Pinecone"""
    print("="*60)
    print("🧪 Probando Pinecone")
    print("="*60)
    
    # Verificar que esté configurado como Pinecone
    if VECTOR_STORE_TYPE.value != "pinecone":
        print(f"❌ Error: VECTOR_STORE_TYPE está configurado como '{VECTOR_STORE_TYPE.value}'")
        print("   Cambia VECTOR_STORE_TYPE=pinecone en backend/.env")
        return False
    
    try:
        # Obtener vector store
        print("\n📦 Conectando a Pinecone...")
        vectordb = get_vector_store()
        
        if not vectordb.is_available():
            print("❌ Error: No se pudo conectar a Pinecone")
            print("   Verifica tu PINECONE_API_KEY en backend/.env")
            print("   Ejecuta 'python ingest.py' primero si no has ingerido datos")
            return False
        
        print("✅ Conectado a Pinecone correctamente")
        
        # Probar búsqueda
        print("\n🔍 Probando búsqueda...")
        test_query = "¿Cuánto es el monto máximo que puedo retirar?"
        print(f"   Query: '{test_query}'")
        
        docs = vectordb.similarity_search(test_query, k=3)
        
        print(f"✅ Búsqueda exitosa: {len(docs)} resultados encontrados")
        
        if docs:
            print("\n📄 Primer resultado:")
            print(f"   {docs[0].page_content[:200]}...")
        
        print("\n✅ Pinecone funciona correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_pinecone()


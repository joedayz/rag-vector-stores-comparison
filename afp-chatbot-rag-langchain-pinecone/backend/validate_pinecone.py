"""
Script de validación para verificar la configuración de Pinecone
Ejecuta este script antes de usar la aplicación para asegurarte de que todo está configurado correctamente.
"""
import os
import sys

# Verificar dependencias antes de continuar
try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ ERROR: El módulo 'python-dotenv' no está instalado")
    print("   Por favor, instala las dependencias:")
    print("   pip install python-dotenv pinecone-client")
    print("\n   O si estás usando el entorno virtual:")
    print("   source venv/bin/activate")
    print("   pip install python-dotenv pinecone-client")
    sys.exit(1)

try:
    from pinecone import Pinecone
except ImportError:
    print("❌ ERROR: El módulo 'pinecone-client' no está instalado")
    print("   Por favor, instala las dependencias:")
    print("   pip install pinecone-client")
    print("\n   O si estás usando el entorno virtual:")
    print("   source venv/bin/activate")
    print("   pip install pinecone-client")
    sys.exit(1)

try:
    from config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME
except ImportError as e:
    print(f"❌ ERROR: No se pudo importar config: {e}")
    print("   Asegúrate de estar ejecutando el script desde el directorio backend/")
    sys.exit(1)

def validate_pinecone():
    """Valida la configuración de Pinecone"""
    print("🔍 Validando configuración de Pinecone...\n")
    
    # Verificar que la API key esté configurada
    if not PINECONE_API_KEY:
        print("❌ ERROR: PINECONE_API_KEY no está configurada en el archivo .env")
        print("   Por favor, agrega tu API key de Pinecone al archivo .env")
        return False
    
    print(f"✅ PINECONE_API_KEY configurada")
    print(f"✅ PINECONE_ENVIRONMENT: {PINECONE_ENVIRONMENT}")
    print(f"✅ PINECONE_INDEX_NAME: {PINECONE_INDEX_NAME}\n")
    
    # Intentar conectar a Pinecone
    try:
        print("🔌 Conectando a Pinecone...")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        print("✅ Conexión exitosa a Pinecone\n")
        
        # Listar índices
        print("📋 Verificando índices...")
        indexes = pc.list_indexes()
        index_names = [index.name for index in indexes]
        
        print(f"   Índices encontrados: {index_names if index_names else 'Ninguno'}\n")
        
        # Verificar si el índice existe
        if PINECONE_INDEX_NAME in index_names:
            print(f"✅ El índice '{PINECONE_INDEX_NAME}' existe")
            
            # Obtener información del índice
            index = pc.Index(PINECONE_INDEX_NAME)
            stats = index.describe_index_stats()
            print(f"   Total de vectores: {stats.get('total_vector_count', 0)}")
            print(f"   Dimensiones: {stats.get('dimension', 'N/A')}")
            
            return True
        else:
            print(f"⚠️  El índice '{PINECONE_INDEX_NAME}' no existe")
            print(f"   Ejecuta 'python ingest.py' para crear el índice y cargar los datos")
            return False
            
    except Exception as e:
        print(f"❌ ERROR al conectar a Pinecone: {e}")
        print("\nPosibles causas:")
        print("  1. API key incorrecta")
        print("  2. Problemas de conexión a internet")
        print("  3. La región/environment no es correcta")
        return False

if __name__ == "__main__":
    success = validate_pinecone()
    
    if success:
        print("\n✅ Validación completada exitosamente!")
        print("   Puedes ejecutar 'python ingest.py' para cargar datos o 'uvicorn main:app --reload' para iniciar el servidor")
    else:
        print("\n❌ Validación fallida. Por favor, corrige los errores antes de continuar.")
        exit(1)


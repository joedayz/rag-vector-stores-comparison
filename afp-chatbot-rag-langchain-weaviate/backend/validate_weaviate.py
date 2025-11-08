"""
Script de validación para verificar la configuración de Weaviate
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
    print("   pip install python-dotenv weaviate-client")
    print("\n   O si estás usando el entorno virtual:")
    print("   source venv/bin/activate")
    print("   pip install python-dotenv weaviate-client")
    sys.exit(1)

try:
    import weaviate
    from weaviate.classes.init import Auth
except ImportError:
    print("❌ ERROR: El módulo 'weaviate-client' no está instalado")
    print("   Por favor, instala las dependencias:")
    print("   pip install weaviate-client")
    print("\n   O si estás usando el entorno virtual:")
    print("   source venv/bin/activate")
    print("   pip install weaviate-client")
    sys.exit(1)

try:
    from config import WEAVIATE_URL, WEAVIATE_API_KEY, WEAVIATE_INDEX_NAME
except ImportError as e:
    print(f"❌ ERROR: No se pudo importar config: {e}")
    print("   Asegúrate de estar ejecutando el script desde el directorio backend/")
    sys.exit(1)

def validate_weaviate():
    """Valida la configuración de Weaviate"""
    print("🔍 Validando configuración de Weaviate...\n")
    
    # Verificar que la URL esté configurada
    if not WEAVIATE_URL:
        print("❌ ERROR: WEAVIATE_URL no está configurada en el archivo .env")
        print("   Por favor, agrega la URL de Weaviate al archivo .env")
        print("   Para Weaviate local: WEAVIATE_URL=http://localhost:8080")
        print("   Para Weaviate Cloud: WEAVIATE_URL=https://cluster-id.weaviate.network")
        return False
    
    print(f"✅ WEAVIATE_URL configurada: {WEAVIATE_URL}")
    if WEAVIATE_API_KEY:
        print(f"✅ WEAVIATE_API_KEY configurada (para Weaviate Cloud)")
    else:
        print(f"ℹ️  WEAVIATE_API_KEY no configurada (usando Weaviate local)")
    print(f"✅ WEAVIATE_INDEX_NAME: {WEAVIATE_INDEX_NAME}\n")
    
    # Intentar conectar a Weaviate
    try:
        print("🔌 Conectando a Weaviate...")
        if WEAVIATE_API_KEY:
            # Para Weaviate Cloud - usar connect_to_weaviate_cloud
            # La URL debe ser sin https:// (el cliente lo agrega automáticamente)
            cluster_url = WEAVIATE_URL.replace("https://", "").replace("http://", "")
            client = weaviate.connect_to_weaviate_cloud(
                cluster_url=cluster_url,
                auth_credentials=Auth.api_key(WEAVIATE_API_KEY)
            )
        else:
            # Para Weaviate local
            host = WEAVIATE_URL.replace("http://", "").replace("https://", "").split(":")[0]
            client = weaviate.connect_to_local(host=host)
        
        # Verificar que Weaviate esté listo
        if client.is_ready():
            print("✅ Conexión exitosa a Weaviate\n")
        else:
            print("❌ ERROR: Weaviate no está listo")
            client.close()
            return False
        
        # Obtener esquema
        print("📋 Verificando clases (índices)...")
        collections = client.collections.list_all()
        collection_names = list(collections.keys()) if collections else []
        
        print(f"   Clases encontradas: {collection_names if collection_names else 'Ninguna'}\n")
        
        # Verificar si la clase existe
        if WEAVIATE_INDEX_NAME in collection_names:
            print(f"✅ La clase '{WEAVIATE_INDEX_NAME}' existe")
            
            # Contar objetos en la clase
            try:
                collection = client.collections.get(WEAVIATE_INDEX_NAME)
                # Usar aggregate para contar objetos
                result = collection.aggregate.over_all(total_count=True).do()
                total_count = result.total_count if hasattr(result, 'total_count') else 0
                print(f"   Total de objetos: {total_count}")
            except Exception as e:
                print(f"   (No se pudo obtener el conteo de objetos: {e})")
            
            client.close()
            return True
        else:
            print(f"⚠️  La clase '{WEAVIATE_INDEX_NAME}' no existe")
            print(f"   Ejecuta 'python ingest.py' para crear la clase y cargar los datos")
            client.close()
            return False
            
    except Exception as e:
        print(f"❌ ERROR al conectar a Weaviate: {e}")
        print("\nPosibles causas:")
        print("  1. URL incorrecta")
        print("  2. Weaviate no está corriendo (si es local)")
        print("  3. API key incorrecta (si es Weaviate Cloud)")
        print("  4. Problemas de conexión a internet")
        print("\nPara Weaviate local, asegúrate de que esté corriendo:")
        print("  docker run -d -p 8080:8080 semitechnologies/weaviate:latest")
        return False

if __name__ == "__main__":
    success = validate_weaviate()
    
    if success:
        print("\n✅ Validación completada exitosamente!")
        print("   Puedes ejecutar 'python ingest.py' para cargar datos o 'uvicorn main:app --reload' para iniciar el servidor")
    else:
        print("\n❌ Validación fallida. Por favor, corrige los errores antes de continuar.")
        exit(1)


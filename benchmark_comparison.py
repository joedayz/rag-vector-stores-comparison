"""
Script de comparativa entre FAISS, Pinecone y Weaviate
Mide rendimiento, características y genera un reporte comparativo
"""

import time
import sys
from pathlib import Path
from typing import List, Dict, Any
import statistics
import os

# Agregar los paths de los backends al sys.path para importar config
sys.path.insert(0, str(Path(__file__).parent / "afp-chatbot-rag-langchain-faiss" / "backend"))
sys.path.insert(0, str(Path(__file__).parent / "afp-chatbot-rag-langchain-pinecone" / "backend"))
sys.path.insert(0, str(Path(__file__).parent / "afp-chatbot-rag-langchain-weaviate" / "backend"))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_pinecone import PineconeVectorStore
from langchain_weaviate import WeaviateVectorStore
import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Queries de prueba
TEST_QUERIES = [
    "¿Cuándo inicia el cuarto retiro de AFP?",
    "¿Cuánto es el monto máximo que puedo retirar?",
    "¿Cómo sé cuándo me toca retirar según mi DNI?",
    "¿Qué es una UIT y cuánto vale?",
    "¿Puedo retirar en cualquier momento?",
]

class VectorStoreBenchmark:
    def __init__(self, name: str, vectordb, embeddings):
        self.name = name
        self.vectordb = vectordb
        self.embeddings = embeddings
        self.results = []
    
    def search(self, query: str, k: int = 3) -> List[Any]:
        """Realiza una búsqueda y retorna los resultados"""
        return self.vectordb.similarity_search(query, k=k)
    
    def benchmark_search(self, query: str, k: int = 3, iterations: int = 5) -> Dict[str, Any]:
        """Ejecuta múltiples búsquedas y mide el tiempo promedio"""
        times = []
        results_count = []
        
        for _ in range(iterations):
            start = time.time()
            docs = self.search(query, k)
            elapsed = time.time() - start
            times.append(elapsed)
            results_count.append(len(docs))
        
        return {
            "query": query,
            "avg_time": statistics.mean(times),
            "min_time": min(times),
            "max_time": max(times),
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
            "results_count": statistics.mean(results_count),
            "times": times
        }
    
    def run_benchmark(self, queries: List[str], iterations: int = 5) -> List[Dict[str, Any]]:
        """Ejecuta el benchmark completo"""
        print(f"\n{'='*60}")
        print(f"Ejecutando benchmark para: {self.name}")
        print(f"{'='*60}")
        
        results = []
        for i, query in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}] Probando query: '{query}'")
            result = self.benchmark_search(query, iterations=iterations)
            results.append(result)
            print(f"  ⏱️  Tiempo promedio: {result['avg_time']*1000:.2f}ms")
            print(f"  📊 Resultados encontrados: {result['results_count']:.0f}")
        
        self.results = results
        return results

def setup_faiss():
    """Configura FAISS (local)"""
    print("\n🔧 Configurando FAISS...")
    try:
        # Cargar .env del backend de FAISS si existe
        faiss_backend_path = Path(__file__).parent / "afp-chatbot-rag-langchain-faiss" / "backend"
        faiss_env_path = faiss_backend_path / ".env"
        if faiss_env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(faiss_env_path)
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore_path = faiss_backend_path / "vector_store"
        
        if not vectorstore_path.exists():
            raise Exception(f"Vectorstore no encontrado en {vectorstore_path}. Ejecuta primero ingest.py en afp-chatbot-rag-langchain-faiss/backend/")
        
        vectordb = FAISS.load_local(
            str(vectorstore_path),
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        print("✅ FAISS configurado correctamente")
        return vectordb, embeddings
    except Exception as e:
        print(f"❌ Error configurando FAISS: {e}")
        return None, None

def setup_pinecone():
    """Configura Pinecone (cloud)"""
    print("\n🔧 Configurando Pinecone...")
    try:
        # Cargar .env del backend de Pinecone si existe
        pinecone_backend_path = Path(__file__).parent / "afp-chatbot-rag-langchain-pinecone" / "backend"
        pinecone_env_path = pinecone_backend_path / ".env"
        if pinecone_env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(pinecone_env_path)
        
        # Intentar cargar config desde el backend de Pinecone
        try:
            from config import PINECONE_API_KEY, PINECONE_INDEX_NAME
            pinecone_api_key = PINECONE_API_KEY
            pinecone_index_name = PINECONE_INDEX_NAME
        except ImportError:
            # Si no se puede importar, usar variables de entorno directamente
            pinecone_api_key = os.getenv("PINECONE_API_KEY")
            pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "afp-chatbot")
        
        if not pinecone_api_key:
            raise Exception("PINECONE_API_KEY no configurada. Configura .env en afp-chatbot-rag-langchain-pinecone/backend/")
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        os.environ["PINECONE_API_KEY"] = pinecone_api_key
        
        vectordb = PineconeVectorStore(
            index_name=pinecone_index_name,
            embedding=embeddings
        )
        print("✅ Pinecone configurado correctamente")
        return vectordb, embeddings
    except Exception as e:
        print(f"❌ Error configurando Pinecone: {e}")
        return None, None

def setup_weaviate():
    """Configura Weaviate (cloud o local)"""
    print("\n🔧 Configurando Weaviate...")
    try:
        # Cargar .env del backend de Weaviate si existe
        weaviate_backend_path = Path(__file__).parent / "afp-chatbot-rag-langchain-weaviate" / "backend"
        weaviate_env_path = weaviate_backend_path / ".env"
        if weaviate_env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(weaviate_env_path)
        
        # Intentar cargar config desde el backend de Weaviate
        try:
            from config import WEAVIATE_URL, WEAVIATE_API_KEY, WEAVIATE_INDEX_NAME
            weaviate_url = WEAVIATE_URL
            weaviate_api_key = WEAVIATE_API_KEY or ""
            weaviate_index_name = WEAVIATE_INDEX_NAME
        except ImportError:
            # Si no se puede importar, usar variables de entorno directamente
            weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
            weaviate_api_key = os.getenv("WEAVIATE_API_KEY", "")
            weaviate_index_name = os.getenv("WEAVIATE_INDEX_NAME", "AFP_Chatbot")
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        if weaviate_api_key:
            cluster_url = weaviate_url.replace("https://", "").replace("http://", "")
            client = weaviate.connect_to_weaviate_cloud(
                cluster_url=cluster_url,
                auth_credentials=Auth.api_key(weaviate_api_key)
            )
        else:
            host = weaviate_url.replace("http://", "").replace("https://", "").split(":")[0]
            client = weaviate.connect_to_local(host=host)
        
        if not client.is_ready():
            raise Exception("Weaviate no está listo")
        
        vectordb = WeaviateVectorStore(
            client=client,
            index_name=weaviate_index_name,
            embedding=embeddings,
            text_key="text"
        )
        print("✅ Weaviate configurado correctamente")
        return vectordb, embeddings, client
    except Exception as e:
        print(f"❌ Error configurando Weaviate: {e}")
        return None, None, None

def generate_comparison_report(benchmarks: List[VectorStoreBenchmark]):
    """Genera un reporte comparativo"""
    print("\n" + "="*80)
    print("REPORTE COMPARATIVO: FAISS vs PINECONE vs WEAVIATE")
    print("="*80)
    
    # Métricas de rendimiento
    print("\n📊 MÉTRICAS DE RENDIMIENTO")
    print("-" * 80)
    print(f"{'Sistema':<15} {'Tiempo Promedio':<20} {'Tiempo Mín':<15} {'Tiempo Máx':<15} {'Desv. Est.':<15}")
    print("-" * 80)
    
    for bench in benchmarks:
        if not bench.results:
            continue
        
        avg_times = [r['avg_time'] for r in bench.results]
        min_times = [r['min_time'] for r in bench.results]
        max_times = [r['max_time'] for r in bench.results]
        std_devs = [r['std_dev'] for r in bench.results]
        
        overall_avg = statistics.mean(avg_times) * 1000
        overall_min = min([r['min_time'] for r in bench.results]) * 1000
        overall_max = max([r['max_time'] for r in bench.results]) * 1000
        overall_std = statistics.mean(std_devs) * 1000
        
        print(f"{bench.name:<15} {overall_avg:>10.2f}ms      {overall_min:>10.2f}ms   {overall_max:>10.2f}ms   {overall_std:>10.2f}ms")
    
    # Comparativa por query
    print("\n\n📝 COMPARATIVA POR QUERY")
    print("-" * 80)
    
    for i, query in enumerate(TEST_QUERIES):
        print(f"\nQuery {i+1}: {query}")
        print("-" * 80)
        for bench in benchmarks:
            if bench.results and i < len(bench.results):
                result = bench.results[i]
                print(f"  {bench.name:<15} {result['avg_time']*1000:>8.2f}ms (min: {result['min_time']*1000:.2f}ms, max: {result['max_time']*1000:.2f}ms)")
    
    # Características
    print("\n\n🔍 CARACTERÍSTICAS COMPARATIVAS")
    print("-" * 80)
    
    characteristics = {
        "FAISS": {
            "Tipo": "Local",
            "Costo": "Gratis (sin costo de infraestructura cloud)",
            "Setup": "Muy fácil (solo archivos locales)",
            "Escalabilidad": "Limitada (depende del hardware local)",
            "Latencia": "Muy baja (sin red)",
            "Mantenimiento": "Bajo (sin servidor que mantener)",
            "Persistencia": "Archivos locales (.faiss, .pkl)",
            "Concurrencia": "Limitada por hardware local",
            "Ideal para": "Desarrollo, pruebas, datasets pequeños-medianos"
        },
        "Pinecone": {
            "Tipo": "Cloud (SaaS)",
            "Costo": "Pago por uso (plan gratuito limitado disponible)",
            "Setup": "Fácil (requiere API key)",
            "Escalabilidad": "Muy alta (manejada por Pinecone)",
            "Latencia": "Media (depende de la región)",
            "Mantenimiento": "Ninguno (totalmente gestionado)",
            "Persistencia": "Cloud (automática)",
            "Concurrencia": "Muy alta",
            "Ideal para": "Producción, datasets grandes, alta concurrencia"
        },
        "Weaviate": {
            "Tipo": "Cloud o Self-hosted",
            "Costo": "Gratis (self-hosted) o pago (cloud)",
            "Setup": "Media (configuración de cliente)",
            "Escalabilidad": "Alta (cloud) o media (self-hosted)",
            "Latencia": "Media-baja (depende de deployment)",
            "Mantenimiento": "Ninguno (cloud) o medio (self-hosted)",
            "Persistencia": "Cloud o local",
            "Concurrencia": "Alta",
            "Ideal para": "Producción, flexibilidad deployment, features avanzadas"
        }
    }
    
    for system, features in characteristics.items():
        print(f"\n{system}:")
        for key, value in features.items():
            print(f"  • {key:<15}: {value}")
    
    # Recomendaciones
    print("\n\n💡 RECOMENDACIONES")
    print("-" * 80)
    print("""
    • FAISS: 
      - Usa para desarrollo, pruebas y prototipos
      - Ideal cuando necesitas control total y no hay restricciones de infraestructura
      - Mejor para datasets < 1M vectores en hardware local
    
    • Pinecone:
      - Usa para producción con alta demanda
      - Ideal cuando necesitas escalabilidad sin preocuparte por infraestructura
      - Mejor para aplicaciones que requieren alta disponibilidad y bajo mantenimiento
    
    • Weaviate:
      - Usa cuando necesitas flexibilidad (cloud o self-hosted)
      - Ideal para aplicaciones que requieren features avanzadas (filtrado, metadata)
      - Mejor cuando quieres control sobre el deployment pero con opciones cloud
    """)

def main():
    """Función principal"""
    print("🚀 Iniciando comparativa de Vector Stores")
    print("="*80)
    
    benchmarks = []
    
    # Setup y benchmark de FAISS
    faiss_vectordb, faiss_embeddings = setup_faiss()
    if faiss_vectordb:
        faiss_bench = VectorStoreBenchmark("FAISS", faiss_vectordb, faiss_embeddings)
        faiss_bench.run_benchmark(TEST_QUERIES, iterations=5)
        benchmarks.append(faiss_bench)
    
    # Setup y benchmark de Pinecone
    pinecone_vectordb, pinecone_embeddings = setup_pinecone()
    if pinecone_vectordb:
        pinecone_bench = VectorStoreBenchmark("Pinecone", pinecone_vectordb, pinecone_embeddings)
        pinecone_bench.run_benchmark(TEST_QUERIES, iterations=5)
        benchmarks.append(pinecone_bench)
    
    # Setup y benchmark de Weaviate
    weaviate_vectordb, weaviate_embeddings, weaviate_client = setup_weaviate()
    if weaviate_vectordb:
        weaviate_bench = VectorStoreBenchmark("Weaviate", weaviate_vectordb, weaviate_embeddings)
        weaviate_bench.run_benchmark(TEST_QUERIES, iterations=5)
        benchmarks.append(weaviate_bench)
    
    # Generar reporte comparativo
    if benchmarks:
        generate_comparison_report(benchmarks)
    else:
        print("\n❌ No se pudo configurar ningún vector store. Verifica las configuraciones.")
    
    # Cerrar conexiones
    if weaviate_client:
        weaviate_client.close()

if __name__ == "__main__":
    main()


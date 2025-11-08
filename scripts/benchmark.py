"""
Script de benchmarking integrado para comparar FAISS, Pinecone y Weaviate
"""
import time
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import statistics

# Agregar el backend al path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from langchain_huggingface import HuggingFaceEmbeddings
from config import VectorStoreType, EMBEDDING_MODEL
from vector_stores import get_vector_store

# Queries de prueba
TEST_QUERIES = [
    "¿Cuándo inicia el cuarto retiro de AFP?",
    "¿Cuánto es el monto máximo que puedo retirar?",
    "¿Cómo sé cuándo me toca retirar según mi DNI?",
    "¿Qué es una UIT y cuánto vale?",
    "¿Puedo retirar en cualquier momento?",
]

class VectorStoreBenchmark:
    def __init__(self, name: str, store_type: VectorStoreType):
        self.name = name
        self.store_type = store_type
        self.vectordb = None
        self.embeddings = None
        self.results = []
    
    def setup(self):
        """Configura el vector store para benchmarking"""
        print(f"\n🔧 Configurando {self.name}...")
        try:
            # Cambiar temporalmente el tipo de vector store
            original_type = os.getenv("VECTOR_STORE_TYPE")
            os.environ["VECTOR_STORE_TYPE"] = self.store_type.value
            
            # Recargar config y crear vector store
            from config import VECTOR_STORE_TYPE
            import importlib
            import config
            importlib.reload(config)
            
            self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            self.vectordb = get_vector_store()
            
            # Restaurar tipo original
            if original_type:
                os.environ["VECTOR_STORE_TYPE"] = original_type
            else:
                os.environ.pop("VECTOR_STORE_TYPE", None)
            
            if self.vectordb and self.vectordb.is_available():
                print(f"✅ {self.name} configurado correctamente")
                return True
            else:
                print(f"⚠️  {self.name} no está disponible (datos no ingeridos)")
                return False
        except Exception as e:
            print(f"❌ Error configurando {self.name}: {e}")
            return False
    
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
        if not self.vectordb:
            return []
        
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

def main():
    """Función principal"""
    print("🚀 Iniciando comparativa de Vector Stores")
    print("="*80)
    
    benchmarks = []
    
    # Setup y benchmark de cada sistema
    for store_type, name in [
        (VectorStoreType.FAISS, "FAISS"),
        (VectorStoreType.PINECONE, "Pinecone"),
        (VectorStoreType.WEAVIATE, "Weaviate")
    ]:
        bench = VectorStoreBenchmark(name, store_type)
        if bench.setup():
            bench.run_benchmark(TEST_QUERIES, iterations=5)
            benchmarks.append(bench)
    
    # Generar reporte comparativo
    if benchmarks:
        generate_comparison_report(benchmarks)
    else:
        print("\n❌ No se pudo configurar ningún vector store. Verifica las configuraciones.")

if __name__ == "__main__":
    main()


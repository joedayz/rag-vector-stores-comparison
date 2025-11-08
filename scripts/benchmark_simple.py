"""
Script simplificado de benchmarking que prueba cada vector store
Requiere cambiar VECTOR_STORE_TYPE en .env manualmente
"""
import time
import sys
from pathlib import Path
from typing import List, Dict, Any
import statistics

# Agregar el backend al path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from vector_stores import get_vector_store
from config import VECTOR_STORE_TYPE

# Queries de prueba
TEST_QUERIES = [
    "¿Cuándo inicia el cuarto retiro de AFP?",
    "¿Cuánto es el monto máximo que puedo retirar?",
    "¿Cómo sé cuándo me toca retirar según mi DNI?",
    "¿Qué es una UIT y cuánto vale?",
    "¿Puedo retirar en cualquier momento?",
]

def benchmark_current_store(iterations: int = 5):
    """Ejecuta benchmark del vector store actualmente configurado"""
    print("="*80)
    print(f"🚀 Benchmarking: {VECTOR_STORE_TYPE.value.upper()}")
    print("="*80)
    
    try:
        # Cargar vector store
        print(f"\n📦 Cargando vector store {VECTOR_STORE_TYPE.value}...")
        vectordb = get_vector_store()
        
        if not vectordb.is_available():
            print(f"❌ Error: Vectorstore {VECTOR_STORE_TYPE.value} no disponible")
            print("   Ejecuta 'python ingest.py' primero en backend/")
            return None
        
        print("✅ Vectorstore cargado correctamente")
        
        # Ejecutar benchmarks
        print(f"\n🔍 Ejecutando {len(TEST_QUERIES)} queries con {iterations} iteraciones cada una...")
        results = []
        
        for i, query in enumerate(TEST_QUERIES, 1):
            print(f"\n[{i}/{len(TEST_QUERIES)}] Query: '{query}'")
            times = []
            
            for j in range(iterations):
                start = time.time()
                docs = vectordb.similarity_search(query, k=3)
                elapsed = time.time() - start
                times.append(elapsed)
            
            avg_time = statistics.mean(times) * 1000
            min_time = min(times) * 1000
            max_time = max(times) * 1000
            std_dev = statistics.stdev(times) * 1000 if len(times) > 1 else 0
            
            result = {
                "query": query,
                "avg_time": statistics.mean(times),
                "min_time": min(times),
                "max_time": max(times),
                "std_dev": std_dev / 1000,
                "results_count": len(docs)
            }
            results.append(result)
            
            print(f"  ⏱️  Promedio: {avg_time:.2f}ms | Min: {min_time:.2f}ms | Max: {max_time:.2f}ms | Std: {std_dev:.2f}ms")
            print(f"  📊 Resultados: {len(docs)}")
        
        # Resumen
        print("\n" + "="*80)
        print("📊 RESUMEN")
        print("="*80)
        avg_times = [r['avg_time'] for r in results]
        overall_avg = statistics.mean(avg_times) * 1000
        overall_min = min([r['min_time'] for r in results]) * 1000
        overall_max = max([r['max_time'] for r in results]) * 1000
        overall_std = statistics.mean([r['std_dev'] for r in results]) * 1000
        
        print(f"Tiempo promedio: {overall_avg:.2f}ms")
        print(f"Tiempo mínimo:   {overall_min:.2f}ms")
        print(f"Tiempo máximo:   {overall_max:.2f}ms")
        print(f"Desviación std:  {overall_std:.2f}ms")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Función principal"""
    print("🚀 Benchmarking Simplificado")
    print("="*80)
    print(f"\n📝 Vector Store configurado: {VECTOR_STORE_TYPE.value.upper()}")
    print("💡 Para probar otro vector store, cambia VECTOR_STORE_TYPE en backend/.env")
    print("   y ejecuta este script nuevamente\n")
    
    benchmark_current_store(iterations=5)
    
    print("\n" + "="*80)
    print("💡 Para comparar con otros vector stores:")
    print("   1. Cambia VECTOR_STORE_TYPE en backend/.env")
    print("   2. Ejecuta 'python ingest.py' en backend/")
    print("   3. Ejecuta este script nuevamente")
    print("="*80)

if __name__ == "__main__":
    main()


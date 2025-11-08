# Guía de Benchmarking: Comparativa de Vector Stores

Este documento explica cómo usar el script de benchmarking para comparar FAISS, Pinecone y Weaviate.

## 🚀 Inicio Rápido

### Prerrequisitos

1. **FAISS**: Debe tener el vectorstore generado
   ```bash
   cd afp-chatbot-rag-langchain-faiss/backend
   # Activar el venv del proyecto FAISS
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   python ingest.py
   ```

2. **Pinecone**: Debe tener cuenta y API key configurada
   ```bash
   cd afp-chatbot-rag-langchain-pinecone/backend
   # Activar el venv del proyecto Pinecone
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   # Configurar .env con PINECONE_API_KEY
   python ingest.py
   ```

3. **Weaviate**: Debe tener Weaviate configurado (cloud o local)
   ```bash
   cd afp-chatbot-rag-langchain-weaviate/backend
   # Activar el venv del proyecto Weaviate
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   # Configurar .env con WEAVIATE_URL y opcionalmente WEAVIATE_API_KEY
   python ingest.py
   ```

### Setup del Entorno de Benchmarking

Como los 3 repos son independientes, necesitas crear un entorno virtual separado para el script de benchmarking:

**En macOS/Linux:**
```bash
# Desde la raíz del proyecto
chmod +x setup_benchmark_env.sh
./setup_benchmark_env.sh
```

**En Windows:**
```bash
# Desde la raíz del proyecto
setup_benchmark_env.bat
```

**O manualmente:**
```bash
# Crear venv
python3 -m venv venv_benchmark

# Activar venv
source venv_benchmark/bin/activate  # En Windows: venv_benchmark\Scripts\activate

# Instalar dependencias
pip install -r requirements_benchmark.txt
```

### Ejecutar Benchmark

```bash
# Activar el entorno virtual de benchmarking
source venv_benchmark/bin/activate  # En Windows: venv_benchmark\Scripts\activate

# Ejecutar el benchmark
python benchmark_comparison.py
```

## 📋 Qué Mide el Benchmark

El script mide:

1. **Tiempo de búsqueda**: Latencia promedio, mínima y máxima
2. **Consistencia**: Desviación estándar de los tiempos
3. **Resultados**: Número de documentos encontrados por query
4. **Rendimiento por query**: Comparativa específica para cada tipo de consulta

## 📊 Salida del Benchmark

El script genera:

1. **Métricas de rendimiento**: Tabla comparativa de tiempos
2. **Comparativa por query**: Análisis detallado por cada query de prueba
3. **Características comparativas**: Tabla de características de cada sistema
4. **Recomendaciones**: Guía de cuándo usar cada sistema

## 🔧 Configuración

### Estructura de Repositorios Independientes

Los 3 proyectos (FAISS, Pinecone, Weaviate) son repositorios independientes, cada uno con su propio:
- Entorno virtual (`venv/`)
- Archivo `.env` con configuraciones específicas
- Vectorstore generado

El script de benchmarking:
1. Crea su propio entorno virtual (`venv_benchmark/`) con todas las dependencias necesarias
2. Lee los archivos `.env` de cada backend automáticamente
3. Accede a los vectorstores de cada proyecto según su ubicación

### Variables de Entorno

El script lee automáticamente las variables de entorno desde los archivos `.env` de cada backend:

**FAISS** (opcional, solo si usas OpenAI):
- `OPENAI_API_KEY`: API key de OpenAI (opcional)

**Pinecone** (requerido si quieres probar Pinecone):
- `PINECONE_API_KEY`: Tu API key de Pinecone
- `PINECONE_INDEX_NAME`: Nombre del índice (default: "afp-chatbot")

**Weaviate** (requerido si quieres probar Weaviate):
- `WEAVIATE_URL`: URL de Weaviate (cloud o local)
- `WEAVIATE_API_KEY`: API key (opcional, solo para cloud)
- `WEAVIATE_INDEX_NAME`: Nombre de la clase (default: "AFP_Chatbot")

### Queries de Prueba

Las queries de prueba están definidas en el script:
```python
TEST_QUERIES = [
    "¿Cuándo inicia el cuarto retiro de AFP?",
    "¿Cuánto es el monto máximo que puedo retirar?",
    "¿Cómo sé cuándo me toca retirar según mi DNI?",
    "¿Qué es una UIT y cuánto vale?",
    "¿Puedo retirar en cualquier momento?",
]
```

Puedes modificar estas queries según tus necesidades.

## 📈 Interpretando los Resultados

### Tiempo Promedio
- **< 10ms**: Excelente (típico de FAISS local)
- **10-50ms**: Muy bueno (típico de sistemas optimizados)
- **50-100ms**: Bueno (aceptable para producción)
- **> 100ms**: Considerar optimización

### Desviación Estándar
- **Baja (< 10ms)**: Comportamiento consistente
- **Media (10-30ms)**: Variabilidad normal
- **Alta (> 30ms)**: Puede indicar problemas de red o carga

## 🐛 Troubleshooting

### Error: "Vectorstore no encontrado"
- **Solución**: Ejecuta `ingest.py` en el backend correspondiente

### Error: "PINECONE_API_KEY no configurada"
- **Solución**: Crea un archivo `.env` en el backend de Pinecone con tu API key

### Error: "No se pudo conectar a Weaviate"
- **Solución**: Verifica que Weaviate esté corriendo (cloud o local) y que las credenciales sean correctas

### Error: "Module not found"
- **Solución**: Instala las dependencias necesarias:
  ```bash
  pip install langchain-community langchain-pinecone langchain-weaviate faiss-cpu
  ```

## 🔄 Ejecutar Solo un Sistema

Si quieres probar solo un sistema, puedes comentar las secciones correspondientes en el script `benchmark_comparison.py`.

## 📝 Personalización

### Agregar Más Queries

Edita la lista `TEST_QUERIES` en el script:
```python
TEST_QUERIES = [
    "Tu query 1",
    "Tu query 2",
    # ...
]
```

### Cambiar Número de Iteraciones

Por defecto, cada query se ejecuta 5 veces. Puedes cambiar esto:
```python
bench.run_benchmark(TEST_QUERIES, iterations=10)  # 10 iteraciones
```

### Cambiar Número de Resultados (k)

Por defecto, se buscan 3 resultados. Puedes cambiar esto en el método `benchmark_search`:
```python
docs = self.search(query, k=5)  # Buscar 5 resultados
```

## 📊 Exportar Resultados

Puedes modificar el script para exportar los resultados a JSON o CSV:

```python
import json

# Al final de generate_comparison_report
with open('benchmark_results.json', 'w') as f:
    json.dump({
        'benchmarks': [
            {
                'name': bench.name,
                'results': bench.results
            }
            for bench in benchmarks
        ]
    }, f, indent=2)
```

## ✅ Checklist Antes de Ejecutar

### Setup de Cada Proyecto (en sus respectivos venv)

- [ ] **FAISS**: 
  - [ ] Vectorstore generado con `ingest.py` en `afp-chatbot-rag-langchain-faiss/backend/`
  - [ ] Archivo `.env` configurado (opcional, solo si usas OpenAI)

- [ ] **Pinecone**: 
  - [ ] API key configurada en `.env` en `afp-chatbot-rag-langchain-pinecone/backend/`
  - [ ] Índice creado y datos ingeridos con `ingest.py`

- [ ] **Weaviate**: 
  - [ ] Servicio corriendo (cloud o local)
  - [ ] Archivo `.env` configurado en `afp-chatbot-rag-langchain-weaviate/backend/`
  - [ ] Datos ingeridos con `ingest.py`

### Setup del Entorno de Benchmarking

- [ ] Entorno virtual `venv_benchmark` creado
- [ ] Dependencias instaladas (`pip install -r requirements_benchmark.txt`)
- [ ] Entorno virtual activado antes de ejecutar el benchmark

## 🎯 Próximos Pasos

Después de ejecutar el benchmark:

1. Revisa el reporte comparativo
2. Analiza qué sistema es mejor para tu caso de uso
3. Consulta `COMPARATIVA_VECTOR_STORES.md` para más detalles
4. Toma una decisión informada basada en tus necesidades


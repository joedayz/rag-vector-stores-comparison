# Recomendación: Estructura de Repositorio

## 🎯 Recomendación: **Un Solo Repositorio**

### ¿Por qué consolidar?

#### ✅ Ventajas de un solo repo:

1. **Menos duplicación de código**
   - Los 3 `main.py` son ~95% idénticos
   - Los 3 `ingest.py` son ~80% idénticos
   - El frontend es idéntico en los 3
   - La lógica de negocio es la misma

2. **Más fácil de mantener**
   - Un solo lugar para actualizar código común
   - Un solo entorno virtual
   - Un solo archivo de dependencias
   - Cambios se propagan automáticamente

3. **Mejor para comparativas**
   - Cambiar entre vector stores es trivial
   - Benchmarking más simple
   - Mismo código base = comparación justa

4. **Mejor experiencia de desarrollo**
   - Setup más rápido
   - Menos configuración
   - Menos confusión sobre qué repo usar

5. **Estructura más profesional**
   - Código modular y reutilizable
   - Separación de concerns
   - Más fácil de escalar

#### ❌ Desventajas (menores):

1. **Menos modularidad** (pero puedes mantenerla con estructura de carpetas)
2. **Dependencias mezcladas** (pero puedes usar optional dependencies)

---

## 📁 Estructura Recomendada

```
rags/
├── README.md
├── requirements.txt
├── .env.example
│
├── backend/
│   ├── main.py                    # FastAPI app unificada
│   ├── config.py                  # Configuración centralizada
│   ├── vector_stores/             # Módulos de vector stores
│   │   ├── __init__.py
│   │   ├── base.py                # Interfaz común
│   │   ├── faiss_store.py
│   │   ├── pinecone_store.py
│   │   └── weaviate_store.py
│   ├── ingest.py                  # Script unificado de ingest
│   ├── data/                      # Datos compartidos
│   │   └── data1.txt
│   └── vector_stores_data/        # Vectorstores generados
│       ├── faiss/
│       ├── pinecone/              # (solo config, datos en cloud)
│       └── weaviate/              # (solo config, datos en cloud)
│
├── frontend/                      # Frontend unificado
│   └── ...
│
├── scripts/
│   ├── benchmark_comparison.py   # Script de benchmarking
│   └── setup.sh                   # Setup del proyecto
│
└── docs/
    ├── COMPARATIVA_VECTOR_STORES.md
    ├── SETUP_FAISS.md
    ├── SETUP_PINECONE.md
    └── SETUP_WEAVIATE.md
```

---

## 🔧 Implementación Sugerida

### 1. Configuración Unificada (`config.py`)

```python
import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class VectorStoreType(str, Enum):
    FAISS = "faiss"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"

# Vector store seleccionado
VECTOR_STORE_TYPE = VectorStoreType(os.getenv("VECTOR_STORE_TYPE", "faiss"))

# Configuración común
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Configuración específica por vector store
if VECTOR_STORE_TYPE == VectorStoreType.PINECONE:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "afp-chatbot")
elif VECTOR_STORE_TYPE == VectorStoreType.WEAVIATE:
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")
    WEAVIATE_INDEX_NAME = os.getenv("WEAVIATE_INDEX_NAME", "AFP_Chatbot")
```

### 2. Factory Pattern para Vector Stores

```python
# backend/vector_stores/__init__.py
from .base import VectorStoreBase
from .faiss_store import FAISSVectorStore
from .pinecone_store import PineconeVectorStore
from .weaviate_store import WeaviateVectorStore
from config import VECTOR_STORE_TYPE, VectorStoreType

def get_vector_store():
    """Factory function para obtener el vector store configurado"""
    if VECTOR_STORE_TYPE == VectorStoreType.FAISS:
        return FAISSVectorStore()
    elif VECTOR_STORE_TYPE == VectorStoreType.PINECONE:
        return PineconeVectorStore()
    elif VECTOR_STORE_TYPE == VectorStoreType.WEAVIATE:
        return WeaviateVectorStore()
    else:
        raise ValueError(f"Vector store type {VECTOR_STORE_TYPE} no soportado")
```

### 3. Main.py Unificado

```python
from fastapi import FastAPI
from vector_stores import get_vector_store
from config import VECTOR_STORE_TYPE

app = FastAPI(title="AI Chatbot - RAG Comparison")

# Inicializar vector store según configuración
vectordb = get_vector_store()

@app.get("/")
async def root():
    return {
        "message": "Servidor funcionando",
        "vector_store": VECTOR_STORE_TYPE.value
    }

@app.post("/afp-query")
async def afp_query(query: AFPQuery):
    docs = vectordb.similarity_search(query.question, k=3)
    # ... resto del código igual
```

### 4. Ingest Unificado

```python
from vector_stores import get_vector_store
from config import VECTOR_STORE_TYPE

# Cargar y procesar documentos (código común)
docs = load_documents()
split_docs = split_documents(docs)
embeddings = create_embeddings()

# Crear vector store según configuración
vectordb = get_vector_store()
vectordb.from_documents(split_docs, embeddings)
```

---

## 🚀 Ventajas de Esta Estructura

### 1. **Fácil de usar**
```bash
# Cambiar entre vector stores es solo cambiar una variable
export VECTOR_STORE_TYPE=faiss
python ingest.py
python main.py

export VECTOR_STORE_TYPE=pinecone
python ingest.py
python main.py
```

### 2. **Fácil de comparar**
```bash
# Benchmark todos los sistemas fácilmente
for store in faiss pinecone weaviate; do
    export VECTOR_STORE_TYPE=$store
    python scripts/benchmark_comparison.py
done
```

### 3. **Fácil de mantener**
- Un solo lugar para actualizar lógica común
- Cambios en endpoints se aplican a todos
- Un solo frontend

### 4. **Fácil de extender**
- Agregar un nuevo vector store es solo agregar un módulo
- No necesitas duplicar código

---

## 📋 Plan de Migración

Si decides consolidar, aquí está el plan:

### Fase 1: Preparación
1. Crear nueva estructura de carpetas
2. Crear `config.py` unificado
3. Crear módulos de vector stores

### Fase 2: Migración
1. Migrar código común a módulos
2. Crear factory pattern
3. Unificar `main.py`
4. Unificar `ingest.py`

### Fase 3: Testing
1. Probar cada vector store
2. Ejecutar benchmarks
3. Verificar que todo funciona

### Fase 4: Limpieza
1. Mover documentación
2. Actualizar README
3. Eliminar repos duplicados (o mantenerlos como referencia)

---

## 🎯 Recomendación Final

**SÍ, consolida en un solo repositorio** porque:

1. ✅ Tienes mucha duplicación (90%+ del código es igual)
2. ✅ Quieres hacer comparativas (más fácil en un repo)
3. ✅ Es más fácil de mantener
4. ✅ Es más profesional
5. ✅ Puedes mantener modularidad con buena estructura

La única razón para mantener repos separados sería si:
- Cada uno va a evolucionar de forma muy diferente
- Son para clientes/proyectos completamente diferentes
- Necesitas versionar cada uno independientemente

Pero en tu caso, son **demos comparativas**, así que un solo repo tiene mucho más sentido.

---

## 💡 Alternativa: Monorepo con Workspaces

Si quieres mantener cierta separación pero compartir código:

```
rags/
├── packages/
│   ├── common/          # Código compartido
│   ├── faiss/           # Demo FAISS
│   ├── pinecone/        # Demo Pinecone
│   └── weaviate/        # Demo Weaviate
└── tools/
    └── benchmark/       # Herramientas de benchmarking
```

Pero esto es más complejo y probablemente innecesario para tu caso.

---

## ✅ Conclusión

**Recomendación: Un solo repositorio con estructura modular**

Es la mejor opción para tu caso de uso (demos comparativas de RAG con diferentes vector stores).


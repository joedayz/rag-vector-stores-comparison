# RAG Chatbot - Comparativa de Vector Stores

Sistema de RAG (Retrieval Augmented Generation) que permite comparar diferentes vector stores: **FAISS** (local), **Pinecone** (cloud) y **Weaviate** (cloud o local).

## 🎯 Características

- ✅ **Múltiples Vector Stores**: Soporta FAISS, Pinecone y Weaviate
- ✅ **Código Unificado**: Un solo repositorio con estructura modular
- ✅ **Fácil Cambio**: Cambiar entre vector stores es solo cambiar una variable
- ✅ **Benchmarking Integrado**: Script para comparar rendimiento
- ✅ **Frontend React**: Interfaz web moderna
- ✅ **API RESTful**: Backend FastAPI

## 📋 Requisitos

- **Python 3.8+**
- **Node.js 16+** (para frontend)
- **8GB RAM mínimo** (para el modelo de embeddings)
- **API Keys** (opcionales según vector store):
  - Pinecone API Key (si usas Pinecone)
  - Weaviate URL/API Key (si usas Weaviate)
  - OpenAI API Key (opcional, para fallback)

## 🚀 Inicio Rápido

### 1. Clonar el Repositorio

```bash
git clone https://github.com/joedayz/rag-vector-stores-comparison.git
cd rag-vector-stores-comparison
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias base
pip install -r requirements.txt

# Instalar dependencias específicas según el vector store que uses:
# Para FAISS (ya incluido en requirements.txt)
# Para Pinecone:
pip install langchain-pinecone pinecone-client

# Para Weaviate:
pip install langchain-weaviate weaviate-client
```

### 3. Configurar Variables de Entorno

Crear archivo `.env` en `backend/`:

```env
# Vector Store a usar: faiss, pinecone, weaviate
VECTOR_STORE_TYPE=faiss

# Configuración común
OPENAI_API_KEY=tu_api_key_opcional
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Configuración del servidor
HOST=localhost
PORT=8000

# Configuración de Pinecone (solo si VECTOR_STORE_TYPE=pinecone)
PINECONE_API_KEY=tu_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=afp-chatbot

# Configuración de Weaviate (solo si VECTOR_STORE_TYPE=weaviate)
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=opcional
WEAVIATE_INDEX_NAME=AFP_Chatbot
```

### 4. Ingerir Datos

```bash
# Asegúrate de estar en backend/ con venv activado
python ingest.py
```

Este comando:
- Lee los archivos `.txt` de la carpeta `data/`
- Divide el texto en chunks
- Crea embeddings usando el modelo configurado
- Guarda los vectores en el vector store seleccionado

### 5. Iniciar el Servidor

```bash
# En backend/ con venv activado
uvicorn main:app --reload --host localhost --port 8000
```

### 6. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

Abre tu navegador en `http://localhost:5173` (o el puerto que Vite indique).

## 🔄 Cambiar entre Vector Stores

Para cambiar entre diferentes vector stores:

1. **Edita `.env`** y cambia `VECTOR_STORE_TYPE`:
   ```env
   VECTOR_STORE_TYPE=faiss      # Para FAISS local
   VECTOR_STORE_TYPE=pinecone  # Para Pinecone cloud
   VECTOR_STORE_TYPE=weaviate  # Para Weaviate
   ```

2. **Configura las variables** específicas del vector store elegido

3. **Re-ejecuta ingest.py** para crear el vectorstore:
   ```bash
   python ingest.py
   ```

4. **Reinicia el servidor**:
   ```bash
   uvicorn main:app --reload
   ```

## 📊 Benchmarking

Para comparar el rendimiento de los diferentes vector stores:

```bash
# Desde la raíz del proyecto
cd scripts
python benchmark.py
```

El script:
- Prueba cada vector store configurado
- Mide tiempos de búsqueda
- Genera un reporte comparativo

**Nota**: Asegúrate de tener datos ingeridos en cada vector store que quieras comparar.

## 📁 Estructura del Proyecto

```
rags/
├── backend/
│   ├── main.py                    # FastAPI app unificada
│   ├── ingest.py                   # Script de ingest unificado
│   ├── config.py                   # Configuración centralizada
│   ├── requirements.txt            # Dependencias Python
│   ├── data/                       # Documentos a indexar
│   │   └── data1.txt
│   ├── vector_stores_data/         # Vectorstores generados (FAISS)
│   │   └── faiss/
│   └── vector_stores/              # Módulos de vector stores
│       ├── __init__.py
│       ├── base.py                 # Clase base abstracta
│       ├── faiss_store.py          # Implementación FAISS
│       ├── pinecone_store.py       # Implementación Pinecone
│       └── weaviate_store.py       # Implementación Weaviate
│
├── frontend/                       # Frontend React + Vite
│   ├── src/
│   │   ├── App.tsx
│   │   └── ...
│   └── package.json
│
├── scripts/
│   └── benchmark.py               # Script de benchmarking
│
└── docs/
    ├── COMPARATIVA_VECTOR_STORES.md
    └── SETUP_*.md                  # Guías de setup específicas
```

## 🔧 Configuración Detallada

### FAISS (Local)

**Ventajas:**
- ✅ Gratis, sin costos
- ✅ Muy rápido (sin latencia de red)
- ✅ Privacidad total (datos locales)
- ✅ Fácil setup

**Desventajas:**
- ❌ Escalabilidad limitada
- ❌ Sin alta disponibilidad
- ❌ Mantenimiento manual

**Setup:**
```env
VECTOR_STORE_TYPE=faiss
```

### Pinecone (Cloud)

**Ventajas:**
- ✅ Totalmente gestionado
- ✅ Alta escalabilidad
- ✅ Alta disponibilidad
- ✅ Sin mantenimiento

**Desventajas:**
- ❌ Costo (pago por uso)
- ❌ Dependencia de internet
- ❌ Vendor lock-in

**Setup:**
```env
VECTOR_STORE_TYPE=pinecone
PINECONE_API_KEY=tu_api_key
PINECONE_INDEX_NAME=afp-chatbot
PINECONE_ENVIRONMENT=us-east-1-aws
```

Ver [docs/SETUP_PINECONE.md](docs/SETUP_PINECONE.md) para más detalles.

### Weaviate (Cloud o Local)

**Ventajas:**
- ✅ Flexibilidad (cloud o self-hosted)
- ✅ Features avanzadas
- ✅ Open source disponible
- ✅ Escalable

**Desventajas:**
- ❌ Setup más complejo
- ❌ Curva de aprendizaje

**Setup:**
```env
VECTOR_STORE_TYPE=weaviate
WEAVIATE_URL=http://localhost:8080  # o URL de cloud
WEAVIATE_API_KEY=opcional
WEAVIATE_INDEX_NAME=AFP_Chatbot
```

Ver [docs/SETUP_WEAVIATE.md](docs/SETUP_WEAVIATE.md) para más detalles.

## 📚 Documentación

- [Comparativa de Vector Stores](COMPARATIVA_VECTOR_STORES.md) - Análisis detallado
- [Guía de Benchmarking](README_BENCHMARK.md) - Cómo usar el benchmark
- [Recomendación de Estructura](RECOMENDACION_ESTRUCTURA.md) - Por qué un solo repo

## 🐛 Troubleshooting

### Error: "Vectorstore no disponible"

**Solución**: Ejecuta `python ingest.py` primero para crear el vectorstore.

### Error: "PINECONE_API_KEY no configurada"

**Solución**: Configura `PINECONE_API_KEY` en tu archivo `.env`.

### Error: "No se pudo conectar a Weaviate"

**Solución**: 
- Verifica que Weaviate esté corriendo (cloud o local)
- Verifica que `WEAVIATE_URL` sea correcta
- Para cloud, verifica que `WEAVIATE_API_KEY` sea correcta

### Error: "Module not found"

**Solución**: Instala las dependencias específicas del vector store:
```bash
# Para Pinecone
pip install langchain-pinecone pinecone-client

# Para Weaviate
pip install langchain-weaviate weaviate-client
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- LangChain por el framework
- FAISS, Pinecone y Weaviate por los vector stores
- La comunidad de código abierto


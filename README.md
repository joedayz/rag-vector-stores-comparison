# RAG Chatbot - Comparativa de Vector Stores

Sistema de RAG (Retrieval Augmented Generation) unificado que permite comparar diferentes vector stores: **FAISS** (local), **Pinecone** (cloud) y **Weaviate** (cloud o local).

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

Crear archivo `.env` en `backend/` (puedes copiar `env.example`):

```bash
cp env.example .env
# Edita .env con tus configuraciones
```

**Configuración mínima para cada vector store:**

#### FAISS (Local)
```env
VECTOR_STORE_TYPE=faiss
OPENAI_API_KEY=opcional
```

#### Pinecone (Cloud)
```env
VECTOR_STORE_TYPE=pinecone
PINECONE_API_KEY=tu_pinecone_api_key
PINECONE_INDEX_NAME=afp-chatbot
PINECONE_ENVIRONMENT=us-east-1-aws
```

#### Weaviate (Cloud o Local)
```env
VECTOR_STORE_TYPE=weaviate
WEAVIATE_URL=http://localhost:8080  # o URL de cloud
WEAVIATE_API_KEY=opcional  # solo para cloud
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

1. **Edita `.env`** en `backend/` y cambia `VECTOR_STORE_TYPE`:
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

**Nota**: Asegúrate de tener datos ingeridos en cada vector store que quieras comparar. Puedes cambiar `VECTOR_STORE_TYPE` en `.env` y ejecutar `ingest.py` para cada uno.

El script:
- Prueba cada vector store configurado
- Mide tiempos de búsqueda
- Genera un reporte comparativo

## 📁 Estructura del Proyecto

```
rag-vector-stores-comparison/
├── backend/
│   ├── main.py                    # FastAPI app unificada
│   ├── ingest.py                   # Script de ingest unificado
│   ├── config.py                   # Configuración centralizada
│   ├── requirements.txt            # Dependencias Python
│   ├── env.example                 # Ejemplo de configuración
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
│   └── benchmark.py                # Script de benchmarking
│
├── README.md                       # Este archivo
└── COMPARATIVA_VECTOR_STORES.md    # Comparativa detallada
```

## 🔧 Configuración Detallada por Vector Store

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

**Instalación:**
```bash
# FAISS ya está incluido en requirements.txt
pip install -r requirements.txt
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

**Instalación:**
```bash
pip install langchain-pinecone pinecone-client
```

**Primera vez:**
1. Crea una cuenta en [Pinecone](https://www.pinecone.io/)
2. Obtén tu API key
3. Configura `.env` con tus credenciales
4. Ejecuta `ingest.py` (creará el índice automáticamente)

### Weaviate (Cloud o Local)

**Ventajas:**
- ✅ Flexibilidad (cloud o self-hosted)
- ✅ Features avanzadas
- ✅ Open source disponible
- ✅ Escalable

**Desventajas:**
- ❌ Setup más complejo
- ❌ Curva de aprendizaje

**Setup Local:**
```env
VECTOR_STORE_TYPE=weaviate
WEAVIATE_URL=http://localhost:8080
WEAVIATE_INDEX_NAME=AFP_Chatbot
```

**Setup Cloud:**
```env
VECTOR_STORE_TYPE=weaviate
WEAVIATE_URL=https://tu-cluster.weaviate.network
WEAVIATE_API_KEY=tu_api_key
WEAVIATE_INDEX_NAME=AFP_Chatbot
```

**Instalación:**
```bash
pip install langchain-weaviate weaviate-client
```

**Primera vez (Local):**
1. Instala Docker
2. Ejecuta: `docker run -d -p 8080:8080 semitechnologies/weaviate:latest`
3. Configura `.env` con `WEAVIATE_URL=http://localhost:8080`
4. Ejecuta `ingest.py`

**Primera vez (Cloud):**
1. Crea una cuenta en [Weaviate Cloud](https://weaviate.io/developers/weaviate-cloud)
2. Crea un cluster
3. Obtén la URL y API key
4. Configura `.env` con tus credenciales
5. Ejecuta `ingest.py`

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

## 📚 Documentación Adicional

- [Comparativa Detallada de Vector Stores](COMPARATIVA_VECTOR_STORES.md) - Análisis completo de FAISS, Pinecone y Weaviate

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- LangChain por el framework
- FAISS, Pinecone y Weaviate por los vector stores
- La comunidad de código abierto

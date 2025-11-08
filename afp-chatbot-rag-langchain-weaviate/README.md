# 🏦 RAG Chatbot con LangChain + Weaviate - Sistema de Consultas Inteligentes

Una aplicación web que implementa **RAG (Retrieval-Augmented Generation)** usando **LangChain** y **Weaviate** para responder consultas sobre el cuarto retiro de AFP en Perú, combinando búsquedas vectoriales con información específica y respuestas contextuales.

## 🛠️ Tecnologías Principales

Este proyecto utiliza:
- **LangChain**: Framework para construir aplicaciones con modelos de lenguaje
- **Weaviate**: Base de datos vectorial open-source para búsqueda eficiente de similitud en vectores (puede usarse localmente o en la nube)
- **FastAPI**: Framework web moderno para Python
- **React + TypeScript**: Frontend moderno y type-safe
- **HuggingFace Embeddings**: Modelos de embeddings para representación semántica

## 🧠 ¿Qué es RAG y cómo funciona en este proyecto?

### ¿Qué es RAG?
**RAG (Retrieval-Augmented Generation)** es una técnica de inteligencia artificial que combina:
1. **Retrieval (Recuperación)**: Busca información relevante en una base de datos vectorial usando **Weaviate** para búsqueda vectorial eficiente
2. **Augmented Generation (Generación Aumentada)**: Usa esa información para generar respuestas más precisas y contextuales con **LangChain**

### ¿Cómo funciona nuestro RAG con LangChain + Weaviate?

```mermaid
graph TD
    A[Usuario hace pregunta] --> B[LangChain: Convierte pregunta a embedding]
    B --> C[Weaviate: Búsqueda de similitud en vectorstore]
    C --> D{¿Encuentra información relevante?}
    D -->|Sí| E[LangChain: Combina información local + contexto]
    D -->|No| F[Busca en internet/OpenAI]
    E --> G[Genera respuesta basada en datos locales]
    F --> H[Genera respuesta con información externa]
    G --> I[Respuesta al usuario]
    H --> I
```

### Ventajas de nuestro sistema RAG con LangChain + Weaviate:
- ✅ **Información específica**: Usa datos oficiales sobre el 4to retiro de AFP en Perú
- ✅ **Búsqueda escalable con Weaviate**: Búsqueda vectorial rápida y escalable (local o en la nube)
- ✅ **Pipeline con LangChain**: Procesamiento de documentos, embeddings y búsqueda semántica
- ✅ **Respuestas contextuales**: Las respuestas están basadas en información real y actualizada
- ✅ **Búsqueda semántica**: Encuentra información relevante aunque no uses las palabras exactas
- ✅ **Fallback inteligente**: Si no encuentra información local, puede buscar en internet
- ✅ **Flexibilidad**: Puedes usar Weaviate localmente (con Docker) o en la nube (Weaviate Cloud)
- ✅ **Open Source**: Weaviate es open-source y gratuito para uso local

## 📋 Requisitos del Sistema

- **Python 3.8+**
- **Node.js 16+**
- **Weaviate** (puede usarse localmente con Docker o en la nube con Weaviate Cloud)
  - **Opción Local**: Docker instalado para ejecutar Weaviate localmente
  - **Opción Cloud**: Cuenta en [Weaviate Cloud](https://cloud.weaviate.io/) (opcional)
- **API Key de OpenAI** (opcional, solo para fallback)
- **8GB RAM mínimo** (para el modelo de embeddings)

## 🛠️ Configuración e Instalación

### 1. Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd afp-chatbot-rag-langchain-pinecone
```

### 2. Configurar el Backend

```bash
# Navegar al directorio del backend
cd backend

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install fastapi uvicorn langchain langchain-community langchain-huggingface langchain-weaviate sentence-transformers weaviate-client openai python-dotenv
```

### 3. Configurar Variables de Entorno

#### 3.1. Configurar Weaviate

Tienes dos opciones para usar Weaviate:

**Opción A: Weaviate Local (Recomendado para desarrollo)**
1. Asegúrate de tener Docker instalado
2. Ejecuta Weaviate localmente:
   ```bash
   docker run -d -p 8080:8080 semitechnologies/weaviate:latest
   ```
3. Verifica que esté corriendo:
   ```bash
   curl http://localhost:8080/v1/.well-known/ready
   ```

**Opción B: Weaviate Cloud (Para producción)**
1. Ve a [cloud.weaviate.io](https://cloud.weaviate.io/) y crea una cuenta
2. Crea un cluster y obtén la URL (formato: `https://cluster-id.weaviate.network`)
3. Obtén tu API key desde el dashboard

#### 3.2. Crear archivo `.env`

Crear archivo `.env` en el directorio `backend/`:

**Para Weaviate Local:**
```env
# Weaviate Local
WEAVIATE_URL=http://localhost:8080
WEAVIATE_INDEX_NAME=AFP_Chatbot

# OpenAI (opcional, solo para fallback)
OPENAI_API_KEY=tu_api_key_aqui_opcional

# Servidor
HOST=localhost
PORT=8000
```

**Para Weaviate Cloud:**
```env
# Weaviate Cloud
WEAVIATE_URL=https://tu-cluster-id.weaviate.network
WEAVIATE_API_KEY=tu_api_key_de_weaviate_cloud
WEAVIATE_INDEX_NAME=AFP_Chatbot

# OpenAI (opcional, solo para fallback)
OPENAI_API_KEY=tu_api_key_aqui_opcional

# Servidor
HOST=localhost
PORT=8000
```

**⚠️ IMPORTANTE**: 
- El archivo `.env` está en `.gitignore` por seguridad.
- Para desarrollo local, usa Weaviate con Docker (gratis y sin límites)
- Para producción, considera usar Weaviate Cloud
- `WEAVIATE_INDEX_NAME` es el nombre de la clase que se creará/usará en Weaviate

#### 3.3. Validar Configuración

Antes de continuar, valida que tu configuración sea correcta:

```bash
cd backend
source venv/bin/activate
python validate_weaviate.py
```

Este script verificará:
- ✅ Que la URL de Weaviate esté configurada
- ✅ Que puedas conectarte a Weaviate
- ✅ Si la clase existe o necesita ser creada

### 4. Procesar los Datos (Crear Vectorstore con LangChain + Pinecone)

```bash
# Asegúrate de estar en el directorio backend con el venv activado
cd backend
source venv/bin/activate

# Ejecutar el script de ingest para procesar los datos
python ingest.py
```

Este comando:
- Lee el archivo `data/data1.txt` con información sobre el 4to retiro de AFP
- **LangChain**: Divide el texto en chunks usando `RecursiveCharacterTextSplitter`
- **LangChain**: Crea embeddings usando el modelo `sentence-transformers/all-MiniLM-L6-v2` con `HuggingFaceEmbeddings`
- **Weaviate**: Crea una clase en Weaviate (si no existe) y sube los vectores para búsqueda eficiente

**Nota**: 
- La primera vez que ejecutes `ingest.py`, se creará automáticamente la clase en Weaviate
- Si la clase ya existe, se agregarán los nuevos documentos a la clase existente
- El proceso puede tardar unos minutos dependiendo de la cantidad de datos
- Asegúrate de que Weaviate esté corriendo antes de ejecutar este script

### 5. Configurar el Frontend

```bash
# Navegar al directorio del frontend
cd frontend

# Instalar dependencias
npm install
```

## 🚀 Ejecutar la Aplicación

### Terminal 1: Backend (API)

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend (Interfaz Web)

```bash
cd frontend
npm run dev
```

### URLs de Acceso:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 🔍 Cómo Funciona la Búsqueda con LangChain + Weaviate

### 1. Búsqueda Vectorial (RAG con LangChain + Weaviate)
Cuando haces una pregunta, el sistema:
1. **LangChain**: Convierte tu pregunta en un vector usando embeddings (`HuggingFaceEmbeddings`)
2. **Weaviate**: Busca en el vectorstore los documentos más similares usando búsqueda de similitud vectorial
3. **LangChain**: Combina la información encontrada para generar una respuesta contextual

### 2. Fallback a Internet
Si no encuentra información relevante localmente, puede:
- Buscar en internet (si está configurado)
- Usar OpenAI para generar una respuesta general

### Ejemplos de Preguntas que Funcionan Bien:
- "¿Cuándo puedo retirar mi AFP?"
- "¿Qué fechas corresponden a mi DNI que termina en 5?"
- "¿Cuánto dinero puedo retirar?"
- "¿Cómo consulto mi AFP?"
- "¿Cuáles son las fechas del cronograma?"

## 🔧 Estructura del Proyecto

```
afp-chatbot-rag-langchain-weaviate/
├── backend/
│   ├── main.py              # API FastAPI con endpoints RAG usando Weaviate
│   ├── ingest.py            # Script para procesar datos y crear vectorstore en Weaviate
│   ├── validate_weaviate.py # Script de validación de configuración de Weaviate
│   ├── diagnose.py          # Script de diagnóstico para probar búsquedas en Weaviate
│   ├── config.py            # Configuración y variables de entorno
│   ├── data/
│   │   └── data1.txt        # Información sobre 4to retiro AFP Perú
│   ├── .env                 # Variables de entorno (no versionado)
│   └── venv/                # Entorno virtual Python
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Componente principal React
│   │   └── App.css          # Estilos de la aplicación
│   ├── package.json         # Dependencias Node.js
│   └── vite.config.ts       # Configuración Vite
├── README.md                # Este archivo
└── SETUP_INSTRUCTIONS.md    # Instrucciones detalladas de configuración
```

## 🚨 Troubleshooting

### Problema: "Puerto ya en uso"

#### 1. Encontrar qué proceso está usando el puerto:
```bash
# Para puerto 8000 (backend)
lsof -i :8000

# Para puerto 5173 (frontend)
lsof -i :5173

# Ver todos los puertos en uso
netstat -tulpn | grep LISTEN
```

#### 2. Matar procesos específicos:
```bash
# Matar proceso por PID (reemplaza XXXX con el PID real)
kill XXXX

# Matar proceso por puerto (macOS/Linux)
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:5173 | xargs kill -9

# Matar todos los procesos de uvicorn
pkill -f uvicorn

# Matar todos los procesos de node/vite
pkill -f "vite\|node"
```

#### 3. Verificar que los procesos se cerraron:
```bash
# Verificar puerto 8000
lsof -i :8000

# Verificar puerto 5173
lsof -i :5173
```

### Problema: "ModuleNotFoundError: No module named 'langchain_weaviate'"

**Solución:**
```bash
cd backend
source venv/bin/activate
pip install langchain-weaviate weaviate-client
```

### Problema: "WEAVIATE_URL no está configurada"

**Solución:**
1. Para Weaviate local: Asegúrate de tener Docker corriendo y ejecuta:
   ```bash
   docker run -d -p 8080:8080 semitechnologies/weaviate:latest
   ```
2. Agrega `WEAVIATE_URL=http://localhost:8080` al archivo `.env` en `backend/`
3. Para Weaviate Cloud: Obtén tu URL del dashboard y agrega `WEAVIATE_URL` y `WEAVIATE_API_KEY` al `.env`
4. Ejecuta `python validate_weaviate.py` para verificar la configuración

### Problema: "Vectorstore no disponible" o "No se pudo conectar a Weaviate"

**Solución:**
1. Ejecuta el script de validación primero:
   ```bash
   cd backend
   source venv/bin/activate
   python validate_weaviate.py
   ```
2. Para Weaviate local: Verifica que Docker esté corriendo:
   ```bash
   docker ps | grep weaviate
   ```
   Si no está corriendo, inícialo:
   ```bash
   docker run -d -p 8080:8080 semitechnologies/weaviate:latest
   ```
3. Verifica que la URL de Weaviate sea correcta
4. Verifica que la clase existe en Weaviate (ejecuta `python ingest.py` si no lo has hecho)
5. Verifica tu conexión a internet (si usas Weaviate Cloud)
6. Revisa los logs del backend para más detalles

### Problema: "Error al crear clase en Weaviate"

**Solución:**
- Verifica que Weaviate esté corriendo y accesible
- Verifica que la URL de Weaviate sea correcta
- Para Weaviate Cloud: Verifica que tu API key sea correcta
- Revisa los logs de Weaviate para más detalles

### Problema: "Error al cargar embeddings"

**Solución:**
```bash
# Reinstalar dependencias de embeddings
pip uninstall sentence-transformers
pip install sentence-transformers
```

### Problema: "LangChainDeprecationWarning: The class HuggingFaceEmbeddings was deprecated"

**Solución:**
```bash
# Instalar el paquete actualizado
pip install -U langchain-huggingface

# El código ya está actualizado para usar:
# from langchain_huggingface import HuggingFaceEmbeddings
# en lugar de:
# from langchain_community.embeddings import HuggingFaceEmbeddings
```

### Problema: "LangChainDeprecationWarning: Importing TextLoader from langchain.document_loaders is deprecated"

**Solución:**
```bash
# El código ya está actualizado para usar:
# from langchain_community.document_loaders import TextLoader
# en lugar de:
# from langchain.document_loaders import TextLoader
```

### Problema: Frontend no se conecta al backend

**Verificar:**
1. Backend está corriendo en puerto 8000
2. Frontend está corriendo en puerto 5173
3. No hay errores de CORS (ya configurado en el backend)
4. Verificar en el navegador: http://localhost:8000 (debe mostrar mensaje de bienvenida)

### Comandos de Diagnóstico Rápido:

```bash
# Verificar que el backend responde
curl http://localhost:8000

# Verificar que el frontend responde
curl http://localhost:5173

# Validar configuración de Weaviate
cd backend
source venv/bin/activate
python validate_weaviate.py

# Probar búsquedas en Weaviate (diagnóstico)
cd backend
source venv/bin/activate
python diagnose.py

# Ver logs del backend
# (Los logs aparecen en la terminal donde ejecutaste uvicorn)

# Ver logs del frontend
# (Los logs aparecen en la terminal donde ejecutaste npm run dev)
```

## 📊 API Endpoints

### `POST /afp-query`
Consulta sobre el 4to retiro de AFP usando RAG con Weaviate.

**Request:**
```json
{
  "question": "¿Cuándo puedo retirar mi AFP si mi DNI termina en 5?"
}
```

**Response:**
```json
{
  "answer": "Basándome en la información oficial disponible sobre el 4to retiro de AFP en Perú:\n\nSi termina en 5: 5, 6 de noviembre o 27 de noviembre...",
  "question": "¿Cuándo puedo retirar mi AFP si mi DNI termina en 5?",
  "source": "Información local del archivo data1.txt"
}
```

### `GET /search`
Búsqueda directa en el vectorstore de Weaviate.

**Request:**
```
GET /search?query=cronograma%20DNI
```

**Response:**
```json
{
  "results": ["Texto relevante encontrado en los documentos..."]
}
```

## 🎯 Casos de Uso Educativos

Este proyecto es ideal para aprender:

1. **RAG (Retrieval-Augmented Generation)**
2. **LangChain**: Framework completo para aplicaciones con LLMs
   - Document loaders (`TextLoader`)
   - Text splitters (`RecursiveCharacterTextSplitter`)
   - Embeddings (`HuggingFaceEmbeddings`)
   - Vectorstores (`WeaviateVectorStore`)
3. **Weaviate**: Base de datos vectorial open-source para búsqueda eficiente
4. **Embeddings y búsqueda semántica**
5. **Vectorstores con Weaviate (local o en la nube)**
6. **APIs REST con FastAPI**
7. **Frontend con React y TypeScript**
8. **Procesamiento de texto con LangChain**
9. **Integración de sistemas de IA**
10. **Docker para despliegue local de Weaviate**

## 🔒 Consideraciones de Seguridad

- ✅ **API Keys protegidas**: Se almacenan en variables de entorno
- ✅ **CORS configurado**: Permite comunicación entre frontend y backend
- ✅ **Validación de entrada**: Se valida la entrada del usuario
- ✅ **Manejo de errores**: Respuestas de error apropiadas
- ✅ **Datos seguros**: Los vectores se almacenan de forma segura en Weaviate (local o en la nube)

## 📝 Próximas Mejoras

- [ ] Agregar más documentos al vectorstore
- [ ] Implementar búsqueda híbrida (Weaviate + internet)
- [ ] Agregar métricas de calidad de respuestas
- [ ] Implementar cache de respuestas
- [ ] Agregar autenticación de usuarios
- [ ] Mejorar la interfaz de usuario
- [ ] Agregar filtros de metadatos en Weaviate
- [ ] Implementar búsqueda híbrida (vectorial + keyword) con Weaviate

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Desarrollado con ❤️ para enseñar RAG y sistemas de IA a estudiantes**

*Este proyecto demuestra cómo implementar un sistema RAG completo con **LangChain** y **Weaviate**, desde el procesamiento de datos hasta la interfaz de usuario, usando tecnologías modernas de IA y almacenamiento vectorial open-source.*

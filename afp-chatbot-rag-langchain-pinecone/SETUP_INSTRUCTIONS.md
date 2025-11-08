# 🚀 Instrucciones de Configuración - AFP Chatbot con Pinecone

## ✅ Estado Actual
- ✅ Backend configurado y funcionando en http://localhost:8000
- ✅ Frontend configurado y funcionando en http://localhost:5173
- ✅ Todas las dependencias instaladas
- ✅ Estructura de archivos completa
- ✅ Usando Pinecone para almacenamiento vectorial en la nube

## 🔑 Configuración de API Keys (PASO CRÍTICO)

**Para que la aplicación funcione completamente, necesitas configurar tu API key de Pinecone (requerida) y opcionalmente OpenAI (solo para fallback):**

### 1. Obtener API Key de Pinecone (REQUERIDO)

1. Ve a [pinecone.io](https://www.pinecone.io/) y crea una cuenta gratuita
2. Una vez dentro del dashboard, ve a "API Keys"
3. Copia tu API key (comienza con `pc-...`)
4. Verifica tu región/environment (por ejemplo: `us-east-1-aws`, `us-west1-gcp`, `eu-west1-aws`)

### 2. Obtener API Key de OpenAI (OPCIONAL - solo para fallback)

1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión en tu cuenta de OpenAI
3. Crea una nueva API key
4. Copia la clave (comienza con `sk-`)

### 3. Configurar las API Keys

```bash
# Navegar al directorio backend
cd backend

# Editar el archivo .env
nano .env
# o usar tu editor preferido: code .env, vim .env, etc.
```

**Configura las siguientes variables en el archivo `.env`:**
```env
# Pinecone (REQUERIDO)
PINECONE_API_KEY=pc-tu_api_key_de_pinecone_aqui
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=afp-chatbot

# OpenAI (OPCIONAL - solo para fallback)
OPENAI_API_KEY=sk-tu_api_key_de_openai_aqui_opcional

# Servidor
HOST=localhost
PORT=8000
```

### 4. Validar Configuración de Pinecone

Antes de continuar, valida que tu configuración sea correcta:

```bash
cd backend
source venv/bin/activate
python validate_pinecone.py
```

Este script verificará:
- ✅ Que la API key esté configurada
- ✅ Que puedas conectarte a Pinecone
- ✅ Si el índice existe o necesita ser creado

### 5. Cargar Datos a Pinecone

Si el índice no existe, ejecuta el script de ingest para crear el índice y cargar los datos:

```bash
cd backend
source venv/bin/activate
python ingest.py
```

Este comando:
- Crea el índice en Pinecone (si no existe)
- Procesa los documentos de `data/data1.txt`
- Crea embeddings y los sube a Pinecone

### 6. Reiniciar el servidor
```bash
# Detener el servidor actual (Ctrl+C en la terminal donde está corriendo)
# Luego ejecutar nuevamente:
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Acceder a la Aplicación

1. **Frontend**: http://localhost:5173
2. **Backend API**: http://localhost:8000
3. **Documentación API**: http://localhost:8000/docs

## 🧪 Probar la Aplicación

1. Abre http://localhost:5173 en tu navegador
2. Escribe una pregunta como: "¿Cuándo puedo retirar mi AFP si mi DNI termina en 5?"
3. Haz clic en "Consultar"
4. Deberías recibir una respuesta basada en la información almacenada en Pinecone

## 🔧 Comandos Útiles

### Iniciar Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Iniciar Frontend
```bash
cd frontend
npm run dev
```

### Verificar que el backend funciona
```bash
curl http://localhost:8000/
```

## ⚠️ Notas Importantes

- **Nunca subas tu API key a un repositorio público**
- **El archivo `.env` está en `.gitignore` para proteger tus claves**
- **Pinecone tiene un plan gratuito generoso para empezar**
- **Los datos se almacenan en la nube en Pinecone, permitiendo escalabilidad**
- **La aplicación usa Pinecone para búsqueda vectorial, no requiere OpenAI para funcionar (solo opcional para fallback)**

## 🆘 Solución de Problemas

### Error: "PINECONE_API_KEY no está configurada"
- Verifica que el archivo `.env` existe en el directorio `backend/`
- Asegúrate de que la API key de Pinecone esté correctamente escrita
- Ejecuta `python validate_pinecone.py` para verificar la configuración

### Error: "Vectorstore no disponible" o "No se pudo conectar a Pinecone"
- Ejecuta `python validate_pinecone.py` para diagnosticar el problema
- Verifica que tu API key de Pinecone sea correcta
- Verifica que el índice existe en Pinecone (ejecuta `python ingest.py` si no lo has hecho)
- Verifica tu conexión a internet
- Verifica que `PINECONE_ENVIRONMENT` coincida con tu región en Pinecone

### Error: "El índice no existe"
- Ejecuta `python ingest.py` para crear el índice y cargar los datos
- Verifica que `PINECONE_INDEX_NAME` en `.env` coincida con el nombre del índice

### Error de conexión entre frontend y backend
- Verifica que ambos servidores estén ejecutándose
- Backend debe estar en puerto 8000
- Frontend debe estar en puerto 5173

### Error de CORS
- El backend ya tiene CORS configurado para permitir conexiones desde el frontend

## 🎉 ¡Listo!

Una vez configurada la API key de Pinecone y cargados los datos, tu aplicación estará completamente funcional y podrás hacer consultas sobre el cuarto retiro de AFP usando RAG con Pinecone para búsqueda vectorial en la nube.

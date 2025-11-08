# 🚀 Guía Rápida de Configuración con Pinecone

Esta guía te ayudará a configurar y validar que tu demo funcione correctamente con Pinecone.

## 📋 Checklist de Configuración

### 1. ✅ Instalar Dependencias

```bash
cd backend
source venv/bin/activate
pip install fastapi uvicorn langchain langchain-community langchain-huggingface langchain-pinecone sentence-transformers pinecone-client openai python-dotenv
```

### 2. ✅ Obtener API Key de Pinecone

1. Ve a [pinecone.io](https://www.pinecone.io/) y crea una cuenta (gratis)
2. En el dashboard, ve a "API Keys"
3. Copia tu API key (formato: `pc-...`)
4. Anota tu región/environment (ej: `us-east-1-aws`)

### 3. ✅ Configurar Variables de Entorno

Crea el archivo `backend/.env` con:

```env
PINECONE_API_KEY=tu_api_key_aqui
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=afp-chatbot
OPENAI_API_KEY=opcional
HOST=localhost
PORT=8000
```

### 4. ✅ Validar Configuración

```bash
cd backend
source venv/bin/activate
python validate_pinecone.py
```

**Salida esperada:**
```
🔍 Validando configuración de Pinecone...

✅ PINECONE_API_KEY configurada
✅ PINECONE_ENVIRONMENT: us-east-1-aws
✅ PINECONE_INDEX_NAME: afp-chatbot

🔌 Conectando a Pinecone...
✅ Conexión exitosa a Pinecone

📋 Verificando índices...
   Índices encontrados: []

⚠️  El índice 'afp-chatbot' no existe
   Ejecuta 'python ingest.py' para crear el índice y cargar los datos
```

### 5. ✅ Cargar Datos a Pinecone

```bash
cd backend
source venv/bin/activate
python ingest.py
```

**Salida esperada:**
```
Creando índice afp-chatbot en Pinecone...
Índice afp-chatbot creado exitosamente
Vectorstore generado y guardado en Pinecone (índice: afp-chatbot)
Total de documentos procesados: X
```

### 6. ✅ Validar que los Datos se Cargaron

Ejecuta nuevamente el script de validación:

```bash
python validate_pinecone.py
```

**Salida esperada:**
```
✅ El índice 'afp-chatbot' existe
   Total de vectores: X
   Dimensiones: 384
```

### 7. ✅ Iniciar el Servidor

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
Conectado exitosamente a Pinecone (índice: afp-chatbot)
```

### 8. ✅ Probar la API

En otra terminal:

```bash
# Probar endpoint raíz
curl http://localhost:8000

# Probar consulta AFP
curl -X POST http://localhost:8000/afp-query \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuándo puedo retirar mi AFP si mi DNI termina en 5?"}'
```

## 🔍 Solución de Problemas Comunes

### Error: "PINECONE_API_KEY no está configurada"

**Solución:**
- Verifica que el archivo `.env` existe en `backend/`
- Verifica que `PINECONE_API_KEY` esté en el archivo `.env`
- No uses comillas alrededor del valor en `.env`

### Error: "No se pudo conectar a Pinecone"

**Solución:**
- Verifica tu conexión a internet
- Verifica que la API key sea correcta
- Ejecuta `python validate_pinecone.py` para diagnóstico

### Error: "El índice no existe"

**Solución:**
- Ejecuta `python ingest.py` para crear el índice y cargar datos
- Verifica que `PINECONE_INDEX_NAME` en `.env` coincida con el nombre del índice

### Error: "Error al crear índice"

**Solución:**
- Verifica que `PINECONE_ENVIRONMENT` coincida con tu región en Pinecone
- Verifica que tu cuenta de Pinecone tenga permisos para crear índices
- Algunas regiones pueden tener nombres diferentes (ej: `us-west1-gcp` vs `us-west-1-aws`)

## 📊 Verificar en el Dashboard de Pinecone

1. Ve a [app.pinecone.io](https://app.pinecone.io/)
2. Selecciona tu proyecto
3. Ve a "Indexes"
4. Deberías ver el índice `afp-chatbot` con vectores cargados

## ✅ Checklist Final

- [ ] Dependencias instaladas
- [ ] API key de Pinecone configurada
- [ ] Script de validación pasa sin errores
- [ ] Datos cargados a Pinecone (`ingest.py` ejecutado)
- [ ] Índice existe y tiene vectores
- [ ] Servidor inicia correctamente
- [ ] API responde a consultas

## 🎉 ¡Listo!

Si todos los pasos anteriores se completaron exitosamente, tu demo está lista para funcionar con Pinecone.

Para iniciar la aplicación completa:

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Accede a http://localhost:5173 para usar la aplicación.


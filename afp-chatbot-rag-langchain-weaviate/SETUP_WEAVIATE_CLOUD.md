# 🚀 Guía Rápida: Configurar Weaviate Cloud

Esta guía te ayudará a configurar Weaviate Cloud para usar con el chatbot AFP.

## 📋 Pasos para Configurar Weaviate Cloud

### 1. Crear Cuenta en Weaviate Cloud

1. Ve a [cloud.weaviate.io](https://cloud.weaviate.io/)
2. Crea una cuenta nueva o inicia sesión
3. Verifica tu email si es necesario

### 2. Crear un Cluster

1. Una vez dentro del dashboard, haz clic en **"Create Cluster"** o **"New Cluster"**
2. Elige un nombre para tu cluster (ej: `afp-chatbot`)
3. Selecciona la región más cercana a ti (ej: `us-east-1`, `eu-west-1`)
4. Elige el plan (puedes empezar con el plan gratuito/trial si está disponible)
5. Haz clic en **"Create"** o **"Deploy"**

### 3. Obtener la URL del Cluster

1. Una vez que el cluster esté creado y desplegado, verás la información del cluster
2. Copia la **URL del cluster** (formato: `https://tu-cluster-id.weaviate.network`)
   - Ejemplo: `https://afp-chatbot-abc123.weaviate.network`
3. Esta URL es tu `WEAVIATE_URL`

### 4. Obtener la API Key

1. En el dashboard de tu cluster, busca la sección **"API Keys"** o **"Authentication"**
2. Haz clic en **"Create API Key"** o **"Generate Key"**
3. Copia la API key generada (guárdala de forma segura, no la compartas)
4. Esta key es tu `WEAVIATE_API_KEY`

### 5. Configurar el archivo .env

1. Abre el archivo `.env` en el directorio `backend/`
2. Actualiza los siguientes valores:

```env
# URL de tu cluster de Weaviate Cloud
WEAVIATE_URL=https://tu-cluster-id.weaviate.network

# API Key de Weaviate Cloud
WEAVIATE_API_KEY=tu_api_key_aqui

# Nombre de la clase en Weaviate
WEAVIATE_INDEX_NAME=AFP_Chatbot
```

**Ejemplo real:**
```env
WEAVIATE_URL=https://afp-chatbot-abc123.weaviate.network
WEAVIATE_API_KEY=WCS-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
WEAVIATE_INDEX_NAME=AFP_Chatbot
```

### 6. Validar la Configuración

Ejecuta el script de validación para verificar que todo esté correcto:

```bash
cd backend
source venv/bin/activate
python validate_weaviate.py
```

**Salida esperada:**
```
🔍 Validando configuración de Weaviate...

✅ WEAVIATE_URL configurada: https://tu-cluster-id.weaviate.network
✅ WEAVIATE_API_KEY configurada (para Weaviate Cloud)
✅ WEAVIATE_INDEX_NAME: AFP_Chatbot

🔌 Conectando a Weaviate...
✅ Conexión exitosa a Weaviate

📋 Verificando clases (índices)...
   Clases encontradas: []

⚠️  La clase 'AFP_Chatbot' no existe
   Ejecuta 'python ingest.py' para crear la clase y cargar los datos
```

### 7. Cargar los Datos

Una vez validada la configuración, carga los datos:

```bash
python ingest.py
```

**Salida esperada:**
```
Conectando a Weaviate en https://tu-cluster-id.weaviate.network...
✅ Conexión exitosa a Weaviate
Verificando clase 'AFP_Chatbot' en Weaviate...
La clase 'AFP_Chatbot' se creará automáticamente al cargar los documentos
✅ Vectorstore generado y guardado en Weaviate (clase: AFP_Chatbot)
Total de documentos procesados: X
```

## ✅ Verificación Final

Ejecuta el script de diagnóstico para probar las búsquedas:

```bash
python diagnose.py
```

Si todo funciona correctamente, verás resultados de búsqueda semántica.

## 🔒 Seguridad

- **Nunca compartas tu API key** públicamente
- **No subas el archivo `.env`** a repositorios públicos
- El archivo `.env` ya está en `.gitignore` por seguridad

## 🆘 Troubleshooting

### Error: "No se pudo conectar a Weaviate"

**Solución:**
- Verifica que la URL del cluster sea correcta
- Verifica que el cluster esté activo en el dashboard
- Verifica que tu API key sea correcta
- Verifica tu conexión a internet

### Error: "API key incorrecta"

**Solución:**
- Genera una nueva API key desde el dashboard
- Asegúrate de copiar la key completa sin espacios
- Verifica que la key no haya expirado

### Error: "Cluster no encontrado"

**Solución:**
- Verifica que el cluster esté desplegado y activo
- Verifica que la URL del cluster sea correcta
- Espera unos minutos si acabas de crear el cluster (puede tardar en estar disponible)

## 📚 Recursos Adicionales

- [Documentación de Weaviate Cloud](https://weaviate.io/developers/weaviate-cloud)
- [Dashboard de Weaviate Cloud](https://cloud.weaviate.io/)
- [Documentación de Weaviate](https://weaviate.io/developers/weaviate)

---

**¡Listo!** Ahora puedes usar Weaviate Cloud con tu chatbot AFP. 🎉


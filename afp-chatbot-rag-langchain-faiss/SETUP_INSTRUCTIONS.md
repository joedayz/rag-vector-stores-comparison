# 🚀 Instrucciones de Configuración - AFP Chatbot

## ✅ Estado Actual
- ✅ Backend configurado y funcionando en http://localhost:8000
- ✅ Frontend configurado y funcionando en http://localhost:5173
- ✅ Todas las dependencias instaladas
- ✅ Estructura de archivos completa

## 🔑 Configuración de API Key (PASO CRÍTICO)

**Para que la aplicación funcione completamente, necesitas configurar tu API key de OpenAI:**

### 1. Obtener API Key de OpenAI
1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión en tu cuenta de OpenAI
3. Crea una nueva API key
4. Copia la clave (comienza con `sk-`)

### 2. Configurar la API Key
```bash
# Navegar al directorio backend
cd backend

# Editar el archivo .env
nano .env
# o usar tu editor preferido: code .env, vim .env, etc.
```

**Reemplaza `your_openai_api_key_here` con tu API key real:**
```env
OPENAI_API_KEY=sk-tu_api_key_real_aqui
HOST=localhost
PORT=8000
```

### 3. Reiniciar el servidor
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
2. Escribe una pregunta como: "¿Cuál es el procedimiento para el cuarto retiro de AFP?"
3. Haz clic en "Consultar"
4. Deberías recibir una respuesta detallada de OpenAI

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
- **El archivo `.env` está en `.gitignore` para proteger tu clave**
- **Cada consulta consume tokens de OpenAI (tiene costo)**
- **La aplicación funciona sin conexión a internet, excepto para las consultas a OpenAI**

## 🆘 Solución de Problemas

### Error: "OPENAI_API_KEY no está configurada"
- Verifica que el archivo `.env` existe en el directorio `backend/`
- Asegúrate de que la API key esté correctamente escrita
- Reinicia el servidor después de cambiar el archivo `.env`

### Error de conexión entre frontend y backend
- Verifica que ambos servidores estén ejecutándose
- Backend debe estar en puerto 8000
- Frontend debe estar en puerto 5173

### Error de CORS
- El backend ya tiene CORS configurado para permitir conexiones desde el frontend

## 🎉 ¡Listo!

Una vez configurada la API key, tu aplicación estará completamente funcional y podrás hacer consultas sobre el cuarto retiro de AFP usando inteligencia artificial.

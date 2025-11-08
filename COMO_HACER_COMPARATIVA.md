# 🔄 Cómo Hacer la Comparativa entre FAISS, Pinecone y Weaviate

## 📋 Resumen del Proceso

Para comparar los 3 vector stores, necesitas:
1. **Ingerir datos** en cada uno de los 3 vector stores
2. **Ejecutar benchmarks** para medir el rendimiento
3. **Comparar los resultados**

---

## 🎯 Opción 1: Comparativa Manual (Recomendada)

Esta opción te da más control y es más clara. Pruebas cada vector store uno por uno.

### Paso 1: Preparar FAISS

```bash
cd backend
source venv/bin/activate

# 1. Configurar .env para FAISS
# Edita backend/.env y pon:
# VECTOR_STORE_TYPE=faiss

# 2. Ingerir datos en FAISS
python ingest.py

# 3. Ejecutar benchmark
cd ../scripts
python benchmark_simple.py > resultados_faiss.txt
```

### Paso 2: Preparar Pinecone

```bash
cd backend
source venv/bin/activate

# 1. Configurar .env para Pinecone
# Edita backend/.env y pon:
# VECTOR_STORE_TYPE=pinecone
# PINECONE_API_KEY=tu_api_key
# PINECONE_INDEX_NAME=afp-chatbot

# 2. Ingerir datos en Pinecone
python ingest.py

# 3. Ejecutar benchmark
cd ../scripts
python benchmark_simple.py > resultados_pinecone.txt
```

### Paso 3: Preparar Weaviate

```bash
# Primero, asegúrate de que Weaviate esté corriendo
docker ps | grep weaviate
# Si no está corriendo:
docker run -d --name weaviate -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e DEFAULT_VECTORIZER_MODULE='none' \
  semitechnologies/weaviate:latest

cd backend
source venv/bin/activate

# 1. Configurar .env para Weaviate
# Edita backend/.env y pon:
# VECTOR_STORE_TYPE=weaviate
# WEAVIATE_URL=http://localhost:8080
# WEAVIATE_INDEX_NAME=AFP_Chatbot

# 2. Ingerir datos en Weaviate
python ingest.py

# 3. Ejecutar benchmark
cd ../scripts
python benchmark_simple.py > resultados_weaviate.txt
```

### Paso 4: Comparar Resultados

```bash
# Ver los resultados de cada uno
cat resultados_faiss.txt
cat resultados_pinecone.txt
cat resultados_weaviate.txt

# O comparar lado a lado
echo "=== FAISS ===" && cat resultados_faiss.txt
echo "=== PINECONE ===" && cat resultados_pinecone.txt
echo "=== WEAVIATE ===" && cat resultados_weaviate.txt
```

---

## 🚀 Opción 2: Comparativa Automática (Avanzada)

El script `benchmark.py` intenta probar todos los vector stores automáticamente, pero requiere que todos estén configurados y con datos ingeridos.

### Requisitos Previos

1. **FAISS**: Ya debe tener datos ingeridos
2. **Pinecone**: Debe estar configurado en `.env` y tener datos ingeridos
3. **Weaviate**: Debe estar corriendo (local o cloud) y tener datos ingeridos

### Ejecutar Comparativa Automática

```bash
cd scripts
source ../backend/venv/bin/activate
python benchmark.py
```

**Nota**: Este script intenta cargar todos los vector stores automáticamente, pero puede fallar si alguno no está configurado correctamente.

---

## 📊 Qué Mide el Benchmark

El benchmark mide:
- ⏱️ **Tiempo de búsqueda**: Cuánto tarda cada query
- 📊 **Resultados encontrados**: Cuántos documentos retorna
- 📈 **Estadísticas**: Promedio, mínimo, máximo, desviación estándar

### Queries de Prueba

El benchmark usa estas 5 queries:
1. "¿Cuándo inicia el cuarto retiro de AFP?"
2. "¿Cuánto es el monto máximo que puedo retirar?"
3. "¿Cómo sé cuándo me toca retirar según mi DNI?"
4. "¿Qué es una UIT y cuánto vale?"
5. "¿Puedo retirar en cualquier momento?"

Cada query se ejecuta 5 veces para obtener estadísticas confiables.

---

## 💡 Recomendación

**Usa la Opción 1 (Manual)** porque:
- ✅ Es más clara y fácil de entender
- ✅ Tienes control total sobre cada paso
- ✅ Puedes ver los resultados de cada uno por separado
- ✅ Es más fácil depurar si algo falla

---

## 🔍 Verificación Rápida

Antes de hacer la comparativa, verifica que cada vector store tenga datos:

```bash
# Verificar FAISS
cd backend
# Edita .env: VECTOR_STORE_TYPE=faiss
python -c "from vector_stores import get_vector_store; vs = get_vector_store(); print('FAISS disponible:', vs.is_available())"

# Verificar Pinecone
# Edita .env: VECTOR_STORE_TYPE=pinecone
python -c "from vector_stores import get_vector_store; vs = get_vector_store(); print('Pinecone disponible:', vs.is_available())"

# Verificar Weaviate
# Edita .env: VECTOR_STORE_TYPE=weaviate
python -c "from vector_stores import get_vector_store; vs = get_vector_store(); print('Weaviate disponible:', vs.is_available())"
```

---

## 📝 Checklist de Comparativa

- [ ] FAISS configurado y con datos ingeridos
- [ ] Pinecone configurado y con datos ingeridos
- [ ] Weaviate corriendo y con datos ingeridos
- [ ] Benchmarks ejecutados para cada uno
- [ ] Resultados comparados

---

## 🎯 Resultado Esperado

Al final, tendrás métricas comparativas como:

```
Sistema        Tiempo Promedio    Tiempo Mín    Tiempo Máx    Desv. Est.
FAISS          15.23ms           12.45ms       18.90ms       2.10ms
Pinecone       45.67ms           38.20ms       52.10ms       4.50ms
Weaviate       28.34ms           24.10ms       32.50ms       3.20ms
```

Esto te permitirá decidir cuál vector store es mejor para tu caso de uso específico.


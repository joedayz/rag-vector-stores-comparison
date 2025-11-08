# Scripts de Testing y Benchmarking

Scripts para probar y comparar los diferentes vector stores.

## 🧪 Scripts de Prueba Individuales

### test_faiss.py
Prueba FAISS (local)
```bash
cd backend
# Configurar .env: VECTOR_STORE_TYPE=faiss
python ingest.py
cd ../scripts
python test_faiss.py
```

### test_pinecone.py
Prueba Pinecone (cloud)
```bash
cd backend
# Configurar .env: VECTOR_STORE_TYPE=pinecone
# Configurar PINECONE_API_KEY
python ingest.py
cd ../scripts
python test_pinecone.py
```

### test_weaviate.py
Prueba Weaviate (local o cloud)
```bash
cd backend
# Configurar .env: VECTOR_STORE_TYPE=weaviate
# Configurar WEAVIATE_URL
python ingest.py
cd ../scripts
python test_weaviate.py
```

## 📊 Scripts de Benchmarking

### benchmark_simple.py
Benchmark simplificado del vector store configurado actualmente
```bash
cd backend
# Configurar .env con el vector store que quieras probar
python ingest.py
cd ../scripts
python benchmark_simple.py
```

### benchmark.py
Benchmark completo que prueba los 3 sistemas (requiere setup especial)

## 🚀 Proceso Completo de Testing

1. **Probar FAISS**:
   ```bash
   cd backend
   source venv/bin/activate
   # Editar .env: VECTOR_STORE_TYPE=faiss
   python ingest.py
   cd ../scripts
   python test_faiss.py
   python benchmark_simple.py
   ```

2. **Probar Pinecone**:
   ```bash
   cd backend
   # Editar .env: VECTOR_STORE_TYPE=pinecone
   # Configurar PINECONE_API_KEY
   python ingest.py
   cd ../scripts
   python test_pinecone.py
   python benchmark_simple.py
   ```

3. **Probar Weaviate**:
   ```bash
   # Iniciar Weaviate local (si usas local)
   docker run -d --name weaviate -p 8080:8080 \
     -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
     semitechnologies/weaviate:latest
   
   cd backend
   # Editar .env: VECTOR_STORE_TYPE=weaviate
   # Configurar WEAVIATE_URL
   python ingest.py
   cd ../scripts
   python test_weaviate.py
   python benchmark_simple.py
   ```

4. **Comparar resultados**: Compara los tiempos de cada `benchmark_simple.py` ejecutado.


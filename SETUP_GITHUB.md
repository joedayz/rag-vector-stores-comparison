# Guía para Subir el Repositorio a GitHub

## 📝 Paso 1: Elegir Nombre del Repositorio

Recomendación: **`rag-vector-stores-comparison`**

Otras opciones:
- `rag-vector-comparison`
- `vector-stores-benchmark`
- `multi-vector-store-rag`

## 🚀 Paso 2: Comandos para Subir a GitHub

### Opción A: Desde la Terminal (Recomendado)

```bash
# 1. Inicializar git (si no está inicializado)
cd /Users/josediaz/Projects/JoeDayz/rags
git init

# 2. Agregar todos los archivos
git add .

# 3. Hacer commit inicial
git commit -m "Initial commit: Unified RAG repository with FAISS, Pinecone, and Weaviate support"

# 4. Crear repositorio en GitHub (hazlo manualmente en github.com o usa gh CLI)
#    - Ve a https://github.com/new
#    - Nombre: rag-vector-stores-comparison
#    - Descripción: "RAG chatbot comparing FAISS, Pinecone, and Weaviate vector stores"
#    - Público o Privado según prefieras
#    - NO inicialices con README, .gitignore o license (ya los tenemos)

# 5. Conectar con el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/rag-vector-stores-comparison.git
# O si usas SSH:
# git remote add origin git@github.com:TU_USUARIO/rag-vector-stores-comparison.git

# 6. Subir todo
git branch -M main
git push -u origin main
```

### Opción B: Usando GitHub CLI (gh)

Si tienes `gh` instalado:

```bash
# 1. Inicializar git
git init
git add .
git commit -m "Initial commit: Unified RAG repository"

# 2. Crear repositorio en GitHub y subir
gh repo create rag-vector-stores-comparison --public --source=. --remote=origin --push
```

## 📋 Checklist Antes de Subir

- [ ] Revisar `.gitignore` (ya está configurado)
- [ ] Revisar que no haya archivos sensibles (API keys, etc.)
- [ ] Verificar que `backend/env.example` no tenga datos reales
- [ ] Revisar que `README.md` esté completo
- [ ] Verificar que no haya archivos temporales grandes

## 🔒 Seguridad

**IMPORTANTE**: Antes de subir, verifica que:

1. ✅ `.env` está en `.gitignore` (ya está)
2. ✅ `env.example` no tiene API keys reales (solo placeholders)
3. ✅ No hay archivos con credenciales hardcodeadas
4. ✅ `venv/` y `node_modules/` están en `.gitignore`

## 📝 Descripción Sugerida para GitHub

```
RAG chatbot comparing FAISS, Pinecone, and Weaviate vector stores. 
Unified repository with modular architecture, benchmarking tools, 
and easy switching between vector stores.
```

## 🏷️ Tags Sugeridos

- `rag`
- `vector-store`
- `faiss`
- `pinecone`
- `weaviate`
- `langchain`
- `fastapi`
- `react`
- `benchmarking`
- `comparison`

## 📄 Licencia

Si quieres agregar una licencia, puedes usar MIT (ya hay un LICENSE en los repos antiguos).


#!/bin/bash

# Script para inicializar y subir el repositorio a GitHub
# Uso: ./scripts/setup_github.sh [nombre-del-repo]

set -e

REPO_NAME=${1:-"rag-vector-stores-comparison"}
GITHUB_USER=${GITHUB_USER:-""}

echo "🚀 Configurando repositorio Git para: $REPO_NAME"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "README.md" ]; then
    echo "❌ Error: No estás en el directorio raíz del proyecto"
    exit 1
fi

# 1. Inicializar git si no está inicializado
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositorio Git..."
    git init
    echo "✅ Repositorio Git inicializado"
else
    echo "✅ Repositorio Git ya está inicializado"
fi

# 2. Verificar que .gitignore existe
if [ ! -f ".gitignore" ]; then
    echo "❌ Error: .gitignore no encontrado"
    exit 1
fi

# 3. Agregar todos los archivos
echo ""
echo "📝 Agregando archivos al staging..."
git add .

# 4. Verificar que no hay archivos sensibles
echo ""
echo "🔍 Verificando archivos sensibles..."
if git diff --cached --name-only | grep -E "\.env$|\.env\." | grep -v "env.example"; then
    echo "⚠️  ADVERTENCIA: Se encontraron archivos .env en el staging"
    echo "   Estos archivos NO deberían subirse a GitHub"
    echo "   ¿Deseas continuar? (s/n)"
    read -r response
    if [[ ! "$response" =~ ^[Ss]$ ]]; then
        echo "❌ Operación cancelada"
        exit 1
    fi
fi

# 5. Hacer commit inicial
echo ""
echo "💾 Creando commit inicial..."
git commit -m "Initial commit: Unified RAG repository with FAISS, Pinecone, and Weaviate support

- Modular architecture with factory pattern
- Support for FAISS (local), Pinecone (cloud), and Weaviate (cloud/local)
- Unified FastAPI backend
- React frontend
- Integrated benchmarking script
- Comprehensive documentation"

echo "✅ Commit inicial creado"

# 6. Crear rama main si no existe
echo ""
echo "🌿 Configurando rama main..."
git branch -M main 2>/dev/null || true

# 7. Instrucciones para conectar con GitHub
echo ""
echo "="*60
echo "✅ Repositorio local configurado exitosamente"
echo "="*60
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Crea el repositorio en GitHub:"
echo "   - Ve a https://github.com/new"
echo "   - Nombre: $REPO_NAME"
echo "   - Descripción: 'RAG chatbot comparing FAISS, Pinecone, and Weaviate vector stores'"
echo "   - Público o Privado según prefieras"
echo "   - NO inicialices con README, .gitignore o license"
echo ""
echo "2. Conecta con el repositorio remoto:"
echo "   git remote add origin https://github.com/TU_USUARIO/$REPO_NAME.git"
echo "   # O si usas SSH:"
echo "   # git remote add origin git@github.com:TU_USUARIO/$REPO_NAME.git"
echo ""
echo "3. Sube todo a GitHub:"
echo "   git push -u origin main"
echo ""
echo "O si tienes GitHub CLI (gh) instalado:"
echo "   gh repo create $REPO_NAME --public --source=. --remote=origin --push"
echo ""


#!/bin/bash

# Script para configurar el entorno virtual para el benchmarking
# Este script crea un venv e instala todas las dependencias necesarias

echo "🚀 Configurando entorno virtual para benchmarking..."
echo ""

# Crear venv si no existe
if [ ! -d "venv_benchmark" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv_benchmark
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar venv
echo ""
echo "🔧 Activando entorno virtual..."
source venv_benchmark/bin/activate

# Actualizar pip
echo ""
echo "📥 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo ""
echo "📚 Instalando dependencias..."
pip install -r requirements_benchmark.txt

echo ""
echo "✅ Setup completado!"
echo ""
echo "Para activar el entorno virtual manualmente:"
echo "  source venv_benchmark/bin/activate"
echo ""
echo "Para ejecutar el benchmark:"
echo "  python benchmark_comparison.py"


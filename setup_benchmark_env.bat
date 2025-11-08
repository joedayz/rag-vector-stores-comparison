@echo off
REM Script para configurar el entorno virtual para el benchmarking en Windows
REM Este script crea un venv e instala todas las dependencias necesarias

echo 🚀 Configurando entorno virtual para benchmarking...
echo.

REM Crear venv si no existe
if not exist "venv_benchmark" (
    echo 📦 Creando entorno virtual...
    python -m venv venv_benchmark
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual ya existe
)

REM Activar venv
echo.
echo 🔧 Activando entorno virtual...
call venv_benchmark\Scripts\activate.bat

REM Actualizar pip
echo.
echo 📥 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo 📚 Instalando dependencias...
pip install -r requirements_benchmark.txt

echo.
echo ✅ Setup completado!
echo.
echo Para activar el entorno virtual manualmente:
echo   venv_benchmark\Scripts\activate
echo.
echo Para ejecutar el benchmark:
echo   python benchmark_comparison.py

pause


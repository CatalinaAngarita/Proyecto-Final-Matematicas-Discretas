#!/bin/bash
# =============================================================================
# Diana Nails Smart Booking - Setup Script
# =============================================================================
# Uso: bash scripts/setup.sh
# =============================================================================

set -e

echo "============================================"
echo " Diana Nails Smart Booking - Setup"
echo "============================================"

echo ""
echo "[1/5] Creando entorno virtual..."
python -m venv venv
echo "OK"

echo ""
echo "[2/5] Activando entorno e instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "OK"

echo ""
echo "[3/5] Configurando variables de entorno..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Archivo .env creado desde .env.example"
    echo "⚠️  Edita .env con tus credenciales de base de datos antes de continuar."
fi
echo "OK"

echo ""
echo "[4/5] Ejecutando migraciones..."
python manage.py migrate
echo "OK"

echo ""
echo "[5/5] Cargando datos iniciales..."
python manage.py shell < scripts/create_superuser.py
python manage.py shell < scripts/seed_data.py
echo "OK"

echo ""
echo "============================================"
echo " Setup completado exitosamente!"
echo "============================================"
echo ""
echo "Comandos útiles:"
echo "  python manage.py runserver   # Iniciar servidor"
echo "  python manage.py createsuperuser  # Crear admin"
echo "  python manage.py shell < scripts/seed_data.py  # Cargar datos"
echo ""
echo "Accede al panel admin en: http://127.0.0.1:8000/admin/"
echo "============================================"

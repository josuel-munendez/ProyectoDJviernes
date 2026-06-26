#!/usr/bin/env bash
set -e

echo "==> Creando entorno virtual..."
python3 -m venv entorno

echo "==> Activando entorno virtual..."
source entorno/bin/activate

echo "==> Instalando dependencias..."
pip install -r requirements.txt --quiet

echo "==> Aplicando migraciones..."
cd dcrm
python manage.py migrate --noinput

echo "==> Cargando datos de seed..."
python manage.py seed_data

echo ""
echo "===================================="
echo "  Setup completo!"
echo "  Ejecuta: cd dcrm && python manage.py runserver"
echo "  O desde la raiz: ../manage.py runserver"
echo "===================================="

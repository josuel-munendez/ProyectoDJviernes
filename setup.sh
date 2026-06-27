#!/usr/bin/env bash
set -e

echo "==> Creando entorno virtual..."
python3 -m venv entorno

echo "==> Activando entorno virtual..."
source entorno/bin/activate

echo "==> Instalando dependencias..."
pip install -r requirements.txt --quiet

echo "==> (Opcional) Intentando instalar mysqlclient..."
pip install mysqlclient==2.2.8 --quiet 2>/dev/null && echo "    mysqlclient instalado (MySQL disponible)" || echo "    mysqlclient no disponible - usando SQLite"

echo "==> Aplicando migraciones..."
cd dcrm && python manage.py migrate --noinput

echo "==> Cargando datos de seed..."
python manage.py seed_data

echo ""
echo "===================================="
echo "  Setup completo!"
echo "  Ejecuta: cd dcrm && python manage.py runserver"
echo "  O desde la raiz: python manage.py runserver"
echo "===================================="

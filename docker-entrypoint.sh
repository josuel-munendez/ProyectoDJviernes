#!/bin/bash
set -e

# Ensure data directory exists for persistent database
DB_DIR=$(dirname "${DJANGO_DB_PATH:-db.sqlite3}")
mkdir -p "$DB_DIR"

echo "==> Applying database migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput --clear

# Seed only once (flag file persists in data volume)
SEED_FLAG="${DB_DIR}/.seed_done"
if [ ! -f "$SEED_FLAG" ]; then
    echo "==> Loading seed data..."
    python manage.py seed_data
    touch "$SEED_FLAG"
else
    echo "==> Seed data already loaded. Skipping."
fi

echo "==> Starting gunicorn..."
exec gunicorn dcrm.wsgi:application --bind 0.0.0.0:8000

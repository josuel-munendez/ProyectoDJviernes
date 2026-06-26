#!/bin/bash
set -e

echo "==> Waiting for database..."
if [ "$DJANGO_DB_ENGINE" = "django.db.backends.mysql" ]; then
    until mysqladmin ping -h"${DJANGO_DB_HOST:-db}" -u"${DJANGO_DB_USER:-dcrm_user}" -p"${DJANGO_DB_PASSWORD:-DcrmPass2026!}" --silent 2>/dev/null; do
        echo "Waiting for MySQL..."
        sleep 2
    done
    echo "MySQL is ready!"
else
    DB_DIR=$(dirname "${DJANGO_DB_PATH:-db.sqlite3}")
    mkdir -p "$DB_DIR"
fi

echo "==> Applying database migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput --clear

# Seed only once
if python manage.py seed_data --check 2>/dev/null; then
    echo "==> Seed data already loaded. Skipping."
else
    echo "==> Loading seed data..."
    python manage.py seed_data
fi

echo "==> Starting gunicorn..."
exec gunicorn dcrm.wsgi:application --bind 0.0.0.0:8000

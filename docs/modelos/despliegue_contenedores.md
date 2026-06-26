# Despliegue con Contenedores

## Resumen

El CRM está containerizado con Docker/Podman para facilitar su despliegue en cualquier entorno. La imagen incluye el servidor Gunicorn, Whitenoise para archivos estáticos, y un entrypoint que automatiza la configuración inicial.

## Arquitectura del Contenedor

```
┌──────────────────────────────────────┐
│         Docker Container             │
│                                      │
│  ┌────────────────────────────────┐  │
│  │     docker-entrypoint.sh       │  │
│  │         (entrypoint)           │  │
│  └──────────┬─────────────────────┘  │
│             │                        │
│  ┌──────────▼─────────────────────┐  │
│  │     python manage.py migrate   │  │
│  └──────────┬─────────────────────┘  │
│             │                        │
│  ┌──────────▼─────────────────────┐  │
│  │  python manage.py collectstatic│  │
│  └──────────┬─────────────────────┘  │
│             │                        │
│  ┌──────────▼─────────────────────┐  │
│  │   python manage.py seed_data   │  │
│  │    (solo si BD vacía)          │  │
│  └──────────┬─────────────────────┘  │
│             │                        │
│  ┌──────────▼─────────────────────┐  │
│  │   gunicorn dcrm.wsgi:app       │  │
│  │   --bind 0.0.0.0:8000          │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │    Whitenoise Middleware       │  │
│  │    (static file serving)       │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
         │
         │ port 8000
         ▼
    Cliente / Navegador
```

## Componentes

### Dockerfile (`Dockerfile`)
- **Base**: `python:3.12-slim` (Debian, ~120MB)
- **Dependencias**: `requirements.prod.txt` (Django, Gunicorn, Whitenoise, sqlparse, asgiref)
- **Build-time**: `collectstatic` para cachear archivos estáticos en la imagen
- **Runtime**: Entrypoint script

### docker-compose.yml
- **Servicio**: `web` con build local
- **Puerto**: `8000:8000`
- **Volumen**: `dcrm_data:/app/data` (persistencia de BD SQLite)
- **Variables de entorno**: SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_PATH

### docker-entrypoint.sh
Script de entrada que ejecuta en orden:
1. Crear directorio de datos
2. Migraciones de BD
3. Recolectar estáticos
4. Seed data (una vez, con flag file)
5. Iniciar Gunicorn

## Whitenoise

Middleware para servir archivos estáticos en producción sin necesidad de nginx:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- después de Security
    ...
]
```

- Sirve `STATIC_ROOT` automáticamente
- Soporta compresión gzip/brotli
- Cache headers para rendimiento

## Persistencia de Datos

La base de datos SQLite se almacena en un volumen Docker:

```yaml
volumes:
  - dcrm_data:/app/data
```

Configurado via `DJANGO_DB_PATH=/app/data/db.sqlite3` para separar la BD del código de la aplicación.

## Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | (key interna) | Clave secreta Django |
| `DJANGO_DEBUG` | `False` | Modo debug |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,0.0.0.0` | Hosts permitidos |
| `DJANGO_DB_PATH` | `db.sqlite3` | Ruta BD SQLite |

## Uso

```bash
# Construir y ejecutar
docker compose up -d

# O con Podman
podman-compose up -d

# Ejecutar seed manualmente
docker exec dcrm_crm python manage.py seed_data

# Ver logs
docker logs dcrm_crm -f

# Detener
docker compose down
```

## Flujo de Request

```
Navegador → :8000 → Gunicorn → Django WSGI → Whitenoise (static)
                                              → URL dispatcher → View → Template → Response
```

## Security Headers (4 Capas)

Implementados en `settings.py`:
1. `SECURE_CONTENT_TYPE_NOSNIFF = True`
2. `SECURE_BROWSER_XSS_FILTER = True`
3. `SESSION_COOKIE_HTTPONLY = True`
4. `SESSION_COOKIE_SAMESITE = 'Lax'`
5. `CSRF_COOKIE_HTTPONLY = True`

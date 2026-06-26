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

### Capa 1 - HTML5
- Atributos `required`, `minlength`, `type="email"`, `type="password"` en todos los inputs
- `autocomplete` para gestion de contraseñas

### Capa 2 - JavaScript (Frontend)
- Validacion client-side al enviar formularios
- Clase `is-invalid` para feedback visual en errores
- Prevencion de envio si hay campos invalidos

### Capa 3 - Django (Backend)
- `@login_required` en todas las vistas protegidas
- `has_admin_role()` para control granular por perfil
- `RegexValidator` en campos criticos (usuario, password, email, telefono)
- CSRF tokens en todos los formularios
- `PasswordChangeForm` con validacion de historial

### Capa 4 - Base de Datos
- Tipos estrictos: `CharField`, `EmailField`, `DecimalField`, `IntegerField`
- Restricciones: `unique`, `blank`, `null`, `default`
- Campos privados (`_rol`, `_telefono`, `_direccion`) no expuestos en formularios
- `db_column` para separar nombre interno del nombre en BD

### Headers HTTP (settings.py + middleware)
Implementados en `settings.py` y `core/middleware.py`:
1. `SECURE_CONTENT_TYPE_NOSNIFF = True`
2. `SECURE_BROWSER_XSS_FILTER = True`
3. `SESSION_COOKIE_HTTPONLY = True`
4. `SESSION_COOKIE_SAMESITE = 'Lax'`
5. `CSRF_COOKIE_HTTPONLY = True`
6. `X-Frame-Options: DENY` (via SecurityHeadersMiddleware)
7. `Referrer-Policy: strict-origin-when-cross-origin`
8. `Permissions-Policy: camera=(), microphone=(), geolocation=()`

### Admin Django Restringido
- Solo superusuarios pueden acceder a `/admin/`
- Custom `SuperuserAdminSite` sobreescribe `has_permission()`
- Roles `admin`, `gestor`, `vendedor`, `cliente` no tienen acceso aunque naveguen directamente

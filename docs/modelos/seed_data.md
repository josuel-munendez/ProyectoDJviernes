# Sistema de Seed Data

## Resumen

El proyecto incluye un sistema de carga de datos de ejemplo para facilitar pruebas y demostraciones. Se implementó mediante un comando de gestión personalizado que carga datos desde un fixture JSON, remapeando claves foráneas correctamente.

## Arquitectura

```
initial_data.json (fixture)
       |
       v
seed_data.py (management command)
       |
       v
  Django ORM
       |
       v
   SQLite DB
```

### Componentes

1. **Fixture**: `website/fixtures/initial_data.json` — 42 registros en 6 modelos
2. **Comando**: `website/management/commands/seed_data.py` — Lógica de carga
3. **Entrypoint**: `docker-entrypoint.sh` — Ejecución automática en contenedor

## Modelos y Datos

| Modelo | Registros | Dependencia |
|--------|-----------|-------------|
| `auth.User` | 4 | Ninguna |
| `usuarios.UserProfile` | 4 | User |
| `website.Record` | 8 | Ninguna |
| `catalogo.Categoria` | 6 | Ninguna |
| `productos.Producto` | 12 | Ninguna |
| `catalogo.Catalogo` | 8 | Categoria, Producto |

## Usuarios de Prueba

| Usuario | Rol | Password | Superuser | Staff |
|---------|-----|----------|-----------|-------|
| admin | Administrador | admin123 | Sí | Sí |
| gestor | Gestor | gestor123 | No | Sí |
| vendedor | Vendedor | vendedor123 | No | No |
| cliente | Cliente | cliente123 | No | No |

## Algoritmo de Carga

1. Limpiar datos existentes en orden FK-safe (Catálogo → Producto → Categoría → Record → Perfil → Usuario)
2. Para cada entrada del fixture:
   - Si es `auth.User`: crear con `create_user()` (password hasheado), guardar mapping PK
   - Si es `usuarios.UserProfile`: lookup user_id via PK mapping, `update_or_create`
   - Si es `catalogo.Categoria` o `productos.Producto`: crear, guardar mapping PK
   - Si es `catalogo.Catalogo`: lookup categoria_id y producto_id via PK mapping, crear
   - Si es `website.Record`: crear directamente
3. Commit transaccional

## PK Mapping

Las claves primarias del fixture no coinciden con las de la BD después de borrar datos previos (SQLite no reinicia auto-increment en DELETE). Se utiliza un diccionario `pk_map` con tuplas `(model_name, old_pk) -> new_pk`:

```
pk_map = {
    ("auth.user", 1): 5,   # admin: fixture PK 1 → BD PK 5
    ("catalogo.categoria", 1): 7,  # Electronica: fixture PK 1 → BD PK 7
    ...
}
```

## Entrypoint Docker

El contenedor ejecuta el seed automáticamente en el primer inicio. Usa un archivo flag (`.seed_done` en el volumen de datos) para evitar reseed en reinicios:

```bash
if [ ! -f "${DB_DIR}/.seed_done" ]; then
    python manage.py seed_data
    touch "${DB_DIR}/.seed_done"
fi
```

## Uso Manual

```bash
# Local
cd dcrm && python manage.py seed_data

# Contenedor
docker exec -it dcrm_crm python manage.py seed_data
```

# ProyectoDJviernes - Sistema CRM

Sistema de gestión de clientes (CRM) desarrollado en Django con arquitectura modular, POO, principios SOLID y 4 capas de seguridad.

## Stack Tecnológico

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Django | 6.0.6 | Framework web |
| Bootstrap 5 | 5.3.x | UI components (local) |
| Bootstrap Icons | 1.11.3 | Iconografía (local) |
| MySQL 8.0+ | 8.0 / 9.x | Base de datos |
| Gunicorn | 26.0.0 | Servidor producción |
| Python | 3.12+ | Lenguaje |

## Diseño UI Moderno

El sistema cuenta con un diseño propio distintivo (apartado del tema original del instructor):

- **Paleta de colores**: Índigo primario (#4F46E5), sky secundario (#0EA5E9), ámbar acento (#F59E0B)
- **Sidebar degradado**: Gradiente púrpura oscuro (#1E1B4B → #312E81)
- **Dashboard Bento-Grid**: Layout de tarjetas tipo bento-grid con estadísticas, actividad reciente y accesos rápidos
- **Glassmorfismo**: Efecto de vidrio esmerilado en navbar y tarjetas
- **Animaciones**: Fade-in, slide-in, stagger en elementos del dashboard
- **Responsive**: Offcanvas sidebar en móviles, layout adaptativo
- **Login**: Tarjeta centrada con fondo degradado (reemplaza el split original del instructor)
- **Recursos 100% locales**: Bootstrap CSS/JS e iconos servidos internamente sin CDNs
- **Catálogo de Productos (Galería)**: Vista pública con tarjetas de producto, filtros por categoría y búsqueda
- **Seguridad 4 capas**: HTML5 + JavaScript + Django + Base de Datos en cada formulario
- **Admin Django restringido**: Solo superusuarios pueden acceder a `/admin/`

## Módulos

- **website**: CRUD principal de clientes (Record) con tabla de datos y paginación
- **usuarios**: Gestión de usuarios con roles (Cliente, Vendedor, Gestor, Admin) y perfiles
- **productos**: CRUD de productos con stock y precios
- **catalogo**: Categorías y catálogos que vinculan productos con categorías
- **core**: Capa base con servicios, repositorios, validadores y seguridad

## Seed Data

El proyecto incluye datos de ejemplo para pruebas inmediatas. Ejecutar después de migrar:

```bash
python manage.py seed_data
```

### Usuarios de prueba

| Usuario | Rol | Password | Staff | Superuser |
|---------|-----|----------|-------|-----------|
| `admin` | Administrador | `admin123` | ✅ | ✅ |
| `gestor` | Gestor | `gestor123` | ✅ | ❌ |
| `vendedor` | Vendedor | `vendedor123` | ❌ | ❌ |
| `cliente` | Cliente | `cliente123` | ❌ | ❌ |

### Datos incluidos

- **8 registros** de clientes colombianos (Bogotá, Medellín, Cali, Barranquilla, etc.)
- **6 categorías**: Electrónica, Ropa y Accesorios, Hogar, Deportes, Libros, Juguetes
- **12 productos** con precios en COP y stock
- **8 catálogos** vinculando productos a categorías

## Roles del Sistema

| Rol | Descripción | Acceso |
|-----|-------------|--------|
| Cliente | Acceso básico de lectura | Ver registros, catálogo público, perfil |
| Vendedor | Gestión de clientes | CRUD clientes, búsqueda, catálogo público |
| Gestor | Administración de productos y catálogos | CRUD clientes, CRUD productos, CRUD catálogos, exportar CSV |
| Admin | Acceso completo (excepto Django admin) | Todo excepto /admin/ |
| Superuser | Acceso total | Todo incluido /admin/ |

## Quick Start (Cualquier SO)

### Requisitos mínimos

| Opción | Requisito |
|--------|-----------|
| **Solo Python** | Python 3.12+ y pip |
| **Solo Docker** | Docker y Docker Compose |

### Opción 1: Solo Python (SQLite) — recomendado para pruebas rápidas

```bash
# 1. Clonar
git clone https://github.com/josuel-munendez/ProyectoDJviernes.git
cd ProyectoDJviernes

# 2. Setup automático
make setup                    # Linux/macOS (si tienes make)
# O:
bash setup.sh                 # Linux/macOS
# O Windows PowerShell:
# .\setup.ps1

# 3. Iniciar servidor
cd dcrm && python manage.py runserver
```

Abrir http://localhost:8000

### Opción 2: Solo Python con MySQL

```bash
# 1. Preparar MySQL (o usa Docker: ver más abajo)
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS dcrm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'dcrm_user'@'localhost' IDENTIFIED BY 'DcrmPass2026!';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON dcrm.* TO 'dcrm_user'@'localhost'; FLUSH PRIVILEGES;"

# 2. Clonar y setup
git clone https://github.com/josuel-munendez/ProyectoDJviernes.git
cd ProyectoDJviernes
python -m venv entorno
source entorno/bin/activate      # Linux/Mac
# .\entorno\Scripts\activate     # Windows
pip install -r requirements.txt

# 3. Migrar y ejecutar
cd dcrm
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### Opción 3: Solo Docker (todo incluido)

```bash
git clone https://github.com/josuel-munendez/ProyectoDJviernes.git
cd ProyectoDJviernes
docker compose up -d
# Esperar ~30s, luego abrir http://localhost:8000
```

### Usuarios de prueba (seed data)

| Usuario | Rol | Contraseña |
|---------|-----|-----------|
| `admin` | Administrador | `admin123` |
| `gestor` | Gestor | `gestor123` |
| `vendedor` | Vendedor | `vendedor123` |
| `cliente` | Cliente | `cliente123` |

## Despliegue con Contenedores (Docker / Podman)

El proyecto incluye un `docker-compose.yml` con dos servicios:

| Servicio | Imagen | Función |
|----------|--------|---------|
| `db` | `mysql:8.0` | Base de datos MySQL |
| `web` | Construcción local | Django + Gunicorn |

### Construir y ejecutar

```bash
# Usando docker-compose
docker compose up -d

# O usando podman-compose
podman-compose up -d
```

El contenedor `web` ejecuta automáticamente:
1. Espera a que MySQL esté listo (healthcheck)
2. Migraciones de base de datos
3. Recolección de archivos estáticos
4. Carga de seed data (solo si no existe)
5. Servidor Gunicorn en puerto 8000

Los datos de MySQL persisten en el volumen `dcrm_mysql_data`.

### Parar y limpiar

```bash
docker compose down          # Parar servicios
docker compose down -v       # Parar y borrar volúmenes (BD incluida)
```

### Variables de entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | (key por defecto) | Clave secreta de Django |
| `DJANGO_DEBUG` | `False` | Modo debug (True/False) |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,0.0.0.0` | Hosts permitidos |
| `DJANGO_DB_ENGINE` | `django.db.backends.mysql` | Motor de BD |
| `DJANGO_DB_NAME` | `dcrm` | Nombre BD |
| `DJANGO_DB_USER` | `dcrm_user` | Usuario BD |
| `DJANGO_DB_PASSWORD` | `DcrmPass2026!` | Contraseña BD |
| `DJANGO_DB_HOST` | `db` (Docker) / `localhost` (local) | Host BD |
| `DJANGO_DB_PORT` | `3306` | Puerto BD |
| `MYSQL_ROOT_PASSWORD` | `Admin12345!` | Contraseña root MySQL (solo contenedor) |
| `MYSQL_PASSWORD` | `DcrmPass2026!` | Contraseña dcrm_user (solo contenedor) |

## Seguridad (4 Capas)

1. **HTML5**: Validación nativa del navegador (`required`, `minlength`, `type="email"`, etc.) en todos los formularios
2. **JavaScript (Frontend)**: Validación client-side con feedback visual (`is-invalid`), prevención de envío si hay errores
3. **Django (Backend)**: Autenticación `@login_required`, autorización por roles, `RegexValidator` en campos críticos, CSRF tokens, formularios con validación
4. **Base de Datos**: Tipos de campo estrictos (`CharField`, `EmailField`, `DecimalField`), valores por defecto, restricciones `unique` y `blank/null`, campos privados (`_rol`) que no se exponen en formularios

## Patrones de Diseño Implementados

| Patrón | Ubicación | Descripción |
|--------|-----------|-------------|
| **Singleton** | `core/services.py` (CrudService) | Instancia única de servicios core |
| **Repository** | `core/repository.py` (DjangoRepository) | Capa de abstracción de acceso a datos |
| **Template Method** | `core/models.py` (BaseModel) | Métodos abstractos concreto/abstracto |
| **ModelForm** | `website/forms.py` | Generación automática de formularios desde modelos (DRY) |
| **Observer** | `usuarios/signals.py` | post_save signal para crear perfil al registrar usuario |
| **Strategy** | `core/validators.py` | Validación intercambiable vía RegexValidator y CustomValidator |

## Arquitectura y Modelado

Ver `docs/` para documentación completa:

| Documento | Descripción |
|-----------|-------------|
| [Modelo C4 (C1-C4)](docs/modelos/) | Contexto, Contenedores, Componentes, Código |
| [Diagramas UML](docs/uml/) | Clases, Casos de Uso, Secuencia, Arquitectura |
| [Matriz de Requerimientos](docs/modelos/matriz_requerimientos.md) | 22 requerimientos priorizados (MoSCoW) |
| [Historias de Usuario](docs/modelos/historias_usuario.md) | 10 HU con criterios de aceptación |
| [Modelo Relacional](docs/modelos/modelo_relacional.md) | Tablas, columnas y relaciones |
| [Diccionario de Datos](docs/modelos/diccionario_datos.md) | Descripción de cada campo |
| [Metodologías](docs/modelos/metodologias.md) | GitFlow, Kanban, MoSCoW, MVP, POO, SOLID |
| [Árboles (Problema/Objetivos/Decisiones)](docs/modelos/arboles.md) | Análisis del problema y soluciones |
| [Mapa de Navegación](docs/modelos/mapa_navegacion.puml) | Flujo de pantallas del sistema |
| [Mapa de Procesos](docs/modelos/mapa_procesos.puml) | Proceso completo del CRM |
| [Mapa de Empatía](docs/modelos/mapa_empatia.md) | Perfiles de usuario |
| [Patrones de Diseño](docs/arquitectura-patrones-diseño/patrones_diseno.md) | 30 patrones documentados |

## Estructura del Proyecto

```
ProyectoDJviernes/
├── dcrm/
│   ├── core/              # Capa base POO (modelos, servicios, repositorios)
│   ├── website/           # CRUD clientes, seed data, templates
│   ├── usuarios/          # Gestión de usuarios y roles
│   ├── productos/         # CRUD productos
│   ├── catalogo/          # Catálogos y categorías
│   └── dcrm/              # Configuración del proyecto
├── Dockerfile             # Construcción de imagen Docker
├── docker-compose.yml     # Orquestación de contenedores
├── docker-entrypoint.sh   # Script de inicio (migraciones + seed)
├── requirements.txt       # Dependencias de desarrollo
├── requirements.prod.txt  # Dependencias de producción
└── README.md
```

## Requisitos

Ver `requirements.txt` y `requirements.prod.txt`.

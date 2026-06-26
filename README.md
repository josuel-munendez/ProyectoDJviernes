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
- **Admin Django oculto**: El enlace a `/admin/` fue eliminado del sidebar. Solo se accede escribiendo la URL manualmente. Exclusivo para superusuarios creados vía `createsuperuser` (sin rol en el sistema)

## Módulos

- **website**: CRUD principal de clientes (Record) con tabla de datos y paginación
- **usuarios**: Gestión de usuarios con roles (Cliente, Vendedor, Gestor, Admin) y perfiles
- **productos**: CRUD de productos con stock y precios
- **catalogo**: Categorías y catálogos que vinculan productos con categorías
- **core**: Capa base con servicios, repositorios, validadores y seguridad

## Seed Data

El proyecto incluye un comando que carga datos de ejemplo para pruebas inmediatas:

```bash
python manage.py seed_data
```

### Datos incluidos

- **4 usuarios** con distintos roles (ver tabla de usuarios de prueba)
- **4 perfiles** de usuario vinculados
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
| Superuser | Acceso total (sin rol en BD) | Creado vía `createsuperuser`, /admin/ solo con URL manual |

## Cómo ejecutar el proyecto

Tienes **4 formas** de ejecutar el proyecto, elige la que mejor se adapte a tu entorno:

| # | Método | Requisitos | Base de datos | Ideal para |
|---|--------|------------|---------------|------------|
| 1 | Python + SQLite | Python 3.12+ | SQLite (archivo local) | Pruebas rápidas, cualquier SO |
| 2 | Python + MySQL | Python 3.12+ + MySQL 8.0+ | MySQL | Entorno de desarrollo completo |
| 3 | Docker / Podman | Docker + Docker Compose | MySQL (contenedor) | Sin instalar Python/MySQL local |
| 4 | Python + Docker MySQL | Python 3.12+ + Docker | MySQL (solo BD en Docker) | Desarrollo local con BD portátil |

---

### ▶️ Opción 1: Python + SQLite (la más rápida)

Sin instalar MySQL, ideal para probar el proyecto al instante.

```bash
# 1. Clonar
git clone https://github.com/josuel-munendez/ProyectoDJviernes.git
cd ProyectoDJviernes

# 2. Setup automático (elige uno):
make setup                          # Linux/macOS con make
bash setup.sh                       # Linux/macOS
.\setup.ps1                         # Windows PowerShell

# 3. Iniciar servidor de desarrollo
cd dcrm
python manage.py runserver
```

Abrir http://localhost:8000

**Manual paso a paso** (si no usas Makefile ni scripts):
```bash
python -m venv entorno
source entorno/bin/activate              # Linux/Mac
# .\entorno\Scripts\activate             # Windows
pip install -r requirements.txt
cd dcrm
export DJANGO_DB_ENGINE=django.db.backends.sqlite3   # Linux/Mac
# set DJANGO_DB_ENGINE=django.db.backends.sqlite3    # Windows CMD
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

---

### ▶️ Opción 2: Python + MySQL (desarrollo completo)

Requiere MySQL 8.0+ instalado y corriendo en tu máquina.

#### 2a. Preparar la base de datos MySQL

```bash
mysql -u root -p -e "
CREATE DATABASE IF NOT EXISTS dcrm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'dcrm_user'@'localhost' IDENTIFIED BY 'DcrmPass2026!';
GRANT ALL PRIVILEGES ON dcrm.* TO 'dcrm_user'@'localhost';
FLUSH PRIVILEGES;
"
```

O si prefieres usar Docker **solo para la base de datos** (ver Opción 4).

#### 2b. Clonar y configurar el entorno Python

```bash
git clone https://github.com/josuel-munendez/ProyectoDJviernes.git
cd ProyectoDJviernes

# Crear entorno virtual
python -m venv entorno

# Activar (según tu SO):
source entorno/bin/activate              # Linux / Mac
# .\entorno\Scripts\activate             # Windows PowerShell
# entorno\Scripts\activate.bat           # Windows CMD

# Instalar dependencias
pip install -r requirements.txt
```

#### 2c. Migrar, cargar datos y ejecutar

```bash
cd dcrm
python manage.py migrate          # Crear tablas en MySQL
python manage.py seed_data        # Cargar datos de ejemplo
python manage.py runserver        # Iniciar servidor en http://localhost:8000
```

---

### ▶️ Opción 3: Docker / Podman (todo en contenedores)

No necesitas Python ni MySQL instalados localmente. Solo Docker.

```bash
# Clonar
git clone https://github.com/josuel-munendez/ProyectoDJviernes.git
cd ProyectoDJviernes

# Iniciar todo (MySQL + Django + Gunicorn)
docker compose up -d

# Ver logs en vivo
docker compose logs -f

# Abrir http://localhost:8000
```

El contenedor `web` ejecuta automáticamente:
1. Espera a que MySQL esté listo (vía healthcheck)
2. Aplica migraciones de base de datos
3. Recolecta archivos estáticos
4. Carga seed data (solo la primera vez)
5. Inicia Gunicorn en el puerto 8000

**Comandos útiles:**

```bash
docker compose logs -f           # Ver logs en tiempo real
docker compose down              # Detener servicios
docker compose down -v           # Detener y borrar la BD
docker compose restart web       # Reiniciar solo Django
```

**Con Podman:**

```bash
podman-compose up -d
```

---

### ▶️ Opción 4: Python local + MySQL en Docker (híbrido)

Usa Docker solo para la base de datos, pero ejecuta Django directamente con Python.

```bash
# 1. Levantar MySQL en Docker
docker run -d --name dcrm_mysql -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=Admin12345! \
  -e MYSQL_DATABASE=dcrm \
  -e MYSQL_USER=dcrm_user \
  -e MYSQL_PASSWORD=DcrmPass2026! \
  mysql:8.0

# 2. Configurar Python (igual que Opción 2)
git clone https://github.com/josuel-munendez/ProyectoDJviernes.git
cd ProyectoDJviernes
python -m venv entorno
source entorno/bin/activate
pip install -r requirements.txt

# 3. Migrar, seed y ejecutar
cd dcrm
python manage.py migrate
python manage.py seed_data
python manage.py runserver

# 4. Al terminar, detener MySQL
docker stop dcrm_mysql
docker rm dcrm_mysql
```

---

### Usuarios de prueba (seed data)

Una vez ejecutado `python manage.py seed_data` (o iniciado con Docker), puedes iniciar sesión con:

| Usuario | Contraseña | Rol | Acceso a `/admin/` |
|---------|-----------|-----|-------------------|
| `admin_usu` | `admin123` | Admin | ❌ No |
| `gestor` | `gestor123` | Gestor | ❌ No |
| `vendedor` | `vendedor123` | Vendedor | ❌ No |
| `cliente` | `cliente123` | Cliente | ❌ No |

> **💡 Nota**: Los superusuarios NO se crean con `seed_data`. Usa `python manage.py createsuperuser` para crear usuarios con acceso total a `/admin/`. Los superusuarios existen fuera del sistema de roles y **no tienen un `rol` asignado** en la base de datos.
>
> ```bash
> python manage.py createsuperuser
> # Usuario: admin | Contraseña: admin123  (ejemplo de prueba)
> ```

---

### Variables de entorno

Copia `.env.example` a `.env` y ajusta según tu entorno:

```bash
cp .env.example .env
```

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | (clave por defecto) | Clave secreta de Django |
| `DJANGO_DEBUG` | `True` | Modo debug |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,0.0.0.0` | Hosts permitidos |
| `DJANGO_DB_ENGINE` | `django.db.backends.mysql` | Motor de BD (`...sqlite3` para SQLite) |
| `DJANGO_DB_NAME` | `dcrm` | Nombre BD (MySQL) |
| `DJANGO_DB_PATH` | `db.sqlite3` | Ruta archivo BD (SQLite) |
| `DJANGO_DB_USER` | `dcrm_user` | Usuario BD |
| `DJANGO_DB_PASSWORD` | `DcrmPass2026!` | Contraseña BD |
| `DJANGO_DB_HOST` | `localhost` | Host BD (`db` dentro de Docker) |
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
├── dcrm/                          # Proyecto Django
│   ├── core/                      #   Capa base POO (modelos, servicios, repositorios)
│   ├── website/                   #   CRUD clientes, seed data, templates
│   ├── usuarios/                  #   Gestión de usuarios y roles
│   ├── productos/                 #   CRUD productos
│   ├── catalogo/                  #   Catálogos y categorías
│   └── dcrm/                      #   Configuración del proyecto
├── Dockerfile                     # Construcción de imagen Docker
├── docker-compose.yml             # Orquestación de contenedores (web + MySQL)
├── docker-entrypoint.sh           # Script de inicio para contenedor web
├── requirements.txt               # Dependencias de Python
├── requirements.prod.txt          # Dependencias de producción
├── manage.py                      # Wrapper de manage.py desde la raíz
├── Makefile                       # Comandos make (setup, run, test, docker)
├── setup.sh                       # Script de setup para Linux/macOS
├── setup.ps1                      # Script de setup para Windows PowerShell
├── .env.example                   # Template de variables de entorno
├── .gitignore                     # Archivos ignorados por git
└── README.md                      # Este archivo
```

## Requisitos

Ver `requirements.txt` y `requirements.prod.txt`.

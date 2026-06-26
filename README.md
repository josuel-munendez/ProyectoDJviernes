# ProyectoDJviernes - Sistema CRM

Sistema de gestión de clientes (CRM) desarrollado en Django con arquitectura modular, POO, principios SOLID y 4 capas de seguridad.

## Módulos

- **website**: CRUD principal de clientes (Record)
- **usuarios**: Gestión de usuarios con roles (Cliente, Vendedor, Gestor, Admin)
- **productos**: CRUD de productos
- **catalogo**: Categorías y catálogos de productos
- **core**: Capa base con servicios, repositorios, validadores y seguridad

## Requisitos

Ver `requirements.txt`.

## Instalación

```bash
python -m venv entorno
source entorno/bin/activate
pip install -r requirements.txt
cd dcrm
python manage.py migrate
python manage.py runserver
```

## Roles

| Rol | Descripción |
|-----|-------------|
| Cliente | Acceso básico de lectura |
| Vendedor | Gestión de clientes y productos |
| Gestor | Administración de catálogos |
| Admin | Acceso completo + panel Django |

## Seguridad (4 Capas)

1. **Autenticación y Autorización**: `@login_required`, roles por perfil
2. **CSRF**: Tokens en todos los formularios
3. **Validación de Entrada**: Django Forms + RegexValidator
4. **Cabeceras HTTP**: X-Frame-Options, X-Content-Type-Options, etc.

## Patrones de Diseño

- **Singleton**: Core services (CrudService instancia única)
- **Repository**: Capa de acceso a datos (DjangoRepository)
- **Template Method**: BaseModel con métodos abstractos
- **ModelForm**: Generación automática de formularios (DRY)

## Documentación de Modelos y Diagramas

Ver `docs/modelos/` para documentación completa:

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
| [Patrones de Diseño](docs/patrones_diseno.md) | 6 patrones documentados |

## Estructura

```
dcrm/
├── core/          # Capa base POO (modelos, servicios, repositorios)
├── website/       # CRUD clientes
├── usuarios/      # Gestión de usuarios y roles
├── productos/     # CRUD productos
├── catalogo/      # Catálogos y categorías
└── dcrm/          # Configuración del proyecto
```

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

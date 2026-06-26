# Árbol del Problema

## Problema Central: Gestión manual e ineficiente de clientes y productos

```
                        ┌─────────────────────────────┐
                        │   Pérdida de oportunidades   │
                        │        de negocio            │
                        └──────────────┬──────────────┘
                                       │
                        ┌──────────────┴──────────────┐
                        │   Datos duplicados y        │
                        │   desactualizados           │
                        └──────────────┬──────────────┘
                                       │
               ┌───────────────────────┼───────────────────────┐
               │                       │                       │
    ┌──────────┴──────────┐ ┌──────────┴──────────┐ ┌──────────┴──────────┐
    │   Toma de decisiones │ │  Acceso no regulado │ │   Baja productividad│
    │   sin información    │ │  a la información   │ │   del equipo        │
    └──────────────────────┘ └─────────────────────┘ └─────────────────────┘
               │                       │                       │
    ┌──────────┴──────────┐ ┌──────────┴──────────┐ ┌──────────┴──────────┐
    │ No hay reportes     │ │ Sin control de roles│ │ Procesos manuales   │
    │ ni estadísticas     │ │ ni permisos         │ │ y repetitivos       │
    └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

# Árbol de Objetivos (Soluciones)

## Objetivo Central: CRM digital con control de acceso y gestión centralizada

```
                        ┌─────────────────────────────┐
                        │   Incremento de oportuni-   │
                        │   dades de negocio          │
                        └──────────────┬──────────────┘
                                       │
                        ┌──────────────┴──────────────┐
                        │   Datos centralizados y     │
                        │   actualizados en tiempo    │
                        │   real                      │
                        └──────────────┬──────────────┘
                                       │
               ┌───────────────────────┼───────────────────────┐
               │                       │                       │
    ┌──────────┴──────────┐ ┌──────────┴──────────┐ ┌──────────┴──────────┐
    │ Dashboard con      │ │ 4 capas de seguridad │ │ CRUD automatizado  │
    │ estadísticas       │ │ + roles de acceso    │ │ con paginación     │
    └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
               │                       │                       │
    ┌──────────┴──────────┐ ┌──────────┴──────────┐ ┌──────────┴──────────┐
    │ Exportación CSV     │ │ Login con roles     │ │ Interfaz responsive │
    │ + búsqueda          │ │ (Cliente, Vendedor, │ │ (móvil, tablet, pc) │
    │                     │ │ Gestor, Admin)      │ │                     │
    └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

# Árbol de Decisiones

```
¿Qué tipo de aplicación desarrollar?

├── ¿Aplicación de escritorio?
│   └── ✗ Descartado: difícil acceso multidispositivo
│
├── ¿Aplicación móvil nativa?
│   └── ✗ Descartado: requiere 2 versions (iOS/Android)
│
└── ¿Aplicación web? ← SELECCIONADO
    │
    ├── ¿Framework?
    │   ├── ¿React/Node.js?
    │   │   └── ✗ Descartado: requiere backend separado
    │   ├── ¿PHP/Laravel?
    │   │   └── ✗ Descartado: menos seguro por defecto
    │   └── ¿Python/Django? ← SELECCIONADO
    │       └── Razones: ORM seguro, admin built-in, autenticación robusta
    │
    ├── ¿Base de datos?
    │   ├── ¿PostgreSQL?
    │   │   └── ✗ Descartado: sobre-dimensionado para el proyecto
    │   ├── ¿MySQL?
    │   │   └── ⏳ Previsto para producción
    │   └── ¿SQLite? ← SELECCIONADO (desarrollo)
    │
    ├── ¿Arquitectura?
    │   ├── ¿Microservicios puros?
    │   │   └── ✗ Descartado: complejo para el alcance
    │   └── ¿Apps Django interconectadas? ← SELECCIONADO
    │
    └── ¿Metodología?
        ├── ¿Scrum?
        │   └── ⚠️ No aplica (equipo de 1 persona)
        ├── ¿Waterfall?
        │   └── ✗ Demasiado rígido
        └── ¿GitFlow + Kanban? ← SELECCIONADO
```

# Metodologías Aplicadas

## GitFlow (Control de Versiones)
**Estado:** ✅ Aplicado
- Ramas: `main` (producción) + `develop` (desarrollo)
- Ramas temporales: `feature/*`, `release/*`, `hotfix/*`
- 21 commits incrementales

## Kanban (Gestión de Tareas)
**Estado:** ✅ Aplicado (informal)
- Tablero personal con columnas: Pendiente / En Progreso / Hecho
- Ideal para equipos pequeños o unipersonales
- Visualización del flujo de trabajo

## MoSCoW (Priorización)
**Estado:** ✅ Aplicado en la matriz de requerimientos

| Prioridad | Descripción | Ejemplos |
|-----------|-------------|----------|
| **M**ust have | Imprescindible | CRUD, Login, Roles, Seguridad |
| **S**hould have | Importante | Dashboard, CSV, Búsqueda |
| **C**ould have | Deseable | Diseño responsive |
| **W**on't have | No se hará ahora | API REST, WebSockets |

## MVP - Minimum Viable Product
**Estado:** ✅ Definido
- **MVP**: Login + CRUD de clientes con paginación
- **V2**: Productos + Catálogo + Dashboard
- **V3**: Exportación CSV + Búsqueda + Diseño responsive

---

## Metodologías NO Aplicadas (con justificación)

| Metodología | Motivo |
|-------------|--------|
| **Scrum** | Requiere equipo de 3+ personas (Scrum Master, PO, Devs) |
| **DevOps** | Excede el alcance del proyecto (CI/CD, infraestructura cloud) |
| **TDD** | No se implementó por tiempo; el proyecto usa validación posterior |
| **BDD** | Requiere definición de comportamiento con stakeholders |
| **SDD** | No aplica para proyectos Django estándar |
| **Waterfall** | Demasiado rígido para un proyecto en evolución constante |
| **Espiral** | Sobredimensionado para un proyecto académico individual |

---

## Paradigmas de Programación

### POO (Programación Orientada a Objetos) ✅ Aplicado

| Principio | Implementación |
|-----------|---------------|
| **Abstracción** | `BaseModel` como clase abstracta base |
| **Encapsulación** | `UserProfile._rol` con getters `@property` |
| **Herencia** | Todos los modelos heredan de `BaseModel` |
| **Polimorfismo** | Métodos CRUD que se comportan según la entidad |

### Principios SOLID ✅

| Principio | Ejemplo |
|-----------|---------|
| **S** - Single Responsibility | Cada app tiene un propósito único |
| **O** - Open/Closed | `BaseModel` abierto a extensión, cerrado a modificación |
| **L** - Liskov | Todas las subclases pueden reemplazar a `BaseModel` |
| **I** - Interface Segregation | Cada modelo expone solo lo que necesita |
| **D** - Dependency Inversion | `CrudService` depende de abstracciones (Repository) |

### DRY (Don't Repeat Yourself) ✅
- `CrudService` singleton centraliza lógica repetitiva
- `BaseModel` evita repetir campos createdAt/updatedAt
- Templates base reutilizados con `{% extends %}`

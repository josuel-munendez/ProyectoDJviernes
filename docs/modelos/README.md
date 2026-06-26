# Modelos y Diagramas - CRM Django

Este directorio contiene la documentación de modelos, diagramas y metodologías del proyecto, organizados según el enfoque del **Modelo C4**.

## Estructura C4

| Nivel | Piezas que lo componen | Archivos |
|-------|----------------------|----------|
| **C1 - Contexto** | Diagrama de contexto del sistema | `c1_contexto.puml` |
| **C2 - Contenedores** | Gunicorn + Django + Whitenoise + SQLite | `c2_contenedores.puml` |
| **C3 - Componentes** | Componentes internos de cada app | `c3_componentes.puml` |
| **C4 - Código** | Diagrama de clases (en docs/uml/) | `../uml/diagrama_clases.puml` |

## Diagramas y Modelos

| Diagrama | Archivo | Descripción |
|----------|---------|-------------|
| Entidad-Relación | `diagrama_entidad_relacion.puml` | Modelo entidad-relación de la BD |
| Modelo Relacional | `modelo_relacional.md` | Tablas, columnas y relaciones |
| Diccionario de Datos | `diccionario_datos.md` | Descripción de cada campo |
| Casos de Uso | `../uml/diagrama_casos_uso.puml` | Interacciones usuario-sistema |
| Diagrama de Clases | `../uml/diagrama_clases.puml` | Clases, atributos y métodos |
| Secuencia Login | `../uml/diagrama_secuencia_login.puml` | Flujo de autenticación |
| Arquitectura | `../uml/diagrama_arquitectura.puml` | Arquitectura general del sistema |
| Flujo Login | `diagrama_flujo_login.puml` | Flowchart del proceso de login |
| Nodos (Despliegue) | `diagrama_nodos.puml` | Infraestructura Docker/Podman |
| Instancias | `diagrama_instancias.puml` | Instancias de apps y templates |
| Mapa de Navegación | `mapa_navegacion.puml` | Flujo de pantallas del sistema |
| Mapa de Procesos | `mapa_procesos.puml` | Proceso completo del CRM |
| **Seed Data** | `diagrama_seed_data.puml` | Flujo de carga de datos de ejemplo |
| **Componentes UI** | `diagrama_ui_componentes.puml` | Árbol de herencia de templates |
| **Diseño UI** | `diseno_ui.md` | Sistema de diseño moderno (índigo, bento-grid) |
| **Seed Data** | `seed_data.md` | Documentación del sistema de seed |
| **Despliegue Contenedores** | `despliegue_contenedores.md` | Documentación de Docker/Podman |

## Documentación de Requerimientos

| Documento | Archivo | Descripción |
|-----------|---------|-------------|
| Historias de Usuario | `historias_usuario.md` | 10 HU con criterios de aceptación |
| Matriz de Requerimientos | `matriz_requerimientos.md` | 22 RF/RNF con estado |
| Mapa de Empatía | `mapa_empatia.md` | Perfil de usuarios (Admin y Cliente) |
| Árboles | `arboles.md` | Problema, Objetivos y Decisiones |

## Metodologías

| Metodología | Archivo | Estado |
|-------------|---------|--------|
| GitFlow | `metodologias.md` | ✅ Aplicado |
| Kanban | `metodologias.md` | ✅ Aplicado |
| MoSCoW | `matriz_requerimientos.md` | ✅ Aplicado |
| MVP | `metodologias.md` | ✅ Definido |
| POO + SOLID + DRY | `metodologias.md` | ✅ Aplicado |
| Patrones de Diseño | `../arquitectura-patrones-diseño/patrones_diseno.md` | ✅ 30 documentados |

## Cómo visualizar los diagramas

Los archivos `.puml` (PlantUML) se pueden ver en:
1. https://www.plantuml.com/plantuml/uml/ — pegar el contenido
2. VS Code con extensión PlantUML — vista previa en vivo
3. `plantuml -tsvg diagrama.puml` — generar SVG/PNG localmente

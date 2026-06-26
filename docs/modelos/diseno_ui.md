# Sistema de Diseño UI - CRM Moderno

## Resumen

El sistema CRM fue rediseñado con una interfaz moderna y distintiva, separándose visualmente del diseño original del instructor. Se implementó una paleta de colores índigo, layout bento-grid, glassmorfismo y animaciones CSS.

## Paleta de Colores

| Rol | Color | Hex | Uso |
|-----|-------|-----|-----|
| Primario | Índigo | `#4F46E5` | Botones, enlaces, acentos |
| Secundario | Sky | `#0EA5E9` | Hovers, badges |
| Acento | Ámbar | `#F59E0B` | Alertas, notificaciones |
| Sidebar inicio | Púrpura oscuro | `#1E1B4B` | Fondo sidebar degradado |
| Sidebar fin | Índigo oscuro | `#312E81` | Fondo sidebar degradado |
| Fondo página | Gris claro | `#F3F4F6` | Background general |
| Texto oscuro | Pizarra | `#1F2937` | Texto principal |
| Éxito | Esmeralda | `#10B981` | Confirmaciones |
| Error | Rojo | `#EF4444` | Errores |

## Componentes de Diseño

### 1. Sidebar (`sidebar-crm`)
- Degradado vertical púrpura oscuro a índigo
- Iconos Bootstrap Icons en blanco con opacidad 0.7
- Active link resaltado con fondo blanco/índigo
- Versión offcanvas para móviles (`d-lg-none`)
- Footer con avatar, nombre de usuario y rol

### 2. Navbar (`navbar-crm`)
- Efecto glassmorphism (`backdrop-filter: blur(10px)`)
- Fondo semi-transparente con opacidad
- Avatar circular con inicial del usuario
- Dropdown de usuario alineado a la derecha

### 3. Dashboard (`bento-grid`)
- Layout tipo bento-grid con `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`
- Stat-cards con icono, valor, etiqueta y tendencia
- Tarjetas de distintos tamaños para crear ritmo visual
- Animación stagger al cargar

### 4. Tarjetas (`card-crm`)
- `border-radius: 16px` con sombra suave
- Hover con elevación (`transform: translateY(-4px)`)
- Header con borde inferior índigo
- Body con padding espaciado

### 5. Login (`login-card`)
- Tarjeta centrada en pantalla con fondo degradado pastel
- Input groups con iconos a la izquierda
- Toggle de visibilidad de contraseña (JavaScript)
- Animación fade-in en carga

### 6. Tablas (`table-crm`)
- Alternancia de colores en filas
- Hover con sombra ligera
- Badges para estados y roles
- Paginación estilizada (`pagination-crm`)

### 7. Formularios (`form-crm`)
- Labels con color índigo
- Inputs con borde sutil y focus ring
- Validación visual con bordes verdes/rojos
- Botones con iconos (`btn-crm`)

### 8. Alertas (`alert-crm`)
- Auto-dismiss después de 5 segundos (JavaScript)
- Iconos contextuales según tipo
- Animación slide-in desde arriba
- Colores: éxito (verde), error (rojo), warning (ámbar), info (azul)

## Animaciones CSS

| Clase | Animación | Aplicación |
|-------|-----------|------------|
| `.animate-fade-in` | Opacity 0→1 + translateY(20px)→0 | Contenedores principales |
| `.animate-slide-in` | Opacity 0→1 + translateY(-10px)→0 | Alertas |
| `.stagger-1` | Fade-in con delay 0.1s | Dashboard cards |
| `.stagger-2` | Fade-in con delay 0.2s | Dashboard cards |
| `.stagger-3` | Fade-in con delay 0.3s | Dashboard cards |
| `.stagger-4` | Fade-in con delay 0.4s | Dashboard cards |

## Responsive Design

| Breakpoint | Comportamiento |
|------------|----------------|
| `< 992px` | Sidebar se oculta, offcanvas toggle aparece |
| `992px - 1200px` | Bento-grid 2 columnas, sidebar compacto |
| `> 1200px` | Bento-grid 3-4 columnas, sidebar completo |

## Archivos de Recursos Locales

| Recurso | Ruta | Tipo |
|---------|------|------|
| Bootstrap 5.3.x CSS | `static/css/bootstrap.min.css` | Local |
| Bootstrap 5.3.x JS | `static/js/bootstrap.bundle.min.js` | Local |
| Bootstrap Icons CSS | `static/css/bootstrap-icons.css` | Local |
| Bootstrap Icons Font | `static/fonts/bootstrap-icons.woff2` | Local |
| Estilos personalizados | `static/css/custom.css` | Propio |

No se utilizan CDNs externas. Todos los recursos están integrados localmente en el proyecto.

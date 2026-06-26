# Diccionario de Datos

## website_record
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Identificador único del registro |
| created_at | DATETIME | Fecha y hora de creación automática |
| first_name | VARCHAR(50) | Nombre del cliente |
| last_name | VARCHAR(50) | Apellido del cliente |
| email | VARCHAR(100) | Correo electrónico del cliente |
| phone | VARCHAR(15) | Número de teléfono |
| address | VARCHAR(100) | Dirección física |
| city | VARCHAR(50) | Ciudad de residencia |
| state | VARCHAR(50) | Estado o departamento |
| zip_code | VARCHAR(10) | Código postal |

## usuarios_userprofile
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Identificador único del perfil |
| rol | VARCHAR(20) | Rol del usuario: Cliente, Vendedor, Gestor o Admin |
| telefono | VARCHAR(20) | Teléfono del usuario |
| direccion | TEXT | Dirección del usuario |
| user_id | INTEGER | FK al usuario de Django auth |

## productos_producto
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Identificador único del producto |
| nombre | VARCHAR(100) | Nombre del producto |
| descripcion | TEXT | Descripción detallada del producto |
| precio | DECIMAL(10,2) | Precio unitario del producto |
| stock | INTEGER | Cantidad disponible en inventario |

## catalogo_categoria
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Identificador único de la categoría |
| nombre | VARCHAR(100) | Nombre de la categoría (único) |
| descripcion | TEXT | Descripción de la categoría |

## catalogo_catalogo
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Identificador único de la relación |
| producto_id | INTEGER | FK al producto |
| categoria_id | INTEGER | FK a la categoría |

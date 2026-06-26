# Modelo Relacional

## Tabla: auth_user
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| id | INTEGER | PK, AutoIncrement |
| username | VARCHAR(150) | NOT NULL, UNIQUE |
| email | VARCHAR(254) | NOT NULL |
| password | VARCHAR(128) | NOT NULL |
| first_name | VARCHAR(150) | NOT NULL |
| last_name | VARCHAR(150) | NOT NULL |
| is_staff | BOOLEAN | NOT NULL, DEFAULT FALSE |
| is_superuser | BOOLEAN | NOT NULL, DEFAULT FALSE |
| date_joined | DATETIME | NOT NULL |

## Tabla: usuarios_userprofile
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| id | INTEGER | PK, AutoIncrement |
| rol | VARCHAR(20) | NOT NULL, CHECK('Cliente','Vendedor','Gestor','Admin') |
| telefono | VARCHAR(20) | NULL |
| direccion | TEXT | NULL |
| user_id | INTEGER | FK -> auth_user.id, UNIQUE |

## Tabla: website_record
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| id | INTEGER | PK, AutoIncrement |
| created_at | DATETIME | NOT NULL |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| email | VARCHAR(100) | NOT NULL |
| phone | VARCHAR(15) | NOT NULL |
| address | VARCHAR(100) | NOT NULL |
| city | VARCHAR(50) | NOT NULL |
| state | VARCHAR(50) | NOT NULL |
| zip_code | VARCHAR(10) | NOT NULL |

## Tabla: productos_producto
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| id | INTEGER | PK, AutoIncrement |
| created_at | DATETIME | NOT NULL |
| updated_at | DATETIME | NOT NULL |
| nombre | VARCHAR(100) | NOT NULL |
| descripcion | TEXT | NULL |
| precio | DECIMAL(10,2) | NOT NULL |
| stock | INTEGER | NOT NULL, DEFAULT 0 |

## Tabla: catalogo_categoria
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| id | INTEGER | PK, AutoIncrement |
| created_at | DATETIME | NOT NULL |
| updated_at | DATETIME | NOT NULL |
| nombre | VARCHAR(100) | NOT NULL, UNIQUE |
| descripcion | TEXT | NULL |

## Tabla: catalogo_catalogo
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| id | INTEGER | PK, AutoIncrement |
| created_at | DATETIME | NOT NULL |
| updated_at | DATETIME | NOT NULL |
| producto_id | INTEGER | FK -> productos_producto.id |
| categoria_id | INTEGER | FK -> catalogo_categoria.id |

## Relaciones
- `auth_user` 1:1 `usuarios_userprofile`
- `productos_producto` M:N `catalogo_categoria` vía `catalogo_catalogo`

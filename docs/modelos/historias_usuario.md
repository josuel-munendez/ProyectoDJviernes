# Historias de Usuario

## HU-1: Inicio de sesión
**Como** usuario del sistema  
**Quiero** iniciar sesión con mi usuario y contraseña  
**Para** acceder a las funcionalidades según mi rol

**Criterios de aceptación:**
- El formulario valida que usuario y contraseña no estén vacíos
- Muestra mensaje de error si las credenciales son inválidas
- Redirige al home tras login exitoso
- El menú se adapta según el rol del usuario

## HU-2: Registro de clientes
**Como** usuario autenticado  
**Quiero** registrar un nuevo cliente en el sistema  
**Para** mantener actualizada la base de datos de clientes

**Criterios de aceptación:**
- El formulario valida todos los campos con regex
- Los campos obligatorios están marcados
- Muestra mensaje de éxito al guardar
- El cliente aparece en la tabla de registros

## HU-3: Ver detalle de cliente
**Como** usuario autenticado  
**Quiero** hacer clic en un ID de cliente  
**Para** ver toda su información detallada

**Criterios de aceptación:**
- Muestra todos los campos del cliente en una tarjeta
- Tiene botones para volver, editar y eliminar

## HU-4: Editar cliente
**Como** usuario autenticado  
**Quiero** modificar los datos de un cliente existente  
**Para** mantener la información actualizada

**Criterios de aceptación:**
- El formulario se precarga con los datos actuales
- Valida los campos igual que el registro
- Guarda los cambios y redirige al home

## HU-5: Eliminar cliente
**Como** usuario autenticado  
**Quiero** eliminar un cliente del sistema  
**Para** depurar registros obsoletos

**Criterios de aceptación:**
- Pide confirmación antes de eliminar
- Elimina el registro y muestra mensaje de éxito

## HU-6: Paginación de registros
**Como** usuario autenticado  
**Quiero** navegar entre páginas de registros  
**Para** ver clientes sin scroll excesivo

**Criterios de aceptación:**
- Muestra 5 registros por página
- Botones: primera, anterior, números, siguiente, última
- Muestra "Página X de Y"

## HU-7: Gestión de productos
**Como** administrador  
**Quiero** crear, editar y eliminar productos  
**Para** mantener el catálogo de productos actualizado

## HU-8: Gestión de catálogo
**Como** administrador  
**Quiero** asignar productos a categorías  
**Para** organizar el catálogo de ventas

## HU-9: Dashboard de administrador
**Como** administrador  
**Quiero** ver estadísticas del sistema  
**Para** monitorear usuarios, clientes, productos y categorías

## HU-10: Exportar datos
**Como** usuario autenticado  
**Quiero** exportar los registros a CSV  
**Para** analizar los datos externamente

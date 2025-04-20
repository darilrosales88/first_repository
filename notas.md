# Validación de Permisos y Grupos de Usuarios

## Grupos de Usuarios Backend

- Se implementaron dos nuevos grupos de usuarios:
  - `AdminUFC`
  - `AdminNomencladores`

## Tareas Pendientes

### Backend

- Actualizar el sistema de validación de permisos
- Implementar la actualización de registros cuando se modifican los permisos de un usuario
- Asegurar que los permisos se reflejen correctamente en tiempo real

### Frontend

- Implementar sistema de validación de permisos
- Mostrar/ocultar funcionalidades según los permisos del usuario
- Actualizar la interfaz cuando cambien los permisos del usuario

### Estilos

- Faltan los estilos propuestos por karmal en los siguientes registros:
  - `Cargados/Descargados`
  - `Pendientes`

## Consideraciones

- Los cambios en permisos deben ser reflejados inmediatamente en la sesión del usuario
- Mantener sincronización entre los permisos del backend y frontend

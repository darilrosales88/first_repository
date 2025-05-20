# Validación de Permisos y Grupos de Usuarios

## Requisitos funcionales pinchando en talla

- Vagones y Productos
- Registros Por Situar
- Registros Situados
- Cargados 2 +2
- Registros Pendientes
- Registros en trenes
- Listo pal cliente casi

## Notas de Revision Antes de la Reunion Viernes 9 de Mayo

- Corregido problema de los DELETE en el CRUD
- Corregido Tablas de Vagones y Productos que habia problema en el adicionar a la hora de cargar los equipos ferroviarios en dependencia del combustible escogido
- Arreglada la Vista de Rotacion que traia problema en los componentes.
- Corregido Desplegable de productos en el adicionar de Situados Carga/Descarga
- Corregido que admin pueda borrar historial de cargados/descargados
- Corregido problemas de En Trenes correspondiente a mal registro de las instancias

## Tareas Pendientes

- Modal de producto vagon se desaparece en Arrastre
- Modificar los editar y los adicionar de los 3 estados Por Situar Situado Pendiente
- Solucionar problemas del serializer

## ISSUES Para crear

- Implementar Validaciones

### Registro de En Trenes

- La combinación de los campos Tipo equipo ferroviario, Estado, Producto, Origen, Destino, deben ser únicos, el valor especificado ya se encuentra en uso.

### Rotacion de vagones

- El campo Tipo equipo ferroviario debe ser único. Si hay una rotacion que use ese tipo equipo debe arrojar un error desde el serializer con su debido mensaje.

### Tiempo Estimado 3 dias.

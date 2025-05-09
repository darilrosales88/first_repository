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

- La hora de los registros no se estan creando con UTC+3 Hora Havana
- En cargados/Descargados se tiene que mostrar el Equipo Ferroviario solo los que su tipos coincidan con el tipo equipo Ferroviario que se halla selecionado
- Ahora en Trenes no puede guardar los registros porque depende de los vagones si estan disponibles o no.

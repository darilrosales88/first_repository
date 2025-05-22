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
- Implementar el editar de arrastres que no funciona como deberia
- Implementar que se pueda crear un informe operativo solamente por entidad
- Se necesita hacer que cuando se cree el informe operativo solo se vean los registros asociados a ese informe de esa entidad,

### Implementacion de filtro segun el id del informe Asociado

- ARRASTRES (check)
- En Trenes (Check)
- Rotacion(Check)
- Situados (Check)
- Cargados (check)
- Por Situar (check)
- Vagones y Productos (Check)

### Se actualizan el estado de los vagones al pasar a Listo el parte o Aprobado

- ARRASTRES (check)
- En Trenes (Check)
- Situados (Problem)
- Cargados (check)
- Por Situar (check)

### Problema al pasar a disponible los registros de Situados. Hay unas llamadas de mas

- Revisar views, serializer, funcion submit, y signals dependientes de este

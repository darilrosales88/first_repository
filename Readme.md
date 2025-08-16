# ChangeLOG V2.0.1

## Documentacion Automatica al backend
- Tenemos 2 endpoints principales `/api/doc` para la documentacion de los endpoints y los tipos de datos que recibe, con la estructura del crud
- `/api/redoc` para las rutas de los endpoints
- Para poder abrir el proyecto tienen que hacer `pip install -r requirements.txt`

## Se va a empezar a usar el la BD PostgresSQL
Por favor leer el [README.md](doc/CambioPOSTGRES.md) que es donde se hacen especificos los pasos para poder cambiar a postgres

## Politica de github a usar en el proyecto.
Por favor leer el [Git Policy](doc/PoliticaGit.md)

## Merge terminado

### Se completo el merge
- Se completo el merge entre las 4 ramas, hasta ahora pasaron los test, y parece no haber problema, pero hay que hacer una busqueda exhaustiva para poder seguir trabajando con esto.
- Se esta trabajando ya con la BD Postgres por favor leer documentacion relacionada.

### Correciones en CCDxProducto
- Se agrego un queryset `informe_ccd__id` para poder desplegar los estados asociados a un informe en especifico asi no muestra todos los estados de todos los informes operativos.
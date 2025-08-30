# ChangeLOG V2.0.0

## Documentacion Automatica al backend
- Tenemos 2 endpoints principales `/api/doc` para la documentacion de los endpoints y los tipos de datos que recibe, con la estructura del crud
- `/api/redoc` para las rutas de los endpoints
- Para poder abrir el proyecto tienen que hacer `pip install -r requirements.txt`

## Se va a empezar a usar el la BD PostgresSQL
Por favor leer el [README.md](doc/CambioPOSTGRES.md) que es donde se hacen especificos los pasos para poder cambiar a postgres

## Politica de github a usar en el proyecto.

### Estableceremos 2 ramas principales (`main`,`develop`).

### La rama main sera la principal del proyecto la cual sera la rama sobre la cual los clientes estaran usando y testeando la app.

* Sobre esta rama el unico comando de git que se debera hacer es git merge develop.

Para lograr la fusion de la rama `develop` con la rama `main` y asi entren los nuevos RF a ser usados por los usuarios. Para lograr esto `git checkout main` y seguido `git merge develop`.

* En la rama develop es donde se ira trabajando e iran implementando cada uno de los RF que tenga la app.

Para la programacion de los RF se deben tomar el siguiente algoritmo de trabajo:

1. Cada nueva funcionalidad/tarea se desarrolla en una rama separada:
usar este comando para la creacion de la rama`git checkout -b feature/login-authentication` 

2. Se trabaja en la funcionalidad sobre esta rama, se recomienda usar nombres descriptivos.
por ejemplo:
```
feature/nombre-feature  # Nueva funcionalidad
fix/nombre-error        # Corrección de bug
docs/actualizacion      # Cambios en documentación
```
3. Se recomienda ademas utilizar nombres descriptivos a la hora de hacer los commits:
```
feat: añadir autenticación con JWT
fix(login): corregir error de validación
docs: actualizar README.md
```
4. Una vez terminado el RF y este listo, asegurarse que se pasen los test de la app ejecutando el comando: `python manage.py test ufc `.
Por el momento estos son los unicos que hay funcionales, pero se seguira trabajando para poder agregar mas para tener un coverage de al menos el 50%


5. Luego de testear usar el comando `git checkout develop` se recomienda actualizar tu rama `develop` en local con `git pull origin develop` despues `git merge feature/login-authentication` y asi logramos incluir los nuevos RF en nuestra rama `develop`.

6. Una vez terminados los RF necesarios y se vayan a poner en produccion, pues se testean todos los RF de cada uno, se determinana NC, se hacen los fix y luego se termina haciendo un merge entre la rama main y la develop.

### Sobre la deteccion de NC o Bugs a corregir en produccion (rama `main`)
* Siempre se van a arreglar sobre la rama develop con el algoritmo de trabajo ya descrito anteriormente
* Luego que se resuelva pasara a la rama `main`

* **Solo por motivos de fuerza mayor se hara `hotfix` (Arreglar el problema sobre la rama main al tiempo que se va usando)**



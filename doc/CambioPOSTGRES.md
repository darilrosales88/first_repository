# Pasos para migrar una base de datos de SQLite a PostgreSQL en un proyecto Django

## 0. **Activar el entorno virtual**
    
```bash
.venv/Scripts/Activate
```

## 1. **Instala el driver de PostgreSQL para Python**
   ```bash
   pip install psycopg[binary]
   ```

## 2. **Hacer una copia de seguridad de la BD SQLITE**

    En este paso se puede copiar la BD a otra carpeta o hacer un comprimido

## 3. **Instalar la BD PostgreSQL en local en la computadora**

Para este paso se tiene que descargar 2 archivos de internet con un peso de aprox 200 mb 

- Descargar el archivo del instalador de la BD 
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

- Luego descargar PgAdmin:
https://www.pgadmin.org/download/pgadmin-4-windows

- Instalar los dos archivos descargados en un momento pedira introducir contrasena para el admin de la BD postgres en dicho caso se pondra:     
        
    - **admin**
    
- Si en algun momento te pierdes ver video: https://www.youtube.com/watch?v=ZgRkGfoy2nE ir a la parte donde hacen la instalacion de estos 2 archivos

## 4. **Creacion de la BD desde PgAdmin**

- Se abre el PgAdmin y aparecera una BD que se llama postgres que es por default, entonces click derecho te sale la opcion de crear nueva BD y le ponemos el nombre "mitrans_db" como mismo hacen en el video del paso anterior.

## 5. **Configuracion del settings.py de python en la raiz del proyecto**

El archivo de settings.py debe tener una seccion asi:
        
```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```
Comenta esas lineas y agrega estas:
```python
   DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "client_encoding": 'UTF8',
            "NAME":"mitrans_db",
            "USER":"postgres",
            "PASSWORD":"admin",
            "HOST":"localhost",
            "PORT":"5432",         
        }
    }
```
### Si has seguido todos los pasos hasta aqui deberias ya tener bien conectada tu BD Postgres con Django
---

## 6V1. Migrar Tablas para tu BD en Postgres.

En la Raiz del proyecto poner en la consola

```bash
python manage.py migrate --run-syncdb
```

Con esto ya se crean las tablas de los models en la BD postgres

## 7V1. Cargar los datos de los nomencladores

- Asegurarse que se tiene en la raiz del proyecto el archivo `nomencladores.json` que guarda los datos de los nomencladores antiguos que teniamos en la BD SQLITE

- En la Raiz del proyecto poner en la consola

```bash
python manage.py loaddata nomencladores.json
```

- Revisar en el log si da algun error y corregirlo, pueden haber diferentes errores
    1. id reptidos
    2. Constraints que son violadas
    3. Max value exceed

    **En cualquiera de los casos se deberia revisar el registro con problemas y corregirlo manualmente en el `nomencladores.json`**

### **Con estos pasos ya deberias tener los registros de los nomencladores cargados en tu BD postgres, de todas maneras usar el Pgadmin para comprobar que esten, ya falta poco para poder tener el proyecto funcional**


## 8V1. Creacion de los Grupos en el admin de DJANGO

- Crear nuevo SuperUsuario para el backend de Django `python manage.py createsuperuser`

    `username:`admin

    `pass:`Pass2022* 

- Montar el backend escribiendo en consola `python manage.py runserver`

- Abrir la direccion del backend http://127.0.0.1:8000/admin

- Ir a las pestanas de Grupos y Crear los siguientes grupos:
    
    * Admin -> Asignarle todos los permisos posibles
    * AdminNomencladores -> Asignarle todos los permisos de los nomencladores
    * VisualizadorNomencladores -> Solo se le agregaran los permisos de los visualizar de los nomencladores
    * AdminUFC -> Todos los permisos posibles de UFC
    * OperadorUFC -> Los permisos para el CRUD de todos los registros de UFC excepto los 2 que se llaman `puede_aprobar_parte`,`puede_rechazar_parte`. Agregarle ademas, todos los visualizar de los nomencladores. ya que les hace falta para poder conformar los registros de informes de UFC.
    * RevisorUFC -> Solamente se le agregaran los visualizar de UFC y `puede_aprobar_parte`,`puede_rechazar_parte`.
    * VisualizardorUFC -> Solo se le agregaran los permisos de los visualizar de UFC

## 6V2 Para hacer las migraciones hay otra manera mas simple
- Abrir PgAdmin
- Cargar los datos de mitrans_dbUTF.sql en el PgAdmin con la herramienta de importar.
- **Asegurarse que la BD este con un encoding UTF-8**



## 9. Comprobar que todo este OK, a Revisar la APP y poblarla con registros UFC

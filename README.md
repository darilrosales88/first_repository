# Pasos para migrar una base de datos de SQLite a PostgreSQL en un proyecto Django

0. **Activar el entorno virtual**

1. **Instala el driver de PostgreSQL para Python**
   ```bash
   pip install psycopg-binary
   ```

2. **Hacer una copia de seguridad de la BD SQLITE**

    En este paso se puede copiar la BD a otra carpeta o hacer un comprimido

3. **Instalar la BD PostgreSQL en local en la computadora**

    Para este paso se tiene que descargar 2 archivos de internet con un peso de aprox 200 mb 

    - Descargar el archivo del instalador de la BD 
    https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

    - Luego descargar PgAdmin
    https://www.pgadmin.org/download/pgadmin-4-windows

    - Instalar los dos archivos descargados en un momento pedira introducir contrasena para el admin de la BD postgres en dicho caso se pondra:     
        
        - **admin**
    
    - Si en algun momento te pierdes ver video: https://www.youtube.com/watch?v=ZgRkGfoy2nE ir a la parte donde hacen la instalacion de estos 2 archivos

4. **Creacion de la BD desde PgAdmin**

    - Se abre el PgAdmin y aparecera una BD que se llama postgres que es por default, entonces click derecho te sale la opcion de crear nueva BD y le ponemos el nombre "mitrans_db" como mismo hacen en el video del paso anterior.

5. **Configuracion del settings.py de python en la raiz del proyecto**

    El archivo de settings.py debe tener una seccion asi:
        
    ```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```
    Comenta estas lineas y agrega estas:
    ```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```
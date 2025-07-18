# Endpoints de CCDxPRODUCTO

## Para obtener los productos de UFC que estan asociados a un tipo de equipo usar el query
  -/ufc/producto-vagon/?tipo_equipo=`ID del tipo de equipo`



## Para Obtener los Accesos y los CCD 
  Se implemento el siguiente endpoint
    -/api/entidades-acceso-ccd/

## Productos Para CCD

- http://localhost:8000/ufc/ccd-productos/?filterset_field=
  Estan implementados los siguientes campos para filtrar
  ```python
  filterset_fields = ['tipo_equipo__id', 'producto__codigo_producto','tipo_embalaje__id','unidad_medida__simbolo']
  ```
- http://localhost:8000/ufc/ccd-productos/?search=
  Y estos buscadores
  ```python
  search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']
  ```

### GET

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "cantidad": 234,
      "estado": "lleno",
      "contiene": "alimentos",
      "producto": {
        "id": 1,
        "codigo_producto": "CHI0012",
        "nombre_producto": "Chícharo",
        "tipo_producto": "alimento",
        "descripcion": "Minsa"
      },
      "tipo_embalaje": {
        "id": 1,
        "nombre_tipo_embalaje": "Nylon"
      },
      "unidad_medida": {
        "id": 1,
        "magnitud": "Física",
        "unidad_medida": "centímetro",
        "simbolo": "cm"
      },
      "tipo_equipo": {
        "id": 6,
        "tipo_equipo": "planc_plat",
        "tipo_carga": "contenedores",
        "tipo_combustible": "combustible_blanco",
        "longitud": "122.00",
        "peso_neto_sin_carga": "1234.00",
        "peso_maximo_con_carga": "1234.00",
        "capacidad_cubica_maxima": "12.00",
        "descripcion": "adsf"
      }
    }
  ]
}
```

### POST/PUT

```json
{
  "cantidad": 1111,
  "estado": "lleno",
  "contiene": "alimentos",
  "producto_id": 1,
  "tipo_embalaje_id": 3,
  "unidad_medida_id": 3,
  "tipo_equipo_id": 6
}
```

### Search

- http://localhost:8000/ufc/ccd-productos/?search=""
- `search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']`

## Informe CCDxProducto

### Verificar si existe el parte ccd para la entidad

- /verificar-informe-ccd-existente/

### Response

```json
{
  "existe": true,
  "id": 2,
  "fecha_operacion": "2025-07-16T11:02:43.418605",
  "estado": "Creado"
}
```

### para el GET

- Se debe proporconar un query_parameter `fecha_operacion` con formato str_time
  de la biblioteca de Js DateTime
- De no propocionarse ningun parametro usa por default la fecha del dia de hoy

### Para obtener los informes una descripcion completa

- /ccd-informe/

### Response ccd-informe

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "arrastres_list": [],
      "en_trenes_list": [],
      "vagones_cargados_descargados_list": [],
      "situados_carga_descarga_list": [],
      "por_situar_list": [],
      "entidad_detalle": "Cuba Ron SA",
      "creado_por_detalle": {
        "id": 1,
        "username": "admin",
        "email": "admin@desoft.cu",
        "first_name": "Administrador",
        "last_name": "Primero",
        "role": "admin",
        "role_name": "Administrador",
        "provincia": {
          "id": 1,
          "codigo": "01",
          "pais": 1,
          "nombre_pais": "Cuba",
          "nombre_provincia": "La Habana"
        },
        "entidad": 1,
        "cargo": 1,
        "cargo_name": "Esp en alimentos",
        "entidad_name": "Cuba Ron SA",
        "groups": [1, 2, 3, 4, 5, 6, 7],
        "user_permissions": []
      },
      "aprobado_por_detalle": null,
      "fecha_operacion": "2025-07-16T11:02:43.418605",
      "fecha_actual": "2025-07-16T11:02:43.418649",
      "estado_parte": "Creado",
      "comentarios": "adsadadaad",
      "provincia": 1,
      "entidad": 1
    },
    {
      "id": 1,
      "arrastres_list": [],
      "en_trenes_list": [],
      "vagones_cargados_descargados_list": [],
      "situados_carga_descarga_list": [],
      "por_situar_list": [],
      "entidad_detalle": "Cuba Ron SA",
      "creado_por_detalle": {
        "id": 1,
        "username": "admin",
        "email": "admin@desoft.cu",
        "first_name": "Administrador",
        "last_name": "Primero",
        "role": "admin",
        "role_name": "Administrador",
        "provincia": {
          "id": 1,
          "codigo": "01",
          "pais": 1,
          "nombre_pais": "Cuba",
          "nombre_provincia": "La Habana"
        },
        "entidad": 1,
        "cargo": 1,
        "cargo_name": "Esp en alimentos",
        "entidad_name": "Cuba Ron SA",
        "groups": [1, 2, 3, 4, 5, 6, 7],
        "user_permissions": []
      },
      "aprobado_por_detalle": null,
      "fecha_operacion": "2025-07-15T23:44:39.463032",
      "fecha_actual": "2025-07-15T23:44:39.463054",
      "estado_parte": "Creado",
      "comentarios": "adadad",
      "provincia": 1,
      "entidad": 1
    }
  ]
}
```

## CCDxProducto 5 estados de los vagones

Con sus respectivos CRUD

```json
{
  "ccd-arrastres": "http://localhost:8000/ufc/ccd-arrastres/",
  "ccd-situados": "http://localhost:8000/ufc/ccd-situados/",
  "ccd-en-trenes": "http://localhost:8000/ufc/ccd-en-trenes/",
  "ccd-por-situar": "http://localhost:8000/ufc/ccd-por-situar/",
  "ccd-vagones-cd": "http://localhost:8000/ufc/ccd-vagones-cd/"
}
```

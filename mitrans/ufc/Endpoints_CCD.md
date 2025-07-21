# Endpoints de CCDxPRODUCTO

## Para obtener los productos de UFC que estan asociados a un tipo de equipo usar el query
  -/ufc/producto-vagon/?tipo_equipo=`ID del tipo de equipo`



## Para Obtener los Accesos y los CCD 
  Se implemento el siguiente endpoint
    -/api/entidades-acceso-ccd/

## Estructuras de los estados 
* ["POR-SITUAR"](#ccd-por-situar-ok)
* ["SITUADOS"](#ccd-situados-ok)
* ["ARRASTRES"](#ccd-arrastres-ok)
* ["EN-TRENES"](#ccd-en-trenes)
* ["VAGONES-CD"](#ccd-vagones-cd)



## Para obtener el Real a la carga/descarga
  Se debe hacer llamada a
  -/ufc/obtener-real-carga-ccd/?tipo_equipo={ID}&informe={ID}&producto={ID}

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

## CCD-arrastres OK

### GET 
  ```json
  {
    "id": 7,
    "producto": {
      "id": 2,
      "producto": {
        "id": 1,
        "codigo_producto": "CHI0012",
        "nombre_producto": "Chícharo",
        "tipo_producto": "alimento",
        "tipo_producto_name": "Alimento",
        "descripcion": "Minsa"
      },
      "tipo_embalaje": {
        "id": 3,
        "nombre_tipo_embalaje": "RAPEL"
      },
      "unidad_medida": {
        "id": 3,
        "magnitud": "volumen",
        "unidad_medida": "Litros",
        "simbolo": "L"
      },
      "tipo_equipo": {
        "id": 6,
        "tipo_equipo": "planc_plat",
        "tipo_equipo_name": "Plancha o Plataforma",
        "tipo_carga": "contenedores",
        "tipo_carga_name": "Contenedores",
        "tipo_combustible": "combustible_blanco",
        "tipo_combustible_name": "Combustible blanco",
        "longitud": "122.00",
        "peso_neto_sin_carga": "1234.00",
        "peso_maximo_con_carga": "1234.00",
        "capacidad_cubica_maxima": "12.00",
        "descripcion": "adsf"
      },
      "cantidad": 1233,
      "estado": "lleno",
      "contiene": "alimentos"
    },
    "acceso": {
      "id": 7,
      "nombre": "CCD Uno",
      "abreviatura": "CCDU",
      "osde_oace_organismo": 1,
      "codigo_reeup": "1212121245",
      "o_o_o_name": "Ministerio de Comercio Interior",
      "provincia": 1,
      "provincia_name": "La Habana",
      "tipo_entidad": "ccd",
      "tipo_entidad_name": "Centro Carga/Descarga",
      "territorio": 2,
      "territorio_name": "Eser"
    },
    "tipo_equipo": {
      "id": 6,
      "tipo_equipo": "planc_plat",
      "tipo_equipo_name": "Plancha o Plataforma",
      "tipo_carga": "contenedores",
      "tipo_carga_name": "Contenedores",
      "tipo_combustible": "combustible_blanco",
      "tipo_combustible_name": "Combustible blanco",
      "longitud": "122.00",
      "peso_neto_sin_carga": "1234.00",
      "peso_maximo_con_carga": "1234.00",
      "capacidad_cubica_maxima": "12.00",
      "descripcion": "adsf"
    },
    "equipo_vagon_detalle": [
      {
        "id": 108,
        "equipo_ferroviario_detalle": {
          "id": 26,
          "tipo_equipo": 6,
          "tipo_equipo_name": "Plancha o Plataforma",
          "estado_actual": "Asignado al estado CCD Pendiente a Arrastre",
          "numero_identificacion": "CAV3",
          "territorio": "centro",
          "territorio_name": "Centro",
          "tipo_carga": "Contenedores",
          "tipo_combustible": "Combustible blanco",
          "tipo_combustible_name": "Combustible blanco",
          "peso_maximo": "1234.00"
        },
        "cant_dias": 1
      }
    ],
    "fecha_registro": "2025-07-18",
    "estado": "cargado",
    "cantidad_vagones": 2,
    "observaciones": "ESTE ULTIMO",
    "informe_ccd": 3
  }
  ```

### POST/PUT
  ```json
  {
      "fecha_registro": "2025-07-18",
      "estado": "cargado",
      "operacion": "descarga",
      "cantidad_vagones": 2,
      "observaciones": "ESTE ULTIMO",
      "informe_ccd": 3,
      "acceso_id": 7,
      "tipo_equipo_id": 6,
      "producto_id": 2,
      "equipo_vagon": [
        {
        "equipo_ferroviario":26,
        "cant_dias":1
        }
      ]
    }
  ```


## CCD-Por-Situar OK

### POST/PUT
  ```json
  {
  "id": 4,
  "producto": {
    "id": 2,
    "producto": {
      "id": 1,
      "codigo_producto": "CHI0012",
      "nombre_producto": "Chícharo",
      "tipo_producto": "alimento",
      "tipo_producto_name": "Alimento",
      "descripcion": "Minsa"
    },
    "tipo_embalaje": {
      "id": 3,
      "nombre_tipo_embalaje": "RAPEL"
    },
    "unidad_medida": {
      "id": 3,
      "magnitud": "volumen",
      "unidad_medida": "Litros",
      "simbolo": "L"
    },
    "tipo_equipo": {
      "id": 6,
      "tipo_equipo": "planc_plat",
      "tipo_equipo_name": "Plancha o Plataforma",
      "tipo_carga": "contenedores",
      "tipo_carga_name": "Contenedores",
      "tipo_combustible": "combustible_blanco",
      "tipo_combustible_name": "Combustible blanco",
      "longitud": "122.00",
      "peso_neto_sin_carga": "1234.00",
      "peso_maximo_con_carga": "1234.00",
      "capacidad_cubica_maxima": "12.00",
      "descripcion": "adsf"
    },
    "cantidad": 1233,
    "estado": "lleno",
    "contiene": "alimentos"
  },
  "acceso": {
    "id": 7,
    "nombre": "CCD Uno",
    "abreviatura": "CCDU",
    "osde_oace_organismo": 1,
    "codigo_reeup": "1212121245",
    "o_o_o_name": "Ministerio de Comercio Interior",
    "provincia": 1,
    "provincia_name": "La Habana",
    "tipo_entidad": "ccd",
    "tipo_entidad_name": "Centro Carga/Descarga",
    "territorio": 2,
    "territorio_name": "Eser"
  },
  "tipo_equipo": {
    "id": 6,
    "tipo_equipo": "planc_plat",
    "tipo_equipo_name": "Plancha o Plataforma",
    "tipo_carga": "contenedores",
    "tipo_carga_name": "Contenedores",
    "tipo_combustible": "combustible_blanco",
    "tipo_combustible_name": "Combustible blanco",
    "longitud": "122.00",
    "peso_neto_sin_carga": "1234.00",
    "peso_maximo_con_carga": "1234.00",
    "capacidad_cubica_maxima": "12.00",
    "descripcion": "adsf"
  },
  "equipo_vagon_detalle": [
    {
      "id": 110,
      "equipo_ferroviario_detalle": {
        "id": 27,
        "tipo_equipo": 8,
        "tipo_equipo_name": "Casilla",
        "estado_actual": "Asignado al estado CCD Por Situar",
        "numero_identificacion": "VCL1",
        "territorio": "centro",
        "territorio_name": "Centro",
        "tipo_carga": "Otros",
        "tipo_combustible": "-",
        "tipo_combustible_name": "Combustible negro",
        "peso_maximo": "12444.00"
      },
      "cant_dias": 1
    }
  ],
  "fecha_registro": "2025-07-18",
  "estado": "cargado",
  "operacion": "descarga",
  "cantidad_vagones": 1,
  "causas_incumplimiento": null,
  "informe_ccd": 3
}
  ```

## CCD-Situados OK

### GET
  ```json
  {
  "id": 1,
  "producto": {
    "id": 2,
    "producto": {
      "id": 1,
      "codigo_producto": "CHI0012",
      "nombre_producto": "Chícharo",
      "tipo_producto": "alimento",
      "tipo_producto_name": "Alimento",
      "descripcion": "Minsa"
    },
    "tipo_embalaje": {
      "id": 3,
      "nombre_tipo_embalaje": "RAPEL"
    },
    "unidad_medida": {
      "id": 3,
      "magnitud": "volumen",
      "unidad_medida": "Litros",
      "simbolo": "L"
    },
    "tipo_equipo": {
      "id": 6,
      "tipo_equipo": "planc_plat",
      "tipo_equipo_name": "Plancha o Plataforma",
      "tipo_carga": "contenedores",
      "tipo_carga_name": "Contenedores",
      "tipo_combustible": "combustible_blanco",
      "tipo_combustible_name": "Combustible blanco",
      "longitud": "122.00",
      "peso_neto_sin_carga": "1234.00",
      "peso_maximo_con_carga": "1234.00",
      "capacidad_cubica_maxima": "12.00",
      "descripcion": "adsf"
    },
    "cantidad": 1233,
    "estado": "lleno",
    "contiene": "alimentos"
  },
  "acceso": {
    "id": 7,
    "nombre": "CCD Uno",
    "abreviatura": "CCDU",
    "osde_oace_organismo": 1,
    "codigo_reeup": "1212121245",
    "o_o_o_name": "Ministerio de Comercio Interior",
    "provincia": 1,
    "provincia_name": "La Habana",
    "tipo_entidad": "ccd",
    "tipo_entidad_name": "Centro Carga/Descarga",
    "territorio": 2,
    "territorio_name": "Eser"
  },
  "tipo_equipo": {
    "id": 6,
    "tipo_equipo": "planc_plat",
    "tipo_equipo_name": "Plancha o Plataforma",
    "tipo_carga": "contenedores",
    "tipo_carga_name": "Contenedores",
    "tipo_combustible": "combustible_blanco",
    "tipo_combustible_name": "Combustible blanco",
    "longitud": "122.00",
    "peso_neto_sin_carga": "1234.00",
    "peso_maximo_con_carga": "1234.00",
    "capacidad_cubica_maxima": "12.00",
    "descripcion": "adsf"
  },
  "equipo_vagon_detalle": [
    {
      "id": 112,
      "equipo_ferroviario_detalle": {
        "id": 26,
        "tipo_equipo": 6,
        "tipo_equipo_name": "Plancha o Plataforma",
        "estado_actual": "Asignado al estado CCD Situado",
        "numero_identificacion": "CAV3",
        "territorio": "centro",
        "territorio_name": "Centro",
        "tipo_carga": "Contenedores",
        "tipo_combustible": "Combustible blanco",
        "tipo_combustible_name": "Combustible blanco",
        "peso_maximo": "1234.00"
      },
      "cant_dias": 1
    }
  ],
  "fecha_registro": "2025-07-18",
  "estado": "cargado",
  "operacion": "descarga",
  "real_carga_descarga": 0.0,
  "causas_incumplimiento": null,
  "informe_ccd": 3
}
  ```
  ### POST/PUT
  ```json
  {
      "fecha_registro": "2025-07-18",
      "estado": "cargado",
      "operacion": "descarga",
      "cantidad_vagones": 1,
      "causas_incumplimiento": "ESTE ULTIMO",
      "real_carga_descarga": 20,
      "informe_ccd": 3,
      "acceso_id": 7,
      "tipo_equipo_id": 6,
      "producto_id": 2,
      "equipo_vagon": [
        {
        "equipo_ferroviario":26,
        "cant_dias":1
        }
      ]
    }
  ```
    - EN este ultimo el campo real carga _ descarga se actualiza en dependencia del tipo de operacion y el tipo de producto 
  [Ver cómo obtener el Real a la carga/descarga](#para-obtener-el-real-a-la-cargadescarga) 

  ### Tecnicamente para estos 3 estados son la misma estructura dde datos, 

## CCD-VAGONES-CD
    
  ### GET
    ```json
    {
  "id": 4,
  "producto": {
    "id": 2,
    "producto": {
      "id": 1,
      "codigo_producto": "CHI0012",
      "nombre_producto": "Chícharo",
      "tipo_producto": "alimento",
      "tipo_producto_name": "Alimento",
      "descripcion": "Minsa"
    },
    "tipo_embalaje": {
      "id": 3,
      "nombre_tipo_embalaje": "RAPEL"
    },
    "unidad_medida": {
      "id": 3,
      "magnitud": "volumen",
      "unidad_medida": "Litros",
      "simbolo": "L"
    },
    "tipo_equipo": {
      "id": 6,
      "tipo_equipo": "planc_plat",
      "tipo_equipo_name": "Plancha o Plataforma",
      "tipo_carga": "contenedores",
      "tipo_carga_name": "Contenedores",
      "tipo_combustible": "combustible_blanco",
      "tipo_combustible_name": "Combustible blanco",
      "longitud": "122.00",
      "peso_neto_sin_carga": "1234.00",
      "peso_maximo_con_carga": "1234.00",
      "capacidad_cubica_maxima": "12.00",
      "descripcion": "adsf"
    },
    "cantidad": 1233,
    "estado": "lleno",
    "contiene": "alimentos"
  },
  "acceso": {
    "id": 7,
    "nombre": "CCD Uno",
    "abreviatura": "CCDU",
    "osde_oace_organismo": 1,
    "codigo_reeup": "1212121245",
    "o_o_o_name": "Ministerio de Comercio Interior",
    "provincia": 1,
    "provincia_name": "La Habana",
    "tipo_entidad": "ccd",
    "tipo_entidad_name": "Centro Carga/Descarga",
    "territorio": 2,
    "territorio_name": "Eser"
  },
  "tipo_equipo": {
    "id": 6,
    "tipo_equipo": "planc_plat",
    "tipo_equipo_name": "Plancha o Plataforma",
    "tipo_carga": "contenedores",
    "tipo_carga_name": "Contenedores",
    "tipo_combustible": "combustible_blanco",
    "tipo_combustible_name": "Combustible blanco",
    "longitud": "122.00",
    "peso_neto_sin_carga": "1234.00",
    "peso_maximo_con_carga": "1234.00",
    "capacidad_cubica_maxima": "12.00",
    "descripcion": "adsf"
  },
  "equipo_vagon_detalle": [
    {
      "id": 4,
      "fecha_despacho": "2020-10-01",
      "no_id": "41414",
      "tipo_origen": "municipio",
      "origen": "CCD uno",
      "fecha_llegada": "2019-11-01",
      "incidencias": true,
      "observaciones": {
        "faltante":0,
        "sobrante":0,
        "averia":0,
        "peso_origen":0,
        "peso_destino":0,
        "observaciones_generales":"",
      },
      "equipo_ferroviario": 25
    }
  ],
  "fecha_registro": "2025-07-18",
  "estado": "cargado",
  "operacion": "descarga",
  "causa_incumplimiento": null,
  "informe_ccd": 3
}
    ``` 
  ### POST/PUT
    ```json
    {
  "fecha_registro": "2025-07-18",
  "estado": "cargado",
  "operacion": "descarga",
  "cantidad_vagones": 1,
  "observaciones": "ESTE ULTIMO",
  "informe_ccd": 3,
  "acceso_id": 7,
  "tipo_equipo_id": 6,
  "producto_id": 2,
  "equipo_vagon": [
    {
      "equipo_ferroviario": 25,
      "incidencias": 1,
      "observaciones": "adsafafasf",
      "fecha_llegada": "2019-11-01",
      "tipo_origen": "municipio",
      "origen": "CCD uno",
      "no_id": "41414",
      "fecha_despacho": "2020-10-1"
    }
  ],
  "causa_incumplimiento":"ALGO"
}
    ```

## CCD-EN-TRENES
  ### GET
    ```json
    {
  "id": 1,
  "producto": {
    "id": 2,
    "producto": {
      "id": 1,
      "codigo_producto": "CHI0012",
      "nombre_producto": "Chícharo",
      "tipo_producto": "alimento",
      "tipo_producto_name": "Alimento",
      "descripcion": "Minsa"
    },
    "tipo_embalaje": {
      "id": 3,
      "nombre_tipo_embalaje": "RAPEL"
    },
    "unidad_medida": {
      "id": 3,
      "magnitud": "volumen",
      "unidad_medida": "Litros",
      "simbolo": "L"
    },
    "tipo_equipo": {
      "id": 6,
      "tipo_equipo": "planc_plat",
      "tipo_equipo_name": "Plancha o Plataforma",
      "tipo_carga": "contenedores",
      "tipo_carga_name": "Contenedores",
      "tipo_combustible": "combustible_blanco",
      "tipo_combustible_name": "Combustible blanco",
      "longitud": "122.00",
      "peso_neto_sin_carga": "1234.00",
      "peso_maximo_con_carga": "1234.00",
      "capacidad_cubica_maxima": "12.00",
      "descripcion": "adsf"
    },
    "cantidad": 1233,
    "estado": "lleno",
    "contiene": "alimentos"
  },
  "acceso": {
    "id": 7,
    "nombre": "CCD Uno",
    "abreviatura": "CCDU",
    "osde_oace_organismo": 1,
    "codigo_reeup": "1212121245",
    "o_o_o_name": "Ministerio de Comercio Interior",
    "provincia": 1,
    "provincia_name": "La Habana",
    "tipo_entidad": "ccd",
    "tipo_entidad_name": "Centro Carga/Descarga",
    "territorio": 2,
    "territorio_name": "Eser"
  },
  "tipo_equipo": {
    "id": 6,
    "tipo_equipo": "planc_plat",
    "tipo_equipo_name": "Plancha o Plataforma",
    "tipo_carga": "contenedores",
    "tipo_carga_name": "Contenedores",
    "tipo_combustible": "combustible_blanco",
    "tipo_combustible_name": "Combustible blanco",
    "longitud": "122.00",
    "peso_neto_sin_carga": "1234.00",
    "peso_maximo_con_carga": "1234.00",
    "capacidad_cubica_maxima": "12.00",
    "descripcion": "adsf"
  },
  "equipo_vagon_detalle": [
    {
      "id": 26,
      "tipo_equipo": 6,
      "tipo_equipo_name": "Plancha o Plataforma",
      "estado_actual": "Asignado al estado CCD Vagon Cargado/Descargado",
      "numero_identificacion": "CAV3",
      "territorio": "centro",
      "territorio_name": "Centro",
      "tipo_carga": "Contenedores",
      "tipo_combustible": "Combustible blanco",
      "tipo_combustible_name": "Combustible blanco",
      "peso_maximo": "1234.00"
    }
  ],
  "fecha_registro": "2025-07-18",
  "estado": "cargado",
  "cantidad_vagones": 1,
  "observaciones": "ESTE ULTIMO",
  "informe_ccd": 3,
  "equipo_vagon": [
    26
  ]
}
    ```
  ### POST/PUT
    ```json
    {
  "fecha_registro": "2025-07-18",
  "estado": "cargado",
  "operacion": "descarga",
  "cantidad_vagones": 1,
  "observaciones": "ESTE ULTIMO",
  "informe_ccd": 3,
  "acceso_id": 7,
  "tipo_equipo_id": 6,
  "producto_id": 2,
  "equipo_vagon": [
    26
  ],
}
    ```
## Casillas x Productos
  ### GET
  ```json
  {
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "total_general": 22,
      "diferencia_descarga": 15,
      "diferencia_carga": null,
      "situados": 4,
      "situados_mas_2dias": 0,
      "por_situar": 6,
      "por_situar_mas_2dias": 0,
      "en_trenes": 1,
      "pendientes": 2,
      "total_ayer": 10,
      "entro_hoy": 12,
      "plan_carga": 15,
      "plan_descarga": 15,
      "recepcion": 2,
      "reexpedciones": 4,
      "informe_ccd": 3,
      "acceso": 1
    }
  ]
}
  ```

### POST/PUT

```json
{

  "acceso_id": 3, //FK del nom de accesos y CCD
  "casillas_ayer": 1,//INT
  "casillas_hoy": 2, //INT
  "plan_carga": "ESTE ULTIMO",
  "plan_descarga": 3,//INT
  "informe_ccd": 3,
  "recepciones": 6,//INT
  "reexpediciones": 2,//INT
  }
```
Que rico que te organizen todo esto en un documento para el FRONT, a darle envidia a los demas
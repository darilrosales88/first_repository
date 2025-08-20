# Documentacion sobre los partes de GEMAR

## Parte Diario de Embarcaciones

##  1. Diario de Embarcaciones
### Validaciones

1. Si la fecha de vencimiento es mayor o igual que la fecha actual, el campo Certificado vencido muestra el valor “1-Sí”.

2. Si la fecha de vencimiento es menor que la fecha actual, el campo  Certificado vencido muestra el valor “2-No”.

3. El campo Tiempo estimado de afectación se habilita si el campo Fuera de servicio tiene valor 1-Sí. El campo Tiempo estimado admite valores de tiempo con formato (HH:mm:ss).

4. El campo CDT del puerto se actualiza: 
CDT del puerto = (Cantidad de embarcaciones asociadas al puerto – Cantidad de embarcaciones asociadas al puerto, con el campo F/S en valor 1-Sí) / Cantidad de embarcaciones asociadas al puerto * 100

5. En la sección Resumen el campo Parque de embarcaciones se actualiza:
Parque de embarcaciones = Cantidad ∑ de embarcaciones de cada puerto.

6.	En la sección Resumen el campo Fuera de servicio se actualiza:
Fuera de servicio = Cantidad ∑ de embarcaciones de cada puerto, con el campo F/S en valor 1-Sí

7.	En la sección Resumen el campo En servicio se actualiza:
En servicio = Parque de embarcaciones – Fuera de servicio

8.	En la sección Resumen el campo Con certificados vencidos se actualiza:
Con certificados vencidos = Cantidad ∑ de embarcaciones de cada puerto, con el campo Certificado vencido en valor 1-Sí

9.	En la sección Resumen el campo Tiempo de afectación se actualiza:
Tiempo de afectación = ∑Tiempo de afectación de la embarcación, con el campo F/S en valor 1-Sí.

10.	En la sección Resumen el campo CDT(%) general se actualiza:
CDT general = En servicio / Parque de embarcaciones * 100

11.	En el listado se muestra el Tipo de embarcación de cada embarcación seleccionada.

12.	La combinación de los campos Fecha de operación, Puerto, Embarcación, son únicos.

## 2. Diario de Buques

1.	El campo Fecha de operación permite seleccionar la fecha de la operación realizada.
2.	El campo Fecha actual muestra la fecha actual del sistema. Esta es la fecha de creación del tipo de parte.
3.	El campo Tipo muestra los valores definidos:

    1-Buques de carga
    
    2-Buques tanque
    
    3-Buques reparando

4.	El campo Registro admite números.
5.	El campo Buque muestra el listado de embarcaciones de tipo buques registrados en el nomenclador de embarcaciones de tipo “Buque”.
6.	El campo Puerto procedencia muestra el listado de puertos registrados en el nomenclador de puertos.
7.	El campo Puerto destino muestra el listado de puertos registrados en el nomenclador de puertos.
8.	El campo Ubicación muestra los valores definidos:
1-Navegando
2-Con ubicación
9.	Si el campo Ubicación es “1-Navegando”, el campo Puerto ubicado no se habilita.
10.	Si el campo Ubicación es “2-Con ubicación”, el campo Puerto muestra el listado de puertos registrados en el nomenclador de puertos.
11.	El campo Atraque muestra el listado de atraques asociados al puerto seleccionado en el campo Puerto.
12.	Los campos Puerto y Puerto procedencia no debe ser iguales.
13.	Los campos Puerto y Puerto destino no debe ser iguales.
14.	El campo Operación muestra los valores definidos:
    1-I- IMPORTACION

    2-E- EXPORTACION
    
    3-CR- CABOTAJE RECIBIDO
    
    4-CE- CABOTAJE EXPEDIDO
    
    5-T- TRASBORDO
    
    6-A- ALIJO 
15.	Los campos Fecha entrada, Fecha arribo, ETA, ETS, NOR, son campos de selección de fecha y hora, con el formato (dd/mm/aaaa HH:mm).
16.	El campo Nacionalidad muestra los valores definidos:

    1-A
    
    2-C
    
    3-T
17.	El campo Observaciones admite letras, números y caracteres especiales.
18.	La combinación de los campos Buque, Puerto procedencia, Puerto, Atraque, Operación, Destino, son únicos.
19.	Validar los campos obligatorios y notificar al usuario mediante un mensaje de información cuando deje alguno vacío.
20.	Validar los campos únicos y notificar al usuario mediante un mensaje de información cuando deje alguno vacío.
21.	Los campos editables no deben comenzar con el carácter espacio.

## 3. Productos Buque
1.	El campo Tipo producto muestra los valores definidos:
   
    1-Producto

    2-Contenedor

2.	Si el campo Tipo producto es “1-Producto”, el campo Producto muestra el listado de productos registrados en el nomenclador de producto.
3.	Si el campo Tipo producto es “1-Producto”, el campo Tipo de embalaje muestra el listado de Tipo de embalajes registradas en el nomenclador de Tipo de embalaje.
4.	El campo Unidad de medida muestra el listado de unidades de medida registradas en el nomenclador de unidad de medida.
5.	Si el campo Tipo producto es “1-Contenedor”, el campo Estado debe mostrar los valores definidos:
   
    1-Vacío
    
    2-Lleno

6.	Si el campo Estado es “2-Lleno”, el campo Contiene debe mostrar los valores definidos:
    
    1-Alimentos
    
    2-Productos varios
7.	La combinación de los campos Producto, Estado, Contiene son únicos.
8.	Validar los campos obligatorios y notificar al usuario mediante un mensaje de información cuando deje alguno vacío.
9.	Validar los campos únicos y notificar al usuario mediante un mensaje de información cuando deje alguno vacío.
10.	Los campos editables no deben comenzar con el carácter espacio.

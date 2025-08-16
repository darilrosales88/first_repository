# Documentacion sobre los partes de GEMAR

## Parte Diario de Embarcaciones

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


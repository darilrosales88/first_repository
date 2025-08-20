# Sobre la APP de UFC

## TEST
Se recomienda siempre ejecutar los tests para ver si hay problemas con los registros

```bash
python manage.py test ufc/test --verbosity 2
```


## Permisos Revisor UFC (RevisroUFC)
```python
permissions = [
            ("puede_rechazar_informe"
            , "Puede rechazar informes operativos"),
            ("puede_aprobar_informe"
            , "Puede aprobar informes operativos"),
            ("visualizar_informe"
            , "Puede Visualizar el  informe"),
        ]`
```

## Operador UFC (OperadorUFC)
Para que un usuario pueda cumplitr bien su Rol de Operador UFC se le debe asignar el Grupo
{OperadorUFC,VisualizadorUFC,VisualizadorNomencladores}
- Tiene Acceso a todo el CRUD de los Estados, tanto a Informe Operativo como a CCD x Producto

## Agregado nueva funcion optimizada para crear las trazas en el CRUD de cada Registro
```python
def registrar_auditoria(request, accion):
    """
    Método centralizado para registrar acciones en el modelo Auditoria
    
    """
    try:
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=accion,
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
    except Exception as e:
        # No romper el flujo principal si hay error al registrar auditoría
        print(f"Error al registrar auditoría: {str(e)}")


#El cual se usa de la siguiente manera , aqui un ejemplo de su uso
registrar_auditoria(request, f"Insertar Informe operativo: {informe.fecha_operacion}")

```

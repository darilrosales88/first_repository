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
    Tiene Acceso a todo el CRUD de los Estados, tanto a Informe Operativo como a CCD x Producto

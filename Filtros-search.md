# Filtros UFC
Esta es una descripcion de como estan implementados los filtros desde el backend para poder hacer las llamadas de la manera correcta.

## Informe OPERATIVO 

### En TRENES

- los parametros de busquda son los siguientes.
```python
    search = filters.CharFilter(method='filtro_busqueda', lookup_expr='icontains')
    informe = filters.NumberFilter(field_name='informe_operativo__id')
    def filtro_busqueda(self, queryset, name, value):
        return queryset.filter(
            Q(tipo_equipo__icontains=value) |
            Q(numero_identificacion_locomotora__icontains=value) |
            Q(origen__icontains=value) |
            Q(destino__icontains=value)|
            Q(producto__nombre_producto__icontains=value) |  # Busca por nombre de producto
            Q(producto__codigo_producto__icontains=value)    # Busca por código de producto
        ).distinct()
```
- El query `search` busca por `[tipo_equipo,numero_identificacion_locomotora,origne,destino,producto__nombre_producto,producto__codigo_producto]`
- El query `informe` busca por el id del informe operativo

### Pendiente a arrastres.

- Los parametros query son los siguientes
```python
filterset_fields = ['tipo_equipo__id', 'producto__producto__codigo_producto','producto__tipo_embalaje__id','producto__unidad_medida__simbolo']
    search_fields = ['producto__producto__nombre_producto','cantidad','=unidad_medida__unidad_medida', 'origen','tipo_origen']

```
- Los filtros se llaman con el query de ejemplo `ufc/arrastres/?tipo_equipo__id={id del equipo}`
- Los search se llaman con `ufc/arrastres/?search={Un string a buscar de los campos anteriores}`
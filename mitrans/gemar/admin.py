from django.contrib import admin
from .models import (
    gemar_hecho_extraordinario, 
    gemar_parte_hecho_extraordinario,
    gemar_programacion_maniobras, 
    gemar_parte_programacion_maniobras,
    PartePBIP, ParteCargaVieja, ParteExistenciaMercancia
)

@admin.register(gemar_hecho_extraordinario)
class gemar_hecho_extraordinarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_diferencia', 'producto_involucrado', 'cantidad_diferencia', 'fecha_operacion']
    list_filter = ['tipo_diferencia', 'fecha_operacion']
    search_fields = ['descripcion_hecho', 'informado']

@admin.register(gemar_parte_hecho_extraordinario)
class gemar_parte_hecho_extraordinarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_parte', 'fecha_operacion', 'fecha_actual', 'estado_parte', 'creado_por']
    list_filter = ['estado_parte', 'fecha_operacion', 'provincia']
    readonly_fields = ['fecha_actual']
    search_fields = ['creado_por__username', 'entidad__nombre']

@admin.register(gemar_parte_programacion_maniobras)
class gemar_parte_programacion_maniobrasAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_parte', 'fecha_operacion', 'fecha_actual', 'estado_parte', 'creado_por']
    list_filter = ['estado_parte', 'fecha_operacion', 'provincia']
    readonly_fields = ['fecha_actual']
    search_fields = ['creado_por__username', 'entidad__nombre']

@admin.register(gemar_programacion_maniobras)
class gemar_programacion_maniobrasAdmin(admin.ModelAdmin):
    list_display = ['id', 'buque', 'puerto', 'terminal', 'fecha_eta', 'fecha_ets']
    list_filter = ['puerto', 'terminal', 'fecha_eta']
    search_fields = ['buque', 'observaciones']

# Register other models
admin.site.register(PartePBIP)
admin.site.register(ParteCargaVieja)
admin.site.register(ParteExistenciaMercancia)
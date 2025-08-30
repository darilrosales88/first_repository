from django.contrib import admin

from .models import vagon_cargado_descargado,en_trenes ,Situado_Carga_Descarga,arrastres,producto_UFC
from .models import (por_situar,registro_vagones_cargados,vagones_productos,rotacion_vagones,ccd_arrastres,ccd_en_trenes,ccd_vagones_cd,ccd_por_situar,ccd_registro_vagones_cd,ccd_situados,ccd_casillas_productos,ccd_producto,ufc_informe_ccd)
from .models import ufc_informe_operativo,vagones_dias



######Modelos de UFC
admin.site.register(en_trenes)
admin.site.register(Situado_Carga_Descarga)
admin.site.register(arrastres)
admin.site.register(registro_vagones_cargados)
admin.site.register(producto_UFC)
admin.site.register(rotacion_vagones)  
admin.site.register(ufc_informe_operativo)
admin.site.register(vagones_dias)

#####Modelos de CCD
admin.site.register(ccd_en_trenes)
admin.site.register(ccd_registro_vagones_cd)
admin.site.register(ccd_arrastres)
admin.site.register(ccd_situados)
admin.site.register(ccd_por_situar)
admin.site.register(ccd_producto)  
admin.site.register(ufc_informe_ccd)
admin.site.register(ccd_casillas_productos)
admin.site.register(ccd_vagones_cd)


@admin.register(vagon_cargado_descargado)
class VagonCargadoDescargadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'origen', 'destino', 'estado')
    readonly_fields = ('fecha', 'tipo_equipo_ferroviario')  # Puedes agregar más campos
    list_filter = ('fecha', 'estado')  # Filtros por fecha
    date_hierarchy = 'fecha'  # Navegación jerárquica por fechas
    
    # Opcional: si quieres un formato específico para la fecha
    def fecha_formateada(self, obj):
        return obj.fecha.strftime('%d/%m/%Y %H:%M')
    fecha_formateada.short_description = 'Fecha formateada'
    
    # Agrega el campo formateado a los campos de solo lectura si lo deseas
    readonly_fields = ('fecha', 'fecha_formateada')

@admin.register(por_situar)
class por_situarAdmin(admin.ModelAdmin):     
    def fecha_formateada(self, obj):
        return obj.fecha.strftime('%d/%m/%Y %H:%M')
    fecha_formateada.short_description = 'Fecha formateada'
    readonly_fields = ('fecha', 'fecha_formateada')    
    list_display = ('id', 'fecha')

@admin.register(vagones_productos)
class vagones_productosAdmin(admin.ModelAdmin):     
    def fecha_formateada(self, obj):
        return obj.fecha.strftime('%d/%m/%Y %H:%M')
    fecha_formateada.short_description = 'Fecha formateada'
    readonly_fields = ('fecha', 'fecha_formateada')    
    list_display = ('id', 'fecha')
# Register your models here.


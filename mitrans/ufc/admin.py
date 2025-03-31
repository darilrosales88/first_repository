from django.contrib import admin

from .models import productos_vagones_cargados_descargados,vagon_cargado_descargado,en_trenes, producto_en_vagon,por_situar_carga_descarga,Situado_Carga_Descarga

admin.site.register(productos_vagones_cargados_descargados)
admin.site.register(vagon_cargado_descargado)
admin.site.register(en_trenes)
admin.site.register(producto_en_vagon)
admin.site.register(por_situar_carga_descarga)
admin.site.register(Situado_Carga_Descarga)
# Register your models here.

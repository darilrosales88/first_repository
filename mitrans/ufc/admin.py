from django.contrib import admin

from .models import vagon_cargado_descargado,en_trenes ,Situado_Carga_Descarga,arrastres,producto_UFC
from .models import registro_vagones_cargados,por_situar,registro_vagones_cargados,vagones_productos

admin.site.register(vagon_cargado_descargado)
admin.site.register(en_trenes)
admin.site.register(por_situar)
admin.site.register(Situado_Carga_Descarga)
admin.site.register(arrastres)
admin.site.register(registro_vagones_cargados)
admin.site.register(vagones_productos)
admin.site.register(producto_UFC)

# Register your models here.

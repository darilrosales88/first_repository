from django.contrib import admin
from .models import (gemar_hecho_extraordinario,gemar_parte_hecho_extraordinario,gemar_parte_carga_descarga,
                     gemar_programacion_maniobras,gemar_parte_programacion_maniobras,gemar_carga_descarga,
                     gemar_producto_carga_descarga,gemar_turno_carga_descarga,gemar_incidencia_por_turno_carga_descarga,
                     PartePBIP,CargaVieja,ExistenciaMercancia
)
# Register your models here.
admin.site.register(gemar_parte_hecho_extraordinario)
admin.site.register(gemar_hecho_extraordinario)
admin.site.register(gemar_programacion_maniobras)
admin.site.register(gemar_parte_programacion_maniobras)
admin.site.register(gemar_parte_carga_descarga)
admin.site.register(gemar_carga_descarga)
admin.site.register(gemar_producto_carga_descarga)
admin.site.register(gemar_turno_carga_descarga)
admin.site.register(gemar_incidencia_por_turno_carga_descarga)
admin.site.register(PartePBIP)
admin.site.register(CargaVieja)
admin.site.register(ExistenciaMercancia)

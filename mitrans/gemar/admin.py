from django.contrib import admin
from .models import (gemar_hecho_extraordinario,gemar_parte_hecho_extraordinario,gemar_parte_carga_descarga,
                     gemar_programacion_maniobras,gemar_parte_programacion_maniobras,PartePBIP,CargaVieja,
                     ExistenciaMercancia
)
# Register your models here.
admin.site.register(gemar_parte_hecho_extraordinario)
admin.site.register(gemar_hecho_extraordinario)
admin.site.register(gemar_programacion_maniobras)
admin.site.register(gemar_parte_programacion_maniobras)
admin.site.register(gemar_parte_carga_descarga)
admin.site.register(PartePBIP)
admin.site.register(CargaVieja)
admin.site.register(ExistenciaMercancia)

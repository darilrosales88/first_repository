from django.contrib import admin
from .models import (gemar_hecho_extraordinario,gemar_parte_hecho_extraordinario,gemar_parte_carga_descarga,
                     gemar_programacion_maniobras,gemar_parte_programacion_maniobras,gemar_carga_descarga,
                     gemar_producto_carga_descarga,gemar_turno_carga_descarga,gemar_incidencia_por_turno_carga_descarga,
                     gemar_informe_diario_enc,gemar_maniobras_portuarias_enc,gemar_afectaciones_maniobras_portuarias_enc,
                     gemar_carga_seca_enc,gemar_remolcadores_maniobras_enc,gemar_remolcador_carga_liquida_enc,
                     gemar_remolcador_cabotaje_auxiliar_enc,
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

admin.site.register(gemar_informe_diario_enc)
admin.site.register(gemar_maniobras_portuarias_enc)
admin.site.register(gemar_afectaciones_maniobras_portuarias_enc)
admin.site.register(gemar_carga_seca_enc)
admin.site.register(gemar_remolcadores_maniobras_enc)
admin.site.register(gemar_remolcador_carga_liquida_enc)
admin.site.register(gemar_remolcador_cabotaje_auxiliar_enc)

admin.site.register(PartePBIP)
admin.site.register(CargaVieja)
admin.site.register(ExistenciaMercancia)

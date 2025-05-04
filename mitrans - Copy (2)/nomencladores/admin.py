from django.contrib import admin
from .models import nom_pais,nom_provincia,nom_municipio,nom_tipo_maniobra_portuaria,nom_contenedor
from .models import nom_cargo,nom_territorio,nom_puerto,nom_terminal,nom_atraque,nom_unidad_medida,nom_osde_oace_organismo,nom_entidades
from .models import nom_destino,nom_tipo_equipo_ferroviario,nom_embarcacion,nom_equipo_ferroviario,nom_estado_tecnico,nom_producto
from .models import nom_tipo_embalaje,nom_incidencia,nom_tipo_estructura_ubicacion,nom_estructura_ubicacion

from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(nom_pais)
admin.site.register(nom_provincia)
admin.site.register(nom_municipio)
admin.site.register(nom_tipo_maniobra_portuaria)
admin.site.register(nom_contenedor)
admin.site.register(nom_cargo)
admin.site.register(nom_territorio)
admin.site.register(nom_puerto)
admin.site.register(nom_terminal)
admin.site.register(nom_atraque)
admin.site.register(nom_unidad_medida)
admin.site.register(nom_osde_oace_organismo)
admin.site.register(nom_entidades)
admin.site.register(nom_destino)
admin.site.register(nom_tipo_equipo_ferroviario)
admin.site.register(nom_embarcacion)
admin.site.register(nom_equipo_ferroviario)
admin.site.register(nom_estado_tecnico)
admin.site.register(nom_producto)
admin.site.register(nom_tipo_embalaje)
admin.site.register(nom_incidencia)
admin.site.register(nom_tipo_estructura_ubicacion)
admin.site.register(nom_estructura_ubicacion)

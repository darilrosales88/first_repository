#5. creacion de las URL
#la forma de tratar las vistas que estan empleando la prop viewsets de rest_framework es la siguiente
#de rest_framework importamos routers, que se va a encargar de redireccionar
from rest_framework import routers
#importamos las vistas
from .views import nom_pais_view_set,nom_provincia_view_set,nom_municipio_view_set,nom_tipo_maniobra_portuaria_view_set
from .views import nom_contenedor_view_set,nom_cargo_view_set,nom_territorio_view_set,nom_puerto_view_set,nom_terminal_view_set
from .views import nom_atraque_view_set,nom_unidad_medida_view_set,nom_osde_oace_organismo_view_set,nom_entidades_view_set
from .views import nom_destino_view_set,nom_tipo_equipo_ferroviario_view_set,nom_embarcacion_view_set,nom_equipo_ferroviario_view_set
from .views import nom_estado_tecnico_view_set,nom_producto_view_set,nom_tipo_equipo_ferroviario_view_set
from .views import nom_incidencia_view_set,nom_tipo_estructura_ubicacion_view_set, nom_estructura_ubicacion_view_set
from .views import nom_tipo_embalaje_view_set,verificar_destino,verificar_codigo_reeup,PorSituarCargaDescargaViewSet
from .views import SituadoCargaDescargaViewset


from django.urls import path


urlpatterns = [
    path('destinos/verificar-existencia/', verificar_destino, name='verificar_destino'),#verificar si existe un destino dado cliente-destino
    path('entidades/verificar-existencia-reeup/', verificar_codigo_reeup, name='verificar_existencia_reeup'),#verificar si existe ya el codigo reeup
    # Otras rutas
    #path('users/<int:user_id>/assign_permission/', assign_permission, name='assign_permission'),
    #path('users/<int:user_id>/revoke_permission/', revoke_permission, name='revoke_permission'),
    #path('obtener-usuario/<int:user_id>/', obtener_usuario, name='obtener_usuario'),  # GET (obtener usuario)
    #path('editar-usuario/<int:user_id>/', editar_usuario, name='editar_usuario'),  # GET (editar usuario)
    #path('obtener-grupo/<int:grupo_id>/', obtener_grupo, name='obtener_grupo'),  # GET (obtener los grupos del usuario)
    #path('user/<int:user_id>/permissions-and-groups/', get_user_permissions_and_groups, name='get_user_permissions_and_groups'),
    #path('editar-grupo/<int:grupo_id>/edit/', editar_grupo, name='editar_grupo'),  # PATCH (editar el grupo del usuario)
    #path('permisos/', obtener_permisos, name='obtener_permisos'),  # GET),
    
]

router = routers.DefaultRouter()
#definimos las rutas
router.register('paises',nom_pais_view_set,basename='paises')#karmal---------------------------------------------------------------------
router.register('provincias',nom_provincia_view_set,basename='provincias')#Armando+++++++++++++++++++++++++++++++++++++++++++++++++++++++
router.register('municipios',nom_municipio_view_set,basename='municipios')#Armando+++++++++++++++++++++++++++++++++++++++++++++++++++++++
router.register('tipo_maniobras',nom_tipo_maniobra_portuaria_view_set,basename='tipo_maniobras')#Armando DARILOK
router.register('contenedores',nom_contenedor_view_set,basename='contenedores')#karmalDARILOK
router.register('cargos',nom_cargo_view_set,basename='cargos')#Armando+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
router.register('territorios', nom_territorio_view_set, basename='territorios')#karmalDARILOK
router.register('puertos',nom_puerto_view_set,basename='puertos')#karmal-----------------------------------------------------------------
router.register('terminales',nom_terminal_view_set,basename='terminales')#karmalDARILOK
router.register('atraques',nom_atraque_view_set,basename='atraques')#karmal DARILOK
router.register('unidades_medida',nom_unidad_medida_view_set,basename='unidades_medida')#DARILOK
router.register('osde',nom_osde_oace_organismo_view_set,basename='osde')#Armando+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
router.register('entidades',nom_entidades_view_set,basename='entidades')#karmal----------------------------------------------------------
router.register('destinos',nom_destino_view_set,basename='destinos')#karmal--------------------------------------------------------------
router.register('tipos_equipos',nom_tipo_equipo_ferroviario_view_set,basename='tipos_equipos')#DARILOK todos a partir de este
router.register('embarcaciones',nom_embarcacion_view_set,basename='embarcaciones')#DARILOK
router.register('equipos_ferroviarios',nom_equipo_ferroviario_view_set,basename='equipos_ferroviarios')#armando++++++++++++++++++++++++++
router.register('estados',nom_estado_tecnico_view_set,basename='estados')#DARILOK
router.register('productos',nom_producto_view_set,basename='productos')#DARILOK
router.register('embalajes',nom_tipo_embalaje_view_set,basename='embalajes')#DARILOK
router.register('incidencias',nom_incidencia_view_set,basename='incidencias')#karmal-----------------------------------------------------
router.register('tipos_estructuras_ubicacion',nom_tipo_estructura_ubicacion_view_set,basename='tipos_estructuras_ubicacion')#darilOK
router.register('estructuras_ubicacion',nom_estructura_ubicacion_view_set,basename='estructuras_ubicacion')#karmal---DARILOK
router.register('por_situar',PorSituarCargaDescargaViewSet, basename="por_situar")
router.register('situados', SituadoCargaDescargaViewset, basename="situados")



#ahora declaramos el urlpatterns y lo igualamos a la propiedad urls de la variable creada de tipo routers
# Ahora combinamos las rutas manuales con las del router
urlpatterns += router.urls



#Hasta aqui se tienen definidas las rutas con esta nueva manera de hacerlo

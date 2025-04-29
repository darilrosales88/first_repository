from rest_framework import routers
#importamos las vistas
from .views import vagon_cargado_descargado_view_set , en_trenes_view_set, producto_vagon_view_set
from .views import SituadoCargaDescargaViewset,PorSituarCargaDescargaViewSet,PendienteArrastreViewset,registro_vagones_cargados_view_set
from .views import vagones_productos_view_set,verificar_productos,RotacionVagonesViewSet

from django.urls import path


urlpatterns = [
    path('productos-vagones/verificar/', verificar_productos, name='verificar-productos'),
   #path('destinos/verificar-existencia/', verificar_destino, name='verificar_destino'),#verificar si existe un destino dado cliente-destino
    #path('entidades/verificar-existencia-reeup/', verificar_codigo_reeup, name='verificar_existencia_reeup'),#verificar si existe ya el codigo reeup
        
]

router = routers.DefaultRouter()
#definimos las rutas

#endpoints asociados a vagones cargados descargados
#endpoints asociados a vagones y productos
router.register('vagones-productos',vagones_productos_view_set,basename='vagones_productos')
#endpoints productos_UFC
router.register('producto-vagon',producto_vagon_view_set, basename='producto-vagon' )

router.register('registro-vagones-cargados',registro_vagones_cargados_view_set,basename='registro-vagones-cargados')
router.register('vagones-cargados-descargados',vagon_cargado_descargado_view_set,basename='vagones_cargados_descargados')
router.register('en-trenes',en_trenes_view_set, basename='en-trenes' )
router.register('por-situar',PorSituarCargaDescargaViewSet, basename="por-situar")
router.register('situados', SituadoCargaDescargaViewset, basename="situados")
router.register('pendiente-arrastre', PendienteArrastreViewset, basename ="pendiente-arrastre")

#endpoint para rotacion de vagones
router.register("rotaciones", RotacionVagonesViewSet, basename="rotacion-vagones")


#ahora declaramos el urlpatterns y lo igualamos a la propiedad urls de la variable creada de tipo routers
# Ahora combinamos las rutas manuales con las del router
urlpatterns += router.urls


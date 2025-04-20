from rest_framework import routers
#importamos las vistas
from .views import vagon_cargado_descargado_view_set,productos_vagones_cargados_descargados_view_set , en_trenes_view_set, producto_vagon_view_set
from .views import SituadoCargaDescargaViewset,PorSituarCargaDescargaViewSet,PendienteArrastreViewset,registro_vagones_cargados_view_set
from .views import vagones_productos_view_set,productos_vagones_productos_view_set,verificar_productos_vagonesyproductos

from django.urls import path


urlpatterns = [
    path('productos-vagones-productos/verificar/', verificar_productos_vagonesyproductos, name='verificar-productos-vagonesyproductos'),
   #path('destinos/verificar-existencia/', verificar_destino, name='verificar_destino'),#verificar si existe un destino dado cliente-destino
    #path('entidades/verificar-existencia-reeup/', verificar_codigo_reeup, name='verificar_existencia_reeup'),#verificar si existe ya el codigo reeup
        
]

router = routers.DefaultRouter()
#definimos las rutas

#endpoints asociados a vagones cargados descargados
router.register('vagones-cargados-descargados',vagon_cargado_descargado_view_set,basename='vagones_cargados_descargados')
router.register('productos-vagones-cargados-descargados',productos_vagones_cargados_descargados_view_set,basename='productos-vagones-cargados-descargados')
router.register('registro-vagones-cargados',registro_vagones_cargados_view_set,basename='registro-vagones-cargados')
#endpoints asociados a vagones y productos
router.register('vagones-productos',vagones_productos_view_set,basename='vagones_productos')
router.register('productos-vagones-productos',productos_vagones_productos_view_set,basename='productos_vagones_productos')

router.register('en-trenes',en_trenes_view_set, basename='en-trenes' )
router.register('producto-vagon',producto_vagon_view_set, basename='producto-vagon' )
router.register('por-situar',PorSituarCargaDescargaViewSet, basename="por-situar")
router.register('situados', SituadoCargaDescargaViewset, basename="situados")
router.register('pendiente-arrastre', PendienteArrastreViewset, basename ="pendiente-arrastre")


#ahora declaramos el urlpatterns y lo igualamos a la propiedad urls de la variable creada de tipo routers
# Ahora combinamos las rutas manuales con las del router
urlpatterns += router.urls


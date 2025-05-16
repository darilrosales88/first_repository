from rest_framework import routers
#importamos las vistas
from .views import vagon_cargado_descargado_view_set , en_trenes_view_set, producto_vagon_view_set
from .views import SituadoCargaDescargaViewset,PorSituarCargaDescargaViewSet,PendienteArrastreViewset,registro_vagones_cargados_view_set
from .views import vagones_productos_view_set,verificar_productos,RotacionVagonesViewSet,ufc_informe_operativo_view_set
from .views import verificar_informe_existente,vagon_cargado_descargado_hoy_view_set,PendienteArrastre_hoy_Viewset
from .views import SituadoCargaDescarga_hoy_Viewset,PorSituarCargaDescarga_hoy_ViewSet,en_trenes_hoy_viewset
from .views import vagones_productos_hoy_viewset,HistorialVagonCargadoDescargadoViewSet,HistorialVagonesProductosViewSet
from .views import VagonesAsociadosViewSet


from django.urls import path


urlpatterns = [
    path('verificar-informe-existente/', verificar_informe_existente, name='verificar-informe-existente'), 
    path('producto-vagon/verificar/', verificar_productos, name='verificar-productos'),
    path('actualizar-estado-parte/', actualizar_estado_parte, name='actualizar_estado_parte'),
    #path('destinos/verificar-existencia/', verificar_destino, name='verificar_destino'),#verificar si existe un destino dado cliente-destino
    #path('entidades/verificar-existencia-reeup/', verificar_codigo_reeup, name='verificar_existencia_reeup'),#verificar si existe ya el codigo reeup
        
]

router = routers.DefaultRouter()
#definimos las rutas

#endpoint para informe operativo
router.register('informe-operativo',ufc_informe_operativo_view_set,basename='informe-operativo')
#endpoints asociados a vagones y productos
router.register('vagones-productos',vagones_productos_view_set,basename='vagones_productos')
router.register('vagones-productos-hoy',vagones_productos_hoy_viewset,basename='vagones_productos-hoy')
router.register('historial-vagones-productos', HistorialVagonesProductosViewSet, basename='historial-vagones-productos')
#endpoints productos_UFC
router.register('producto-vagon',producto_vagon_view_set, basename='producto-vagon' )

router.register('registro-vagones-cargados',registro_vagones_cargados_view_set,basename='registro-vagones-cargados')
router.register('vagones-cargados-descargados',vagon_cargado_descargado_view_set,basename='vagones_cargados_descargados')
router.register('vagones-cargados-descargados-hoy',vagon_cargado_descargado_hoy_view_set,basename='vagones_cargados_descargados-hoy')
router.register('historial-vagones-cargados', HistorialVagonCargadoDescargadoViewSet, basename='historial-vagones-cargados')

router.register('en-trenes',en_trenes_view_set, basename='en-trenes' )
router.register('en-trenes-hoy',en_trenes_hoy_viewset, basename='en-trenes-hoy' )

router.register('por-situar',PorSituarCargaDescargaViewSet, basename="por-situar")
router.register('por-situar-hoy',PorSituarCargaDescarga_hoy_ViewSet, basename="por-situar-hoy")

router.register('situados', SituadoCargaDescargaViewset, basename="situados")
router.register('situados-hoy', SituadoCargaDescarga_hoy_Viewset, basename="situados-hoy")
router.register('pendiente-arrastre', PendienteArrastreViewset, basename ="pendiente-arrastre")
router.register('pendiente-arrastre-hoy', PendienteArrastre_hoy_Viewset, basename ="pendiente-arrastre-hoy")
router.register(r'vagones-asociados', VagonesAsociadosViewSet, basename='vagones-asociados')

#endpoint para rotacion de vagones
router.register("rotaciones", RotacionVagonesViewSet, basename="rotacion-vagones")


#ahora declaramos el urlpatterns y lo igualamos a la propiedad urls de la variable creada de tipo routers
# Ahora combinamos las rutas manuales con las del router
urlpatterns += router.urls


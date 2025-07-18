
from rest_framework import routers
#importamos las vistas
from .views import vagon_cargado_descargado_view_set , en_trenes_view_set, producto_vagon_view_set
from .views import SituadoCargaDescargaViewset,PorSituarCargaDescargaViewSet,PendienteArrastreViewset,registro_vagones_cargados_view_set
from .views import vagones_productos_view_set,verificar_productos,RotacionVagonesViewSet,ufc_informe_operativo_view_set
from .views import verificar_informe_existente,verificar_informe_ccd_existente
from .views import VagonesDiasViewSet

###Imports View from CCD
from .views import (obtener_real_carga_ccd,ccd_productoViewSet,ccd_informeViewSet,ccd_arrastresViewSet,ccd_casillas_productosViewSet,ccd_en_trenesViewSet,ccd_por_situarViewSet,ccd_registro_vagones_cdViewSet,ccd_vagones_cdViewSet,ccd_situadosViewSet)

from django.urls import path


urlpatterns = [
    path('verificar-informe-existente/', verificar_informe_existente, name='verificar-informe-existente'), 
    path('producto-vagon/verificar/', verificar_productos, name='verificar-productos'),
    path('verificar-informe-ccd-existente/', verificar_informe_ccd_existente, name='verificar-informe-ccd-existente'), 
    path("obtener-real-carga-ccd/",obtener_real_carga_ccd ,name="obtener-real-carga"),
    #path('destinos/verificar-existencia/', verificar_destino, name='verificar_destino'),#verificar si existe un destino dado cliente-destino
    #path('entidades/verificar-existencia-reeup/', verificar_codigo_reeup, name='verificar_existencia_reeup'),#verificar si existe ya el codigo reeup
        
]

router = routers.DefaultRouter()
#definimos las rutas
############### Aqui empiezan los endpoint de UFC
router.register('informe-operativo',ufc_informe_operativo_view_set,basename='informe-operativo')
#endpoints asociados a vagones y productos
router.register('vagones-productos',vagones_productos_view_set,basename='vagones_productos')
#router.register('vagones-productos-hoy',vagones_productos_hoy_viewset,basename='vagones_productos-hoy')

#endpoints productos_UFC
router.register('producto-vagon',producto_vagon_view_set, basename='producto-vagon' )

router.register('registro-vagones-cargados',registro_vagones_cargados_view_set,basename='registro-vagones-cargados')
router.register('vagones-cargados-descargados',vagon_cargado_descargado_view_set,basename='vagones_cargados_descargados')
#router.register('vagones-cargados-descargados-hoy',vagon_cargado_descargado_hoy_view_set,basename='vagones_cargados_descargados-hoy')


router.register('en-trenes',en_trenes_view_set, basename='en-trenes' )
router.register('vagones-dias',VagonesDiasViewSet,basename='vagones_dias')
router.register('por-situar',PorSituarCargaDescargaViewSet, basename="por-situar")
router.register('situados', SituadoCargaDescargaViewset, basename="situados")
router.register('pendiente-arrastre', PendienteArrastreViewset, basename ="pendiente-arrastre")
router.register("rotaciones", RotacionVagonesViewSet, basename="rotacion-vagones")



############Aqui empiezan los router de CCDxPRODUCTO
router.register("ccd-productos",ccd_productoViewSet, basename="ccd-productos")
router.register("ccd-informe",ccd_informeViewSet, basename="ccd-informe")
##Los 5 Estados
router.register("ccd-arrastres",ccd_arrastresViewSet, basename="ccd-arrastres")
router.register("ccd-situados",ccd_situadosViewSet, basename="ccd-situados")
router.register("ccd-en-trenes",ccd_en_trenesViewSet, basename="ccd-en-trenes")
router.register("ccd-por-situar",ccd_por_situarViewSet, basename="ccd-por-situar")
router.register("ccd-vagones-cd",ccd_vagones_cdViewSet, basename="ccd-vagones-cd")






#ahora declaramos el urlpatterns y lo igualamos a la propiedad urls de la variable creada de tipo routers
# Ahora combinamos las rutas manuales con las del router
urlpatterns += router.urls


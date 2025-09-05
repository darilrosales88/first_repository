#5. creacion de las URL
#la forma de tratar las vistas que estan empleando la prop viewsets de rest_framework es la siguiente
#de rest_framework importamos routers, que se va a encargar de redireccionar
from rest_framework import routers
from django.urls import path
from gemar import views
#importamos las vistas
from .views import (gemar_parte_hecho_extraordinario_view_set, 
                    gemar_hecho_extraordinario_view_set,verificar_informe_he_existente,
                    gemar_programacion_maniobras_view_set,verificar_parte_programacion_maniobra_existente,
                    gemar_parte_programacion_maniobras_view_set,listar_partes_combinados,
                    gemar_parte_carga_descarga_view_set,gemar_carga_descarga_view_set,gemar_producto_carga_descarga_view_set,
                    gemar_turno_carga_descarga_view_set,gemar_incidencia_por_turno_carga_descarga_view_set,
                    gemar_informe_diario_enc_view_set,gemar_maniobras_portuarias_enc_view_set,
                    gemar_afectaciones_maniobras_portuarias_enc_view_set,gemar_carga_seca_enc_view_set,
                    gemar_remolcadores_maniobras_enc_view_set,gemar_remolcador_carga_liquida_enc_view_set,
                    gemar_remolcador_cabotaje_auxiliar_enc_view_set)
    


urlpatterns = [
    path('gemar-partes-combinados/', listar_partes_combinados, name='listar-partes-combinados'),
    path('gemar-verificar-informe-existente/', verificar_informe_he_existente, name='verificar-informe'),
    path('gemar-verificar-informe-programacion-maniobra-existente/', verificar_parte_programacion_maniobra_existente, name='verificar-informe-programacion-maniobra'),
    #Lo que hizo Raider
    path('resumen-diario/', views.ResumenDiarioView.as_view(), name='resumen-diario'),
    
]

router = routers.DefaultRouter()
#definimos las rutas
router.register('gemar-partes-hechos-extraordinarios',gemar_parte_hecho_extraordinario_view_set,basename='gemar-partes-hechos-extraordinarios')
router.register('gemar-hechos-extraordinarios',gemar_hecho_extraordinario_view_set,basename='gemar-hechos-extraordinarios')

router.register('gemar-partes-programacion-maniobras', gemar_parte_programacion_maniobras_view_set, basename='gemar-partes-programacion-maniobras')  # Nueva ruta
router.register('gemar-programacion-maniobras', gemar_programacion_maniobras_view_set, basename='gemar-programacion-maniobras')  # Nueva ruta

router.register('gemar-parte-carga-descarga', gemar_parte_carga_descarga_view_set, basename='gemar-parte-carga-descarga')  # Nueva ruta
router.register('gemar-carga-descarga', gemar_carga_descarga_view_set, basename='gemar-carga-descarga')
router.register('gemar-producto-carga-descarga',gemar_producto_carga_descarga_view_set, basename='gemar-producto-carga-descarga')
router.register('gemar-turno-carga-descarga',gemar_turno_carga_descarga_view_set, basename='gemar-turno-carga-descarga')
router.register('gemar-incidencia-por-turno-carga-descarga',gemar_incidencia_por_turno_carga_descarga_view_set, 
                basename='gemar-incidencia-por-turno-carga-descarga')

router.register('gemar-informe-diario-enc',gemar_informe_diario_enc_view_set, basename='gemar-informe-diario-enc')
router.register('gemar-maniobra-portuaria-enc',gemar_maniobras_portuarias_enc_view_set, basename='gemar-maniobra-portuaria-enc')
router.register('gemar-afectacion-maniobra-portuaria-enc',gemar_afectaciones_maniobras_portuarias_enc_view_set, 
                basename='gemar-afectacion-maniobra-portuaria-enc')
router.register('gemar-carga-seca-enc',gemar_carga_seca_enc_view_set, basename='gemar-carga-seca-enc')
router.register('gemar-remolcador-maniobra-enc',gemar_remolcadores_maniobras_enc_view_set, basename='gemar-remolcador-maniobra-enc')
router.register('gemar-remolcador-carga-liquida-enc',gemar_remolcador_carga_liquida_enc_view_set, basename='gemar-remolcador-carga-liquida-enc')
router.register('gemar-remolcador-cabotaje-auxiliar-enc',gemar_remolcador_cabotaje_auxiliar_enc_view_set, basename='gemar-remolcador-cabotaje-auxiliar-enc')
router.register(r'partes-pbip', views.PartePBIPViewSet, basename='partepbip')
router.register(r'cargas-viejas', views.CargaViejaViewSet, basename='cargavieja')
router.register(r'existencias-mercancia', views.ExistenciaMercanciaViewSet, basename='existenciamercancia')

#ahora declaramos el urlpatterns y lo igualamos a la propiedad urls de la variable creada de tipo routers
# Ahora combinamos las rutas manuales con las del router
urlpatterns += router.urls
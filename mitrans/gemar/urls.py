#5. creacion de las URL
#la forma de tratar las vistas que estan empleando la prop viewsets de rest_framework es la siguiente
#de rest_framework importamos routers, que se va a encargar de redireccionar
from rest_framework import routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gemar import views
#importamos las vistas
from .views import (
    gemar_parte_hecho_extraordinario_view_set, 
    gemar_hecho_extraordinario_view_set,
    verificar_informe_he_existente,
    gemar_programacion_maniobras_view_set,
    verificar_parte_programacion_maniobra_existente,
    gemar_parte_programacion_maniobras_view_set,
    listar_partes_combinados,
    detalle_parte_combinado,
    actualizar_estado_parte,
    eliminar_parte_combinado,
    detalle_hecho_extraordinario,
    detalle_programacion_maniobras,
    detalle_pbip,
    detalle_existencia_mercancia,
    actualizar_estado_existencia
)

    

from django.urls import path

urlpatterns = [
    path('gemar-partes-combinados/', listar_partes_combinados, name='listar-partes-combinados'),
    path('gemar-partes-combinados/<int:pk>/detalle_parte', detalle_parte_combinado, name='detalle-parte-combinado'),
    path('gemar-partes-combinados/<int:pk>/actualizar-estado/', actualizar_estado_parte, name='actualizar-estado-parte'),
    path('gemar-partes-combinados/<int:pk>/eliminar/', eliminar_parte_combinado, name='eliminar-parte-combinado'),
    path('gemar-verificar-informe-existente/', verificar_informe_he_existente, name='verificar-informe'),
    path('gemar-verificar-informe-programacion-maniobra-existente/', verificar_parte_programacion_maniobra_existente, name='verificar-informe-programacion-maniobra'),
    path('resumen-diario/', views.ResumenDiarioView.as_view(), name='resumen-diario'),
    path('hechos-extraordinarios/<int:pk>/detalle', detalle_hecho_extraordinario, name='detalle-hecho-extraordinario'),
    path('programacion-maniobras/<int:pk>/detalle', detalle_programacion_maniobras, name='detalle-programacion-maniobras'),
    path('partes-pbip/<int:pk>/detalle', detalle_pbip, name='detalle-pbip'),
    path('existencias-mercancia/<int:pk>/detalle', detalle_existencia_mercancia, name='detalle-existencia-mercancia'),
    path('existencias-mercancia/<int:pk>/actualizar-estado/', actualizar_estado_existencia, name='actualizar_estado_existencia'),
]

router = routers.DefaultRouter()
router.register('gemar-partes-hechos-extraordinarios', gemar_parte_hecho_extraordinario_view_set, basename='gemar-partes-hechos-extraordinarios')
router.register('gemar-hechos-extraordinarios', gemar_hecho_extraordinario_view_set, basename='gemar-hechos-extraordinarios')
router.register('gemar-partes-programacion-maniobras', gemar_parte_programacion_maniobras_view_set, basename='gemar-partes-programacion-maniobras')
router.register('gemar-programacion-maniobras', gemar_programacion_maniobras_view_set, basename='gemar-programacion-maniobras')
router.register(r'partes-pbip', views.PartePBIPViewSet, basename='partepbip')
router.register(r'cargas-viejas', views.CargaViejaViewSet, basename='cargavieja')
router.register(r'existencias-mercancia', views.ExistenciaMercanciaViewSet, basename='existenciamercancia')

urlpatterns += router.urls
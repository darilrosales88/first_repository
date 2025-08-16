#5. creacion de las URL
#la forma de tratar las vistas que estan empleando la prop viewsets de rest_framework es la siguiente
#de rest_framework importamos routers, que se va a encargar de redireccionar
from rest_framework import routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gemar import views
#importamos las vistas
from .views import (gemar_parte_hecho_extraordinario_view_set, 
                    gemar_hecho_extraordinario_view_set,verificar_informe_he_existente,
                    gemar_programacion_maniobras_view_set,verificar_parte_programacion_maniobra_existente,
                    gemar_parte_programacion_maniobras_view_set,listar_partes_combinados)
    

from django.urls import path

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
router.register(r'partes-pbip', views.PartePBIPViewSet, basename='partepbip')
router.register(r'cargas-viejas', views.CargaViejaViewSet, basename='cargavieja')
router.register(r'existencias-mercancia', views.ExistenciaMercanciaViewSet, basename='existenciamercancia')

#ahora declaramos el urlpatterns y lo igualamos a la propiedad urls de la variable creada de tipo routers
# Ahora combinamos las rutas manuales con las del router
urlpatterns += router.urls
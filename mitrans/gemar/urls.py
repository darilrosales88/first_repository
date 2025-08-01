#5. creacion de las URL
#la forma de tratar las vistas que estan empleando la prop viewsets de rest_framework es la siguiente
#de rest_framework importamos routers, que se va a encargar de redireccionar
from rest_framework import routers
#importamos las vistas
from .views import (gemar_parte_hecho_extraordinario_view_set, 
                    gemar_hecho_extraordinario_view_set,verificar_informe_he_existente,
                    gemar_programacion_maniobras_view_set)
    

from django.urls import path

urlpatterns = [
    path('gemar-verificar-informe-existente/', verificar_informe_he_existente, name='verificar-informe'),
    
]

router = routers.DefaultRouter()
#definimos las rutas
router.register('gemar-partes-hechos-extraordinarios',gemar_parte_hecho_extraordinario_view_set,basename='gemar-partes-hechos-extraordinarios')
router.register('gemar-hechos-extraordinarios',gemar_hecho_extraordinario_view_set,basename='gemar-hechos-extraordinarios')
router.register('gemar-programacion-maniobras', gemar_programacion_maniobras_view_set, basename='gemar-programacion-maniobras')  # Nueva ruta

#ahora declaramos el urlpatterns y lo igualamos a la propiedad urls de la variable creada de tipo routers
# Ahora combinamos las rutas manuales con las del router
urlpatterns += router.urls
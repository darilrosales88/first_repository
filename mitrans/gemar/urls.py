# gemar/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gemar import views

router = DefaultRouter()
router.register(r'partes-pbip', views.PartePBIPViewSet, basename='partepbip')
router.register(r'cargas-viejas', views.CargaViejaViewSet, basename='cargavieja')
router.register(r'existencias-mercancia', views.ExistenciaMercanciaViewSet, basename='existenciamercancia')

urlpatterns = [
    path('', include(router.urls)),
    path('resumen-diario/', views.ResumenDiarioView.as_view(), name='resumen-diario'),
]
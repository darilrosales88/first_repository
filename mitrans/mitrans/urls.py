# mitrans/urls.py
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/', include('nomencladores.urls')),
    path('apiAdmin/', include('Administracion.urls')),    
    path('ufc/', include('ufc.urls')),
    path('api/gemar/', include('gemar.urls')),  
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
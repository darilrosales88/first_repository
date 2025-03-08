from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Auditoria

# Registra el modelo CustomUser con UserAdmin
admin.site.register(CustomUser, UserAdmin)

# Registra el modelo Auditoria
admin.site.register(Auditoria)
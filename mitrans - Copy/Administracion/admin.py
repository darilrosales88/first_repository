from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Auditoria

# Registra el modelo CustomUser con UserAdmin
class CustomUserAdmin(UserAdmin):
    # Agrega los campos personalizados al formulario de creación/edición
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datos adicionales', {'fields': ('role', 'entidad', 'cargo')}),  # Campos personalizados
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'role', 'entidad', 'cargo'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')  # Muestra el rol en la lista
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')  # Filtra por rol
    search_fields = ('username', 'first_name', 'last_name', 'email')  # Búsqueda por campos
    ordering = ('username',)  # Ordena por nombre de usuario





admin.site.register(CustomUser, CustomUserAdmin)
# Registra el modelo Auditoria
admin.site.register(Auditoria)
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los usuarios del grupo Admin realizar operaciones de administración.
    """
    def has_permission(self, request,view):
        return request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()
    
class ReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo operaciones de lectura (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS
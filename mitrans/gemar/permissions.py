from rest_framework import permissions

class IsAdminGemarPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los usuarios del grupo AdminGemar
    realizar operaciones de administración.
    """
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y pertenezca al grupo AdminGemar
        return request.user.is_authenticated and request.user.groups.filter(name='AdminGemar').exists()

class IsVisualizadorGemarPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir a los usuarios del grupo VisualizadorGemar 
    realizar operaciones de solo lectura.
    """
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y pertenezca al grupo VisualizadorGemar
        return request.user.is_authenticated and request.user.groups.filter(name='VisualizadorGemar').exists()

    def has_object_permission(self, request, view, obj):
        # Solo permitir operaciones de lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS
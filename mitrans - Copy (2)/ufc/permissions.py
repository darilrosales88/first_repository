from rest_framework import permissions

class IsAdminUFCPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los usuarios del grupo AdminUFC
    realizar operaciones de administración.
    """
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y pertenezca al grupo AdminUFC
        return request.user.is_authenticated and request.user.groups.filter(name='AdminUFC').exists()

class IsVisualizadorUFCPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir a los usuarios del grupo VisualizadorUFC 
    realizar operaciones de solo lectura.
    """
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y pertenezca al grupo VisualizadorUFC
        return request.user.is_authenticated and request.user.groups.filter(name='VisualizadorUFC').exists()

    def has_object_permission(self, request, view, obj):
        # Solo permitir operaciones de lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
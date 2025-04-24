from rest_framework import permissions

class IsAdminNomenladoresPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los usuarios del grupo AdminNomencladores
    realizar operaciones de administración.
    """
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y pertenezca al grupo AdminNomencladores
        return request.user.is_authenticated and request.user.groups.filter(name='AdminNomencladores').exists()

class IsVisualizadorNomencladoresPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir a los usuarios del grupo VisualizadorNomencladores 
    realizar operaciones de solo lectura.
    """
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y pertenezca al grupo VisualizadorNomencladores
        return request.user.is_authenticated and request.user.groups.filter(name='VisualizadorNomencladores').exists()

    def has_object_permission(self, request, view, obj):
        # Solo permitir operaciones de lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
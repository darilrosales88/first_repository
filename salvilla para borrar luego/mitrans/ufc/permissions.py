from rest_framework import permissions

OPERADOR_METHODS = ('GET', 'POST', 'PUT', 'PATCH','OPTIONS', 'DELETE')
REVISOR_METHODS = ( 'PUT', 'PATCH')
# Verifica si el usuario tiene el rol "ufc"
class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
class OperadorUFCPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir a los usuarios del grupo OperadorUFC
    realizar operaciones de revisión.
    """
    message = "Solo miembros del grupo Operador y Admin pueden acceder a esta información"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="OperadorUFC").exists() and request.method in OPERADOR_METHODS

class RevisorUFCPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir a los usuarios del grupo RevisorUFC
    realizar operaciones de revisión.
    """
    message = "Solo miembros del grupo RevisorUFC pueden acceder a esta información"
    def has_permission(self, request, view):
        print(view)
        return request.user.is_authenticated and request.user.groups.filter(name="RevisorUFC").exists() and request.method in REVISOR_METHODS


class IsUFCPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ROLES_PERMITIDO=['ufc','admin']
        return request.user.role in ROLES_PERMITIDO
    
#la otra variante de asignacion de permisos en base a grupos(AdminUFC, VisualizadorUFC)

#asignando a permission_classes los permisos asociados al usuario, extraido a la raiz pues sera comun para todos los ModelViewSet
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUFCPermission]
        else:  # Para list y retrieve
            # Permitir tanto a AdminUFC como a VisualizadorUFC ver los registros
            permission_classes = [IsAdminUFCPermission | IsVisualizadorUFCPermission | RevisorUFCPermission | OperadorUFCPermission, ReadOnly]
        return [permission() for permission in permission_classes]

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

class IsRevisorUFCPermission(permissions.BasePermission):
    """
    Permiso personalizado para permitir a los usuarios del grupo RevisorUFC
    realizar operaciones de revisión.
    """
    message = "Solo miembros del grupo RevisorUFC pueden acceder a esta información"
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y pertenezca al grupo RevisorUFC
        return request.user.is_authenticated and request.user.groups.filter(name='RevisorUFC').exists()

    
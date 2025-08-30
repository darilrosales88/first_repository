from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Permiso para usuarios administradores (pueden hacer todo)
    """
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

class IsGEMARUser(BasePermission):
    """
    Permiso para usuarios GEMAR (solo lectura y aprobación/rechazo)
    """
    def has_permission(self, request, view):
        # Permitir solo GET, OPTIONS, HEAD para list y retrieve
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return True
        
        # Permitir acciones personalizadas de aprobación
        if view.action in ['aprobar', 'rechazar', 'cancelar']:
            return True
            
        # Solo admin puede hacer otras operaciones
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Misma lógica que has_permission
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return True
            
        if view.action in ['aprobar', 'rechazar', 'cancelar']:
            return True
            
        return request.user.is_superuser
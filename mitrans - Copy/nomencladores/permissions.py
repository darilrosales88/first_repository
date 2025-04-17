from rest_framework import permissions

#1.2	Crear clases asociadas a cada uno de los grupos que se usarán
class IsAdminNomenladoresPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='AdminNomencladores').exists()
    
class IsVisualizadorNomencladoresPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='VisualizadorNomencladores').exists()



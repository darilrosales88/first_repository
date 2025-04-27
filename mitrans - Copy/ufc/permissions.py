from rest_framework import permissions

class IsAdminUFCPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='AdminUFC').exists()

class IsVisualizadorUFCPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['AdminUFC', 'VisualizadorUFC']).exists()
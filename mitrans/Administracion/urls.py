from django.urls import path
from rest_framework import routers
from .views import (
    nom_user_view_set, GroupViewSet, obtener_permisos, editar_grupo, obtener_grupo,
    UserCreateView, obtener_usuario, editar_usuario, get_user_permissions_and_groups,
    AuditoriaViewSet, assign_permission, revoke_permission,
)

#referente a creacion de usuarios, gurpos, permisos,auditoria, etc

router = routers.DefaultRouter()
router.register('users', nom_user_view_set, basename='users')
router.register('groups', GroupViewSet, basename='groups')#DARIL FULAAAA gestion de los grupos de los usuarios
router.register('auditoria', AuditoriaViewSet, basename='auditoria')

urlpatterns = [
    path('users/<int:user_id>/assign_permission/', assign_permission, name='assign_permission'),
    path('users/<int:user_id>/revoke_permission/', revoke_permission, name='revoke_permission'),
    path('obtener-usuario/<int:user_id>/', obtener_usuario, name='obtener_usuario'),
    path('editar-usuario/<int:user_id>/', editar_usuario, name='editar_usuario'),
    path('creacion-usuario/', UserCreateView.as_view(), name='creacion-usuario'),
    path('obtener-grupo/<int:grupo_id>/', obtener_grupo, name='obtener_grupo'),
    path('user/<int:user_id>/permissions-and-groups/', get_user_permissions_and_groups, name='get_user_permissions_and_groups'),
    path('editar-grupo/<int:grupo_id>/edit/', editar_grupo, name='editar_grupo'),
    path('permisos/', obtener_permisos, name='obtener_permisos'),
]

urlpatterns += router.urls
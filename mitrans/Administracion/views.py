from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from .models import CustomUser, Auditoria
from .serializers import UserPermissionSerializer, GroupSerializer, AuditoriaSerializer, auditoria_filter, user_filter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from nomencladores.models import nom_cargo, nom_entidades  # Asegúrate de que los nombres sean correctos
#Para la paginacion
from rest_framework.pagination import PageNumberPagination

# Usa get_user_model() para obtener el modelo de usuario activo
User = get_user_model()

# Vista para gestionar grupos
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]  # Asegura que solo usuarios autenticados puedan acceder


    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nombre de grupo
        n_g = self.request.query_params.get('nombre_grupo')
        if n_g:
            queryset = queryset.filter(name__icontains=n_g)
        return queryset

    def create(self, request, *args, **kwargs):
        # Extrae los datos del request
        name = request.data.get('name')
        permisos_ids = request.data.get('permissions', [])

        # Crea el grupo
        grupo = Group.objects.create(name=name)

        # Asigna los permisos al grupo
        permisos = Permission.objects.filter(id__in=permisos_ids)
        grupo.permissions.set(permisos)

        # Serializa el grupo creado para la respuesta
        serializer = self.get_serializer(grupo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtén el grupo que se va a eliminar

        # Elimina el grupo de los usuarios que lo tienen asignado
        for user in CustomUser.objects.filter(groups=instance):
            user.groups.remove(instance)  # Elimina el grupo del usuario

        # Elimina el grupo
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Vista para obtener un grupo específico
@api_view(['GET'])
def obtener_grupo(request, grupo_id):
    try:
        grupo = Group.objects.get(id=grupo_id)
        permisos = grupo.permissions.all()
        data = {
            'id': grupo.id,
            'name': grupo.name,
            'permissions': [{'id': p.id, 'name': p.name} for p in permisos],
        }
        return Response(data, status=status.HTTP_200_OK)
    except Group.DoesNotExist:
        return Response({'error': 'Grupo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Vista para obtener todos los permisos
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_permisos(request):
    permisos = Permission.objects.all()
    data = [{'id': p.id, 'name': p.name} for p in permisos]
    return Response(data)

# Vista para editar un grupo
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editar_grupo(request, grupo_id):
    grupo = Group.objects.get(id=grupo_id)
    permisos_ids = request.data.get('permissions', [])
    grupo.permissions.set(permisos_ids)
    return Response({'status': 'success'})

# Vista para obtener permisos y grupos de un usuario
@api_view(['GET'])
def get_user_permissions_and_groups(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        first_name = user.first_name
        last_name = user.last_name
        entidad = {
            'id': user.entidad.id,
            'nombre': user.entidad.nombre,
        }
        cargo = {
            'id': user.cargo.id,
            'nombre_cargo': user.cargo.nombre_cargo,
        }

        # Obtener permisos y grupos
        groups = user.groups.all()
        permissions = user.user_permissions.all()

        # Formatear grupos y permisos
        grupos_formateados = [{'id': g.id, 'name': g.name} for g in groups]
        permisos_formateados = [{'id': p.id, 'name': p.name} for p in permissions]

        return Response({
            'first_name': first_name,
            'last_name': last_name,
            'entidad': entidad,
            'cargo': cargo,
            'groups': grupos_formateados,
            'user_permissions': permisos_formateados,
        })
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=404)

# Usa get_user_model() para obtener el modelo de usuario activo
User = get_user_model()

# Vista para gestionar usuarios
class nom_user_view_set(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserPermissionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = user_filter  # Asegúrate de que esté correctamente referenciado

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username')
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

# Vista para crear usuarios
class UserCreateView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        role = request.data.get('role')
        password = request.data.get('password')
        entidad_id = request.data.get('entidad')
        cargo_id = request.data.get('cargo')
        groups = request.data.get('groups', [])
        permissions = request.data.get('permissions', [])

        # Obtener instancias de los modelos relacionados
        entidad = get_object_or_404(nom_entidades, id=entidad_id)
        cargo = get_object_or_404(nom_cargo, id=cargo_id)

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            password=password,
            entidad=entidad,
            cargo=cargo
        )

        if groups:
            user.groups.set(groups)

        if permissions:
            for permission_id in permissions:
                permission = Permission.objects.get(id=permission_id)
                user.user_permissions.add(permission)

        return Response(
            {"message": "Usuario creado exitosamente"},
            status=status.HTTP_201_CREATED
        )

# Vista para obtener un usuario específico
@api_view(['GET'])
def obtener_usuario(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        grupos = user.groups.all()
        permisos = user.user_permissions.all()
        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,            
            'last_name': user.last_name,
            'role': user.role,
            'entidad': {
                'id': user.entidad.id,
                'nombre': user.entidad.nombre  # Asegúrate de que 'nombre' es el campo correcto
            },
            'cargo': {
                'id': user.cargo.id,
                'nombre_cargo': user.cargo.nombre_cargo  # Asegúrate de que 'nombre_cargo' es el campo correcto
            },
            'email': user.email,
            'groups': [{'id': g.id, 'name': g.name} for g in grupos],
            'user_permissions': [{'id': p.id, 'name': p.name} for p in permisos],
        }
        return Response(data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Vista para editar un usuario
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editar_usuario(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        serializer = UserPermissionSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Vista para asignar un permiso a un usuario
@api_view(['POST'])
def assign_permission(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    permission = Permission.objects.get(codename=request.data['permission'])
    user.user_permissions.add(permission)
    return Response({'status': 'permission assigned'})

# Vista para revocar un permiso a un usuario
@api_view(['POST'])
def revoke_permission(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    permission = Permission.objects.get(codename=request.data['permission'])
    user.user_permissions.remove(permission)
    return Response({'status': 'permission revoked'})

# Vista para gestionar auditoría
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.all().order_by('-fecha')#ordenando por fecha en forma descendente
    serializer_class = AuditoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = auditoria_filter  # Usar el filtro personalizado
    pagination_class = CustomPagination
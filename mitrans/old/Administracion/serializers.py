from rest_framework import serializers
from django_filters import rest_framework as filters
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model
from .models import CustomUser, Auditoria
from nomencladores.serializers import nom_provincia_serializer, nom_entidades_serializer

CustomUser = get_user_model()

# Serializador para grupos
class group_filter(filters.FilterSet):
    nombre_grupo = filters.CharFilter(method='filter_by_nombre', lookup_expr='icontains')

    def filter_by_nombre(self, queryset, value):
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Group
        fields = {
            'name': ['exact'],
        }

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
        filterset_class = group_filter

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')
        filterset_class = group_filter

# Serializador para usuarios
class user_filter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='exact')  # Cambiado de 'user_n' a 'username'

    class Meta:
        model = CustomUser
        fields = {
            'username': ['exact'],  # Cambiado de 'user_n' a 'username'
        }

class UserPermissionSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
    provincia=serializers.SerializerMethodField()

    cargo_name = serializers.ReadOnlyField(source = 'cargo.nombre_cargo')
    entidad_name = serializers.ReadOnlyField(source = 'entidad.nombre')
    role_name = serializers.ReadOnlyField(source='get_role_display')

    class Meta:
        model = CustomUser        
        fields = ['id', 'username', 'email', 'first_name', 'last_name','role','role_name','provincia' ,'entidad','cargo','cargo_name','entidad_name', 'password', 'groups', 'user_permissions']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}
    
    
    def get_provincia(self, obj):
        """Obtiene todos los arrastres asociados al informe operativo."""
        provincia_queryset = obj.entidad.provincia
        return nom_provincia_serializer(provincia_queryset).data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.entidad = validated_data.get('entidad', instance.entidad)
        instance.cargo = validated_data.get('cargo', instance.cargo)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        if 'groups' in validated_data:
            instance.groups.set(validated_data['groups'])

        if 'user_permissions' in validated_data:
            instance.user_permissions.set(validated_data['user_permissions'])

        instance.save()
        return instance

# Serializador para auditoría
class auditoria_filter(filters.FilterSet):
    usuario = filters.CharFilter(field_name='usuario__username', lookup_expr='exact')
    fecha_after = filters.DateTimeFilter(field_name='fecha', lookup_expr='gte')
    fecha_before = filters.DateTimeFilter(field_name='fecha', lookup_expr='lte')
    accion = filters.CharFilter(field_name='accion', lookup_expr='icontains')

    class Meta:
        model = Auditoria
        fields = ['usuario', 'fecha_after', 'fecha_before', 'accion']

class AuditoriaSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Auditoria
        fields = '__all__'
        filterset_class = auditoria_filter
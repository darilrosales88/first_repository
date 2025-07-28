 #1. en este archivo se implementaran todos los serializadores que se usaran en la app, primero
# se importa desde restframeuork los serializadores(serializers), luego se importan los modelos,
from rest_framework import serializers
#para trabajar con el filtrado de los serialziadores debemos hacer la siguiente importacion
from django_filters import rest_framework as filters

from django.db.models import Q

from .models import gemar_hecho_extraordinario,gemar_parte_hecho_extraordinario

from Administracion.models import CustomUser


class gemar_parte_hecho_extraordinario_filter(filters.FilterSet):

    fecha_entidad = filters.CharFilter(method='filtrado_por_fecha_entidad',lookup_expr = 'icontains')

    def filtrado_por_fecha_entidad(self,queryset,value):        
        return queryset.filter(fecha_operacion__icontains = value) | queryset.filter(entidad__icontains = value) 
        
    
    class Meta:  
        model:gemar_parte_hecho_extraordinario    
        fields:{
            'fecha_entidad':['icontains'],
        }

        
class gemar_parte_hecho_extraordinario_serializer(serializers.ModelSerializer):
    creado_por = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = gemar_parte_hecho_extraordinario
        fields = '__all__'
        extra_kwargs = {
            'creado_por': {'required': False},
            'entidad': {'required': False},
            'provincia': {'required': False},
        }

#/***************************************************************************************************************************

class gemar_hecho_extraordinario_filter(filters.FilterSet):

    informado_garante = filters.CharFilter(method='filtrado_por_informado_garante',lookup_expr = 'icontains')

    def filtrado_por_informado_garante(self,queryset,value):        
        return queryset.filter(informado__icontains = value) | queryset.filter(garante__icontains = value) 
        
    
    class Meta:  
        model:gemar_hecho_extraordinario    
        fields:{
            'informado_garante':['icontains'],
        }
        
class gemar_hecho_extraordinario_serializer(serializers.ModelSerializer):
    producto_name = serializers.ReadOnlyField(source = 'producto_involucrado.nombre_producto')
    incidencia_name = serializers.ReadOnlyField(source = 'incidencia_involucrada.nombre_incidencia') 
    garante_name = serializers.ReadOnlyField(source = 'garante.nombre') 
    embalaje_name = serializers.ReadOnlyField(source = 'embalaje.nombre_tipo_embalaje')
    unidad_medida_name = serializers.ReadOnlyField(source = 'unidad_medida.unidad_medida')
    incidencia_involucrada_name = serializers.ReadOnlyField(source = 'incidencia_involucrada.nombre_incidencia')
    
    

    class Meta:
        model = gemar_hecho_extraordinario       
        fields = '__all__'
        filterset_class: gemar_hecho_extraordinario_filter #esto es para que se aplique al serializador el filtro



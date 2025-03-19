
from rest_framework import serializers
from django_filters import rest_framework as filters

from django.db.models import Q
from nomencladores.models import nom_producto,nom_tipo_embalaje,nom_unidad_medida,nom_tipo_equipo_ferroviario
from .models import vagon_cargado_descargado,productos_vagones_cargados_descargados, en_trenes,nom_equipo_ferroviario, producto_en_vagon



#****************-------------------------********************--------------------***************-----------------********************************
class producto_vagon_cargado_descargado_filter(filters.FilterSet):
    producto_contenido = filters.CharFilter(method='filtrado_por_producto_contenido',lookup_expr = 'icontains') 
    

    def filtrado_por_producto_contenido(self,queryset,value):        
        return queryset.filter(producto__icontains = value) | queryset.filter(contenido__icontains = value)
        
    
    class Meta:
  
        model : productos_vagones_cargados_descargados    
        fields:{
            'producto_contenido':['icontains'],        
        }



class productos_vagones_cargados_descargados_serializer(serializers.ModelSerializer):
    tipo_producto_name = serializers.ReadOnlyField(source='get_tipo_producto_display')
    producto_name = serializers.ReadOnlyField(source='producto.nombre_producto')
    tipo_embalaje_name = serializers.ReadOnlyField(source='tipo_embalaje.nombre_tipo_embalaje')
    tipo_embalaje_name = serializers.ReadOnlyField(source='tipo_embalaje.nombre_tipo_embalaje')
    unidad_medida_name = serializers.ReadOnlyField(source='unidad_medida.unidad_medida')
    estado_name = serializers.ReadOnlyField(source='get_estado_display')
    contiene_name = serializers.ReadOnlyField(source='get_contiene_display')

    class Meta:
        model = productos_vagones_cargados_descargados
        fields = (
            'id', 
            'tipo_producto', 
            'tipo_producto_name', 
            'producto', 
            'producto_name', 
            'tipo_embalaje', 
            'tipo_embalaje_name', 
            'unidad_medida', 
            'unidad_medida_name', 
            'cantidad', 
            'estado', 
            'estado_name', 
            'contiene', 
            'contiene_name',
        )
        extra_kwargs = {
            'estado': {'allow_null': True},
            'contiene': {'allow_null': True},
        }
#****************-------------------------********************--------------------***************-----------------********************************
class vagon_cargado_descargado_filter(filters.FilterSet):
    origen_t_e_ferroviario = filters.CharFilter(method='filtrado_por_origen_t_e_ferroviario',lookup_expr = 'icontains') 
    

    def filtrado_por_origen_t_e_ferroviario(self,queryset,value):        
        return queryset.filter(origen__icontains = value) | queryset.filter(tipo_equipo_ferroviario_name__icontains = value)
        
    
    class Meta:
  
        model : vagon_cargado_descargado    
        fields:{
            'origen_t_e_ferroviario':['icontains'],        
        }



class vagon_cargado_descargado_serializer(serializers.ModelSerializer):
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
    tipo_equipo_ferroviario_name = serializers.ReadOnlyField(source='tipo_equipo_ferroviario.get_tipo_equipo_display')
    estado_name = serializers.ReadOnlyField(source='get_estado_display')
    operacion_name = serializers.ReadOnlyField(source='get_operacion_display')
    tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto_name = serializers.ReadOnlyField(source='producto.producto.nombre_producto')

    class Meta:
        model = vagon_cargado_descargado
        fields = (
            'id', 
            'tipo_origen', 
            'tipo_origen_name', 
            'origen', 
            'tipo_equipo_ferroviario', 
            'tipo_equipo_ferroviario_name', 
            'estado', 
            'estado_name', 
            'operacion', 
            'operacion_name', 
            'plan_diario_carga_descarga', 
            'real_carga_descarga', 
            'tipo_destino', 
            'tipo_destino_name', 
            'destino', 
            'causas_incumplimiento', 
            'producto', 
            'producto_name'
        )
        extra_kwargs = {
            'causas_incumplimiento': {'allow_null': True},
        }
        
#-------------------------********************------------EN_TRENES--------------------***************-----------------************    

class en_trenes_filter(filters.FilterSet):
    origen_destino_producto = filters.CharFilter(method='filter_by_origen_destino_producto_trenes',lookup_expr = 'icontains')

    #filtrado por origen,destino y descripcion del producto
    def filter_by_origen_destino_producto_trenes(self,queryset,value):        
        return  queryset.filter(origen_en_trenes__icontains = value) | queryset.filter(destino_en_trenes_exact = value)
    
    class Meta:
  
        model : en_trenes    
        fields:{
            'origen_destino_producto':['icontains'],
        }




class en_trenes_serializer(serializers.ModelSerializer):
   # tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
   # estado_name = serializers.ReadOnlyField(source='get_estado_display')
   # tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto_name = serializers.ReadOnlyField(source='producto.producto.nombre_producto')
    tipo_equipo_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_equipo_display')
    equipo_carga_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_carga_display')
    equipo_vagon_id=serializers.ReadOnlyField(source='equipo_vagon.numero_identificacion')
   
    class Meta:
        model = en_trenes
        fields = (
            'id', 
            'tipo_origen', 
           # 'tipo_origen_name', 
            'origen', 
            'locomotora',
            'numero_identificacion_locomotora',
            'tipo_equipo', 
            'tipo_equipo_name',
            'equipo_carga_name',
            'equipo_vagon',
            'equipo_vagon_id',
            'estado', 
          #  'estado_name',  
            'tipo_destino', 
           # 'tipo_destino_name', 
            'destino', 
            'producto', 
            'producto_name',
            'cantidad_vagones',
            'observaciones',
        )
        filterset_class=en_trenes_filter
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
        # Filtra las opciones del campo locomotora
            if 'locomotora' in self.fields:
                self.fields['locomotora'].queryset = nom_equipo_ferroviario.objects.filter(
                tipo_equipo__tipo_equipo='locomotora'
            )
                
                
class producto_vagon_serializer(serializers.ModelSerializer):
   # tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
   # estado_name = serializers.ReadOnlyField(source='get_estado_display')
   # tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto_name = serializers.ReadOnlyField(source='producto.nombre_producto')
    producto_codigo = serializers.ReadOnlyField(source='producto.codigo_producto')
    tipo_embalaje_name=serializers.ReadOnlyField(source='tipo_embalaje.nombre_tipo_embalaje')
    unidad_medida_name=serializers.ReadOnlyField(source='unidad_medida.unidad_medida')
    
    class Meta:
        model = producto_en_vagon
        fields = (
            'id', 
           'producto',
           'producto_name',
           'producto_codigo',
           'tipo_embalaje',
           'tipo_embalaje_name',
           'unidad_medida',
           'unidad_medida_name',
           'producto',
           'cantidad',
           'contiene',
           'estado'
        )
        filterset_class=en_trenes_filter
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
  
    
from rest_framework import serializers
from django_filters import rest_framework as filters

from django.db.models import Q
from nomencladores.models import nom_producto,nom_tipo_embalaje,nom_unidad_medida,nom_tipo_equipo_ferroviario
from .models import vagon_cargado_descargado,productos_vagones_cargados_descargados, en_trenes,nom_equipo_ferroviario, producto_en_vagon
from .models import por_situar_carga_descarga,Situado_Carga_Descarga,arrastres
from .models import registro_vagones_cargados

from Administracion.models import Auditoria 
from rest_framework.response import Response
from rest_framework import status

#transaction.atomic crea una transacción atómica que asegura que:
#O todas las operaciones se ejecutan correctamente O ninguna se ejecuta (si ocurre algún error)
from django.db import transaction 

#para cada modelo del que deseemos realizar el filtrado debemos hacer un filtrado
#nom_pais_filter es una clase que se implementa para definir sobre qué campos quiero filtrar los registros de mi API, 
#hereda de filters.FilterSet




#****************-------------------------********************--------------------***************-----------------********************************
#serializador para los productos de vagones cargados/descargados
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
#serializador para el estado de vagones cargados/descargados
class vagon_cargado_descargado_filter(filters.FilterSet):
    tef_prod_estado = filters.CharFilter(method='filtrado_por_tef_prod_estado', lookup_expr='icontains')
    
    def filtrado_por_tef_prod_estado(self, queryset, name, value):        
        return queryset.filter(
            Q(tipo_equipo_ferroviario_name__icontains=value) | 
            Q(productos_list__icontains=value) | 
            Q(estado_name__icontains=value)
        )
    
    class Meta:
        model = vagon_cargado_descargado
        fields = ['tef_prod_estado']



class vagon_cargado_descargado_serializer(serializers.ModelSerializer):
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
    tipo_equipo_ferroviario_name = serializers.ReadOnlyField(source='tipo_equipo_ferroviario.get_tipo_equipo_display')
    estado_name = serializers.ReadOnlyField(source='get_estado_display')
    operacion_name = serializers.ReadOnlyField(source='get_operacion_display')
    tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto_name = serializers.ReadOnlyField(source='producto.nombre_producto')
    productos_list = serializers.SerializerMethodField()  # Campo custom para nombres

    producto_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=productos_vagones_cargados_descargados.objects.all(),
        source='producto',  # Esto mapea al campo ManyToManyField
        write_only=True,
        required=False
    )
    
    registros_vagones_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
        help_text="Lista de objetos para crear registros_vagones_cargados"
    )

    
    

    class Meta:
        model = vagon_cargado_descargado
        fields = '__all__'  # O lista explícita incluyendo 'productos_list'
        extra_kwargs = {
            'producto': {'read_only': True},
            'registros_vagones': {'read_only': True}
        }

    def create(self, validated_data):
        try:
            with transaction.atomic():
                # Extraer datos para relaciones
                productos_ids = validated_data.pop('producto_ids', [])
                registros_data = validated_data.pop('registros_vagones_data', [])
                
                # Crear instancia principal
                instance = super().create(validated_data)
                
                # Asignar productos
                if productos_ids:
                    instance.producto.set(productos_ids)
                
                # Crear y asociar registros de vagones
                for registro_data in registros_data:
                    registro = registro_vagones_cargados.objects.create(**registro_data)
                    instance.registros_vagones.add(registro)
                
                return instance
                
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el registro: {str(e)}")
                
        except Exception as e:
            raise serializers.ValidationError(
                f"Error al crear el vagon: {str(e)}"
            )    

    def get_productos_list(self, obj):
        return ", ".join([
            p.producto.nombre_producto 
            for p in obj.producto.all() 
            if hasattr(p, 'producto')
        ])
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Registrar acción de auditoría antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar vagón cargado/descargado y sus registros asociados: {instance.id}",
            navegador=navegador,
        )
        
        # Esto activará el método delete() del modelo que maneja la eliminación en cascada
        instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


#serializador para los vagones asignados al estado vagones cargados/descargados
class registro_vagones_cargados_filter(filters.FilterSet):
    no_id_origen = filters.CharFilter(method='filtrado_por_no_id_origen',lookup_expr = 'icontains') 
    

    def filtrado_por_no_id_origen(self,queryset,value):        
        return queryset.filter(origen__icontains = value) | queryset.filter(no_id__icontains = value)
        
    
    class Meta:
  
        model : registro_vagones_cargados    
        fields:{
            'no_id_origen':['icontains'],        
        }



class registro_vagones_cargados_serializer(serializers.ModelSerializer):
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
    identificacion = serializers.SerializerMethodField()
    
    class Meta:
        model = registro_vagones_cargados
        fields = '__all__'
        extra_kwargs = {
            'no_id': {
                'validators': []  # Remover validación única del serializer
            }
        }

        read_only_fields = ('identificacion', 'tipo_origen_name')  # Marcar campos como solo lectura
    
    def get_identificacion(self, obj):
        return obj.no_id if obj.no_id else f"Registro-{obj.id}"
    
    def validate_no_id(self, value):
        # Validación manual que permite actualización pero no duplicados nuevos
        if self.instance is None and registro_vagones_cargados.objects.filter(no_id=value).exists():
            raise serializers.ValidationError("Ya existe un vagón con este ID")
        return value

    def create(self, validated_data):
        try:
            # Intentar obtener o crear
            obj, created = registro_vagones_cargados.objects.get_or_create(
                no_id=validated_data['no_id'],
                defaults=validated_data
            )
            if not created:
                # Si ya existía, actualizar sus datos
                for attr, value in validated_data.items():
                    setattr(obj, attr, value)
                obj.save()
            return obj
        except Exception as e:
            raise serializers.ValidationError(f"Error al guardar el vagón: {str(e)}")
        
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
  
        # Validar combinación única de Tipo equipo ferroviario y No. ID
       
                
                
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
        
  
    
class SituadoCargaDescargaFilter(filters.FilterSet):
    tipo_equipo = filters.CharFilter(lookup_expr='icontains')  # Filtro exacto (puedes usar 'icontains' para parcial
    
    
    class Meta:
        model = por_situar
        fields = ['tipo_equipo']  # Campos filtrables
        
        
class SituadoCargaDescargaSerializers(serializers.ModelSerializer):
    producto_name = serializers.ReadOnlyField(source='producto.producto.nombre_producto')
    class Meta:
        model = Situado_Carga_Descarga
        fields = ('id','tipo_origen','origen', 'tipo_equipo', 'estado', 'operacion', 'producto','producto_name', 'situados','pendiente_proximo_dia')
        filterset_class = SituadoCargaDescargaFilter
        
        
        
        
class PorSituarCargaDescargaFilter(filters.FilterSet):
    tipo_equipo = filters.CharFilter(lookup_expr='icontains')  # Filtro exacto (puedes usar 'icontains' para parcial
   
    class Meta:
        model = por_situar
        fields = ['tipo_equipo']  # Campos filtrables


class PorSituarCargaDescargaSerializer(serializers.ModelSerializer):
    producto_name = serializers.ReadOnlyField(source='producto.producto.nombre_producto')
    tipo_origen_name = serializers.ReadOnlyField(source='tipo_origen')
    
    class Meta:
        model = por_situar
        fields = ('id','tipo_origen','tipo_origen_name','origen','tipo_equipo', 'estado', 'operacion', 'producto', 'por_situar','producto_name')
        filterset_class = PorSituarCargaDescargaFilter
        extra_kwargs = {
            'producto': {'allow_null': True, 'required': False},
            'observaciones': {'allow_null': True, 'required': False}
        }

    def validate(self, data):
        # Validar que el producto sea opcional
        if 'producto' not in data:
            data['producto'] = None
            
        return data


class PendienteArrastreFilter(filters.FilterSet):
    tipo_equipo = filters.CharFilter(lookup_expr='icontains')  # Filtro exacto (puedes usar 'icontains' para parcial
    
    class Meta:
        model = arrastres
        fields = ['tipo_equipo']  # Campos filtrables
        
class PendienteArrastreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = arrastres
        fields= ('id','tipo_origen','tipo_equipo','estado','producto','cantidad_vagones','destino')
        filterset_class = PendienteArrastreFilter



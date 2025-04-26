import django_filters
from rest_framework import serializers
from django_filters import rest_framework as filters

from django.db.models import Q
from nomencladores.models import nom_producto,nom_tipo_embalaje,nom_unidad_medida,nom_tipo_equipo_ferroviario

#Importando modelos de UFC
from .models import (vagon_cargado_descargado,producto_UFC, en_trenes,nom_equipo_ferroviario
                    ,por_situar,Situado_Carga_Descarga,arrastres 
                    ,registro_vagones_cargados,vagones_productos,rotacion_vagones 
                     )

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



#****************************************************************************************************************
#serializador para los productos del modelo vagones y  productos


#****************-------------------------********************--------------------***************-----------------********************************
#serializador para el modelo vagones y productos
class vagones_productos_filter(filters.FilterSet):
    origen_tipo_prod_tef = filters.CharFilter(method='filtrado_por_origen_tipo_prod_tef', lookup_expr='icontains')
    
    def filtrado_por_origen_tipo_prod_tef(self, queryset, name, value):        
        return queryset.filter(
            Q(tipo_equipo_ferroviario_name__icontains=value) | 
            Q(productos_list__icontains=value) | 
            Q(tipo_origen_name__icontains=value)
        )
    
    class Meta:
        model = vagones_productos
        fields = ['origen_tipo_prod_tef']



class vagones_productos_serializer(serializers.ModelSerializer):
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')    
    tipo_equipo_ferroviario_name = serializers.ReadOnlyField(source='tipo_equipo_ferroviario.get_tipo_equipo_display')
    tipo_combustible_name = serializers.ReadOnlyField(source='get_tipo_combustible_display')    
    producto_name = serializers.ReadOnlyField(source='producto.nombre_producto')
    productos_list = serializers.SerializerMethodField()  # Campo custom para nombres

    producto_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        source='producto',  # Esto mapea al campo ManyToManyField
        write_only=True,
        required=False
    )   
    

    class Meta:
        model = vagones_productos
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
                
                return instance
                
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el registro: {str(e)}")
                
        except Exception as e:
            raise serializers.ValidationError(
                f"Error al crear el registro: {str(e)}"
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
            accion=f"Eliminar vagones y productos: {instance.id}",
            navegador=navegador,
        )
        
        # Esto activará el método delete() del modelo que maneja la eliminación en cascada
        instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
#**************************************************************************************************************************************
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
        queryset=producto_UFC.objects.all(),
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
        fields: dict[str, list[str]] = {
            'no_id_origen': ['icontains'],        
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

class en_trenes_filter(django_filters.FilterSet):
    search = filters.CharFilter(method='filtro_busqueda', lookup_expr='icontains')

    def filtro_busqueda(self, queryset, name, value):
        return queryset.filter(
            Q(tipo_equipo__icontains=value) |
            Q(numero_identificacion_locomotora__icontains=value) |
            Q(origen__icontains=value) |
            Q(destino__icontains=value)|
            Q(producto__nombre_producto__icontains=value) |  # Busca por nombre de producto
            Q(producto__codigo_producto__icontains=value)    # Busca por código de producto
        ).distinct()
    

    class Meta:
        model = en_trenes
        fields = ['search']  # Campos filtrables




class en_trenes_serializer(serializers.ModelSerializer):
   # tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
   # estado_name = serializers.ReadOnlyField(source='get_estado_display')
   # tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto_name = serializers.ReadOnlyField(source='producto.producto.nombre_producto')
    tipo_equipo_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_equipo_display')
    equipo_carga_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_carga_display')
    equipo_vagon_id=serializers.ReadOnlyField(source='equipo_vagon.numero_identificacion')
    productos_info = serializers.SerializerMethodField()
    producto = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    class Meta:
        model = en_trenes
        fields = (
            'id', 
            'tipo_origen', 
            'origen', 
            'locomotora',
            'numero_identificacion_locomotora',
            'tipo_equipo', 
            'tipo_equipo_name',
            'equipo_carga_name',
            'equipo_vagon',
            'equipo_vagon_id',
            'estado', 
            'tipo_destino',  
            'destino', 
            'producto', 
            'productos_info',
            'producto_name',
            'cantidad_vagones',
            'observaciones',
        )
        
    def get_productos_info(self, obj):
        productos = obj.producto.all()
        return [{
            'id': p.id,
            'nombre_producto': p.producto.nombre_producto,
            'codigo_producto': p.producto.codigo_producto,
            'tipo_embalaje': p.tipo_embalaje.nombre if hasattr(p.tipo_embalaje, 'nombre') else str(p.tipo_embalaje),
            'unidad_medida': p.unidad_medida.nombre if hasattr(p.unidad_medida, 'nombre') else str(p.unidad_medida),
            'cantidad': p.cantidad,
            'estado': p.estado,
            'contiene': p.contiene
        } for p in productos]

    def create(self, validated_data):
        productos_data = validated_data.pop('producto', [])
        instance = por_situar.objects.create(**validated_data)
        instance.producto.set(productos_data)
        return instance

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('producto', None)
        instance = super().update(instance, validated_data)
        if productos_data is not None:
            instance.producto.set(productos_data)
        return instance

        
            
    filterset_class=en_trenes_filter
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtra las opciones del campo locomotora
        if 'locomotora' in self.fields:
                self.fields['locomotora'].queryset = nom_equipo_ferroviario.objects.filter(
                tipo_equipo__tipo_equipo='locomotora'
            )
  
        # Validar combinación única de Tipo equipo ferroviario y No. ID
       
       # if 'tipo_equipo' in self.initial_data and 'numero_identificacion_locomotora' in self.initial_data:
       #     tipo_equipo = self.initial_data['tipo_equipo']
       #     numero_identificacion_locomotora = self.initial_data['numero_identificacion_locomotora']
       #     if en_trenes.objects.filter(tipo_equipo=tipo_equipo, numero_identificacion_locomotora=numero_identificacion_locomotora).exists():
       #         raise serializers.ValidationError("La combinación de tipo de equipo y número de identificación de locomotora ya existe.")
                
                
class producto_vagon_serializer(serializers.ModelSerializer):
   # tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
   # estado_name = serializers.ReadOnlyField(source='get_estado_display')
   # tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto_name = serializers.ReadOnlyField(source='producto.nombre_producto')
    producto_codigo = serializers.ReadOnlyField(source='producto.codigo_producto')
    tipo_embalaje_name=serializers.ReadOnlyField(source='tipo_embalaje.nombre_tipo_embalaje')
    unidad_medida_name=serializers.ReadOnlyField(source='unidad_medida.unidad_medida')
    
    class Meta:
        model = producto_UFC
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
    productos_info = serializers.SerializerMethodField()
    producto = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    situados = serializers.IntegerField()
    pendiente_proximo_dia = serializers.IntegerField()
    
    class Meta:
        model = Situado_Carga_Descarga
        fields = ('id', 'tipo_origen', 'origen', 'tipo_equipo', 'estado', 
                 'operacion', 'producto', 'productos_info', 'situados', 
                 'pendiente_proximo_dia', 'observaciones')
        extra_kwargs = {
            'producto': {'required': False},
            'observaciones': {'required': False, 'allow_null': True}
        }

    def get_productos_info(self, obj):
        productos = obj.producto.all()
        return [{
            'id': p.id,
            'nombre_producto': p.producto.nombre_producto,
            'codigo_producto': p.producto.codigo_producto,
            'tipo_embalaje': p.tipo_embalaje.nombre if hasattr(p.tipo_embalaje, 'nombre') else str(p.tipo_embalaje),
            'unidad_medida': p.unidad_medida.nombre if hasattr(p.unidad_medida, 'nombre') else str(p.unidad_medida),
            'cantidad': p.cantidad,
            'estado': p.estado,
            'contiene': p.contiene
        } for p in productos] # (truco) Esta bueno este truquito para evitar errores si el objeto no tiene el atributo
        
    def to_internal_value(self, data):
        # Convertir los valores de string a integer antes de la validación
        if 'situados' in data:
            data['situados'] = int(data['situados']) if data['situados'] else 0
        if 'pendiente_proximo_dia' in data:
            data['pendiente_proximo_dia'] = int(data['pendiente_proximo_dia']) if data['pendiente_proximo_dia'] else 0
        return super().to_internal_value(data)
        
    def validate(self, data):
        # Validar que el producto sea opcional
        if 'producto' not in data:
            data['producto'] = []
        return data

    def create(self, validated_data):
        # Extraer los productos si vienen en los datos
        productos_data = validated_data.pop('producto', [])
        instance = super().create(validated_data)
        
        # Asignar los productos al modelo
        if productos_data:
            instance.producto.set(productos_data)
        return instance

    def update(self, instance, validated_data):
        # Extraer los productos si vienen en los datos
        productos_data = validated_data.pop('producto', None)
        
        # Actualizar los otros campos
        instance = super().update(instance, validated_data)
        
        # Actualizar los productos si se proporcionaron
        if productos_data is not None:
            instance.producto.set(productos_data)
        return instance        
        
        
        
class PorSituarCargaDescargaFilter(filters.FilterSet):
    tipo_equipo = filters.CharFilter(lookup_expr='icontains')  # Filtro exacto (puedes usar 'icontains' para parcial
   
    class Meta:
        model = por_situar
        fields = ['tipo_equipo']  # Campos filtrables


class PorSituarCargaDescargaSerializer(serializers.ModelSerializer):
    productos_info = serializers.SerializerMethodField()
    tipo_origen_name = serializers.ReadOnlyField(source='tipo_origen')
    producto = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    
    class Meta:
        model = por_situar
        fields = ('id', 'tipo_origen', 'tipo_origen_name', 'origen', 'tipo_equipo', 
                 'estado', 'operacion', 'producto', 'por_situar', 'productos_info', 'observaciones')
        extra_kwargs = {
            'producto': {'required': False},
            'observaciones': {'required': False, 'allow_null': True}
        }

    def get_productos_info(self, obj):
        productos = obj.producto.all()
        return [{
            'id': p.id,
            'nombre_producto': p.producto.nombre_producto,
            'codigo_producto': p.producto.codigo_producto,
            'tipo_embalaje': p.tipo_embalaje.nombre if hasattr(p.tipo_embalaje, 'nombre') else str(p.tipo_embalaje),
            'unidad_medida': p.unidad_medida.nombre if hasattr(p.unidad_medida, 'nombre') else str(p.unidad_medida),
            'cantidad': p.cantidad,
            'estado': p.estado,
            'contiene': p.contiene
        } for p in productos]

    def create(self, validated_data):
        productos_data = validated_data.pop('producto', [])
        instance = por_situar.objects.create(**validated_data)
        instance.producto.set(productos_data)
        return instance

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('producto', None)
        instance = super().update(instance, validated_data)
        if productos_data is not None:
            instance.producto.set(productos_data)
        return instance


class PendienteArrastreFilter(filters.FilterSet):
    tipo_equipo = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = arrastres
        fields = ['tipo_equipo']

class PendienteArrastreSerializer(serializers.ModelSerializer):
    productos_info = serializers.SerializerMethodField()
    producto = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    
    class Meta:
        model = arrastres
        fields = ('id', 'tipo_origen', 'origen', 'tipo_equipo', 'estado', 
                 'producto', 'productos_info', 'cantidad_vagones', 'tipo_destino', 'destino')
        filterset_class = PendienteArrastreFilter

    def get_productos_info(self, obj):
        productos = obj.producto.all()
        return [{
           'id': p.id,
            'nombre_producto': p.producto.nombre_producto,
            'codigo_producto': p.producto.codigo_producto,
            'tipo_embalaje': p.tipo_embalaje.nombre if hasattr(p.tipo_embalaje, 'nombre') else str(p.tipo_embalaje),
            'unidad_medida': p.unidad_medida.nombre if hasattr(p.unidad_medida, 'nombre') else str(p.unidad_medida),
            'cantidad': p.cantidad,
            'estado': p.estado,
            'contiene': p.contiene
        } for p in productos]

    def create(self, validated_data):
        productos_data = validated_data.pop('producto', [])
        instance = arrastres.objects.create(**validated_data)
        instance.producto.set(productos_data)
        return instance

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('producto', None)
        instance = super().update(instance, validated_data)
        if productos_data is not None:
            instance.producto.set(productos_data)
        return instance


class RotacionVagonesSerializer(serializers.ModelSerializer):
    tipo_equipo_ferroviario_nombre = serializers.CharField(
        source="tipo_equipo_ferroviario.tipo_eqipo", read_only=True
    )

    class Meta:
        model = rotacion_vagones
        fields = [
            "id",
            "tipo_equipo_ferroviario",
            "tipo_equipo_ferroviario_nombre",  # Campo adicional para mostrar el nombre del equipo
            "en_servicio",
            "plan_carga",
            "real_carga",
            "plan_rotacion",
            "real_rotacion",
            "creado_el",
            "actualizado_el",
        ]
        read_only_fields = ["creado_el", "actualizado_el"]


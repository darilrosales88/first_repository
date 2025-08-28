 #1. en este archivo se implementaran todos los serializadores que se usaran en la app, primero
# se importa desde restframeuork los serializadores(serializers), luego se importan los modelos,
from rest_framework import serializers
#para trabajar con el filtrado de los serialziadores debemos hacer la siguiente importacion
from django_filters import rest_framework as filters
from gemar.models import PartePBIP, CargaVieja, ExistenciaMercancia
from nomencladores.serializers import (
    nom_embarcacion_serializer, nom_puerto_serializer, nom_terminal_serializer, 
    nom_producto_serializer, nom_osde_oace_organismo_serializer, nom_tipo_embalaje_serializer,
    nom_unidad_medida_serializer
)
from django.db.models import Q

from .models import (gemar_hecho_extraordinario,gemar_parte_hecho_extraordinario,gemar_programacion_maniobras,
                     gemar_parte_programacion_maniobras,gemar_parte_carga_descarga)
from nomencladores.models import nom_embarcacion as Buque  # Add this import
from nomencladores.models import nom_puerto as Puerto  # Also need this for puerto_id
from nomencladores.models import nom_terminal as Terminal  # For terminal_id
from nomencladores.models import nom_producto as Producto  # For producto_id
from nomencladores.models import nom_osde_oace_organismo as Organismo  # For organismo_id
from nomencladores.models import nom_tipo_embalaje as TipoEmbalaje  # For tipo_embalaje_id
from nomencladores.models import nom_unidad_medida as UnidadMedida
from nomencladores.models import nom_puerto
from Administracion.serializers import UserPermissionSerializer as CustomUserSerializer
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
    creado_por_name = serializers.ReadOnlyField(source = 'creado_por.username')
    aprobado_por_name = serializers.ReadOnlyField(source = 'aprobado_por.username')
    entidad_name = serializers.ReadOnlyField(source = 'entidad.nombre')
    provincia_name = serializers.ReadOnlyField(source = 'provincia.nombre_provincia')
    organismo_name = serializers.ReadOnlyField(source = 'organismo.nombre')
    
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

#***************************************************************************************************************************
class gemar_parte_programacion_maniobras_filter(filters.FilterSet):
    fecha_entidad = filters.CharFilter(method='filtrado_por_fecha_entidad')
    
    def filtrado_por_fecha_entidad(self, queryset, name, value):        
        return queryset.filter(
            Q(fecha_operacion__icontains=value) | 
            Q(entidad__nombre__icontains=value)
        )
    
    class Meta:  
        model = gemar_parte_programacion_maniobras    
        fields = {
            'fecha_operacion': ['exact', 'contains'],
            'entidad__nombre': ['exact', 'contains'],
        }

class gemar_parte_programacion_maniobras_serializer(serializers.ModelSerializer):
    creado_por = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    creado_por_name = serializers.ReadOnlyField(source='creado_por.username')
    aprobado_por_name = serializers.ReadOnlyField(source='aprobado_por.username')
    entidad_name = serializers.ReadOnlyField(source='entidad.nombre')
    provincia_name = serializers.ReadOnlyField(source='provincia.nombre_provincia')    
    organismo_name = serializers.ReadOnlyField(source = 'organismo.nombre')
    
    class Meta:
        model = gemar_parte_programacion_maniobras
        fields = '__all__'
        extra_kwargs = {
            'creado_por': {'required': False},
            'entidad': {'required': False},
            'provincia': {'required': False},
        }
#***************************************************************************************************************************
class gemar_parte_carga_descarga_filter(filters.FilterSet):
    fecha_entidad = filters.CharFilter(method='filtrado_por_fecha_entidad')
    
    def filtrado_por_fecha_entidad(self, queryset, name, value):        
        return queryset.filter(
            Q(fecha_operacion__icontains=value) | 
            Q(entidad__nombre__icontains=value)
        )
    
    class Meta:  
        model = gemar_parte_carga_descarga    
        fields = {
            'fecha_operacion': ['exact', 'contains'],
            'entidad__nombre': ['exact', 'contains'],
        }

class gemar_parte_carga_descarga_serializer(serializers.ModelSerializer):
    creado_por = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    creado_por_name = serializers.ReadOnlyField(source='creado_por.username')
    aprobado_por_name = serializers.ReadOnlyField(source='aprobado_por.username')
    entidad_name = serializers.ReadOnlyField(source='entidad.nombre')
    provincia_name = serializers.ReadOnlyField(source='provincia.nombre_provincia')    
    organismo_name = serializers.ReadOnlyField(source = 'organismo.nombre')
    
    class Meta:
        model = gemar_parte_carga_descarga
        fields = '__all__'
        extra_kwargs = {
            'creado_por': {'required': False},
            'entidad': {'required': False},
            'provincia': {'required': False},
        }
#***************************************************************************************************************************
class gemar_programacion_maniobras_filter(filters.FilterSet):
    buque_puerto = filters.CharFilter(method='filtrado_por_buque_puerto', lookup_expr='icontains')

    def filtrado_por_buque_puerto(self, queryset, value):        
        return queryset.filter(buque__icontains=value) | queryset.filter(puerto__nombre__icontains=value)
    
    class Meta:  
        model = gemar_programacion_maniobras    
        fields = []

class gemar_programacion_maniobras_serializer(serializers.ModelSerializer):
    buque_name = serializers.ReadOnlyField(source='puerto.nombre_puerto')
    puerto_name = serializers.ReadOnlyField(source='puerto.nombre_puerto')
    terminal_name = serializers.ReadOnlyField(source='terminal.nombre_terminal')
    atraque_name = serializers.ReadOnlyField(source='atraque.nombre_atraque')
    puerto_procedencia_name = serializers.ReadOnlyField(source='puerto_procedencia.nombre_puerto')
    tipo_maniobra_name = serializers.ReadOnlyField(source='tipo_maniobra.tipo_maniobra')
    
    class Meta:
        model = gemar_programacion_maniobras
        fields = '__all__'
        filterset_class = gemar_programacion_maniobras_filter

class PartePBIPSerializer(serializers.ModelSerializer):
    buque = nom_embarcacion_serializer(read_only=True)
    buque_id = serializers.PrimaryKeyRelatedField(
        queryset=Buque.objects.all(),  # O Buque.objects.filter(tipo_embarcacion='buque') si aplica
        write_only=True,
        source='buque'
    )
    puerto = nom_puerto_serializer(read_only=True)
    puerto_id = serializers.PrimaryKeyRelatedField(
        queryset=nom_puerto.objects.all(),
        write_only=True,
        source='puerto'
    )
    creado_por = CustomUserSerializer(read_only=True)

    class Meta:
        model = PartePBIP
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'creado_por', 'aprobado_por')

    def create(self, validated_data):
        validated_data['creado_por'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        # Validar combinación única de buque, puerto y nivel
        if PartePBIP.objects.filter(
            buque=data.get('buque'),
            puerto=data.get('puerto'),
            nivel=data.get('nivel'),
            fecha_operacion=data.get('fecha_operacion')
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(
                "La combinación de Buque, Puerto y Nivel para esta fecha ya existe."
            )
        return data

# gemar/serializers.py (actualización de CargaViejaSerializer)
class CargaViejaSerializer(serializers.ModelSerializer):
    parte = serializers.PrimaryKeyRelatedField(queryset=PartePBIP.objects.all())
    puerto = nom_puerto_serializer(read_only=True)
    puerto_id = serializers.PrimaryKeyRelatedField(
        queryset=Puerto.objects.all(),
        write_only=True,
        source='puerto',
        required=True
    )
    terminal = nom_terminal_serializer(read_only=True)
    terminal_id = serializers.PrimaryKeyRelatedField(
        queryset=Terminal.objects.all(),
        write_only=True,
        source='terminal',
        required=True
    )
    producto = nom_producto_serializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        write_only=True,
        source='producto',
        required=True
    )
    organismo = nom_osde_oace_organismo_serializer(read_only=True)
    organismo_id = serializers.PrimaryKeyRelatedField(
        queryset=Organismo.objects.all(),
        write_only=True,
        source='organismo',
        required=True
    )

    class Meta:
        model = CargaVieja
        fields = '__all__'
        extra_kwargs = {
            'manifiesto': {'required': True},
            'toneladas_ayer': {'required': True},
            'toneladas_hoy': {'required': True},
            'dias_almacen': {'required': True},
            'plan': {'required': True},
            'real': {'required': True}
        }

    def validate(self, data):
        parte = data.get('parte')
        puerto = data.get('puerto')
        terminal = data.get('terminal')
        producto = data.get('producto')
        manifiesto = data.get('manifiesto')
        organismo = data.get('organismo')

        if CargaVieja.objects.filter(
            parte=parte,
            puerto=puerto,
            terminal=terminal,
            producto=producto,
            manifiesto=manifiesto,
            organismo=organismo
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(
                "Ya existe un registro con esta combinación de Puerto, Terminal, Producto, Manifiesto y Organismo."
            )
        
        # Validar que terminal pertenezca al puerto
        if terminal.puerto != puerto:
            raise serializers.ValidationError(
                "La terminal seleccionada no pertenece al puerto especificado."
            )
        
        return data

class ExistenciaMercanciaSerializer(serializers.ModelSerializer):
    terminal = nom_terminal_serializer(read_only=True)
    terminal_id = serializers.PrimaryKeyRelatedField(
        queryset=Terminal.objects.filter(),
        write_only=True,
        source='terminal'
    )
    producto = nom_producto_serializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.filter(),
        write_only=True,
        source='producto'
    )
    tipo_embalaje = nom_tipo_embalaje_serializer(read_only=True, required=False)
    tipo_embalaje_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoEmbalaje.objects.filter(),
        write_only=True,
        source='tipo_embalaje',
        required=False,
        allow_null=True
    )
    unidad_medida = nom_unidad_medida_serializer(read_only=True)
    unidad_medida_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadMedida.objects.filter(),
        write_only=True,
        source='unidad_medida'
    )
    creado_por = CustomUserSerializer(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    tipo_producto_display = serializers.CharField(source='get_tipo_producto_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    contiene_display = serializers.CharField(source='get_contiene_display', read_only=True)
    estado_registro_display = serializers.CharField(source='get_estado_registro_display', read_only=True)

    class Meta:
        model = ExistenciaMercancia
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'creado_por')

    def validate(self, data):
        fecha_operacion = data.get('fecha_operacion')
        terminal = data.get('terminal')
        tipo = data.get('tipo')
        producto = data.get('producto')
        tipo_embalaje = data.get('tipo_embalaje')
        unidad_medida = data.get('unidad_medida')

        if ExistenciaMercancia.objects.filter(
            fecha_operacion=fecha_operacion,
            terminal=terminal,
            tipo=tipo,
            producto=producto,
            tipo_embalaje=tipo_embalaje,
            unidad_medida=unidad_medida
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(
                "Ya existe un registro con esta combinación de Terminal, Tipo, Producto, Tipo de Embalaje y Unidad de Medida para esta fecha."
            )
        
        # Validaciones específicas para contenedores
        tipo_producto = data.get('tipo_producto')
        estado = data.get('estado')
        contiene = data.get('contiene')
        
        if tipo_producto == 2:  # Contenedor
            if not estado:
                raise serializers.ValidationError(
                    "Para contenedores debe especificar el estado."
                )
            if estado == 2 and not contiene:  # Lleno
                raise serializers.ValidationError(
                    "Para contenedores llenos debe especificar qué contienen."
                )
        else:
            data['estado'] = None
            data['contiene'] = None
            
        return data

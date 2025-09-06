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
                     gemar_parte_programacion_maniobras,gemar_parte_carga_descarga,gemar_carga_descarga,
                     gemar_producto_carga_descarga,gemar_turno_carga_descarga,gemar_incidencia_por_turno_carga_descarga,
                     gemar_informe_diario_enc,gemar_maniobras_portuarias_enc,gemar_afectaciones_maniobras_portuarias_enc,
                     gemar_carga_seca_enc,gemar_remolcadores_maniobras_enc,gemar_remolcador_carga_liquida_enc,
                     gemar_remolcador_cabotaje_auxiliar_enc)
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
class gemar_carga_descarga_filter(filters.FilterSet):
    operacion_buque_terminal = filters.CharFilter(method='filtrado_por_operacion_buque_terminal')
    
    def filtrado_por_operacion_buque_terminal(self, queryset, name, value):        
        return queryset.filter(
            Q(operacion__icontains=value) | 
            Q(buque__nombre_embarcacion__icontains=value) |
            Q(terminal__nombre_terminal__icontains=value)
        )
    
    class Meta:  
        model = gemar_carga_descarga    
        fields = {
            'operacion': ['exact', 'contains'],
            'buque__nombre_embarcacion': ['exact', 'contains'],
            'terminal__nombre_terminal': ['exact', 'contains'],
        }

class gemar_carga_descarga_serializer(serializers.ModelSerializer):    
    operacion_name = serializers.ReadOnlyField(source = 'get_operacion_display')
    categoria_name = serializers.ReadOnlyField(source = 'get_categoria_display')
    puerto_name = serializers.ReadOnlyField(source='puerto.nombre_puerto')
    segundo_puerto_name = serializers.ReadOnlyField(source='segundo_puerto.nombre_puerto')
    terminal_name = serializers.ReadOnlyField(source='terminal.nombre_terminal')
    atraque_name = serializers.ReadOnlyField(source='atraque.nombre_atraque')
    buque_name = serializers.ReadOnlyField(source='buque.nombre_embarcacion')
    
    
    class Meta:
        model = gemar_carga_descarga
        fields = '__all__'
        
#***************************************************************************************************************************
class gemar_producto_carga_descarga_filter(filters.FilterSet):
    producto_estado = filters.CharFilter(method='filtrado_por_producto_estado')
    
    def filtrado_por_producto_estado(self, queryset, name, value):        
        return queryset.filter(
            Q(estado__icontains=value) | 
            Q(producto__nombre_producto__icontains=value) 
        )
    
    class Meta:  
        model = gemar_producto_carga_descarga
        fields = {
            'estado': ['exact', 'contains'],
            'producto__nombre_producto': ['exact', 'contains'],
        }

class gemar_producto_carga_descarga_serializer(serializers.ModelSerializer):    
    tipo_producto_name = serializers.ReadOnlyField(source = 'get_tipo_producto_display')
    estado_name = serializers.ReadOnlyField(source = 'get_estado_display')
    producto_name = serializers.ReadOnlyField(source='producto.nombre_producto')
    tipo_embalaje_name = serializers.ReadOnlyField(source='tipo_embalaje.nombre_tipo_embalaje')
    unidad_medida_name = serializers.ReadOnlyField(source='unidad_medida.simbolo')
    
    
    class Meta:
        model = gemar_producto_carga_descarga
        fields = '__all__'
        
#***************************************************************************************************************************
class gemar_turno_carga_descarga_filter(filters.FilterSet):
    turno_cantidad_toneladas = filters.CharFilter(method='filtrado_por_turno_cantidad_toneladas')
    
    def filtrado_por_turno_cantidad_toneladas(self, queryset, name, value):        
        return queryset.filter(
            Q(turno__icontains=value) | 
            Q(cantidad_toneladas__icontains=value) 
        )
    
    class Meta:  
        model = gemar_turno_carga_descarga
        fields = {
            'turno': ['exact', 'contains'],
            'cantidad_toneladas': ['exact', 'contains'],
        }

class gemar_turno_carga_descarga_serializer(serializers.ModelSerializer):    
    turno_name = serializers.ReadOnlyField(source = 'get_turno_display')
    
    class Meta:
        model = gemar_turno_carga_descarga
        fields = '__all__'
        
#***************************************************************************************************************************
class gemar_incidencia_por_turno_carga_descarga_filter(filters.FilterSet):
    turno_incidencia = filters.CharFilter(method='filtrado_por_turno_incidencia')
    
    def filtrado_por_turno_incidencia(self, queryset, name, value):        
        return queryset.filter(
            Q(turno__icontains=value) | 
            Q(incidencia__nombre_incidencia__icontains=value) 
        )
    
    class Meta:  
        model = gemar_incidencia_por_turno_carga_descarga
        fields = {
            'turno': ['exact', 'contains'],
            'incidencia__nombre_incidencia': ['exact', 'contains'],
        }

class gemar_incidencia_por_turno_carga_descarga_serializer(serializers.ModelSerializer):    
    turno_name = serializers.ReadOnlyField(source = 'get_turno_display')
    incidencia_name = serializers.ReadOnlyField(source = 'incidencia.nombre_incidencia')
    class Meta:        
        model = gemar_incidencia_por_turno_carga_descarga
        fields = '__all__'
        
#***************************************************************************************************************************
class gemar_programacion_maniobras_filter(filters.FilterSet):
    buque_puerto = filters.CharFilter(method='filtrado_por_buque_puerto', lookup_expr='icontains')

    def filtrado_por_buque_puerto(self, queryset, value):        
        return queryset.filter(buque__icontains=value) | queryset.filter(puerto__nombre__icontains=value)
    
    class Meta:  
        model = gemar_programacion_maniobras    
        fields = []

class gemar_programacion_maniobras_serializer(serializers.ModelSerializer):
    buque_name = serializers.ReadOnlyField(source='buque.nombre_embarcacion')
    puerto_name = serializers.ReadOnlyField(source='puerto.nombre_puerto')
    terminal_name = serializers.ReadOnlyField(source='terminal.nombre_terminal')
    atraque_name = serializers.ReadOnlyField(source='atraque.nombre_atraque')
    puerto_procedencia_name = serializers.ReadOnlyField(source='puerto_procedencia.nombre_puerto')
    tipo_maniobra_name = serializers.ReadOnlyField(source='tipo_maniobra.tipo_maniobra')
    
    class Meta:
        model = gemar_programacion_maniobras
        fields = '__all__'
        filterset_class = gemar_programacion_maniobras_filter

################************* INFORME DIARIO ENC *****************##################****************************************
class gemar_informe_diario_enc_filter(filters.FilterSet):
    fecha_entidad = filters.CharFilter(method='filtrado_por_fecha_entidad')
    
    def filtrado_por_fecha_entidad(self, queryset, name, value):        
        return queryset.filter(
            Q(fecha_operacion__icontains=value) | 
            Q(entidad__nombre__icontains=value)
        )
    
    class Meta:  
        model = gemar_informe_diario_enc    
        fields = {
            'fecha_operacion': ['exact', 'contains'],
            'entidad__nombre': ['exact', 'contains'],
        }

class gemar_informe_diario_enc_serializer(serializers.ModelSerializer):
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
        model = gemar_informe_diario_enc
        fields = '__all__'
        extra_kwargs = {
            'creado_por': {'required': False},
            'entidad': {'required': False},
            'provincia': {'required': False},
        }
#**********************************************************************************************************************
class gemar_maniobras_portuarias_enc_filter(filters.FilterSet):
    buque_puerto = filters.CharFilter(method='filtrado_por_buque_puerto', lookup_expr='icontains')

    def filtrado_por_buque_puerto(self, queryset, value):        
        return queryset.filter(buque__icontains=value) | queryset.filter(puerto__nombre__icontains=value)
    
    class Meta:  
        model = gemar_maniobras_portuarias_enc    
        fields = []

class gemar_maniobras_portuarias_enc_serializer(serializers.ModelSerializer):
    buque_name = serializers.ReadOnlyField(source='buque.nombre_embarcacion')
    puerto_name = serializers.ReadOnlyField(source='puerto.nombre_puerto')    
    class Meta:
        model = gemar_maniobras_portuarias_enc
        fields = '__all__'
        filterset_class = gemar_maniobras_portuarias_enc_filter
#**********************************************************************************************************************
class gemar_afectaciones_maniobras_portuarias_enc_filter(filters.FilterSet):
    buque_puerto = filters.CharFilter(method='filtrado_por_buque_puerto', lookup_expr='icontains')

    def filtrado_por_buque_puerto(self, queryset, value):        
        return queryset.filter(buque__icontains=value) | queryset.filter(puerto__nombre__icontains=value)
    
    class Meta:  
        model = gemar_afectaciones_maniobras_portuarias_enc    
        fields = []

class gemar_afectaciones_maniobras_portuarias_enc_serializer(serializers.ModelSerializer):
    buque_name = serializers.ReadOnlyField(source='buque.nombre_embarcacion')
    puerto_name = serializers.ReadOnlyField(source='puerto.nombre_puerto')
    
    class Meta:
        model = gemar_afectaciones_maniobras_portuarias_enc
        fields = '__all__'
        filterset_class = gemar_afectaciones_maniobras_portuarias_enc_filter
#**********************************************************************************************************************
class gemar_carga_seca_enc_filter(filters.FilterSet):
    unidad_basica_puerto = filters.CharFilter(method='filtrado_por_u_b_puerto', lookup_expr='icontains')

    def filtrado_por_u_b_puerto(self, queryset, value):        
        return queryset.filter(unidad_basica__nombre__icontains=value) | queryset.filter(puerto_ubicado__nombre_puerto__icontains=value)
    
    class Meta:  
        model = gemar_carga_seca_enc    
        fields = []

class gemar_carga_seca_enc_serializer(serializers.ModelSerializer):
    unidad_basica_name = serializers.ReadOnlyField(source='unidad_basica.nombre')
    puerto_ubicado_name = serializers.ReadOnlyField(source='puerto_ubicado.nombre_puerto')
    ubicacion_name = serializers.ReadOnlyField(source='get_ubicacion_display')
    estado_operativo_name = serializers.ReadOnlyField(source='get_estado_operativo_display')
    certificado_vencido_name = serializers.ReadOnlyField(source='get_certificado_vencido_display')
    
    class Meta:
        model = gemar_carga_seca_enc
        fields = '__all__'
        filterset_class = gemar_carga_seca_enc_filter
#**********************************************************************************************************************
class gemar_remolcadores_maniobras_enc_filter(filters.FilterSet):
    unidad_basica_puerto = filters.CharFilter(method='filtrado_por_u_b_puerto', lookup_expr='icontains')

    def filtrado_por_u_b_puerto(self, queryset, value):        
        return queryset.filter(unidad_basica__nombre__icontains=value) | queryset.filter(puerto_ubicado__nombre_puerto__icontains=value)
    
    class Meta:  
        model = gemar_remolcadores_maniobras_enc    
        fields = []

class gemar_remolcadores_maniobras_enc_serializer(serializers.ModelSerializer):
    unidad_basica_name = serializers.ReadOnlyField(source='unidad_basica.nombre')
    puerto_ubicado_name = serializers.ReadOnlyField(source='puerto_ubicado.nombre_puerto')
    ubicacion_name = serializers.ReadOnlyField(source='get_ubicacion_display')
    estado_operativo_name = serializers.ReadOnlyField(source='get_estado_operativo_display')
    certificado_vencido_name = serializers.ReadOnlyField(source='get_certificado_vencido_display')
    
    class Meta:
        model = gemar_remolcadores_maniobras_enc
        fields = '__all__'
        filterset_class = gemar_remolcadores_maniobras_enc_filter
#**********************************************************************************************************************
class gemar_remolcador_carga_liquida_enc_filter(filters.FilterSet):
    unidad_basica_puerto = filters.CharFilter(method='filtrado_por_u_b_puerto', lookup_expr='icontains')

    def filtrado_por_u_b_puerto(self, queryset, value):        
        return queryset.filter(unidad_basica__nombre__icontains=value) | queryset.filter(puerto_ubicado__nombre_puerto__icontains=value)
    
    class Meta:  
        model = gemar_remolcador_carga_liquida_enc    
        fields = []

class gemar_remolcador_carga_liquida_enc_serializer(serializers.ModelSerializer):
    unidad_basica_name = serializers.ReadOnlyField(source='unidad_basica.nombre')
    puerto_ubicado_name = serializers.ReadOnlyField(source='puerto_ubicado.nombre_puerto')
    ubicacion_name = serializers.ReadOnlyField(source='get_ubicacion_display')
    estado_operativo_name = serializers.ReadOnlyField(source='get_estado_operativo_display')
    certificado_vencido_name = serializers.ReadOnlyField(source='get_certificado_vencido_display')
    tipo_carga_name = serializers.ReadOnlyField(source='get_tipo_carga_display')
    
    class Meta:
        model = gemar_remolcador_carga_liquida_enc
        fields = '__all__'
        filterset_class = gemar_remolcador_carga_liquida_enc_filter
#**********************************************************************************************************************
class gemar_remolcador_cabotaje_auxiliar_enc_filter(filters.FilterSet):
    unidad_basica_puerto = filters.CharFilter(method='filtrado_por_u_b_puerto', lookup_expr='icontains')

    def filtrado_por_u_b_puerto(self, queryset, value):        
        return queryset.filter(unidad_basica__nombre__icontains=value) | queryset.filter(puerto_ubicado__nombre_puerto__icontains=value)
    
    class Meta:  
        model = gemar_remolcador_cabotaje_auxiliar_enc    
        fields = []

class gemar_remolcador_cabotaje_auxiliar_enc_serializer(serializers.ModelSerializer):
    unidad_basica_name = serializers.ReadOnlyField(source='unidad_basica.nombre')
    puerto_ubicado_name = serializers.ReadOnlyField(source='puerto_ubicado.nombre_puerto')
    ubicacion_name = serializers.ReadOnlyField(source='get_ubicacion_display')
    estado_operativo_name = serializers.ReadOnlyField(source='get_estado_operativo_display')
    certificado_vencido_name = serializers.ReadOnlyField(source='get_certificado_vencido_display')
    tipo_remolcador_name = serializers.ReadOnlyField(source='get_tipo_remolcador_display')
    
    class Meta:
        model = gemar_remolcador_cabotaje_auxiliar_enc
        fields = '__all__'
        filterset_class = gemar_remolcador_cabotaje_auxiliar_enc_filter
#**********************************************************************************************************************

class RegistroPBIPSerializer(serializers.ModelSerializer):
    buque = nom_embarcacion_serializer(read_only=True)
    buque_id = serializers.PrimaryKeyRelatedField(
        queryset=Buque.objects.all(),
        write_only=True,
        source='buque'
    )
    puerto = nom_puerto_serializer(read_only=True)
    puerto_id = serializers.PrimaryKeyRelatedField(
        queryset=Puerto.objects.all(),
        write_only=True,
        source='puerto'
    )
    
    class Meta:
        model = RegistroPBIP
        fields = '__all__'

class PartePBIPSerializer(serializers.ModelSerializer):
    registros = RegistroPBIPSerializer(many=True, read_only=True)
    buque = nom_embarcacion_serializer(read_only=True)
    buque_id = serializers.PrimaryKeyRelatedField(
        queryset=Buque.objects.all(),
        write_only=True,
        source='buque'
    )
    puerto = nom_puerto_serializer(read_only=True)
    puerto_id = serializers.PrimaryKeyRelatedField(
        queryset=Puerto.objects.all(),
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
class RegistroCargaViejaSerializer(serializers.ModelSerializer):
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
    fecha_operacion = serializers.DateField(source='parte.fecha_operacion', read_only=True)
    estado = serializers.CharField(source='parte.estado', read_only=True)

    class Meta:
        model = RegistroCargaVieja
        fields = '__all__'
        read_only_fields = ('id',)

class ParteCargaViejaSerializer(serializers.ModelSerializer):
    registros = RegistroCargaViejaSerializer(many=True, read_only=True)
    creado_por = CustomUserSerializer(read_only=True)

    class Meta:
        model = ParteCargaVieja
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'creado_por', 'aprobado_por')

class RegistroExistenciaMercanciaSerializer(serializers.ModelSerializer):
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
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    tipo_producto_display = serializers.CharField(source='get_tipo_producto_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    contiene_display = serializers.CharField(source='get_contiene_display', read_only=True)
    
    # Añadir campos de búsqueda para los nombres
    producto_nombre = serializers.CharField(source='producto.nombre_producto', read_only=True)
    terminal_nombre = serializers.CharField(source='terminal.nombre_terminal', read_only=True)

    class Meta:
        model = RegistroExistenciaMercancia
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
        extra_fields = ['producto_nombre', 'terminal_nombre']

class ParteExistenciaMercanciaSerializer(serializers.ModelSerializer):
    registros = RegistroExistenciaMercanciaSerializer(many=True, read_only=True)
    creado_por = CustomUserSerializer(read_only=True)

    class Meta:
        model = ParteExistenciaMercancia
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'creado_por', 'aprobado_por')
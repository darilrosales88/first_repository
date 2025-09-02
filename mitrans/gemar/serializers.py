 #1. en este archivo se implementaran todos los serializadores que se usaran en la app, primero
# se importa desde restframeuork los serializadores(serializers), luego se importan los modelos,
from django.utils import timezone
#para trabajar con el filtrado de los serialziadores debemos hacer la siguiente importacion
from django_filters import rest_framework as filters
from rest_framework import serializers
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
from nomencladores.models import nom_terminal
from nomencladores.models import nom_producto
from nomencladores.models import nom_osde_oace_organismo
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

class PartePBIPSerializer(serializers.ModelSerializer):
    buque = nom_embarcacion_serializer(read_only=True)
    buque_id = serializers.PrimaryKeyRelatedField(
        queryset=Buque.objects.all(),
        write_only=True,
        source='buque',
        required=True,
        error_messages={
            'does_not_exist': 'El buque especificado no existe',
            'incorrect_type': 'El ID del buque debe ser un número'
        }
    )
    puerto = nom_puerto_serializer(read_only=True)
    puerto_id = serializers.PrimaryKeyRelatedField(
        queryset=nom_puerto.objects.all(),
        write_only=True,
        source='puerto',
        required=True,
        error_messages={
            'does_not_exist': 'El puerto especificado no existe',
            'incorrect_type': 'El ID del puerto debe ser un número'
        }
    )
    creado_por = CustomUserSerializer(read_only=True)
    aprobado_por = CustomUserSerializer(read_only=True, required=False)

    estado = serializers.ChoiceField(
        choices=[
            ('Creado', 'Creado'),
            ('Listo', 'Listo'),
            ('Aprobado', 'Aprobado'),
            ('Rechazado', 'Rechazado')
        ],
        required=False
    )
    
    fecha_creacion = serializers.DateTimeField(read_only=True)
    fecha_operacion = serializers.DateField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ✅ Hacer que los campos no sean requeridos para actualización (PUT/PATCH)
        if self.context.get('request') and self.context['request'].method in ['PUT', 'PATCH']:
            for field_name in self.fields:
                if field_name not in ['estado']:  # Mantener estado como requerido si es necesario
                    self.fields[field_name].required = False

    class Meta:
        model = PartePBIP
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'creado_por', 'aprobado_por')
        extra_kwargs = {
            'nivel': {
                'error_messages': {
                    'invalid': 'El nivel debe ser un número entero',
                    'max_value': 'El nivel no puede ser mayor a 5',
                    'min_value': 'El nivel no puede ser menor a 1'
                }
            },
            'fecha_operacion': {
                'error_messages': {
                    'invalid': 'Formato de fecha inválido (YYYY-MM-DD)'
                }
            },
            'estado': {
                'error_messages': {
                    'invalid_choice': 'Estado inválido. Opciones válidas: CREADO, APROBADO, RECHAZADO, CANCELADO, LISTO'
                }
            }
        }

    def create(self, validated_data):
        try:
            if 'request' not in self.context:
                raise serializers.ValidationError("No se pudo determinar el usuario creador")
                
            validated_data['creado_por'] = self.context['request'].user
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def validate(self, data):
        # ✅ Solo validar campos requeridos para creación (POST), no para actualización (PUT/PATCH)
        if self.context.get('request') and self.context['request'].method == 'POST':
            required_fields = ['buque', 'puerto', 'nivel', 'fecha_operacion']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(
                        {field: "Este campo es requerido"}
                    )

            # Validar que la fecha de operación no sea futura
            if data['fecha_operacion'] > timezone.now().date():
                raise serializers.ValidationError(
                    {'fecha_operacion': "La fecha de operación no puede ser futura"}
                )

            # Validar combinación única de buque, puerto y nivel
            if PartePBIP.objects.filter(
                buque=data['buque'],
                puerto=data['puerto'],
                nivel=data['nivel'],
                fecha_operacion=data['fecha_operacion']
            ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError(
                    "Ya existe un registro con la misma combinación de Buque, Puerto y Nivel para esta fecha"
                )

        return data

    def validate_estado(self, value):
        estados_validos = ['Creado', 'Aprobado', 'Rechazado', 'Cancelado', 'Listo']
        if value not in estados_validos:
            raise serializers.ValidationError(
                f"Estado inválido. Opciones válidas: {', '.join(estados_validos)}"
            )
        return value
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
        source='terminal',
        required=True,
        error_messages={
            'does_not_exist': 'La terminal especificada no existe',
            'incorrect_type': 'El ID de la terminal debe ser un número'
        }
    )
    producto = nom_producto_serializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.filter(),
        write_only=True,
        source='producto',
        required=True,
        error_messages={
            'does_not_exist': 'El producto especificado no existe',
            'incorrect_type': 'El ID del producto debe ser anúmero'
        }
    )
    tipo_embalaje = nom_tipo_embalaje_serializer(read_only=True, required=False)
    tipo_embalaje_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoEmbalaje.objects.filter(),
        write_only=True,
        source='tipo_embalaje',
        required=False,
        allow_null=True,
        error_messages={
            'does_not_exist': 'El tipo de embalaje especificado no existe',
            'incorrect_type': 'El ID del tipo de embalaje debe ser un número'
        }
    )
    unidad_medida = nom_unidad_medida_serializer(read_only=True)
    unidad_medida_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadMedida.objects.filter(),
        write_only=True,
        source='unidad_medida',
        required=True,
        error_messages={
            'does_not_exist': 'La unidad de medida especificada no existe',
            'incorrect_type': 'El ID de la unidad de medida debe ser un número'
        }
    )
    creado_por = CustomUserSerializer(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    tipo_producto_display = serializers.CharField(source='get_tipo_producto_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    contiene_display = serializers.CharField(source='get_contiene_display', read_only=True)
    estado_registro_display = serializers.CharField(source='get_estado_registro_display', read_only=True)
    
    # ✅ CORREGIR: Las opciones deben estar en mayúsculas para coincidir con el error message
    estado_registro = serializers.ChoiceField(
        choices=[
            ('CREADO', 'Creado'),
            ('APROBADO', 'Aprobado'),
            ('RECHAZADO', 'Rechazado'),
            ('LISTO', 'Listo')
        ],
        required=False
    )
    
    # ✅ AGREGAR: Campo estado con required=False para PATCH
    estado = serializers.CharField(
        required=False,
        write_only=True,
        allow_null=True,
        allow_blank=True,
        error_messages={
            'invalid_choice': 'Estado inválido. Consulte las opciones válidas'
        }
    )
    
    fecha_creacion = serializers.DateTimeField(read_only=True)
    fecha_operacion = serializers.DateField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ✅ FORZAR que el campo estado no sea requerido para PATCH
        if self.context.get('request') and self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['estado'].required = False

    def validate(self, data):
        # ✅ Transformar 'estado_registro' a 'estado' para el backend
        if 'estado_registro' in data:
            data['estado'] = data.pop('estado_registro')
        
        # ✅ Saltar validaciones de campos requeridos para PATCH
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            return data
            
        # ✅ Solo validar campos requeridos para creación (POST), no para actualización (PUT/PATCH)
        if self.context.get('request') and self.context['request'].method == 'POST':
            # Validar campos requeridos
            required_fields = ['terminal', 'producto', 'unidad_medida', 'fecha_operacion', 'tipo', 'tipo_producto']
            for field in required_fields:
                if field not in data:
                    raise serializers.ValidationError(
                        {field: "Este campo es requerido"}
                    )

            # Validar que la fecha de operación no sea futura
            if data['fecha_operacion'] > timezone.now().date():
                raise serializers.ValidationError(
                    {'fecha_operacion': "La fecha de operación no puede ser futura"}
                )

            # Validar combinación única
            if ExistenciaMercancia.objects.filter(
                fecha_operacion=data['fecha_operacion'],
                terminal=data['terminal'],
                tipo=data['tipo'],
                producto=data['producto'],
                tipo_embalaje=data.get('tipo_embalaje'),
                unidad_medida=data['unidad_medida']
            ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError(
                    "Ya existe un registro con esta combinación de Terminal, Tipo, Producto, Tipo de Embalaje y Unidad de Medida para esta fecha."
                )
            
            # Validaciones específicas para contenedors
            tipo_producto = data['tipo_producto']
            estado = data.get('estado')
            contiene = data.get('contiene')
            
            if tipo_producto == 2:  # Contenedor
                if not estado:
                    raise serializers.ValidationError(
                        {'estado': "Para contenedores debe especificar el estado."}
                    )
                if estado == 2 and not contiene:  # Lleno
                    raise serializers.ValidationError(
                        {'contiene': "Para contenedores llenos debe especificar qué contienen."}
                    )
            else:
                data['estado'] = None
                data['contiene'] = None
                
        return data
    
    def to_representation(self, instance):
        # ✅ Transformar 'estado' de vuelta a 'estado_registro' para la respuesta
        representation = super().to_representation(instance)
        if 'estado' in representation:
            representation['estado_registro'] = representation.pop('estado')
        return representation

    def validate_estado_registro(self, value):
        """
        Validación personalizada para el campo estado_registro
        """
        
        # ✅ CORREGIR: Debe coincidir con las opciones del ChoiceField
        estados_validos = ['CREADO', 'APROBADO', 'RECHAZADO', 'LISTO']
        if value not in estados_validos:
            raise serializers.ValidationError(
                f"Estado de registro inválido. Opciones válidas: {', '.join(estados_validos)}"
            )
        return value

    def validate_tipo_producto(self, value):
        """
        Validación personalizada para el campo tipo_producto
        """
        if value not in [1, 2]:  # 1: Normal, 2: Contenedor
            raise serializers.ValidationError(
                "Tipo de producto inválido. Opciones válidas: 1 (Normal), 2 (Contenedor)"
            )
        return value

    def create(self, validated_data):
        try:
            # Asegurar que el request está en el contexto
            if 'request' not in self.context:
                raise serializers.ValidationError("No se pudo determinar el usuario creador")
                
            validated_data['creado_por'] = self.context['request'].user
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))

    # ✅ AGREGAR: Método update para manejar correctamente los PATCH
    def update(self, instance, validated_data):
        """
        Sobrescribir el método update para manejar campos opcionales en PATCH
        """
        # Actualizar solo los campos que vienen en validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    class Meta:
        model = ExistenciaMercancia
        fields = [
            'id', 'terminal', 'terminal_id', 'producto', 'producto_id', 
            'tipo_embalaje', 'tipo_embalaje_id', 'unidad_medida', 'unidad_medida_id',
            'creado_por', 'tipo_display', 'tipo_producto_display', 'estado_display',
            'contiene_display', 'estado_registro_display', 'estado_registro', 'estado',
            'fecha_creacion', 'fecha_operacion', 'tipo', 'tipo_producto', 'existencia',
            'contiene', 'aprobado_por'
        ]
        read_only_fields = ('fecha_creacion', 'creado_por')
        extra_kwargs = {
            'fecha_operacion': {
                'error_messages': {
                    'invalid': 'Formato de fecha inválido (YYYY-MM-DD)'
                }
            },
            'tipo': {
                'error_messages': {
                    'invalid_choice': 'Tipo inválido. Consulte las opciones válidas'
                }
            },
            'tipo_producto': {
                'error_messages': {
                    'invalid_choice': 'Tipo de producto inválido. Opciones válidas: 1 (Normal), 2 (Contenedor)'
                }
            },
            'estado': {
                'error_messages': {
                    'invalid_choice': 'Estado inválido. Consulte las opciones válidas'
                }
            },
            'contiene': {
                'error_messages': {
                    'invalid_choice': 'Contenido inválido. Consulte las opciones válidas'
                }
            },
            'estado_registro': {
                'error_messages': {
                    # ✅ CORREGIR: Debe coincidir con las opciones de arriba
                    'invalid_choice': 'Estado de registro inválido. Opciones válidas: CREADO, APROBADO, RECHAZADO, CANCELADO, LISTO'
                }
            }
        }
class ParteCombinadoSerializer(serializers.ModelSerializer):
    tipo_parte_display = serializers.CharField(source='get_tipo_parte_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    creado_por_name = serializers.CharField(source='creado_por.get_full_name', read_only=True)
    aprobado_por_name = serializers.CharField(source='aprobado_por.get_full_name', read_only=True, allow_null=True)
    
    # Usar SerializerMethodField para manejar valores nulos
    entidad_name = serializers.SerializerMethodField()
    organismo_name = serializers.SerializerMethodField()
    provincia_name = serializers.SerializerMethodField()
    entidad_abreviatura = serializers.SerializerMethodField()
    organismo_abreviatura = serializers.SerializerMethodField()

    class Meta:
        model = ParteCombinado
        fields = [
            'id', 'tipo_parte', 'tipo_parte_display', 'fecha_actual', 
            'estado_parte', 'estado_parte_display', 'creado_por', 'creado_por_name',
            'aprobado_por', 'aprobado_por_name', 'entidad', 'entidad_name', 'entidad_abreviatura',
            'organismo', 'organismo_name', 'organismo_abreviatura', 'provincia', 'provincia_name',
            'entidad_nombre', 'organismo_nombre', 'provincia_nombre',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

    def get_entidad_name(self, obj):
        return obj.entidad.nombre if obj.entidad else None

    def get_organismo_name(self, obj):
        return obj.organismo.nombre if obj.organismo else None

    def get_provincia_name(self, obj):
        return obj.provincia.nombre_provincia if obj.provincia else None

    def get_entidad_abreviatura(self, obj):
        return obj.entidad.abreviatura if obj.entidad else None

    def get_organismo_abreviatura(self, obj):
        return obj.organismo.abreviatura if obj.organismo else None

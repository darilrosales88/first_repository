import django_filters
from rest_framework import serializers
from django_filters import rest_framework as filters

from django.db.models import Q,Sum

#Importando modelos de UFC
from .models import (ufc_informe_operativo, vagon_cargado_descargado,producto_UFC, en_trenes,nom_equipo_ferroviario
                    ,por_situar,Situado_Carga_Descarga,arrastres,HistorialVagonesProductos 
                    ,registro_vagones_cargados,vagones_productos,rotacion_vagones,HistorialVagonCargadoDescargado
                     )

from Administracion.models import Auditoria 
from rest_framework.response import Response
from rest_framework import status

#transaction.atomic crea una transacción atómica que asegura que:
#O todas las operaciones se ejecutan correctamente O ninguna se ejecuta (si ocurre algún error)
from django.db import transaction 
import json
from django.utils import timezone
from .models import HistorialVagonCargadoDescargado, vagon_cargado_descargado, registro_vagones_cargados,vagones_dias
from nomencladores.models import nom_equipo_ferroviario,nom_tipo_equipo_ferroviario,nom_provincia
from Administracion.models import CustomUser

#######Importamos serializadores externos para poder tener una lectura mas detallada
from nomencladores.serializers import nom_equipo_ferroviario_serializer
from Administracion.serializers import UserPermissionSerializer


#para cada modelo del que deseemos realizar el filtrado debemos hacer un filtrado
#nom_pais_filter es una clase que se implementa para definir sobre qué campos quiero filtrar los registros de mi API, 
#hereda de filters.FilterSet



#****************-------------------------********************--------------------***************-----------------********************************
#Funcion para actualizar el estado de los vagones deberia estar global
def actualizar_estado_equipo_ferroviario( equipo_o_id, nuevo_estado, id=None):
        """
        Método auxiliar para actualizar el estado de un equipo ferroviario
        """
        try:
            from nomencladores.models import nom_equipo_ferroviario
            if (id) is not None:
                equipo = nom_equipo_ferroviario.objects.get(id=id)
                equipo.estado_actual=nuevo_estado
                equipo.save()
                return True
            if isinstance(equipo_o_id, nom_equipo_ferroviario):
                equipo = equipo_o_id
            else:
                equipo = nom_equipo_ferroviario.objects.filter(numero_identificacion=equipo_o_id).first()
            if equipo:
                equipo.estado_actual = nuevo_estado
                equipo.save()
        except Exception as e:
            # No romper el flujo principal si hay error al actualizar el estado
            print(f"Error al actualizar estado del equipo: {str(e)}")    
        
#****************-------------------------********************--------------------***************-----------------****
class DateTimeToDateField(serializers.ReadOnlyField):
    """Campo personalizado para convertir datetime a date"""
    def to_representation(self, value):
        if value:
            return value.date() if hasattr(value, 'date') else value
        return None

#****************-------------------------********************--------------------***************-----------------********************************
#******************-Producto UFC en vagones-*********************************#
class producto_vagon_filter(filters.FilterSet):
    tipo_equipo= filters.NumberFilter(field_name='tipo_equipo__id')
    tipo_equipo_nombre = filters.CharFilter(
        field_name='tipo_equipo__tipo_equipo', 
        lookup_expr='icontains'
    )
    class Meta:
        model = producto_UFC
        fields = ['tipo_equipo']                 
                
#serializador de productoUFC
class producto_vagon_serializer(serializers.ModelSerializer):
   # tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
   # estado_name = serializers.ReadOnlyField(source='get_estado_display')
   # tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto_name = serializers.ReadOnlyField(source='producto.nombre_producto')
    producto_codigo = serializers.ReadOnlyField(source='producto.codigo_producto')
    tipo_embalaje_name=serializers.ReadOnlyField(source='tipo_embalaje.nombre_tipo_embalaje')
    unidad_medida_name=serializers.ReadOnlyField(source='unidad_medida.unidad_medida')
    estado_name=serializers.ReadOnlyField(source='get_estado_display')
    tipo_equipo_nombre = serializers.CharField(source='tipo_equipo.tipo_equipo', read_only=True)
    class Meta:
        model = producto_UFC
        fields = '__all__'
        filterset_class=producto_vagon_filter
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
#Serializador para Modelo dVagones por dias de situados, por situar, Arrastres
class vagones_dias_serializer(serializers.ModelSerializer):
    # Mantenemos los campos existentes para lectura
    equipo_ferroviario_detalle = nom_equipo_ferroviario_serializer(
        source="equipo_ferroviario", 
        read_only=True
    )
    
    # Cambiamos el campo equipo_ferroviario para manejar la estructura deseada
    equipo_ferroviario = serializers.PrimaryKeyRelatedField(
        queryset=nom_equipo_ferroviario.objects.all(), 
        write_only=True,
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = vagones_dias
        fields = '__all__'
    
    


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
        fields = ['origen_tipo_prod_tef','informe']



class vagones_productos_serializer(serializers.ModelSerializer):
    fecha_registro = serializers.DateTimeField(
        source='fecha', 
        format='%Y-%m-%d %H:%M', 
        read_only=True,  # Solo lectura, no necesita write_only
        help_text="Fecha y hora en que se creó el registro (automático)"
    )
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
                
                registros_data = validated_data.pop('registros_vagones_data', [])
                
                # Crear instancia principal
                instance = super().create(validated_data)
                
                # Asignar productos
                
                
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
    
class HistorialVagonesProductosSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    informe_operativo_fecha = DateTimeToDateField(source='informe_operativo.fecha_operacion')
    
    # Campos JSON con parseo seguro
    datos_vagon_producto = serializers.SerializerMethodField()
    datos_productos = serializers.SerializerMethodField()
    
    class Meta:
        model = HistorialVagonesProductos
        fields = '__all__'
    
    def get_datos_vagon_producto(self, obj):
        try:
            data = obj.datos_vagon_producto
            if isinstance(data, str):
                data = json.loads(data)
            
            if isinstance(data, dict):
                # Convertir campos de fecha si existen
                if 'fecha' in data and isinstance(data['fecha'], str):
                    try:
                        data['fecha'] = timezone.datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S.%f').date()
                    except ValueError:
                        pass
                
                # Asegurar que los campos numéricos sean correctos
                numeric_fields = [
                    'plan_mensual', 'plan_dia', 'vagones_situados', 'vagones_cargados',
                    'plan_acumulado_actual', 'real_acumulado_actual', 'plan_acumulado_anual',
                    'real_acumulado_anual', 'plan_aseguramiento_proximos_dias', 'plan_anual',
                    'plan_acumulado_dia_anterior', 'real_acumulado_dia_anterior'
                ]
                
                for field in numeric_fields:
                    if field in data and not isinstance(data[field], (int, float)):
                        try:
                            data[field] = int(data[field])
                        except (ValueError, TypeError):
                            data[field] = 0
                
                # Manejar el campo tipo_equipo_ferroviario correctamente
                if 'tipo_equipo_ferroviario' in data:
                    if isinstance(data['tipo_equipo_ferroviario'], str):
                        # Si es un string, podría ser el nombre del equipo
                        try:
                            equipo = nom_tipo_equipo_ferroviario.objects.get(tipo_equipo=data['tipo_equipo_ferroviario'])
                            data['tipo_equipo_ferroviario_id'] = equipo.id
                            data['tipo_equipo_ferroviario_name'] = equipo.get_tipo_equipo_display()
                        except nom_tipo_equipo_ferroviario.DoesNotExist:
                            data['tipo_equipo_ferroviario_id'] = None
                            data['tipo_equipo_ferroviario_name'] = data['tipo_equipo_ferroviario']
                    elif isinstance(data['tipo_equipo_ferroviario'], dict):
                        # Si es un diccionario, extraer id y nombre
                        data['tipo_equipo_ferroviario_id'] = data['tipo_equipo_ferroviario'].get('id')
                        data['tipo_equipo_ferroviario_name'] = data['tipo_equipo_ferroviario'].get('name', '')
                
                # Agregar nombres descriptivos para los choices
                if 'tipo_origen' in data:
                    data['tipo_origen_name'] = dict(vagones_productos.TIPO_ORIGEN_CHOICES).get(
                        data['tipo_origen'], data.get('tipo_origen', ''))
                
                if 'tipo_producto' in data:
                    data['tipo_producto_name'] = dict(vagones_productos.TIPO_PRODUCTO_CHOICES).get(
                        data['tipo_producto'], data.get('tipo_producto', ''))
                
                if 'tipo_combustible' in data:
                    data['tipo_combustible_name'] = dict(vagones_productos.TIPO_COMBUSTIBLE_CHOICES).get(
                        data['tipo_combustible'], data.get('tipo_combustible', ''))
            
            return data
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Error al parsear datos_vagon_producto: {str(e)}")
            return {
                'error': 'Error al parsear los datos del vagon producto',
                'detalle': str(e)
            }
    
    def get_datos_productos(self, obj):
        try:
            data = obj.datos_productos
            if isinstance(data, str):
                data = json.loads(data)
            
            if isinstance(data, list):
                for producto in data:
                    # Asegurar que la cantidad sea un número
                    if 'cantidad' in producto and not isinstance(producto['cantidad'], (int, float)):
                        try:
                            producto['cantidad'] = int(producto['cantidad'])
                        except (ValueError, TypeError):
                            producto['cantidad'] = 0
                    
                    # Manejar producto como diccionario o ID
                    if 'producto' in producto:
                        if isinstance(producto['producto'], dict):
                            producto['producto_id'] = producto['producto'].get('id')
                            producto['producto_name'] = producto['producto'].get('nombre_producto', '')
                        elif isinstance(producto['producto'], int):
                            producto['producto_id'] = producto['producto']
                            producto['producto_name'] = 'Producto ID: ' + str(producto['producto'])
                    
                    # Manejar tipo_embalaje
                    if 'tipo_embalaje' in producto:
                        if isinstance(producto['tipo_embalaje'], dict):
                            producto['tipo_embalaje_id'] = producto['tipo_embalaje'].get('id')
                            producto['tipo_embalaje_name'] = producto['tipo_embalaje'].get('nombre_tipo_embalaje', '')
                        elif isinstance(producto['tipo_embalaje'], int):
                            producto['tipo_embalaje_id'] = producto['tipo_embalaje']
                            producto['tipo_embalaje_name'] = 'Embalaje ID: ' + str(producto['tipo_embalaje'])
                    
                    # Manejar unidad_medida
                    if 'unidad_medida' in producto:
                        if isinstance(producto['unidad_medida'], dict):
                            producto['unidad_medida_id'] = producto['unidad_medida'].get('id')
                            producto['unidad_medida_name'] = producto['unidad_medida'].get('unidad_medida', '')
                            producto['unidad_medida_simbolo'] = producto['unidad_medida'].get('simbolo', '')
                        elif isinstance(producto['unidad_medida'], int):
                            producto['unidad_medida_id'] = producto['unidad_medida']
                            producto['unidad_medida_name'] = 'Unidad ID: ' + str(producto['unidad_medida'])
            
            return data
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Error al parsear datos_productos: {str(e)}")
            return [{
                'error': 'Error al parsear los datos de productos',
                'detalle': str(e)
            }]
#**************************************************************************************************************************************
#serializador para el estado de vagones cargados/descargados
class vagon_cargado_descargado_filter(filters.FilterSet):
    tef_prod_estado = filters.CharFilter(method='filtrado_por_tef_prod_estado', lookup_expr='icontains')
    informe = filters.NumberFilter(field_name='informe_operativo__id')
    def filtrado_por_tef_prod_estado(self, queryset, name, value):        
        return queryset.filter(
            Q(tipo_equipo_ferroviario_name__icontains=value) | 
            Q(productos_list__icontains=value) | 
            Q(estado_name__icontains=value)
        )
    
    class Meta:
        model = vagon_cargado_descargado
        fields = ['tef_prod_estado','informe']



class vagon_cargado_descargado_serializer(serializers.ModelSerializer):
    fecha_registro = serializers.DateTimeField(
        source='fecha', 
        format='%Y-%m-%d %H:%M', 
        read_only=True,
        help_text="Fecha y hora en que se creó el registro (automático)"
    )
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
    tipo_equipo_ferroviario_name = serializers.ReadOnlyField(source='tipo_equipo_ferroviario.get_tipo_equipo_display')
    estado_name = serializers.ReadOnlyField(source='get_estado_display')
    operacion_name = serializers.ReadOnlyField(source='get_operacion_display')
    tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    producto_detalle=producto_vagon_serializer(many=False,source='producto', read_only=True)
    
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

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                # Extraer datos para relaciones
               
                registros_data = validated_data.pop('registros_vagones_data', [])
                
                # Actualizar campos directos
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                
                # Actualizar productos si se proporcionaron
              
                # Manejar registros de vagones
                if registros_data:
                    # Eliminar registros antiguos no incluidos
                    ids_nuevos = [r.get('id') for r in registros_data if r.get('id')]
                    
                    # Primero, liberar equipos ferroviarios de registros que se eliminarán
                    registros_a_eliminar = instance.registros_vagones.exclude(id__in=ids_nuevos)
                    for registro in registros_a_eliminar:
                        actualizar_estado_equipo_ferroviario(registro.no_id, 'Disponible')
                    registros_a_eliminar.delete()
                    
                    # Actualizar o crear registros
                    for registro_data in registros_data:
                        registro_id = registro_data.get('id')
                        if registro_id:
                            # Actualizar registro existente
                            registro = registro_vagones_cargados.objects.get(id=registro_id)
                            for attr, value in registro_data.items():
                                setattr(registro, attr, value)
                            registro.save()
                        else:
                            # Crear nuevo registro
                            registro = registro_vagones_cargados.objects.create(**registro_data)
                            instance.registros_vagones.add(registro)
                        
                        # Actualizar estado del equipo ferroviario
                        actualizar_estado_equipo_ferroviario(registro.no_id, 'Asignado al estado Cargado/Descargado')
                
                return instance
                
        except Exception as e:
            raise serializers.ValidationError(f"Error al actualizar el registro: {str(e)}")
        
    
    def validate(self, data):
        # Validación para causas_incumplimiento
        data['causas_incumplimiento'] = data.get('causas_incumplimiento', '')
        
        # Validación para real_carga_descarga
        if 'real_carga_descarga' not in data or data['real_carga_descarga'] is None:
            # Calcular valor basado en registros_vagones_data si está disponible
            registros_data = data.get('registros_vagones_data', [])
            data['real_carga_descarga'] = len(registros_data)
            
        return data

    def create(self, validated_data):
        try:
            with transaction.atomic():
                # Extraer datos para relaciones
        
                registros_data = validated_data.pop('registros_vagones_data', [])

                # Asegurar que real_carga_descarga no sea sobrescrito
                if validated_data.get('real_carga_descarga', 0) == 0:
                    registros_data = validated_data.get('registros_vagones_data', [])
                    validated_data['real_carga_descarga'] = len(registros_data)
                
                # Crear instancia principal
                instance = super().create(validated_data)
                
                # Asignar productos
                
                
                # Crear y asociar registros de vagones
                for registro_data in registros_data:
                    registro = registro_vagones_cargados.objects.create(**registro_data)
                    instance.registros_vagones.add(registro)
                    
                    # Actualizar estado del equipo ferroviario
                    actualizar_estado_equipo_ferroviario(registro.no_id, 'Asignado al estado Cargado/Descargado')
                
                return instance
                
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el registro: {str(e)}")
    
    
    def get_productos_list(self, obj):
        return ", ".join([
            p.producto.nombre_producto 
            for p in obj.producto.all() 
            if hasattr(p, 'producto')
        ])  

#serializador para el historial de vagon_cargado_descargado**************************************************


class HistorialVagonCargadoDescargadoSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    informe_operativo_fecha = DateTimeToDateField(source='informe_operativo.fecha_operacion')
    
    # Campos JSON con parseo seguro
    datos_vagon = serializers.SerializerMethodField()
    datos_productos = serializers.SerializerMethodField()
    datos_registros_vagones = serializers.SerializerMethodField()
    
    class Meta:
        model = HistorialVagonCargadoDescargado
        fields = '__all__'

    def get_datos_vagon(self, obj):
        """
        Método para procesar y enriquecer los datos del vagón almacenados en formato JSON.
        Recibe el objeto serializado (obj) y devuelve un diccionario con los datos procesados.
        """
        try:
            # 1. Obtener los datos del vagón desde el objeto
            data = obj.datos_vagon
            
            # 2. Verificar si los datos están en formato string (JSON serializado)
            if isinstance(data, str):
                # 3. Si es string, convertirlo a diccionario Python
                data = json.loads(data)
            
            # 4. Verificar si los datos son un diccionario
            if isinstance(data, dict):
                # 5. Procesamiento de fecha (si existe en los datos)
                if 'fecha' in data and isinstance(data['fecha'], str):
                    try:
                        # 6. Convertir string de fecha a objeto date
                        data['fecha'] = timezone.datetime.strptime(
                            data['fecha'], 
                            '%Y-%m-%d %H:%M:%S.%f'
                        ).date()
                    except ValueError:
                        # 7. Si falla la conversión, continuar sin modificar la fecha
                        pass
                
                # 8. Establecer valores por defecto para campos numéricos si no existen
                data.setdefault('plan_diario_carga_descarga', 0)
                data.setdefault('real_carga_descarga', 0)
                data.setdefault('causas_incumplimiento', '')
                
                # 9. Agregar nombres descriptivos para campos con choices
                
                # 9.1. Nombre descriptivo para tipo_origen
                data['tipo_origen_name'] = dict(
                    vagon_cargado_descargado.TIPO_ORIGEN_DESTINO_CHOICES
                ).get(data.get('tipo_origen'), '')
                
                # 9.2. Nombre descriptivo para estado
                data['estado_name'] = dict(
                    vagon_cargado_descargado.ESTADO_CHOICES
                ).get(data.get('estado'), '')
                
                # 9.3. Nombre descriptivo para operación
                data['operacion_name'] = dict(
                    vagon_cargado_descargado.OPERACION_CHOICES
                ).get(data.get('operacion'), '')
                
                # 9.4. Nombre descriptivo para tipo_destino
                data['tipo_destino_name'] = dict(
                    vagon_cargado_descargado.TIPO_DESTINO_CHOICES
                ).get(data.get('tipo_destino'), '')
                
                # 10. Procesamiento especial para el tipo de equipo ferroviario
                if 'tipo_equipo_ferroviario_id' in data:
                    try:
                        # 10.1. Obtener el equipo ferroviario completo desde la base de datos
                        equipo = nom_equipo_ferroviario.objects.get(
                            pk=data['tipo_equipo_ferroviario_id']
                        )
                        
                        # 10.2. Obtener el nombre legible del tipo de equipo
                        # usando get_tipo_equipo_display() que es generado automáticamente
                        # por Django para campos con choices
                        data['tipo_equipo_ferroviario_name'] = equipo.tipo_equipo.get_tipo_equipo_display()
                        
                    except nom_equipo_ferroviario.DoesNotExist:
                        # 10.3. Si no existe el equipo, establecer nombre vacío
                        data['tipo_equipo_ferroviario_name'] = ''
            
            # 11. Devolver los datos procesados
            return data
        
        except (json.JSONDecodeError, TypeError, KeyError):
            # 12. Manejo de errores: si hay problemas al procesar los datos,
            # devolver un diccionario con valores por defecto
            return {
                'plan_diario_carga_descarga': 0,
                'real_carga_descarga': 0,
                'causas_incumplimiento': ''
            }
    

    def get_datos_productos(self, obj):
        try:
            data = obj.datos_productos
            if isinstance(data, str):
                data = json.loads(data)
            
            if isinstance(data, list):
                for producto in data:
                    if 'unidad_medida' in producto and isinstance(producto['unidad_medida'], dict):
                        producto['unidad_medida_name'] = producto['unidad_medida'].get('nombre', '')
                    if 'tipo_embalaje' in producto and isinstance(producto['tipo_embalaje'], dict):
                        producto['tipo_embalaje_name'] = producto['tipo_embalaje'].get('nombre', '')
                    if 'producto_name' in producto and isinstance(producto['producto_name'], dict):
                        producto['producto_name'] = "isisco"
                        #producto['producto_name'] = producto['producto'].get('nombre_producto', '')
                        
            
            return data
        except (json.JSONDecodeError, TypeError):
            return []
    
    def get_datos_registros_vagones(self, obj):
        try:
            data = obj.datos_registros_vagones
            if isinstance(data, str):
                data = json.loads(data)
            
            if isinstance(data, list):
                for registro in data:
                    if 'tipo_origen' in registro:
                        registro['tipo_origen_name'] = dict(registro_vagones_cargados.TIPO_ORIGEN_CHOICES).get(
                            registro['tipo_origen'], '')
                    
                    # Convertir campos de fecha si existen
                    for field in ['fecha_despacho', 'fecha_llegada']:
                        if field in registro and isinstance(registro[field], str):
                            try:
                                registro[field] = timezone.datetime.strptime(registro[field], '%Y-%m-%d').date()
                            except ValueError:
                                pass
            
            return data
        except (json.JSONDecodeError, TypeError):
            return []


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
    informe = filters.NumberFilter(field_name='informe_operativo__id')
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
        fields = ['search','informe']  # Campos filtrables




class en_trenes_serializer(serializers.ModelSerializer):
    fecha_registro = serializers.DateTimeField(
        source='fecha', 
        format='%Y-%m-%d %H:%M', 
        read_only=True,  # Solo lectura, no necesita write_only
        help_text="Fecha y hora en que se creó el registro (automático)"
    )
   # tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
   # estado_name = serializers.ReadOnlyField(source='get_estado_display')
   # tipo_destino_name = serializers.ReadOnlyField(source='get_tipo_destino_display')
    producto_name = serializers.ReadOnlyField(source='producto.producto.nombre_producto')
    tipo_equipo_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_equipo_display')
   # equipo_vagon_id=serializers.ReadOnlyField(source='equipo_vagon.numero_identificacion')
    # productos_info = serializers.SerializerMethodField()
    vagones_info=serializers.SerializerMethodField()
    
    producto = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    producto_detalle=producto_vagon_serializer(many=False,source='producto', read_only=True)
    

    equipo_vagon = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=nom_equipo_ferroviario.objects.all(),
        required=False
    )
   
    class Meta:
        model = en_trenes
        fields = (
            'id', 
            'tipo_origen', 
            'fecha_registro',
            'origen', 
            'locomotora',
            'numero_identificacion_locomotora',
            'tipo_equipo', 
            'tipo_equipo_name',
            'equipo_vagon',
            'vagones_info',
            'estado', 
            'tipo_destino',  
            'destino', 
            'producto', 
            'producto_name',
            'producto_detalle',
            'cantidad_vagones',
            'observaciones',
            'informe_operativo',
        )
        
    # def get_productos_info(self, obj):
    #     p = obj.producto
    #     return {
    #         'id': p.id,
    #         'nombre_producto': p.producto.nombre_producto,
    #         'codigo_producto': p.producto.codigo_producto,
    #         'tipo_embalaje': p.tipo_embalaje.nombre if hasattr(p.tipo_embalaje, 'nombre') else str(p.tipo_embalaje),
    #         'unidad_medida': p.unidad_medida.nombre if hasattr(p.unidad_medida, 'nombre') else str(p.unidad_medida),
    #         'cantidad': p.cantidad,
    #         'estado': p.estado,
    #         'contiene': p.contiene
    #     }
        
    def get_vagones_info(self, obj):
        equipo_vagon = obj.equipo_vagon.all()
        return [{
            'id': e.id,
            'tipo_equipo': e.tipo_equipo.tipo_equipo,
            'numero_identificacion': e.numero_identificacion,
            'tipo_carga': e.tipo_carga,
            'tipo_combustible': e.tipo_combustible
        } for e in equipo_vagon]

    def create(self, validated_data):
        equipo_vagon_data=validated_data.pop('equipo_vagon',[])
        instance = en_trenes.objects.create(**validated_data)
    
        instance.equipo_vagon.set(equipo_vagon_data)
        
        for equipo in equipo_vagon_data:    
        # Actualizar estado del equipo ferroviario
            print("Este es el id a cambiar", equipo)
            actualizar_estado_equipo_ferroviario(equipo.numero_identificacion, 'Asignado al estado En Trenes')
        
        return instance

    def update(self, instance, validated_data):
        
        equipo_vagon_data=validated_data.pop('equipo_vagon',None)
        instance = super().update(instance, validated_data)
        instance.equipo_vagon.set(equipo_vagon_data)
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
                
                
                
                

    
class SituadoCargaDescargaFilter(filters.FilterSet):
    tipo_equipo = filters.CharFilter(lookup_expr='icontains')  # Filtro exacto (puedes usar 'icontains' para parcial
    informe = filters.NumberFilter(field_name='informe_operativo__id')
    
    class Meta:
        model = Situado_Carga_Descarga
        fields = ['tipo_equipo','informe']  # Campos filtrables
        
        
class SituadoCargaDescargaSerializers(serializers.ModelSerializer):
   # productos_info = serializers.SerializerMethodField()
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
    tipo_equipo_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_equipo_display')
    producto = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    equipo_vagon = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=vagones_dias.objects.all(),
        required=False
    )
    equipo_vagon_detalle=vagones_dias_serializer(many=True,source='equipo_vagon', read_only=True)
    situados = serializers.IntegerField()
    pendiente_proximo_dia = serializers.IntegerField()
    
    class Meta:
        model = Situado_Carga_Descarga
        fields = '__all__'
        extra_kwargs = {
            'producto': {'required': False},
            'observaciones': {'required': False, 'allow_null': True}
        }

    # def get_productos_info(self, obj):
    #     p = obj.producto
    #     return {
    #         'id': p.id,
    #         'nombre_producto': p.producto.nombre_producto,
    #         'codigo_producto': p.producto.codigo_producto,
    #         'tipo_embalaje': p.tipo_embalaje.nombre if hasattr(p.tipo_embalaje, 'nombre') else str(p.tipo_embalaje),
    #         'unidad_medida': p.unidad_medida.nombre if hasattr(p.unidad_medida, 'nombre') else str(p.unidad_medida),
    #         'cantidad': p.cantidad,
    #         'estado': p.estado,
    #         'contiene': p.contiene
    #     }  # (truco) Esta bueno este truquito para evitar errores si el objeto no tiene el atributo
        
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
        productos_data = validated_data.pop('producto', [])
        instance = super().create(validated_data)
        
        # Asociar productos MANUALMENTE después de crear la instancia
        if productos_data:
            instance.producto.set(productos_data)
            instance.save()  # Guardar explícitamente
        
        return instance

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('producto', None)
        instance = super().update(instance, validated_data)
        
        if productos_data is not None:
            instance.producto.set(productos_data)
            instance.save()
        
        for equipo in instance.equipo_vagon.all():
            equipo_id=equipo.equipo_ferroviario
            actualizar_estado_equipo_ferroviario(equipo_id,"Disponible")
        # Actualizar vagones si se proporcionan
        if vagones_data is not None:
            instance.equipo_vagon.clear()
            for vagon_data in vagones_data:
                equipo=nom_equipo_ferroviario.objects.get(id=vagon_data['equipo_ferroviario'])
                actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado Situado")
                vagon = vagones_dias.objects.create(
                    equipo_ferroviario=equipo,
                    cant_dias=vagon_data['cant_dias']
                )
                instance.equipo_vagon.add(vagon)
                
       
        
        return instance        
        
        
        
class PorSituarCargaDescargaFilter(filters.FilterSet):
    tipo_equipo = filters.CharFilter(lookup_expr='icontains')  # Filtro exacto (puedes usar 'icontains' para parcial
    informe = filters.NumberFilter(field_name='informe_operativo__id')
    class Meta:
        model = por_situar
        fields = ['tipo_equipo','informe']  # Campos filtrables


class PorSituarCargaDescargaSerializer(serializers.ModelSerializer):
    fecha_registro = serializers.DateTimeField(
        source='fecha', 
        format='%Y-%m-%d %H:%M', 
        read_only=True,  # Solo lectura, no necesita write_only
        help_text="Fecha y hora en que se creó el registro (automático)"
    )
   # productos_info = serializers.PrimaryKeyRelatedField(,many=True)
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
    tipo_equipo_name=serializers.ReadOnlyField(source='get_tipo_equipo_display')
    producto = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    equipo_vagon = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=vagones_dias.objects.all(),
        required=False,
    )
    equipo_vagon_detalle=vagones_dias_serializer(many=True,source='equipo_vagon', read_only=True)
    
    class Meta:
        model = por_situar
        fields = '__all__'
        extra_kwargs = {
            'producto': {'required': False},
            'observaciones': {'required': False, 'allow_null': True}
        }


    def create(self, validated_data):
        productos_data = validated_data.pop('producto', [])
        instance = por_situar.objects.get(**validated_data)
        instance.producto.get(productos_data)
        return instance

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('producto', None)
        instance = super().update(instance, validated_data)
        if productos_data is not None:
            instance.producto.set(productos_data)
        return instance


class PendienteArrastreFilter(filters.FilterSet):
    tipo_equipo = filters.CharFilter(lookup_expr='icontains')
    informe = filters.NumberFilter(field_name='informe_operativo__id')
    class Meta:
        model = arrastres
        fields = ['tipo_equipo',"informe"]

class PendienteArrastreSerializer(serializers.ModelSerializer):
    fecha_registro = serializers.DateTimeField(
        source='fecha', 
        format='%Y-%m-%d %H:%M', 
        read_only=True,  # Solo lectura, no necesita write_only
        help_text="Fecha y hora en que se creó el registro (automático)"
    )
    tipo_equipo_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_equipo_display')
    # productos_info = serializers.SerializerMethodField()
    
    producto = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    equipo_vagon = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=vagones_dias.objects.all(),
        required=False,
        write_only=True
    )
    equipo_vagon_detalle=vagones_dias_serializer(many=True,source='equipo_vagon', read_only=True)
    class Meta:
        model = arrastres
        fields = '__all__'
        filterset_class = PendienteArrastreFilter

    # def get_productos_info(self, obj):
    #     p = obj.producto
    #     return {
    #        'id': p.id,
    #         'nombre_producto': p.producto.nombre_producto,
    #         'codigo_producto': p.producto.codigo_producto,
    #         'tipo_embalaje': p.tipo_embalaje.nombre if hasattr(p.tipo_embalaje, 'nombre') else str(p.tipo_embalaje),
    #         'unidad_medida': p.unidad_medida.nombre if hasattr(p.unidad_medida, 'nombre') else str(p.unidad_medida),
    #         'cantidad': p.cantidad,
    #         'estado': p.estado,
    #         'contiene': p.contiene
    #     }

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


class rotacion_filter(django_filters.FilterSet):
    informe = filters.NumberFilter(field_name='informe_operativo__id')
    
    
    class Meta:
        model = en_trenes
        fields = ['informe']  # Campos filtrables


class RotacionVagonesSerializer(serializers.ModelSerializer):
    fecha_registro = serializers.DateTimeField(
        source='fecha', 
        format='%Y-%m-%d %H:%M', 
        read_only=True,  # Solo lectura, no necesita write_only
        help_text="Fecha y hora en que se creó el registro (automático)"
    )
    tipo_equipo_ferroviario_nombre = serializers.SerializerMethodField()
    plan_carga = serializers.IntegerField(read_only=True)
    real_carga = serializers.IntegerField(read_only=True)
    plan_rotacion = serializers.FloatField(read_only=True)
    real_rotacion = serializers.FloatField(read_only=True,)
    tipo_carga_name= serializers.ReadOnlyField(source='tipo_equipo_ferroviario.get_tipo_carga_display')
    class Meta:
        model = rotacion_vagones
        fields = [
            "id",
            "tipo_equipo_ferroviario",
            "tipo_equipo_ferroviario_nombre",
            "tipo_carga_name",
            "fecha_registro",
            "en_servicio",
            "plan_carga",
            "real_carga",
            "plan_rotacion",
            "real_rotacion",
            "informe_operativo",
        ]
        extra_kwargs = {
            "tipo_equipo_ferroviario": {"required": True},
            "en_servicio": {"required": True},
        }

    def get_tipo_equipo_ferroviario_nombre(self, obj):
        """Devuelve el nombre del tipo de equipo ferroviario."""
        return obj.tipo_equipo_ferroviario.get_tipo_equipo_display()

    def validate_tipo_equipo_ferroviario(self, value):
        """Valida que el tipo de equipo ferroviario no sea 'Locomotora'."""
        if value.tipo_equipo == "locomotora":
            raise serializers.ValidationError(
                "El tipo de equipo ferroviario no puede ser 'Locomotora'."
            )
        return value

    def validate_en_servicio(self, value):
        """Valida que el campo 'Vagones en servicio' sea un número entero positivo."""
        if value <= 0:
            raise serializers.ValidationError(
                "El número de vagones en servicio debe ser un número entero positivo."
            )
        return value

    def calculate_plan_carga(self,validated_data):
        """Calcula la sumatoria del plan diario de carga para la operación 'carga'."""
        hoy=timezone.now().date()
        print(validated_data)
        return (
            vagon_cargado_descargado.objects.filter(fecha__date=hoy,operacion="carga",tipo_equipo_ferroviario=validated_data["tipo_equipo_ferroviario"],informe_operativo=validated_data["informe_operativo"])
            .aggregate(total_plan_carga=Sum("plan_diario_carga_descarga"))
            .get("total_plan_carga", 0) or 0
        )

    def calculate_real_carga(self,validated_data):
        """Calcula la sumatoria del real de carga para la operación 'carga'."""
        hoy=timezone.now().date()
        return (
            vagon_cargado_descargado.objects.filter(fecha__date=hoy,operacion="carga",tipo_equipo_ferroviario=validated_data["tipo_equipo_ferroviario"],informe_operativo=validated_data["informe_operativo"])
            .aggregate(total_real_carga=Sum("real_carga_descarga"))
            .get("total_real_carga", 0) or 0
        )

    def calculate_plan_rotacion(self, plan_carga, en_servicio):
        """Calcula el plan de rotación."""
        if en_servicio == 0:
            return 0
        return round(plan_carga / en_servicio,2)

    def calculate_real_rotacion(self, real_carga, en_servicio):
        """Calcula el real de rotación."""
        if en_servicio == 0:
            return 0
        return round(real_carga / en_servicio,2)

    def create(self, validated_data):
        """Crea una nueva instancia de rotación de vagones."""
        # Calcular valores dinámicos
        plan_carga = self.calculate_plan_carga(validated_data)
        real_carga = self.calculate_real_carga(validated_data)
        en_servicio = validated_data["en_servicio"]

        # Calcular rotaciones
        plan_rotacion = self.calculate_plan_rotacion(plan_carga, en_servicio)
        real_rotacion = self.calculate_real_rotacion(real_carga, en_servicio)

        # Crear instancia
        instance = rotacion_vagones.objects.create(
            **validated_data,
            plan_carga=plan_carga,
            real_carga=real_carga,
            plan_rotacion=plan_rotacion,
            real_rotacion=real_rotacion,
        )
        return instance

    def update(self, instance, validated_data):
        """Actualiza una instancia existente de rotación de vagones."""
        # Calcular valores dinámicos
        plan_carga = self.calculate_plan_carga(validated_data)
        real_carga = self.calculate_real_carga(validated_data)
        en_servicio = validated_data.get("en_servicio", instance.en_servicio)

        # Calcular rotaciones
        plan_rotacion = self.calculate_plan_rotacion(plan_carga, en_servicio)
        real_rotacion = self.calculate_real_rotacion(real_carga, en_servicio)

        # Actualizar campos
        instance.tipo_equipo_ferroviario = validated_data.get(
            "tipo_equipo_ferroviario", instance.tipo_equipo_ferroviario
        )
        instance.en_servicio = en_servicio
        instance.plan_carga = plan_carga
        instance.real_carga = real_carga
        instance.plan_rotacion = plan_rotacion
        instance.real_rotacion = real_rotacion
        instance.save()

        return instance
    

class ufc_informe_operativo_filter(filters.FilterSet):
    fecha_operacion = filters.CharFilter(field_name='fecha_operacion',lookup_expr = 'exact')  
    
    class Meta:
        model = ufc_informe_operativo
        fields = '__all__' 
        
class ufc_informe_operativo_serializer(serializers.ModelSerializer):                      
    arrastres_list = serializers.SerializerMethodField()
    en_trenes_list = serializers.SerializerMethodField()
    vagones_cargados_descargados_list = serializers.SerializerMethodField()
    situados_carga_descarga_list = serializers.SerializerMethodField()
    por_situar_list = serializers.SerializerMethodField()
    vagones_productos_list = serializers.SerializerMethodField()
    rotacion_vagones_list = serializers.SerializerMethodField()
    entidad_detalle=serializers.ReadOnlyField(source = 'entidad.nombre') 
#    equipos_list=serializers.SerializerMethodField()
    creado_por = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), 
        write_only=True,
        required=False,
        allow_null=True,
    )
    
    aprobado_por = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), 
        write_only=True,
        required=False,
        allow_null=True,
    )
    
    
    creado_por_detalle=UserPermissionSerializer(source='creado_por', read_only=True)
    aprobado_por_detalle=UserPermissionSerializer(source='aprobado_por', read_only=True)
    class Meta:
        model = ufc_informe_operativo       
        fields = [
            'id',
            'fecha_operacion',
            'plan_mensual_total',
            'plan_diario_total_vagones_cargados',
            'real_total_vagones_cargados',
            'total_vagones_situados',
            'estado_parte',
            'entidad',
            'entidad_detalle',
            'creado_por',
            'creado_por_detalle',
            'aprobado_por',
            'aprobado_por_detalle',
            'arrastres_list',
            'en_trenes_list',
            'vagones_cargados_descargados_list',
            'situados_carga_descarga_list',
            'por_situar_list',
            'vagones_productos_list',
            'rotacion_vagones_list',
        #    'equipos_list',
        ]
        filterset_class: ufc_informe_operativo_filter
        
    def get_arrastres_list(self, obj):
        """Obtiene todos los arrastres asociados al informe operativo."""
        arrastres_queryset = obj.arrastres.all()
        return PendienteArrastreSerializer(arrastres_queryset, many=True).data

    def get_en_trenes_list(self, obj):
        """Obtiene todos los trenes asociados al informe operativo."""
        en_trenes_queryset = obj.en_trenes.all()
        return en_trenes_serializer(en_trenes_queryset, many=True).data

    def get_vagones_cargados_descargados_list(self, obj):
        """Obtiene todos los vagones cargados/descargados asociados al informe operativo."""
        vagones_cargados_descargados_queryset = obj.vagones_cargados_descargados.all()
        return vagon_cargado_descargado_serializer(vagones_cargados_descargados_queryset, many=True).data

    def get_situados_carga_descarga_list(self, obj):
        """Obtiene todos los situados de carga/descarga asociados al informe operativo."""
        situados_carga_descarga_queryset = obj.situados.all()
        return SituadoCargaDescargaSerializers(situados_carga_descarga_queryset, many=True).data

    def get_por_situar_list(self, obj):
        """Obtiene todos los registros por situar asociados al informe operativo."""
        por_situar_queryset = obj.por_situar.all()
        return PorSituarCargaDescargaSerializer(por_situar_queryset, many=True).data

    def get_vagones_productos_list(self, obj):
        """Obtiene todos los productos de vagones asociados al informe operativo."""
        vagones_productos_queryset = obj.vagones_productos.all()
        return vagones_productos_serializer(vagones_productos_queryset, many=True).data

    def get_rotacion_vagones_list(self, obj):
        """Obtiene todas las rotaciones de vagones asociadas al informe operativo."""
        rotacion_vagones_queryset = obj.rotacion.all()
        return RotacionVagonesSerializer(rotacion_vagones_queryset, many=True).data
    
    # def get_equipos_list(self, obj):
    #     """Obtiene todos los equipos asociadas al informe operativo."""
    #     en_trenes_queryset = obj.en_trenes.all()
    #     por_situar_queryset = obj.por_situar.all()
    #     en_trenes_queryset = obj.en_trenes.all()
    #     en_trenes_queryset = obj.en_trenes.all()
    #     en_trenes_queryset = obj.en_trenes.all()
    #     equipos_list=[]
    #     for tren in en_trenes_queryset:
    #         equipos_list=tren.equipo_vagon.all()
    #         print(type(equipos_list))
        

        
    #     return nom_equipo_ferroviario_serializer(equipos_list, many=True).data
    
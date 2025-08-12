import django_filters
from rest_framework import serializers
from django_filters import rest_framework as filters

from django.db.models import Q,Sum

#Importando modelos de UFC
from .models import(en_trenes,Situado_Carga_Descarga,producto_UFC,registro_vagones_cargados,por_situar,vagones_productos,rotacion_vagones,arrastres,ufc_informe_operativo)

from Administracion.models import Auditoria 
from rest_framework.response import Response
from rest_framework import status

#transaction.atomic crea una transacción atómica que asegura que:
#O todas las operaciones se ejecutan correctamente O ninguna se ejecuta (si ocurre algún error)
from django.db import transaction 
import json
from django.utils import timezone
from .models import  vagon_cargado_descargado,vagones_dias
from nomencladores.models import nom_equipo_ferroviario,nom_tipo_equipo_ferroviario
from Administracion.models import CustomUser

#######Importamos serializadores externos para poder tener una lectura mas detallada
from nomencladores.serializers import nom_equipo_ferroviario_serializer
from Administracion.serializers import UserPermissionSerializer


#para cada modelo del que deseemos realizar el filtrado debemos hacer un filtrado
#nom_pais_filter es una clase que se implementa para definir sobre qué campos quiero filtrar los registros de mi API, 
#hereda de filters.FilterSet

#### USADO POR CCD
## Modelos de CCD
from .models import (ccd_arrastres,ccd_en_trenes,ccd_vagones_cd,ccd_por_situar,ccd_registro_vagones_cd,ccd_situados,ccd_casillas_productos,ccd_producto,ufc_informe_ccd)

from nomencladores.serializers import (
    nom_producto_serializer,
    nom_tipo_embalaje_serializer,
    nom_unidad_medida_serializer,
    nom_tipo_equipo_ferroviario_serializer,
    nom_entidades_serializer,
)
from nomencladores.models import (
    nom_producto,
    nom_tipo_embalaje,
    nom_unidad_medida,
    nom_tipo_equipo_ferroviario,
    nom_entidades)

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
    informe = filters.NumberFilter(field_name='informe_operativo__id')
    
    def filtrado_por_origen_tipo_prod_tef(self, queryset, name, value):        
        return queryset.filter(
            Q(tipo_equipo_ferroviario_name__icontains=value) | 
            Q(producto=value) | 
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
    producto_name = serializers.ReadOnlyField(source='producto.producto.nombre_producto')   

    class Meta:
        model = vagones_productos
        fields = '__all__'
        extra_kwargs = {
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
    producto_name = serializers.ReadOnlyField(source='producto.nombre_producto')
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
        
    #Esto es una cosa que no me gusta, pero es necesario para que el serializer funcione
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
               
                # Crear y asociar registros de vagones
                for registro_data in registros_data:
                    registro = registro_vagones_cargados.objects.create(**registro_data)
                    instance.registros_vagones.add(registro)
                    
                    # Actualizar estado del equipo ferroviario
                    actualizar_estado_equipo_ferroviario(registro.no_id, 'Asignado al estado Cargado/Descargado')
                
                return instance
                
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el registro: {str(e)}")
    


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
        print("###**Log: ",equipo_vagon_data)
        #instance = super().update(instance, validated_data)
       
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
            
        if equipo_vagon_data:
# Eliminar registros antiguos no incluidos
            ids_nuevos = [equipo_id.id for equipo_id in equipo_vagon_data if equipo_id.id]
            print("###**Log: ",ids_nuevos)
            # Primero, liberar equipos ferroviarios de registros que se eliminarán
            registros_a_eliminar = instance.equipo_vagon.all()
            print("###**Log: ",registros_a_eliminar)
            for registro in registros_a_eliminar:
                actualizar_estado_equipo_ferroviario(registro, 'Disponible')
            
            
            # Actualizar o crear registros
            for registro_id in equipo_vagon_data:
                
                if registro_id:
                    # Actualizar registro existente
                    registro = nom_equipo_ferroviario.objects.get(id=registro_id.id)
                    instance.equipo_vagon.add(registro)
                
                # Actualizar estado del equipo ferroviario
                actualizar_estado_equipo_ferroviario(registro_id, 'Asignado al estado En Trenes')
        
        instance.equipo_vagon.set(equipo_vagon_data)
        
        
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
    producto_detalle=producto_vagon_serializer(many=False,source='producto', read_only=True)
    
    equipo_vagon = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
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
        
        vagones_data = validated_data.pop('equipo_vagon', [])
        instance = super().create(validated_data)
        
        # Asociar productos MANUALMENTE después de crear la instancia
        for vagon_data in vagones_data:
            equipo=nom_equipo_ferroviario.objects.get(id=vagon_data['equipo_ferroviario'])
            vagon = vagones_dias.objects.create(
                equipo_ferroviario=equipo,
                cant_dias=vagon_data['cant_dias']
            )
            
            actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado Situado")
            instance.equipo_vagon.add(vagon)
        
        print(instance,validated_data)
        return instance

    def update(self, instance, validated_data):
        vagones_data = validated_data.pop('equipo_vagon', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
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
    tipo_equipo_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_equipo_display')
    
    producto = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    producto_detalle=producto_vagon_serializer(many=False,source='producto', read_only=True)
    #-#
    
    equipo_vagon = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
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
        # Extraer datos de vagones
        vagones_data = validated_data.pop('equipo_vagon', [])
        
        # Crear instancia principal
        instance = super().create(validated_data)
        
        # Crear registros de vagones_dias y asociarlos
        for vagon_data in vagones_data:
            equipo=nom_equipo_ferroviario.objects.get(id=vagon_data['equipo_ferroviario'])
            vagon = vagones_dias.objects.create(
                equipo_ferroviario=equipo,
                cant_dias=vagon_data['cant_dias']
            )
            
            actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado Por Situar")
            instance.equipo_vagon.add(vagon)
        
        # Asociar productos
        
        return instance

###Tanke

    def update(self, instance:por_situar, validated_data):
        vagones_data = validated_data.pop('equipo_vagon', None)
        
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        
        for equipo in instance.equipo_vagon.all():
            equipo_id=equipo.equipo_ferroviario
            actualizar_estado_equipo_ferroviario(equipo_id,"Disponible")
        # Actualizar vagones si se proporcionan
        if vagones_data is not None:
            instance.equipo_vagon.clear()
            for vagon_data in vagones_data:
                equipo=nom_equipo_ferroviario.objects.get(id=vagon_data['equipo_ferroviario'])
                actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado Por Situar")
                vagon = vagones_dias.objects.create(
                    equipo_ferroviario=equipo,
                    cant_dias=vagon_data['cant_dias']
                )
                instance.equipo_vagon.add(vagon)
        
        # Actualizar productos si se proporcionan
       
        
        print(validated_data)
        instance.save()
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
    producto_detalle=producto_vagon_serializer(many=False,source='producto', read_only=True)
    
    equipo_vagon = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
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
        # Extraer datos de vagones
        vagones_data = validated_data.pop('equipo_vagon', [])
       
        
        # Crear instancia principal
        instance = super().create(validated_data)
        
        # Crear registros de vagones_dias y asociarlos
        for vagon_data in vagones_data:
            equipo=nom_equipo_ferroviario.objects.get(id=vagon_data['equipo_ferroviario'])
            vagon = vagones_dias.objects.create(
                equipo_ferroviario=equipo,
                cant_dias=vagon_data['cant_dias']
            )
            
            actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado Pendiente a Arrastre")
            instance.equipo_vagon.add(vagon)
        
        # Asociar productos
    
        return instance

    def update(self, instance:arrastres, validated_data):
        vagones_data = validated_data.pop('equipo_vagon', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        
        for equipo in instance.equipo_vagon.all():
            equipo_id=equipo.equipo_ferroviario
            actualizar_estado_equipo_ferroviario(equipo_id,"Disponible")
        # Actualizar vagones si se proporcionan
        if vagones_data is not None:
            instance.equipo_vagon.clear()
            for vagon_data in vagones_data:
                equipo=nom_equipo_ferroviario.objects.get(id=vagon_data['equipo_ferroviario'])
                actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado Pendiente a Arrastre")
                vagon = vagones_dias.objects.create(
                    equipo_ferroviario=equipo,
                    cant_dias=vagon_data['cant_dias']
                )
                instance.equipo_vagon.add(vagon)
        
        # Actualizar productos si se proporcionan
       
        
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



#######Aqui empiezan los serializadores de CCDxProducto###########
#######Los Filtros se ponen en la view o viewSet #########

def create_nested_field_pair(serializer_class, model_class, field_name, allow_null=False,many=False):
    """
    Crea un par de campos (read/write) para relaciones anidadas.
    
    return read_field, write_field
    
    #REF2

    """
    read_field = serializer_class(read_only=True,many=many)
    write_field = serializers.PrimaryKeyRelatedField(
        queryset=model_class.objects.all(),
        source=field_name,
        write_only=True,
        allow_null=allow_null
    )
    return read_field, write_field


#OK read/wirte para que se haga entrada con los id y devuelva el serializador del objeto en el write
class ccd_productoSerializer(serializers.ModelSerializer):

    
    #### Usando la nueva estructura creada
    producto, producto_id = create_nested_field_pair(
        nom_producto_serializer, nom_producto, 'producto'
    )
    
    tipo_embalaje, tipo_embalaje_id = create_nested_field_pair(
        nom_tipo_embalaje_serializer, nom_tipo_embalaje, 'tipo_embalaje'
    )
    
    unidad_medida, unidad_medida_id = create_nested_field_pair(
        nom_unidad_medida_serializer, nom_unidad_medida, 'unidad_medida'
    )
    
    tipo_equipo, tipo_equipo_id = create_nested_field_pair(
        nom_tipo_equipo_ferroviario_serializer, 
        nom_tipo_equipo_ferroviario, 
        'tipo_equipo',
        allow_null=True
    )
    ##@darilrosales88 Este campo permite hacer cositas para anidar las ForeignKey
    class Meta:
        model=ccd_producto
        fields="__all__"


    def validate(self, data):
        # Validar que el producto sea opcional
        print ("###**Log: ",data)
        
        
        return data
        
## En talla
class ccd_arrastresSerializer(serializers.ModelSerializer):
    
    producto, producto_id = create_nested_field_pair(
        ccd_productoSerializer, ccd_producto, 'producto'
    )
    acceso, acceso_id = create_nested_field_pair(
        nom_entidades_serializer, nom_entidades, 'acceso'
    )
    tipo_equipo, tipo_equipo_id = create_nested_field_pair(
        nom_tipo_equipo_ferroviario_serializer, nom_tipo_equipo_ferroviario, 'tipo_equipo'
    )
    equipo_vagon = vagones_dias_serializer(
        many=True,
        write_only=True
    )
    equipo_vagon_detalle=vagones_dias_serializer(many=True,source='equipo_vagon', read_only=True)

    class Meta:
        model=ccd_arrastres
        fields="__all__"
        
    def validate(self, attrs):
        error=""
        if attrs.get('tipo_equipo') and attrs['tipo_equipo'].tipo_equipo.lower() == 'locomotora':
            error+= "No se permite seleccionar 'locomotora' como tipo de equipo ferroviario. "
        if attrs.get('cantidad_vagones') and attrs.get('equipo_vagon'):
            if attrs['cantidad_vagones'] != len(attrs['equipo_vagon']):
                error += "La cantidad de vagones debe coincidir con la cantidad de equipos ferroviarios proporcionados."
        if error:
            raise serializers.ValidationError(detail=error,code="Field Errors")
        return super().validate(attrs)
    
    #### Por el momento esta es la unica manera de crear los Nested serializer asi que hasta que no se me ocurra otra relacion se mantendra asi
    ## Aqui esta el create para los vagones_dias   
    def create(self, validated_data):
        # Extraer datos de vagones
        vagones_data = validated_data.pop('equipo_vagon', [])
       
        
        # Crear instancia principal
        instance = super().create(validated_data)
        
        # Crear registros de vagones_dias y asociarlos
        for vagon_data in vagones_data:
            equipo=vagon_data['equipo_ferroviario']
            vagon = vagones_dias.objects.create(
                equipo_ferroviario=equipo,
                cant_dias=vagon_data['cant_dias']
            )
            
            actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado CCD Pendiente a Arrastre")
            instance.equipo_vagon.add(vagon)
        return instance
        
            
    ## Aqui esta el update para los vagones_dias   ####revisar
    def update(self, instance:ccd_arrastres, validated_data):
        vagones_data = validated_data.pop('equipo_vagon', None)
    
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        
        for equipo in instance.equipo_vagon.all():
            equipo_id=equipo.equipo_ferroviario
            actualizar_estado_equipo_ferroviario(equipo_id,"Disponible")
        # Actualizar vagones si se proporcionan
        if vagones_data is not None:
            instance.equipo_vagon.clear()
            for vagon_data in vagones_data:
                equipo=vagon_data['equipo_ferroviario']
                actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado CCD Pendiente a Arrastre")
                vagon = vagones_dias.objects.create(
                    equipo_ferroviario=equipo,
                    cant_dias=vagon_data['cant_dias']
                )
                instance.equipo_vagon.add(vagon)
        return instance

class ccd_en_trenesSerializer(serializers.ModelSerializer):
    producto, producto_id = create_nested_field_pair(
        ccd_productoSerializer, ccd_producto, 'producto'
    )
    acceso, acceso_id = create_nested_field_pair(
        nom_entidades_serializer, nom_entidades, 'acceso'
    )
    tipo_equipo, tipo_equipo_id = create_nested_field_pair(
        nom_tipo_equipo_ferroviario_serializer, nom_tipo_equipo_ferroviario, 'tipo_equipo'
    )
    equipo_vagon_detalle=nom_equipo_ferroviario_serializer(many=True,source='equipo_vagon', read_only=True)
    class Meta:
        model=ccd_en_trenes
        fields="__all__"
        
    def validate(self, attrs):
        error=""
        if attrs.get('tipo_equipo') and attrs['tipo_equipo'].tipo_equipo.lower() == 'locomotora':
            error+= "No se permite seleccionar 'locomotora' como tipo de equipo ferroviario. "
        if attrs.get('cantidad_vagones') and attrs.get('equipo_vagon'):
            if attrs['cantidad_vagones'] != len(attrs['equipo_vagon']):
                error += "La cantidad de vagones debe coincidir con la cantidad de equipos ferroviarios proporcionados."
        if error:
            raise serializers.ValidationError(detail=error,code="Field Errors")
        return super().validate(attrs)
    def create(self, validated_data):
        equipo_vagon_data=validated_data.pop('equipo_vagon',[])
        instance = ccd_en_trenes.objects.create(**validated_data)
    
        instance.equipo_vagon.set(equipo_vagon_data)
        
        for equipo in equipo_vagon_data:    
        # Actualizar estado del equipo ferroviario
            print("Este es el id a cambiar", equipo)
            actualizar_estado_equipo_ferroviario(equipo.numero_identificacion, 'Asignado al estado CCD En Trenes')
        
        return instance

    def update(self, instance, validated_data):
        
        equipo_vagon_data=validated_data.pop('equipo_vagon',None)
        #instance = super().update(instance, validated_data)
       
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
            
        if equipo_vagon_data:
# Eliminar registros antiguos no incluidos
            # Primero, liberar equipos ferroviarios de registros que se eliminarán
            registros_a_eliminar = instance.equipo_vagon.all()
            for registro in registros_a_eliminar:
                actualizar_estado_equipo_ferroviario(registro, 'Disponible')
            
            
            # Actualizar o crear registros
            for registro_id in equipo_vagon_data:
                
                if registro_id:
                    # Actualizar registro existente
                    registro = nom_equipo_ferroviario.objects.get(id=registro_id.id)
                    instance.equipo_vagon.add(registro)
                
                # Actualizar estado del equipo ferroviario
                actualizar_estado_equipo_ferroviario(registro_id, 'Asignado al estado CCD En Trenes')
        
        instance.equipo_vagon.set(equipo_vagon_data)
        
        
        return instance
    

class ccd_por_situarSerializer(serializers.ModelSerializer):
    
    producto, producto_id = create_nested_field_pair(
        ccd_productoSerializer, ccd_producto, 'producto'
    )
    acceso, acceso_id = create_nested_field_pair(
        nom_entidades_serializer, nom_entidades, 'acceso'
    )
    tipo_equipo, tipo_equipo_id = create_nested_field_pair(
        nom_tipo_equipo_ferroviario_serializer, nom_tipo_equipo_ferroviario, 'tipo_equipo'
    )
    equipo_vagon = vagones_dias_serializer(
        many=True,
        write_only=True
    )
    equipo_vagon_detalle=vagones_dias_serializer(many=True,source='equipo_vagon', read_only=True)
    
    class Meta:
        model=ccd_por_situar
        fields="__all__"
    
    def validate(self, attrs):
        error=""
        if attrs.get('tipo_equipo') and attrs['tipo_equipo'].tipo_equipo.lower() == 'locomotora':
            error+= "No se permite seleccionar 'locomotora' como tipo de equipo ferroviario. "
        if attrs.get('cantidad_vagones') and attrs.get('equipo_vagon'):
            if attrs['cantidad_vagones'] != len(attrs['equipo_vagon']):
                error += "La cantidad de vagones debe coincidir con la cantidad de equipos ferroviarios proporcionados."
        if error:
            raise serializers.ValidationError(detail=error,code="Field Errors")
        return super().validate(attrs)
    
    #### Por el momento esta es la unica manera de crear los Nested serializer asi que hasta que no se me ocurra otra relacion se mantendra asi
    ## Aqui esta el create para los vagones_dias   
    def create(self, validated_data):
        # Extraer datos de vagones
        vagones_data = validated_data.pop('equipo_vagon', [])
       
        
        # Crear instancia principal
        instance = super().create(validated_data)
        
        # Crear registros de vagones_dias y asociarlos
        for vagon_data in vagones_data:
            equipo=vagon_data['equipo_ferroviario']
            vagon = vagones_dias.objects.create(
                equipo_ferroviario=equipo,
                cant_dias=vagon_data['cant_dias']
            )
            
            actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado CCD Por Situar")
            instance.equipo_vagon.add(vagon)
        return instance
        
            
    ## Aqui esta el update para los vagones_dias   ####revisar
    def update(self, instance:ccd_arrastres, validated_data):
        vagones_data = validated_data.pop('equipo_vagon', None)
    
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        
        for equipo in instance.equipo_vagon.all():
            equipo_id=equipo.equipo_ferroviario
            actualizar_estado_equipo_ferroviario(equipo_id,"Disponible")
        # Actualizar vagones si se proporcionan
        if vagones_data is not None:
            instance.equipo_vagon.clear()
            for vagon_data in vagones_data:
                equipo=vagon_data['equipo_ferroviario']
                actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado CCD Por Situar")
                vagon = vagones_dias.objects.create(
                    equipo_ferroviario=equipo,
                    cant_dias=vagon_data['cant_dias']
                )
                instance.equipo_vagon.add(vagon)
        return instance
        
    
#####
class ccd_situadosSerializer(serializers.ModelSerializer):
    
    producto, producto_id = create_nested_field_pair(
        ccd_productoSerializer, ccd_producto, 'producto'
    )
    acceso, acceso_id = create_nested_field_pair(
        nom_entidades_serializer, nom_entidades, 'acceso'
    )
    tipo_equipo, tipo_equipo_id = create_nested_field_pair(
        nom_tipo_equipo_ferroviario_serializer, nom_tipo_equipo_ferroviario, 'tipo_equipo'
    )
    equipo_vagon = vagones_dias_serializer(
        many=True,
        write_only=True
    )
    equipo_vagon_detalle=vagones_dias_serializer(many=True,source='equipo_vagon', read_only=True)
    
    class Meta:
        model=ccd_situados
        fields="__all__"
    
    def validate(self, attrs):
        error=""
        if attrs.get('tipo_equipo') and attrs['tipo_equipo'].tipo_equipo.lower() == 'locomotora':
            error+= "No se permite seleccionar 'locomotora' como tipo de equipo ferroviario. "
        if error:
            raise serializers.ValidationError(detail=error,code="Field Errors")
        return super().validate(attrs)
    
    #### Por el momento esta es la unica manera de crear los Nested serializer asi que hasta que no se me ocurra otra relacion se mantendra asi
    ## Aqui esta el create para los vagones_dias   
    def create(self, validated_data):
        # Extraer datos de vagones
        vagones_data = validated_data.pop('equipo_vagon', [])
       
        
        # Crear instancia principal
        instance = super().create(validated_data)
        
        # Crear registros de vagones_dias y asociarlos
        for vagon_data in vagones_data:
            equipo=vagon_data['equipo_ferroviario']
            vagon = vagones_dias.objects.create(
                equipo_ferroviario=equipo,
                cant_dias=vagon_data['cant_dias']
            )
            
            actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado CCD Situado")
            instance.equipo_vagon.add(vagon)
        return instance
        
            
    ## Aqui esta el update para los vagones_dias   ####revisar
    def update(self, instance:ccd_arrastres, validated_data):
        vagones_data = validated_data.pop('equipo_vagon', None)
    
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        
        for equipo in instance.equipo_vagon.all():
            equipo_id=equipo.equipo_ferroviario
            actualizar_estado_equipo_ferroviario(equipo_id,"Disponible")
        # Actualizar vagones si se proporcionan
        if vagones_data is not None:
            instance.equipo_vagon.clear()
            for vagon_data in vagones_data:
                equipo=vagon_data['equipo_ferroviario']
                actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado CCD Situado")
                vagon = vagones_dias.objects.create(
                    equipo_ferroviario=equipo,
                    cant_dias=vagon_data['cant_dias']
                )
                instance.equipo_vagon.add(vagon)
        return instance
    


class ccd_registro_vagones_cdSerializer(serializers.ModelSerializer):
    class Meta:
        model=ccd_registro_vagones_cd
        fields="__all__"
       
    
    

class ccd_vagones_cdSerializer(serializers.ModelSerializer):
    
    producto, producto_id = create_nested_field_pair(
        ccd_productoSerializer, ccd_producto, 'producto'
    )
    acceso, acceso_id = create_nested_field_pair(
        nom_entidades_serializer, nom_entidades, 'acceso'
    )
    tipo_equipo, tipo_equipo_id = create_nested_field_pair(
        nom_tipo_equipo_ferroviario_serializer, nom_tipo_equipo_ferroviario, 'tipo_equipo'
    )
    equipo_vagon = ccd_registro_vagones_cdSerializer(
        many=True,
        write_only=True
    )
    equipo_vagon_detalle=ccd_registro_vagones_cdSerializer(many=True,source='equipo_vagon', read_only=True)
    
    class Meta:
        model=ccd_vagones_cd
        fields="__all__"
        
    def create(self, validated_data):
        # Extraer datos de vagones
        vagones_data = validated_data.pop('equipo_vagon', [])
       
        
        # Crear instancia principal
        instance = super().create(validated_data)
        
        # Crear registros de vagones_dias y asociarlos
        for vagon_data in vagones_data:
            equipo=vagon_data['equipo_ferroviario']
            vagon = ccd_registro_vagones_cd.objects.create(
                **vagon_data,  # Asumiendo que vagon_data contiene los campos necesarios
            )
            
            actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado CCD Vagon Cargado/Descargado")
            instance.equipo_vagon.add(vagon)
        return instance
        
            
    ## Aqui esta el update para los vagones_dias   ####revisar
    def update(self, instance:ccd_arrastres, validated_data):
        vagones_data = validated_data.pop('equipo_vagon', None)
    
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        
        for equipo in instance.equipo_vagon.all():
            equipo_id=equipo.equipo_ferroviario
            actualizar_estado_equipo_ferroviario(equipo_id,"Disponible")
        # Actualizar vagones si se proporcionan
        if vagones_data is not None:
            instance.equipo_vagon.clear()
            for vagon_data in vagones_data:
                equipo=vagon_data['equipo_ferroviario']
                actualizar_estado_equipo_ferroviario(equipo,"Asignado al estado Vagon Cargado/Descargado")
                vagon = ccd_registro_vagones_cd.objects.create(
                    **vagon_data,  # Asumiendo que vagon_data contiene los campos necesarios
                )
                instance.equipo_vagon.add(vagon)
        return instance
        

class ccd_casillas_productosSerializer(serializers.ModelSerializer):
    """sumary_line: Este serializador maneja los productos de las casillas CCD
    
    Me bote cuando hice este , con 0 IA , referencia para demas proyectos #REF1
    """
    
    acceso, acceso_id = create_nested_field_pair(
        nom_entidades_serializer, nom_entidades, 'acceso'
    )
    
    real_carga=serializers.SerializerMethodField()
    real_descarga=serializers.SerializerMethodField()
    
    diferencia_descarga=serializers.SerializerMethodField()
    diferencia_carga=serializers.SerializerMethodField()
    
    situados=serializers.SerializerMethodField()
    situados_mas_2dias=serializers.SerializerMethodField()
    
    por_situar=serializers.SerializerMethodField()
    por_situar_mas_2dias=serializers.SerializerMethodField()
    
    en_trenes=serializers.SerializerMethodField()
    pendientes=serializers.SerializerMethodField()
    total=serializers.SerializerMethodField()
    
    class Meta:
        model=ccd_casillas_productos
        fields="__all__"
      
    def validate_total_ayer(self, value):
        """Valida que el total ayer sea un número entero positivo."""
        # Quiero que se compruebe si hay un registro del 
        
        if value < 0:
            raise serializers.ValidationError("El total ayer debe ser un número entero positivo.")
        if ufc_informe_ccd.objects.all().count() == 0:
            raise serializers.ValidationError("No hay un informe CCD registrado, por favor registre uno antes de continuar.")
        if ufc_informe_ccd.objects.all().count() == 1: 
            return value 
        if ufc_informe_ccd.objects.filter(acceso=self.context['request'].user.entidad).all().count() > 1:
            # Obtener el penúltimo informe (o el del día anterior si existe)
            informes = ufc_informe_ccd.filter(acceso=self.context['request'].user.entidad).objects.order_by('-fecha_operacion')
            if informes.count() > 1:
                informe_ccd = informes[1]  # Penúltimo
            registro=informe_ccd.casillas_ccd.filter(acceso=self.context['request'].user.entidad).first()
            return registro.total_general
        
    def get_real_carga(self,object:ccd_casillas_productos):
        """6.	El campo Real carga se actualiza:

        Real carga = ∑No. ID registrados en la sección Cargados/Descargados 
        del producto seleccionado de la pestaña Situados a la carga/descarga, cuando el campo Operación sea “1-Carga”.

        """
        vagones=object.informe_ccd.vagones_cd_ccd.filter(operacion='carga').all()
        
        try:    
            contador=[vagon.real_carga_descarga for vagon in vagones]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            real=sum(contador)
            return real
        
    def get_real_descarga(self,object:ccd_casillas_productos):
        """7.	El campo Real descarga se actualiza:
        
        Real descarga = ∑No. ID registrados en la sección Cargados/Descargados 
        del producto seleccionado de la pestaña Situados a la carga/descarga, cuando el campo Operación sea “2-Descarga”.

        """
        vagones=object.informe_ccd.vagones_cd_ccd.filter(operacion='descarga').all()
        
        try:    
            contador=[vagon.real_carga_descarga for vagon in vagones]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            real=sum(contador)
            return real
        
    
    
    def get_diferencia_descarga(self,object:ccd_casillas_productos):
        """4.	El campo Diferencia descarga de cada acceso comercial es el resultado de:
        
                Diferencia descarga = Real descarga – Plan descarga
        """
        vagones=object.informe_ccd.vagones_cd_ccd.filter(operacion='descarga').all()
        
        try:    
            contador=[vagon.real_carga_descarga for vagon in vagones]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            diferencia=sum(contador)-object.plan_descarga
            return diferencia

    
    def get_diferencia_carga(self,object:ccd_casillas_productos):
        """4.	El campo Diferencia Carga de cada acceso comercial es el resultado de:
        
                Diferencia carga = Real carga – Plan carga
        """
        vagones=object.informe_ccd.vagones_cd_ccd.filter(operacion='carga').all()
        
        try:    
            contador=[vagon.real_carga_descarga for vagon in vagones]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            diferencia=sum(contador)-object.plan_carga
            return diferencia
        
    def get_situados(self,object:ccd_casillas_productos):
        """
        6.	El campo Situados carga/descarga de cada acceso comercial es el resultado de: 

        Situados carga/descarga = ∑ Cantidad de vagones del registro de la pestaña Situados a la carga/descarga
        
        """
        situados = object.informe_ccd.situados_ccd.all()
        contador=0
        
        try:    
            contador=[registro.equipo_vagon.count() for registro in situados]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            return sum(contador)
        
    def get_situados_mas_2dias(self,object:ccd_casillas_productos):
        """Esta funcion retorna la cantidad de vagones situados que tienen mas de 2 dias"""
        situados = object.informe_ccd.situados_ccd.all()
        contador=0  
        try:    
            contador=[registro.equipo_vagon.filter(cant_dias__gt=2).count() for registro in situados if registro.equipo_vagon.filter(cant_dias__gt=2)]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            return sum(contador)
        
    
    def get_por_situar(self,object:ccd_casillas_productos):
        """
        8.	El campo Por situar de cada acceso comercial es el resultado de: 
        
        Por situar = ∑ Cantidad de vagones del registro de la pestaña Por situar a la carga/descarga
        """
        
        por_situar = object.informe_ccd.por_situar_ccd.all()
        contador=0
        
        try:    
            contador=[registro.equipo_vagon.count() for registro in por_situar]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            return sum(contador)
    def get_por_situar_mas_2dias(self,object:ccd_casillas_productos):
        """Esta funcion retorna la cantidad de vagones por situar que tienen mas de 2 dias"""
        por_situar = object.informe_ccd.por_situar_ccd.all()
        contador=0  
        try:    
            contador=[registro.equipo_vagon.filter(cant_dias__gt=2).count() for registro in por_situar if registro.equipo_vagon.filter(cant_dias__gt=2)]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de por_situar: {e}')
        finally:
            return sum(contador)
        
        
    def get_en_trenes(self,object:ccd_casillas_productos):
        """10.	El campo En trenes de cada acceso comercial es el resultado de: 
        
        En trenes = ∑ Cantidad de vagones del registro de la pestaña En trenes
        """
        
        en_trenes = object.informe_ccd.en_trenes_ccd.all()
        contador=0
        
        try:    
            contador=[registro.equipo_vagon.count() for registro in en_trenes]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            return sum(contador)
        
    def get_pendientes(self,object:ccd_casillas_productos):
        """11.	El campo Pendientes de arrastre de cada acceso comercial es el resultado de: 
        
        Pendientes de arrastre = ∑ Cantidad de vagones del registro de la pestaña Pendientes de arrastre


        Args:
            object (ccd_casillas_productos): 

        Raises:
            serializers.ValidationError: detail= f'No se pudo contar la cantidad de situados: ERROR

        Returns:
            int: ∑ Cantidad de vagones del registro de la pestaña Pendientes de arrastre
        """
        
        arrastres = object.informe_ccd.arrastres_ccd.all()
        contador=0
        
        try:    
            contador=[registro.equipo_vagon.count() for registro in arrastres]
        except Exception as e:
            raise serializers.ValidationError(detail= f'No se pudo contar la cantidad de situados: {e}')
        finally:
            return sum(contador)
    
    def get_total(self, object: ccd_casillas_productos):
        """12. El campo Total de cada acceso comercial es el resultado de:
        pendientes + en_trenes + por_situar + situados
        """
        pendientes = self.get_pendientes(object)
        en_trenes = self.get_en_trenes(object)
        por_situar = self.get_por_situar(object)
        situados = self.get_situados(object)
        return pendientes + en_trenes + por_situar + situados


class ufc_informe_ccdSerializer(serializers.ModelSerializer):
    arrastres_list = serializers.SerializerMethodField()
    en_trenes_list = serializers.SerializerMethodField()
    vagones_cargados_descargados_list = serializers.SerializerMethodField()
    situados_carga_descarga_list = serializers.SerializerMethodField()
    por_situar_list = serializers.SerializerMethodField()
    casillas_list = serializers.SerializerMethodField()
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
        model = ufc_informe_ccd   
        fields="__all__"    
  
    
    #OK Arrastres
    def get_arrastres_list(self, obj):
        """Obtiene todos los arrastres asociados al informe operativo."""
        arrastres_queryset = obj.arrastres_ccd.all()
        return ccd_arrastresSerializer(arrastres_queryset, many=True).data
    #OK En Trenes
    def get_en_trenes_list(self, obj):
        """Obtiene todos los trenes asociados al informe operativo."""
        en_trenes_queryset = obj.en_trenes_ccd.all()
        return ccd_en_trenesSerializer(en_trenes_queryset, many=True).data
    #OK vagones C/D
    def get_vagones_cargados_descargados_list(self, obj):
        """Obtiene todos los vagones cargados/descargados asociados al informe operativo."""
        vagones_cargados_descargados_queryset = obj.vagones_cd_ccd.all()
        return ccd_vagones_cdSerializer(vagones_cargados_descargados_queryset, many=True).data
    #OK Situados
    def get_situados_carga_descarga_list(self, obj):
        """Obtiene todos los situados de carga/descarga asociados al informe operativo."""
        situados_carga_descarga_queryset = obj.situados_ccd.all()
        return ccd_situadosSerializer(situados_carga_descarga_queryset, many=True).data
    #OK Por Situar
    def get_por_situar_list(self, obj):
        """Obtiene todos los registros por situar asociados al informe operativo."""
        por_situar_queryset = obj.por_situar_ccd.all()
        return ccd_por_situarSerializer(por_situar_queryset, many=True).data

    def get_casillas_list(self, obj):
        """Obtiene todos los productos de vagones asociados al informe operativo."""
        casillas_queryset = obj.casillas_ccd.all()
        return ccd_casillas_productosSerializer(casillas_queryset, many=True).data

    def get_rotacion_vagones_list(self, obj):
        """Obtiene todas las rotaciones de vagones asociadas al informe operativo."""
        rotacion_vagones_queryset = obj.rotacion.all()
        return RotacionVagonesSerializer(rotacion_vagones_queryset, many=True).data
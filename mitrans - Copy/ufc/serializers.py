import django_filters
from rest_framework import serializers
from django_filters import rest_framework as filters

from django.db.models import Q,Sum

#Importando modelos de UFC
from .models import (ufc_informe_operativo, vagon_cargado_descargado,producto_UFC, en_trenes,nom_equipo_ferroviario
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
class ufc_informe_operativo_filter(filters.FilterSet):
    fecha_operacion = filters.CharFilter(field_name='fecha_operacion',lookup_expr = 'exact')  
    
    class Meta:
        model = ufc_informe_operativo
        fields = '__all__' 
        
class ufc_informe_operativo_serializer(serializers.ModelSerializer):                      
    
    class Meta:
        model = ufc_informe_operativo       
        fields = '__all__'
        filterset_class: ufc_informe_operativo_filter
#****************-------------------------********************--------------------***************-----------------****

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

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                # Extraer datos para relaciones
                productos_data = validated_data.pop('producto', None)
                registros_data = validated_data.pop('registros_vagones_data', [])
                
                # Actualizar campos directos
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                
                # Actualizar productos si se proporcionaron
                if productos_data is not None:
                    instance.producto.set(productos_data)
                
                # Manejar registros de vagones
                if registros_data:
                    # Eliminar registros antiguos no incluidos
                    ids_nuevos = [r.get('id') for r in registros_data if r.get('id')]
                    
                    # Primero, liberar equipos ferroviarios de registros que se eliminarán
                    registros_a_eliminar = instance.registros_vagones.exclude(id__in=ids_nuevos)
                    for registro in registros_a_eliminar:
                        self.actualizar_estado_equipo_ferroviario(registro.no_id, 'Disponible')
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
                        self.actualizar_estado_equipo_ferroviario(registro.no_id, 'Asignado al estado Cargado/Descargado')
                
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
                productos_ids = validated_data.pop('producto_ids', [])
                registros_data = validated_data.pop('registros_vagones_data', [])

                def validate(self, data):
                    # Forzar el valor de causas_incumplimiento si viene vacío
                    if 'causas_incumplimiento' in data and not data['causas_incumplimiento']:
                        data['causas_incumplimiento'] = 'Sin causas especificadas'  # Valor por defecto

                # Asegurar que real_carga_descarga no sea sobrescrito
                if validated_data.get('real_carga_descarga', 0) == 0:
                    registros_data = validated_data.get('registros_vagones_data', [])
                    validated_data['real_carga_descarga'] = len(registros_data)
                
                # Crear instancia principal
                instance = super().create(validated_data)
                
                # Asignar productos
                if productos_ids:
                    instance.producto.set(productos_ids)
                
                # Crear y asociar registros de vagones
                for registro_data in registros_data:
                    registro = registro_vagones_cargados.objects.create(**registro_data)
                    instance.registros_vagones.add(registro)
                    
                    # Actualizar estado del equipo ferroviario
                    self.actualizar_estado_equipo_ferroviario(registro.no_id, 'Asignado al estado Cargado/Descargado')
                
                return instance
                
        except Exception as e:
            raise serializers.ValidationError(f"Error al crear el registro: {str(e)}")
    
    def actualizar_estado_equipo_ferroviario(self, no_id, nuevo_estado):
        """
        Método auxiliar para actualizar el estado de un equipo ferroviario
        """
        try:
            from nomencladores.models import nom_equipo_ferroviario
            
            equipo = nom_equipo_ferroviario.objects.filter(numero_identificacion=no_id).first()
            if equipo:
                equipo.estado_actual = nuevo_estado
                equipo.save()
        except Exception as e:
            # No romper el flujo principal si hay error al actualizar el estado
            print(f"Error al actualizar estado del equipo {no_id}: {str(e)}")        

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
   # equipo_vagon_id=serializers.ReadOnlyField(source='equipo_vagon.numero_identificacion')
    productos_info = serializers.SerializerMethodField()
    vagones_info=serializers.SerializerMethodField()
    producto = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        required=False
    )

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
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
    tipo_equipo_name=serializers.ReadOnlyField(source='get_tipo_equipo_display')
    producto = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    situados = serializers.IntegerField()
    pendiente_proximo_dia = serializers.IntegerField()
    
    class Meta:
        model = Situado_Carga_Descarga
        fields = ('id', 'tipo_origen' , 'tipo_origen_name', 'origen', 'tipo_equipo' , 'tipo_equipo_name', 'estado', 
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
    tipo_origen_name = serializers.ReadOnlyField(source='get_tipo_origen_display')
    tipo_equipo_name=serializers.ReadOnlyField(source='get_tipo_equipo_display')
    producto = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=producto_UFC.objects.all(),
        required=False
    )
    
    class Meta:
        model = por_situar
        fields = ('id', 'tipo_origen', 'tipo_origen_name', 'origen', 'tipo_equipo','tipo_equipo_name', 
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
    tipo_equipo_ferroviario_nombre = serializers.SerializerMethodField()
    plan_carga = serializers.IntegerField(read_only=True)
    real_carga = serializers.IntegerField(read_only=True)
    plan_rotacion = serializers.FloatField(read_only=True)
    real_rotacion = serializers.FloatField(read_only=True)
    tipo_carga_name= serializers.ReadOnlyField(source='tipo_equipo_ferroviario.get_tipo_carga_display')
    class Meta:
        model = rotacion_vagones
        fields = [
            "id",
            "tipo_equipo_ferroviario",
            "tipo_equipo_ferroviario_nombre",
            "tipo_carga_name",
            "en_servicio",
            "plan_carga",
            "real_carga",
            "plan_rotacion",
            "real_rotacion",
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
        return (
            vagon_cargado_descargado.objects.filter(operacion="carga",tipo_equipo_ferroviario=validated_data["tipo_equipo_ferroviario"])
            .aggregate(total_plan_carga=Sum("plan_diario_carga_descarga"))
            .get("total_plan_carga", 0) or 0
        )

    def calculate_real_carga(self,validated_data):
        """Calcula la sumatoria del real de carga para la operación 'carga'."""
        return (
            vagon_cargado_descargado.objects.filter(operacion="carga",tipo_equipo_ferroviario=validated_data["tipo_equipo_ferroviario"])
            .aggregate(total_real_carga=Sum("real_carga_descarga"))
            .get("total_real_carga", 0) or 0
        )

    def calculate_plan_rotacion(self, plan_carga, en_servicio):
        """Calcula el plan de rotación."""
        if en_servicio == 0:
            return 0
        return plan_carga / en_servicio

    def calculate_real_rotacion(self, real_carga, en_servicio):
        """Calcula el real de rotación."""
        if en_servicio == 0:
            return 0
        return real_carga / en_servicio

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
        plan_carga = self.calculate_plan_carga()
        real_carga = self.calculate_real_carga()
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
    


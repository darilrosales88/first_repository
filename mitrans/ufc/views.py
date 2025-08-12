#4.1 una variante para trabajar con los serializadores  es la propiedad viewsets
# de rest_framework, facilita el CRUD
from rest_framework import viewsets,generics,permissions
from rest_framework.pagination import PageNumberPagination
#importacion de modelos
from .models import vagon_cargado_descargado,producto_UFC,en_trenes
from .models import registro_vagones_cargados,vagones_productos
from .models import por_situar,Situado_Carga_Descarga,arrastres,rotacion_vagones,ufc_informe_operativo,vagones_dias
#importacion de serializadores asociados a los modelos
from .serializers import (vagon_cargado_descargado_filter, vagon_cargado_descargado_serializer, 
                        producto_vagon_serializer, en_trenes_serializer,PorSituarCargaDescargaSerializer, SituadoCargaDescargaSerializers, 
                        PendienteArrastreSerializer, registro_vagones_cargados_serializer,
                        registro_vagones_cargados_filter, vagones_productos_filter, producto_vagon_filter,
                        vagones_productos_serializer, en_trenes_filter, RotacionVagonesSerializer,PorSituarCargaDescargaFilter,
                        ufc_informe_operativo_serializer,ufc_informe_operativo_filter,
                        vagones_dias_serializer, rotacion_filter,PendienteArrastreFilter
                        )
from django.core.cache import cache
from Administracion.models import Auditoria

from rest_framework.response import Response
from rest_framework import status,filters

#para el filtrado
from django_filters.rest_framework import DjangoFilterBackend

#para usar el or
from django.db.models import Q,Prefetch

from django.db.models import Sum
from django.db import transaction

from django.utils import timezone
#para usar el or

#Actualizando el ModelViewSet para usar diferentes permisos según la acción
from .permissions import IsAdminUFCPermission,IsVisualizadorUFCPermission,IsRevisorUFCPermission,IsUFCPermission,OperadorUFCPermission,RevisorUFCPermission,ReadOnly

from rest_framework.decorators import action,api_view  # Importa el decorador action

#Para las validaciones de las fechas en el informe operativo
from django.db.models.functions import TruncDate
from django.db.models import DateField
from datetime import datetime
from django.db.models.functions import Cast


from django.http import JsonResponse

import json

# Función auxiliar para crear registros de auditoría
def registrar_auditoria(request, accion):
    """
    Método centralizado para registrar acciones en el modelo Auditoria
    
    """
    try:
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=accion,
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
    except Exception as e:
        # No romper el flujo principal si hay error al registrar auditoría
        print(f"Error al registrar auditoría: {str(e)}")


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
             
        
#**********************************************************************************************************************************

#Para Informe operativo
class ufc_informe_operativo_view_set(viewsets.ModelViewSet):
    queryset = ufc_informe_operativo.objects.all().order_by('-id')
    serializer_class = ufc_informe_operativo_serializer
    permission_classes= [OperadorUFCPermission|IsAdminUFCPermission|IsVisualizadorUFCPermission|RevisorUFCPermission|ReadOnly]


    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrado por fecha de operación
        fecha_operacion = self.request.query_params.get('fecha_operacion')
        search_term = self.request.query_params.get('search', None)
        if search_term:
           queryset = queryset.prefetch_related('entidad').filter(
            Q(entidad_detalle__icontains=search_term) |
            Q(estado_parte__icontains=search_term) 
            
).distinct()
        return queryset
            
        if fecha_operacion:
            try:
                # Parsear la fecha ignorando la hora si está presente
                fecha_operacion = datetime.strptime(fecha_operacion.split('T')[0], '%Y-%m-%d').date()
                queryset = queryset.annotate(
                    fecha_op_date=Cast('fecha_operacion', DateField())
                ).filter(fecha_op_date=fecha_operacion)
            except (ValueError, AttributeError):
                pass  # O manejar el error adecuadamente
        
        return queryset  # ¡No olvidar retornar el queryset!       
        

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='RevisorUFC').exists() and not (request.user.groups.filter(name='OperadorUFC').exists() or request.user.groups.filter(name='AdminUFC').exists() ):
            return Response(
                {"detail": "No tiene permiso para realizar esta acción.\n Solo los Operadores UFC pueden crear partes"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Verificar si ya existe un informe para esta fecha (solo día, mes y año)
        fecha_operacion_str = request.data.get('fecha_operacion')
        if fecha_operacion_str:
            try:
                # Parsear la fecha ignorando la hora si está presente
                fecha_operacion = datetime.strptime(fecha_operacion_str.split('T')[0], '%Y-%m-%d').date()
                
                # Solución para SQLite - Dos alternativas:

                # Opción 1: Usando TruncDate (requiere Django 1.10+)
                """ if ufc_informe_operativo.objects.annotate(
                    fecha_op_date=TruncDate('fecha_operacion')
                ).filter(fecha_op_date=fecha_operacion).exists():
                    return Response(
                        {"detail": "Ya existe un informe operativo para esta fecha."},
                        status=status.HTTP_400_BAD_REQUEST
                    ) """

                # Opción 2: Usando Cast (alternativa más universal)
                if ufc_informe_operativo.objects.annotate(
                     fecha_op_date=Cast('fecha_operacion', DateField())
                 ).filter(fecha_op_date=fecha_operacion).exists():
                     return Response(
                         {"detail": "Ya existe un informe operativo para esta fecha."},
                         status=status.HTTP_400_BAD_REQUEST
                 )

            except (ValueError, AttributeError):
                # Manejar error si el formato de fecha no es válido
                return Response(
                    {"detail": "Formato de fecha inválido."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        informe = serializer.save()
        
        # Auditoría centralizada
        registrar_auditoria(request, f"Insertar Informe operativo: {informe.fecha_operacion}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    #funcion añadida para la actualizacion del campo estado_parte***
    def partial_update(self, request, *args, **kwargs):
            
        instance = self.get_object()
        
        # Solo permitir actualizar el estado_parte
        if 'estado_parte' not in request.data:
            return Response(
                {"detail": "Se requiere el campo 'estado_parte'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
            
        serializer = self.get_serializer(
            instance, 
            data={'estado_parte': request.data['estado_parte']
                  }, 
            partial=True
        )
        
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Auditoría centralizada
        registrar_auditoria(request, f"Actualizar estado del Informe operativo a {serializer.data.estado_parte}")

        return Response(serializer.data)
 
    def update(self, request, *args, **kwargs):
        #
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        informe = serializer.save()

        # Auditoría centralizada
        registrar_auditoria(request, f"Modificar Informe operativo: {informe.fecha_operacion}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        fecha_oper = instance.fecha_operacion

        # Auditoría centralizada
        registrar_auditoria(request, f"Eliminar Informe operativo: {fecha_oper}")

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de Partes informe operativo")
        
        return super().list(request, *args, **kwargs)  

#Verificando que exista el informe creado antes de insertar
@api_view(['GET'])
def verificar_informe_existente(request):
    entidad=request.user.entidad
    fecha_operacion = request.query_params.get('fecha_operacion')
    if not fecha_operacion:
        return Response({"error": "Parámetro fecha_operacion requerido"}, status=400)
    
    try:
        fecha_obj = datetime.strptime(fecha_operacion, '%Y-%m-%d').date()
        existe = ufc_informe_operativo.objects.filter(
            fecha_operacion__date=fecha_obj,
            entidad=entidad
        ).exists()
        print(existe)
        if existe:
            informe = ufc_informe_operativo.objects.filter(
                fecha_operacion__date=fecha_obj,
                entidad=entidad
            ).first()
            return Response({
                "existe": True,
                "id": informe.id,
                "fecha_operacion": informe.fecha_operacion,
                "estado":informe.estado_parte,
            })
        return Response({"existe": False})
    except ValueError:
        return Response({"error": "Formato de fecha inválido"}, status=400)
    
#vista para cambiar estado_parte en ufc_informe_operativo
# En tu archivo views.py de la app ufc
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import ufc_informe_operativo
from django.utils import timezone
import json

@require_http_methods(["PATCH"])
def actualizar_estado_parte(request):
    try:
        data = json.loads(request.body)
        nuevo_estado = data.get('nuevo_estado')
        informe_id= data.get('id')
        print("LOG #### ID: ",informe_id)
        
        if not nuevo_estado:
            return JsonResponse({'error': 'Estado no proporcionado'}, status=400)
        
        if not informe_id:
            return JsonResponse({'error': 'No se esta pasando bien  el id'}, status=400)
        
        # Obtener la fecha actual
        hoy = timezone.now().date()
        
        # Buscar el informe del día actual
        informe = ufc_informe_operativo.objects.filter(
            fecha_operacion__date=hoy,
            id=informe_id
        ).first()
        
        
        
        if not informe:
            return JsonResponse({'error': 'No existe un informe operativo para la fecha actual'}, status=404)
        
        informe.estado_parte = nuevo_estado
        informe.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Estado actualizado a {nuevo_estado} correctamente',
            'nuevo_estado': nuevo_estado,
            'informe_id': informe.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
#****************************************************************************************************************************

#para vagones y productos
class vagones_productos_view_set(viewsets.ModelViewSet):
    queryset = vagones_productos.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = vagones_productos_serializer
    filter_class = vagones_productos_filter
    permission_classes= [IsUFCPermission|ReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('origen_tipo_prod_tef', None)
        
        # Utiliza el filtro definido en vagon_cargado_descargado_filter
        if search is not None:
            return self.filter_class({'origen_tipo_prod_tef': search}, queryset=queryset).qs
        
        informe_id = self.request.query_params.get('informe')
        if informe_id:
            queryset = queryset.filter(informe_operativo__id=informe_id)
        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_vagones_productos = serializer.save()
        registrar_auditoria(request, f"Insertar vagón y producto/s: {objeto_vagones_productos.id}")
        

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_vagones_productos = serializer.save()
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, f"Modificar instancia de vagones y productos: {objeto_vagones_productos.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        #permisos de acceso a la operacion   
        instance = self.get_object()
        id_objeto_vagon_producto = instance.id
        registrar_auditoria(request, f"Eliminar instancia de vagones y productos: {id_objeto_vagon_producto}")
        
        
        # Esto activará el método delete() del modelo que maneja la eliminación en cascada
        instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de vagones y productos")

        return super().list(request, *args, **kwargs)   

    @action(detail=False, methods=['get'], url_path='calcular-campos-automaticos')
    def calcular_campos_automaticos(self, request):
        """
        Calcula los campos automáticos del modelo vagones y productos.
        """
        informe_id = request.query_params.get('informe_id')
        if not informe_id:
            return Response({'error': 'Se requiere el parámetro informe_id'}, status=400)
        
        try:            
            hoy = timezone.now().date()
            año_actual = hoy.year

            # Verificar si es el primer día del mes
            es_primer_dia_mes = hoy.day == 1            

            # Obtener el informe operativo asociado
            informe_operativo = ufc_informe_operativo.objects.filter(id=informe_id).first()
            
            if not informe_operativo:
                return Response({'error': 'Informe operativo no encontrado'}, status=404)

            # Verificar si hay otros informes operativos en el año actual
            informes_año_actual = ufc_informe_operativo.objects.filter(
                fecha_operacion__year=año_actual
            ).exclude(id=informe_operativo.id)  
                    
            es_unico_informe_año = not informes_año_actual.exists()
            
            # Calcular plan_dia basado en vagones cargados
            plan_dia = (
                vagon_cargado_descargado.objects.filter(
                    operacion="carga",
                    informe_operativo=informe_operativo
                ).aggregate(
                    total=Sum("plan_diario_carga_descarga")
                )["total"] or 0
            )

            vagones_cargados = (
                vagon_cargado_descargado.objects.filter(
                    operacion="carga",
                    informe_operativo=informe_operativo
                ).aggregate(
                    total=Sum("real_carga_descarga")
                )["total"] or 0
            )
            
            vagones_situados = (
                Situado_Carga_Descarga.objects.filter(
                    operacion="carga",
                    informe_operativo=informe_operativo
                ).aggregate(
                    total=Sum("situados")
                )["total"] or 0
            )
            
            plan_aseguramiento = (
                vagon_cargado_descargado.objects.filter(
                    operacion="carga",
                    informe_operativo=informe_operativo
                ).aggregate(
                    total=Sum("real_carga_descarga")
                )["total"] or 0
            )

            # Preparar datos de respuesta
            response_data = {
                'plan_dia': plan_dia,
                'es_primer_dia_mes': es_primer_dia_mes,
                'es_unico_informe_año': es_unico_informe_año,
                'plan_acumulado_dia_anterior': 0,
                'real_acumulado_dia_anterior': 0,
                'vagones_situados':vagones_situados,
                'vagones_cargados':vagones_cargados,
                'plan_aseguramiento':plan_aseguramiento
            }
            print("Mijitoooooooooo ", response_data)

            # Manejar los diferentes casos según las condiciones
            if es_unico_informe_año and es_primer_dia_mes:
                # Caso 1: Único informe en el año y es primer día del mes
                response_data.update({
                    'plan_acumulado_dia_anterior': 0,
                    'real_acumulado_dia_anterior': 0
                })
                
            elif not es_unico_informe_año and es_primer_dia_mes:
                # Caso 3: No es único informe en el año pero es primer día del mes
                response_data.update({
                    'plan_acumulado_dia_anterior': 0,
                    'real_acumulado_dia_anterior': 0
                })
                
                # Obtener datos del informe anterior si existe
                informe_anterior = informes_año_actual.filter(
                    fecha_operacion__lt=informe_operativo.fecha_operacion
                ).order_by('-fecha_operacion').first()
                
                if informe_anterior:
                    vagon_producto_anterior = vagones_productos.objects.filter(
                        informe_operativo=informe_anterior
                    ).first()
                    if vagon_producto_anterior:
                        response_data['plan_anual'] = vagon_producto_anterior.plan_anual
                        
            elif not es_unico_informe_año and not es_primer_dia_mes:
                # Caso 4: No es único informe en el año ni es primer día del mes
                informe_anterior = informes_año_actual.filter(
                    fecha_operacion__lt=informe_operativo.fecha_operacion
                ).order_by('-fecha_operacion').first()                
                
                if informe_anterior:
                    vagon_producto_anterior = vagones_productos.objects.filter(
                        informe_operativo=informe_anterior
                    ).first()
                    print("no jodaas mas ",vagon_producto_anterior.plan_anual)
                    if vagon_producto_anterior:
                        response_data.update({
                            'plan_anual': vagon_producto_anterior.plan_anual,
                            'plan_acumulado_dia_anterior': vagon_producto_anterior.plan_acumulado_actual,
                            'real_acumulado_dia_anterior': vagon_producto_anterior.real_acumulado_actual,
                            'plan_aseguramiento_proximos_dias': vagon_producto_anterior.plan_aseguramiento_proximos_dias
                        })

            return Response(response_data)
            
        except Exception as e:
            return Response(
                {"error": f"Error al calcular los campos automáticos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 


#/*********************************************************************************************************************************************
#para el estado de vagones cargados/descargados
#para el estado de vagones cargados/descargados
class vagon_cargado_descargado_view_set(viewsets.ModelViewSet):
    queryset = vagon_cargado_descargado.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = vagon_cargado_descargado_serializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend, # Para filtros exactos
                       filters.OrderingFilter]  # Para ordenamiento
    filterset_fields = ['tipo_equipo_ferroviario__id', 'producto__producto__codigo_producto','producto__tipo_embalaje__id','producto__unidad_medida__simbolo']
    search_fields = ['producto__producto__nombre_producto','cantidad','=unidad_medida__unidad_medida', 'origen','tipo_origen']

    filter_class = vagon_cargado_descargado_filter
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    def get_queryset(self):
        queryset = super().get_queryset()
        informe_id = self.request.query_params.get('informe')
        search = self.request.query_params.get('tef_prod_estado', None)
        if informe_id:
            queryset = queryset.filter(informe_operativo__id=informe_id)
        
        # Utiliza el filtro definido en vagon_cargado_descargado_filter
        if search is not None:
            return self.filter_class({'tef_prod_estado': search}, queryset=queryset).qs
        
        return queryset
    def perform_destroy(self, instance):
        registros_asociados = instance.registros_vagones.all()
        
        for registro in registros_asociados:
            actualizar_estado_equipo_ferroviario(registro.no_id, 'Disponible')
        
        registros_asociados.delete()
        instance.delete()

    def create(self, request, *args, **kwargs):
        print("Datos recibidos en create:", request.data)  # Verificar datos entrantes
        #permisos de acceso a la operacion
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_vagon_cargado_descargado = serializer.save()
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, f"Insertar vagón cargado/descargado: {objeto_vagon_cargado_descargado.id}")
        

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_vagon_cargado_descargado = serializer.save()

        registrar_auditoria(request, f"Modificar vagón cargado/descargado: {objeto_vagon_cargado_descargado.id}")

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        
        
        try:
            instance = self.get_object()
            id_objeto_vagon_cargado_descargado = instance.id
            
            registrar_auditoria(request, f"Eliminar vagón cargado/descargado y sus registros asociados: {id_objeto_vagon_cargado_descargado}")
            
            
            # Eliminar la instancia (esto activará el método delete() del modelo)
            instance.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {"error": f"No se pudo eliminar el registro: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
    def list(self, request, *args, **kwargs):
        
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de vagones cargados/descargados")

        return super().list(request, *args, **kwargs)
    #calculando el campo real_carga_descarga
    @action(detail=False, methods=['post'])
    def calcular_total_vagones_por_productos(self, request):
        producto_ids = request.data.get('producto_ids', [])
        
        if not producto_ids:
            return Response({'total': 0})
        
        # Buscar todos los registros que tengan al menos uno de los productos seleccionados
        registros = vagon_cargado_descargado.objects.filter(
            producto__id__in=producto_ids
        ).distinct()
        
        # Sumar todos los vagones asociados a estos registros
        total = 0
        for registro in registros:
            total += registro.registros_vagones.count()
            
        return Response({'total': total})
   
    @action(detail=True, methods=['get'], url_path='registros-vagones')
    def obtener_registros_vagones(self, request, pk=None):
        """
        Endpoint para obtener los registros de vagones asociados a un vagon_cargado_descargado
        """
        try:
            # Obtener la instancia principal
            instance = self.get_object()
            
            # Obtener los registros asociados a través de la relación ManyToMany
            registros_vagones = instance.registros_vagones.all()
            
            # Serializar los datos
            serializer = registro_vagones_cargados_serializer(registros_vagones, many=True)
            
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {"error": f"No se pudieron obtener los registros de vagones: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # También agrega este otro action para obtener los registros completos (como mencionaste en tu código)
    @action(detail=True, methods=['get'], url_path='registros-completos')
    def obtener_registros_completos(self, request, pk=None):
        """
        Endpoint alternativo que devuelve los registros de vagones con más detalles
        """
        try:
            instance = self.get_object()
            registros_vagones = instance.registros_vagones.all().values(
                'id',
                'no_id',
                'fecha_despacho',
                'tipo_origen',
                'origen',
                'fecha_llegada',
                'observaciones'
            )            
            return Response(list(registros_vagones))
        
        except Exception as e:
            return Response(
                {"error": f"No se pudieron obtener los registros completos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def verificar_productos(request):
    producto_ids = request.data.get('producto_ids', [])
    existentes = producto_UFC.objects.filter(id__in=producto_ids).values_list('id', flat=True)
    return Response({
        'todos_existen': len(existentes) == len(producto_ids),
        'ids_existentes': list(existentes),
        'ids_faltantes': list(set(producto_ids) - set(existentes))
    })

    
#para vagones agregados a cargados/descargados
class registro_vagones_cargados_view_set(viewsets.ModelViewSet):
    queryset = registro_vagones_cargados.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = registro_vagones_cargados_serializer    

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('no_id_origen', None)

        if search is not None:
            #filtrado por origen y por no_id
            queryset = queryset.filter( Q(no_id__icontains=search) | Q(origen__icontains=search) 
            )

        return queryset

    def create(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_registro_vagones_cargados = serializer.save()


        registrar_auditoria(request, f"Insertar vagón a estado cargado/descargado: {objeto_registro_vagones_cargados.id}")
        

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_registro_vagones_cargados = serializer.save()


        registrar_auditoria(request, f"Modificar vagón del estado cargado/descargado: {objeto_registro_vagones_cargados.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
       
        
        instance = self.get_object()
        id_objeto_registro_vagones_cargados = instance.id


        registrar_auditoria(request, f"Eliminar vagón del estado cargado/descargado: {id_objeto_registro_vagones_cargados}")

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        
        registrar_auditoria(request, "Visualizar lista de vagones del estado cargado/descargado")
        

        return super().list(request, *args, **kwargs)
    
#/********************************************************EN_TRENES*********************************************************************
class en_trenes_view_set(viewsets.ModelViewSet):
    queryset = en_trenes.objects.all().order_by('-id')
    serializer_class = en_trenes_serializer
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    filter_class = en_trenes_filter
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    ordering_fields = ['id'] 
    ordering = ['-id']  # Orden por defecto (descendente por id)    

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        informe_id = self.request.query_params.get('informe')
        if informe_id:
            queryset = queryset.filter(informe_operativo__id=informe_id)
        if search_term:
            # Filtra por coincidencia en cualquiera de los campos
            queryset = queryset.prefetch_related('equipo_vagon','producto').filter(
            Q(origen__icontains=search_term) |
            Q(destino__icontains=search_term) |
            Q(producto__producto__nombre_producto__icontains=search_term) |
            Q(producto__producto__codigo_producto__icontains=search_term) |
            Q(numero_identificacion_locomotora__icontains=search_term)
).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        #si no esta en el grupo AdminUFC no puede haver la accion
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_en_trenes = serializer.save()


        registrar_auditoria(request, f"Insertado formulario en trenes: {objeto_en_trenes.id}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
       
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_en_trenes = serializer.save()

        registrar_auditoria(request, f"Modificar formulario en trenes: {objeto_en_trenes.id}")

        return Response(serializer.data)

    # En views.py (en_trenes_view_set)
    def destroy(self, request, *args, **kwargs):
       
        instance = self.get_object()
        id_objeto_en_trenes = instance.id
        
        # 1. Primero obtener todos los equipos asociados
        equipos_asociados = instance.equipo_vagon.all()
        
        # 2. Actualizar estado de cada equipo
        for equipo in equipos_asociados:
            try:
                # Pasar el objeto completo en lugar de solo el número
                actualizar_estado_equipo_ferroviario(equipo, "Disponible")
            except Exception as e:
                print(f"Error al actualizar equipo {equipo.id}: {str(e)}")
                continue
        

        registrar_auditoria(request,f"Eliminar formulario en trenes {id_objeto_en_trenes}")

        # 4. Finalmente eliminar la instancia
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def list(self, request, *args, **kwargs):

        registrar_auditoria(request, "Visualizar lista de formularios en trenes")

        return super().list(request, *args, **kwargs)
    

#***********************************************************************************************************

class producto_vagon_view_set(viewsets.ModelViewSet):
    queryset = producto_UFC.objects.all().order_by('-id') # Definir el queryset
    serializer_class = producto_vagon_serializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filterset_class = producto_vagon_filter

    search_fields=[
        'tipo_equipo__tipo_equipo'
    ]

    def create(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_producto_en_vagon = serializer.save()

        # Registrar la acción en el modelo de Auditoria

        registrar_auditoria(request, f"Insertado Productos en Vagon: {objeto_producto_en_vagon.id}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_producto_en_vagon = serializer.save()

        registrar_auditoria(request, f"Modificar formulario producto en vagon: {objeto_producto_en_vagon.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        
        
        instance = self.get_object()
        id_objeto_en_trenes = instance.id


        registrar_auditoria(request, f"Eliminar formulario producto en vagon {id_objeto_en_trenes}")

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de formularios productos en vagon")

        return super().list(request, *args, **kwargs)
#*******************************************************************************************************


#Voy a agregar los modulos de auditoria a los que hizo Karmal
class PorSituarCargaDescargaViewSet(viewsets.ModelViewSet):
    queryset = por_situar.objects.all().order_by("-id")
    serializer_class = PorSituarCargaDescargaSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend, # Para filtros exactos
                       filters.OrderingFilter]  # Para ordenamiento
    filterset_fields = ['tipo_equipo__id', 'producto__producto__codigo_producto','producto__tipo_embalaje__id','producto__unidad_medida__simbolo']
    search_fields = ['producto__producto__nombre_producto','cantidad','=unidad_medida__unidad_medida', 'origen','tipo_origen']

    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_equipo = self.request.query_params.get("tipo_equipo")
        informe_id = self.request.query_params.get('informe')
        if informe_id:
            queryset = queryset.filter(informe_operativo__id=informe_id)
        
        if tipo_equipo:
            if "," in tipo_equipo:
                tipos = tipo_equipo.split(",")
                queryset = queryset.filter(tipo_equipo__in=tipos)
        return queryset.prefetch_related('producto')  # Optimización para la relación M2M
    
    # Los métodos create, update, destroy, list permanecen igual
    # ya que el serializer ahora maneja la lógica de los productos
    

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            objeto_por_situar = serializer.save()


            registrar_auditoria(request, f"Insertado formulario en Por Situar carga o descarga: {objeto_por_situar.id}")

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            # Manejo de excepciones para errores de validación
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_por_situar = serializer.save()


        registrar_auditoria(request,f"Modificar formulario Por situar carga o descarga: {objeto_por_situar.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        
        
        instance = self.get_object()
        id_objeto_por_situar = instance.id

 
        registrar_auditoria(request, f"Eliminar formulario Por Situar carga y Descarga {id_objeto_por_situar}")

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        
        registrar_auditoria(request, "Visualizar lista de formularios Por Situar")

        return super().list(request, *args, **kwargs)
    

class SituadoCargaDescargaViewset(viewsets.ModelViewSet):
    queryset = Situado_Carga_Descarga.objects.all().order_by("-id")
    serializer_class = SituadoCargaDescargaSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend, # Para filtros exactos
                       filters.OrderingFilter]  # Para ordenamiento
    filterset_fields = ['tipo_equipo__id', 'producto__producto__codigo_producto','producto__tipo_embalaje__id','producto__unidad_medida__simbolo']
    search_fields = ['producto__producto__nombre_producto','cantidad','=unidad_medida__unidad_medida', 'origen','tipo_origen']

    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_equipo = self.request.query_params.get("tipo_equipo")
        informe_id = self.request.query_params.get('informe')
        if informe_id:
            queryset = queryset.filter(informe_operativo__id=informe_id)
        if tipo_equipo:
            if "," in tipo_equipo:
                tipos = tipo_equipo.split(",")
                queryset = queryset.filter(tipo_equipo__in=tipos)
        return queryset.prefetch_related('producto')  # Optimización para la relación M2M
    
    # Los métodos create, update, destroy, list permanecen igual
    # ya que el serializer ahora maneja la lógica de los productos
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_situado = serializer.save()

        registrar_auditoria(request,f"Insertado formulario en Situado carga o descarga: {objeto_situado.id}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
       
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_situado = serializer.save()


        registrar_auditoria(request, f"Modificar formulario Situado: {objeto_situado.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
       
        instance = self.get_object()
        id_objeto_situado = instance.id


        registrar_auditoria(request, f"Eliminar formulario Situado carga y Descarga {id_objeto_situado}")

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request,"Visualizar lista de formularios Situados")

        return super().list(request, *args, **kwargs)
 
class PendienteArrastreViewset(viewsets.ModelViewSet):
    queryset = arrastres.objects.all()
    serializer_class = PendienteArrastreSerializer
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filter_backends = [filters.SearchFilter,DjangoFilterBackend, # Para filtros exactos
                       filters.OrderingFilter]  # Para ordenamiento
    filterset_fields = ['tipo_equipo__id', 'producto__producto__codigo_producto','producto__tipo_embalaje__id','producto__unidad_medida__simbolo']
    search_fields = ['producto__producto__nombre_producto','cantidad','=unidad_medida__unidad_medida', 'origen','tipo_origen']
    filter_class = PendienteArrastreFilter

    
    def get_queryset(self):
        queryset = super().get_queryset()
        informe_id = self.request.query_params.get('informe')
        if informe_id:
            queryset = queryset.filter(informe_operativo__id=informe_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_pendiente = serializer.save()

        registrar_auditoria(request, f"Insertado formulario en Pendiente Arrastre: {objeto_pendiente.id}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_pendiente = serializer.save()

        registrar_auditoria(request, f"Modificar formulario Pendiente Arrastre: {objeto_pendiente.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
       
        
        instance = self.get_object()
        id_objeto_pediente = instance.id


        registrar_auditoria(request, f"Eliminar formulario Pendiente Arrastre {id_objeto_pediente}")

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        
 
        registrar_auditoria(request,"Visualizar lista de Rotacion de Vagones")

        return super().list(request, *args, **kwargs)
    

    
    
#*************Registro de vagones Dia*******************
class VagonesDiasViewSet(viewsets.ModelViewSet):
    queryset=vagones_dias.objects.all()
    serializer_class=vagones_dias_serializer
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 


#*************Empieza View Rotacion de Vagones **********************
class RotacionVagonesViewSet(viewsets.ModelViewSet):
    """
    Vista para gestionar registros de rotación de vagones.
    Permite listar, crear, actualizar y eliminar registros.
    """
    
    
    queryset = rotacion_vagones.objects.all()
    serializer_class = RotacionVagonesSerializer
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
  # Permite acceso de solo lectura a usuarios sin permisos de escritura
    filter_class = rotacion_filter

    ordering_fields = ['id'] 
    ordering = ['-id']  # Orden por defecto (descendente por id)    
    def get_queryset(self):
        queryset = super().get_queryset()
        informe_id = self.request.query_params.get('informe')
        if informe_id:
            queryset = queryset.filter(informe_operativo__id=informe_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_rotacion = serializer.save()


        registrar_auditoria(request, f"Insertado formulario en Rotacion de vagones: {objeto_rotacion.id}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
       
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_rotacion = serializer.save()


        registrar_auditoria(request, f"Modificar formulario Rotacion de vagones: {objeto_rotacion.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
       
        
        instance = self.get_object()
        id_objeto_rotacion = instance.id


        registrar_auditoria(request, f"Eliminar formulario Rotacion de vagones {id_objeto_rotacion}")

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        
        # Registrar la acción en el modelo de Auditoria

        registrar_auditoria(request,"Visualizar lista de Rotacion de Vagones")

        return super().list(request, *args, **kwargs)
    
#*************Termina View Rotacion de Vagones **********************



#*************Aqui empieza la ViewSet de CCDxPRODUCTO****************
#************Imports****************
from .serializers import (ccd_productoSerializer,ccd_arrastresSerializer,ccd_en_trenesSerializer,ccd_por_situarSerializer,ccd_registro_vagones_cdSerializer, ccd_situadosSerializer,ccd_vagones_cdSerializer, ufc_informe_ccdSerializer, ccd_casillas_productosSerializer)

from .models import (ccd_vagones_cd,ccd_arrastres,ccd_en_trenes,ccd_por_situar,ccd_producto,ccd_registro_vagones_cd,ccd_situados,ccd_casillas_productos,ufc_informe_ccd)
#***********************************


##### Methods Api view para Real Carga/Descarga
@api_view(['GET'])
def obtener_real_carga_ccd(request):
    """
    Obtiene los registros de Real Carga/Descarga filtrando por tipo_equipo_ferroviario (id).
    Parámetros esperados en la query: tipo_equipo (id), informe (id, opcional)
    """
    tipo_equipo_id = request.query_params.get('tipo_equipo')
    informe_id = request.query_params.get('informe')
    producto_id = request.query_params.get('producto')
    
    hoy = timezone.now().date()
    error=""
    if not tipo_equipo_id:
        error+="Debe proporcionar el parámetro tipo_equipo (id)"
    if not informe_id:
        error+="\nDebe proporcionar el parámetro informe (id)"
    if not producto_id:
        error+="\nDebe proporcionar el parámetro producto (id)"
    
    if error:
        return Response({"error": error}, status=400)
    
    filtros = {
        "tipo_equipo__id": tipo_equipo_id,
        "fecha_registro": hoy,
        "informe_ccd__id":informe_id,
        "producto__id":producto_id
    }
    
    registros_carga = ccd_vagones_cd.objects.filter(**filtros,operacion="carga")
    registros_descarga = ccd_vagones_cd.objects.filter(**filtros,operacion="descarga")
    
    real_carga=0
    for registro in registros_carga:
        real_carga+=registro.equipo_vagon.count()
    
    real_descarga=0
    for registro in registros_descarga:
        real_descarga+=registro.equipo_vagon.count()
        
    
    return Response({"real_carga":real_carga,
                     "real_descarga":real_descarga}, status=200)
    





#*************VIEWSSET**************
#### View CCD Productos OK
class ccd_productoViewSet(viewsets.ModelViewSet):
    serializer_class=ccd_productoSerializer
    queryset=ccd_producto.objects.order_by("-id").all()
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission]     
    filter_backends = [filters.SearchFilter,DjangoFilterBackend, # Para filtros exactos
                       filters.OrderingFilter]  # Para ordenamiento
    
    filterset_fields = ['tipo_equipo__id', 'producto__codigo_producto','tipo_embalaje__id','unidad_medida__simbolo']
    search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']

#### View CCD Informe general OK
class ccd_informeViewSet(viewsets.ModelViewSet):
    serializer_class=ufc_informe_ccdSerializer
    queryset=ufc_informe_ccd.objects.order_by("-id").all()
    
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    # search_fields = ['contiene', 'producto__nombre_producto', 'cantidad']
    # filterset_fields = ['producto', 'tipo_embalaje', 'unidad_medida']
    # ordering_fields = ['id', 'contiene', 'cantidad']
    # ordering = ['-id']


#### View Verificar OK
@api_view(['GET'])
def verificar_informe_ccd_existente(request):
    entidad=request.user.entidad
    
    fecha_operacion = request.query_params.get('fecha_operacion')
    
    
    try:
        fecha_obj=""
        if not fecha_operacion:
            fecha_obj=datetime.now().date()
        else:
            fecha_obj = datetime.strptime(fecha_operacion, '%Y-%m-%d').date()
        
        existe = ufc_informe_ccd.objects.filter(
            fecha_operacion__date=fecha_obj,
            entidad=entidad
        ).exists()
        print(existe)
        if existe:
            informe = ufc_informe_ccd.objects.filter(
                fecha_operacion__date=fecha_obj,
                entidad=entidad
            ).first()
            return Response({
                "existe": True,
                "id": informe.id,
                "fecha_operacion": informe.fecha_operacion,
                "estado":informe.estado_parte,
            })
        return Response({"existe": False})
    except ValueError:
        return Response({"error": "Formato de fecha inválido"}, status=400)

#### View CCD arrastres OK
class ccd_arrastresViewSet(viewsets.ModelViewSet):
    serializer_class=ccd_arrastresSerializer
    queryset=ccd_arrastres.objects.order_by("-id").all()
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    #search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']

#### View CCD En Trenes OK
class ccd_en_trenesViewSet(viewsets.ModelViewSet):
    serializer_class=ccd_en_trenesSerializer
    queryset=ccd_en_trenes.objects.order_by("-id").all()
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    #search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']
    
#### View CCD Vagones Carga/Descarga OK
class ccd_vagones_cdViewSet(viewsets.ModelViewSet):
    serializer_class=ccd_vagones_cdSerializer
    queryset=ccd_vagones_cd.objects.order_by("-id").all()
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    #search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']
    
#### View CCD por Situar OK
class ccd_por_situarViewSet(viewsets.ModelViewSet):
    serializer_class=ccd_por_situarSerializer
    queryset=ccd_por_situar.objects.order_by("-id").all()
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    #search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']

#### View CCD Situados OK
class ccd_situadosViewSet(viewsets.ModelViewSet):
    serializer_class=ccd_situadosSerializer
    queryset=ccd_situados.objects.order_by("-id").all()
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    #search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']
    
#### View CCD Casillas Productos
class ccd_casillas_productosViewSet(viewsets.ModelViewSet):
    serializer_class=ccd_casillas_productosSerializer
    queryset=ccd_casillas_productos.objects.order_by("-id").all()
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    #search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']
    
#### View CCD Registro Vagones Carga/Descarga
class ccd_registro_vagones_cdViewSet(viewsets.ModelViewSet):
    serializer_class=ccd_registro_vagones_cdSerializer
    queryset=ccd_registro_vagones_cd.objects.order_by("-id").all()
    permission_classes = [IsUFCPermission|ReadOnly|OperadorUFCPermission|RevisorUFCPermission] 
    filter_backends = [ 
        DjangoFilterBackend,  # Para filtros exactos
        filters.SearchFilter,  # Para búsqueda de texto
        filters.OrderingFilter  # Para ordenamiento
        ]
    #search_fields = ['contiene','producto__nombre_producto','cantidad','=unidad_medida__unidad_medida']
#4.1 una variante para trabajar con los serializadores  es la propiedad viewsets
# de rest_framework, facilita el CRUD
from rest_framework import viewsets,generics,permissions
from rest_framework.pagination import PageNumberPagination
#importacion de modelos
from .models import vagon_cargado_descargado,producto_UFC,en_trenes
from .models import registro_vagones_cargados,vagones_productos,HistorialVagonesProductos
from .models import por_situar,Situado_Carga_Descarga,arrastres,rotacion_vagones,ufc_informe_operativo,vagones_dias
#importacion de serializadores asociados a los modelos
from .serializers import (vagon_cargado_descargado_filter, vagon_cargado_descargado_serializer, 
                        producto_vagon_serializer, en_trenes_serializer,PorSituarCargaDescargaSerializer, SituadoCargaDescargaSerializers, 
                        PendienteArrastreSerializer, registro_vagones_cargados_serializer,
                        registro_vagones_cargados_filter, vagones_productos_filter, 
                        vagones_productos_serializer, en_trenes_filter, RotacionVagonesSerializer,
                        ufc_informe_operativo_serializer,ufc_informe_operativo_filter,
                        HistorialVagonCargadoDescargado,HistorialVagonCargadoDescargadoSerializer,
                        HistorialVagonesProductosSerializer,vagones_dias_serializer
                        )
from django.core.cache import cache
from Administracion.models import Auditoria

from rest_framework.response import Response
from rest_framework import status

#para el filtrado
from django_filters.rest_framework import DjangoFilterBackend

#para usar el or
from django.db.models import Q,Prefetch


from django.utils import timezone
#para usar el or

#Actualizando el ModelViewSet para usar diferentes permisos según la acción
from .permissions import IsAdminUFCPermission,IsVisualizadorUFCPermission

from rest_framework.decorators import action,api_view  # Importa el decorador action

#Para las validaciones de las fechas en el informe operativo
from django.db.models.functions import TruncDate
from django.db.models import DateField
from datetime import datetime
from django.db.models.functions import Cast
from django.db import transaction

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date



# Verifica si el usuario tiene el rol "ufc"
class IsUFCPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ROLES_PERMITIDO=['ufc','admin']
        return request.user.role in ROLES_PERMITIDO
    
#la otra variante de asignacion de permisos en base a grupos(AdminUFC, VisualizadorUFC)

#asignando a permission_classes los permisos asociados al usuario, extraido a la raiz pues sera comun para todos los ModelViewSet
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUFCPermission]
        else:  # Para list y retrieve
            # Permitir tanto a AdminUFC como a VisualizadorUFC ver los registros
            permission_classes = [IsAdminUFCPermission | IsVisualizadorUFCPermission]
        return [permission() for permission in permission_classes]


#**********************************************************************************************************************************

#Para Informe operativo
class ufc_informe_operativo_view_set(viewsets.ModelViewSet):
    queryset = ufc_informe_operativo.objects.all().order_by('-id')
    serializer_class = ufc_informe_operativo_serializer

    

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrado por fecha de operación
        fecha_operacion = self.request.query_params.get('fecha_operacion')
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
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
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
        
        # Auditoría
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar Informe operativo: {informe.fecha_operacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    #funcion añadida para la actualizacion del campo estado_parte***
    def partial_update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        instance = self.get_object()
        
        # Solo permitir actualizar el estado_parte
        if 'estado_parte' not in request.data:
            return Response(
                {"detail": "Se requiere el campo 'estado_parte'."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = self.get_serializer(
            instance, 
            data={'estado_parte': request.data['estado_parte']}, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Auditoría
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user,
            accion=f"Actualizar estado del Informe operativo a {serializer.data['estado_parte']}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)
 

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        informe = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar Informe operativo: {informe.fecha_operacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        fecha_oper = instance.fecha_operacion

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar Informe operativo: {fecha_oper}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de Partes informe operativo",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)  

#Verificando que exista el informe creado antes de insertar
@api_view(['GET'])
def verificar_informe_existente(request):
    print(request)
    fecha_operacion = request.query_params.get('fecha_operacion')
    if not fecha_operacion:
        return Response({"error": "Parámetro fecha_operacion requerido"}, status=400)
    
    try:
        fecha_obj = datetime.strptime(fecha_operacion, '%Y-%m-%d').date()
        existe = ufc_informe_operativo.objects.filter(
            fecha_operacion__date=fecha_obj
        ).exists()
        
        if existe:
            informe = ufc_informe_operativo.objects.filter(
                fecha_operacion__date=fecha_obj
            ).first()
            return Response({
                "existe": True,
                "id": informe.id,
                "fecha_operacion": informe.fecha_operacion
            })
        return Response({"existe": False})
    except ValueError:
        return Response({"error": "Formato de fecha inválido"}, status=400)

#para vagones y productos
class vagones_productos_view_set(viewsets.ModelViewSet):
    queryset = vagones_productos.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = vagones_productos_serializer
    filter_class = vagones_productos_filter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('origen_tipo_prod_tef', None)
        
        # Utiliza el filtro definido en vagon_cargado_descargado_filter
        if search is not None:
            return self.filter_class({'origen_tipo_prod_tef': search}, queryset=queryset).qs
        
        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_vagones_productos = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertar vagón y producto/s: {objeto_vagones_productos.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_vagones_productos = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar instancia de vagones y productos: {objeto_vagones_productos.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        id_objeto_vagon_producto = instance.id
        
        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar instancia de vagones y productos: {id_objeto_vagon_producto}",
            navegador=navegador,
        )
        
        # Esto activará el método delete() del modelo que maneja la eliminación en cascada
        instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones y productos",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs) 

class vagones_productos_hoy_viewset(viewsets.ModelViewSet):
    queryset = vagones_productos.objects.all()
    serializer_class = vagones_productos_serializer
    
    def get_queryset(self):
        # Obtener la fecha actual (sin la hora)
        hoy = timezone.now().date()
        
        # Filtrar registros donde la fecha (truncada a día) sea igual a hoy
        return self.queryset.annotate(
            fecha_dia=TruncDate('fecha', output_field=DateField())
        ).filter(fecha_dia=hoy).order_by('-fecha')
    
    def list(self, request, *args, **kwargs):
        # Verificar permisos como en la vista original
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones cargados/descargados hoy",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        
        return super().list(request, *args, **kwargs)  

class HistorialVagonesProductosViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistorialVagonesProductos.objects.all().order_by('-fecha_creacion')
    serializer_class = HistorialVagonesProductosSerializer
    permission_classes = [IsUFCPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        informe_id = self.request.query_params.get('informe_id')

        if informe_id:
            queryset = queryset.filter(informe_operativo_id=informe_id)

        return queryset.select_related('informe_operativo')

    def list(self, request, *args, **kwargs):
        # Verificar permisos del grupo
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Auditoría
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar historial de vagones y productos",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs) 

#/*********************************************************************************************************************************************
#para el estado de vagones cargados/descargados
#para el estado de vagones cargados/descargados
class vagon_cargado_descargado_view_set(viewsets.ModelViewSet):
    queryset = vagon_cargado_descargado.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = vagon_cargado_descargado_serializer
    filter_class = vagon_cargado_descargado_filter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('tef_prod_estado', None)
        
        # Utiliza el filtro definido en vagon_cargado_descargado_filter
        if search is not None:
            return self.filter_class({'tef_prod_estado': search}, queryset=queryset).qs
        
        return queryset
    def perform_destroy(self, instance):
        registros_asociados = instance.registros_vagones.all()
        
        for registro in registros_asociados:
            self.actualizar_estado_equipo_ferroviario(registro.no_id, 'Disponible')
        
        registros_asociados.delete()
        instance.delete()

    def create(self, request, *args, **kwargs):
        print("Datos recibidos en create:", request.data)  # Verificar datos entrantes
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_vagon_cargado_descargado = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertar vagón cargado/descargado: {objeto_vagon_cargado_descargado.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_vagon_cargado_descargado = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar vagón cargado/descargado: {objeto_vagon_cargado_descargado.id}",
            navegador=navegador,
        )

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            instance = self.get_object()
            id_objeto_vagon_cargado_descargado = instance.id
            
            # Registrar la acción en el modelo de Auditoria antes de eliminar
            navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
            direccion_ip = request.META.get('REMOTE_ADDR')
            
            Auditoria.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                direccion_ip=direccion_ip,
                accion=f"Eliminar vagón cargado/descargado y sus registros asociados: {id_objeto_vagon_cargado_descargado}",
                navegador=navegador,
            )
            
            # Eliminar la instancia (esto activará el método delete() del modelo)
            instance.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {"error": f"No se pudo eliminar el registro: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    
    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones cargados/descargados",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

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
class vagon_cargado_descargado_hoy_view_set(viewsets.ModelViewSet):
    queryset = vagon_cargado_descargado.objects.all()
    serializer_class = vagon_cargado_descargado_serializer
    
    def get_queryset(self):
        # Obtener la fecha actual (sin la hora)
        hoy = timezone.now().date()
        
        # Filtrar registros donde la fecha (truncada a día) sea igual a hoy
        return self.queryset.annotate(
            fecha_dia=TruncDate('fecha', output_field=DateField())
        ).filter(fecha_dia=hoy).order_by('-fecha')
    
    def list(self, request, *args, **kwargs):
        # Verificar permisos como en la vista original
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones cargados/descargados hoy",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        
        return super().list(request, *args, **kwargs)
    
#vista para el historial de vagon_cargado_descargado
class HistorialVagonCargadoDescargadoViewSet(viewsets.ModelViewSet):
    queryset = HistorialVagonCargadoDescargado.objects.all().order_by('-fecha_creacion')
    serializer_class = HistorialVagonCargadoDescargadoSerializer
    permission_classes = [IsUFCPermission]
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        informe_id = self.request.query_params.get('informe_id')
        
        if informe_id:
            queryset = queryset.filter(informe_operativo_id=informe_id)
            
        return queryset.select_related('informe_operativo')
    
    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Auditoría
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar historial de vagones cargados/descargados",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        
        return super().list(request, *args, **kwargs)
#para productos de vagones y productos

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
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_registro_vagones_cargados = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertar vagón a estado cargado/descargado: {objeto_registro_vagones_cargados.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_registro_vagones_cargados = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar vagón del estado cargado/descargado: {objeto_registro_vagones_cargados.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        id_objeto_registro_vagones_cargados = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar vagón del estado cargado/descargado: {id_objeto_registro_vagones_cargados}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones del estado cargado/descargado",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
    
#/********************************************************EN_TRENES*********************************************************************
class en_trenes_view_set(viewsets.ModelViewSet):
    queryset = en_trenes.objects.all().order_by('-id')
    serializer_class = en_trenes_serializer
    filter_backends = [DjangoFilterBackend]
    filter_class = en_trenes_filter

    ordering_fields = ['id'] 
    ordering = ['-id']  # Orden por defecto (descendente por id)    

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)

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
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_en_trenes = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertado formulario en trenes: {objeto_en_trenes.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_en_trenes = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar formulario en trenes: {objeto_en_trenes.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()
        id_objeto_en_trenes = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar formulario en trenes {id_objeto_en_trenes}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        #si no pertenece a VisualizadorUFC o AdminUFC no puede realizar la accion
        if not request.user.groups.filter(name='AdminUFC').exists() and not request.user.groups.filter(name='VisualizadorUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de formularios en trenes",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
    
class en_trenes_hoy_viewset(viewsets.ModelViewSet):
    queryset = en_trenes.objects.all()
    serializer_class = en_trenes_serializer
    
    def get_queryset(self):
        # Obtener la fecha actual (sin la hora)
        hoy = timezone.now().date()
        
        # Filtrar registros donde la fecha (truncada a día) sea igual a hoy
        return self.queryset.annotate(
            fecha_dia=TruncDate('fecha', output_field=DateField())
        ).filter(fecha_dia=hoy).order_by('-fecha')
    
    def list(self, request, *args, **kwargs):
        # Verificar permisos como en la vista original
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones pendientes de arrastre hoy",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        
        return super().list(request, *args, **kwargs)


#***********************************************************************************************************

class producto_vagon_view_set(viewsets.ModelViewSet):
    queryset = producto_UFC.objects.all().order_by('-id') # Definir el queryset
    serializer_class = producto_vagon_serializer
    permission_classes = [IsUFCPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('buscar_producto', None)

        if search_term:
            # Filtra por coincidencia en cualquiera de los campos
            queryset = queryset.select_related('producto').filter(
            Q(id__icontains=search_term) |
            Q(tpo_embalaje__icontains=search_term)|
            Q(producto__nombre_producto__icontains=search_term)|
            Q(producto___codigo_producto__icontains=search_term)
            
)
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_producto_en_vagon = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertado formulario en trenes: {objeto_producto_en_vagon.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_producto_en_vagon = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar formulario producto en vagon: {objeto_producto_en_vagon.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        id_objeto_en_trenes = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar formulario producto en vagon {id_objeto_en_trenes}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        print("mayeya")
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de formularios productos en vagon",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#*******************************************************************************************************


#Voy a agregar los modulos de auditoria a los que hizo Karmal
class PorSituarCargaDescargaViewSet(viewsets.ModelViewSet):
    queryset = por_situar.objects.all().order_by("-id").prefetch_related('vagones')
    serializer_class = PorSituarCargaDescargaSerializer
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_equipo = self.request.query_params.get("tipo_equipo")
        if tipo_equipo:
            if "," in tipo_equipo:
                tipos = tipo_equipo.split(",")
                queryset = queryset.filter(tipo_equipo__in=tipos)
        return queryset.prefetch_related('producto')  # Optimización para la relación M2M
    
    # Los métodos create, update, destroy, list permanecen igual
    # ya que el serializer ahora maneja la lógica de los productos
    

    def create(self, request, *args, **kwargs):
        try:
            if not request.user.groups.filter(name='AdminUFC').exists():
                return Response(
                    {"detail": "No tiene permiso para realizar esta acción."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            objeto_por_situar = serializer.save()

                # Registrar la acción en el modelo de Auditoria
            navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
            direccion_ip = request.META.get('REMOTE_ADDR')
            Auditoria.objects.create(
                    usuario=request.user if request.user.is_authenticated else None,
                    direccion_ip=direccion_ip,
                    accion=f"Insertado formulario en Por Situar carga o descarga: {objeto_por_situar.id}",
                    navegador=navegador,
                )

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            # Manejo de excepciones para errores de validación
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_por_situar = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar formulario Por situar carga o descarga: {objeto_por_situar.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        id_objeto_por_situar = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar formulario Por Situar carga y Descarga {id_objeto_por_situar}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de formularios Por Situar",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
    
class PorSituarCargaDescarga_hoy_ViewSet(viewsets.ModelViewSet):
    queryset = por_situar.objects.all()
    serializer_class = PorSituarCargaDescargaSerializer
    
    def get_queryset(self):
        # Obtener la fecha actual (sin la hora)
        hoy = timezone.now().date()
        
        # Filtrar registros donde la fecha (truncada a día) sea igual a hoy
        return self.queryset.annotate(
            fecha_dia=TruncDate('fecha', output_field=DateField())
        ).filter(fecha_dia=hoy).order_by('-fecha')
    
    def list(self, request, *args, **kwargs):
        # Verificar permisos como en la vista original
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones por situar hoy",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        
        return super().list(request, *args, **kwargs)
    #**********************************************************************************************

class SituadoCargaDescargaViewset(viewsets.ModelViewSet):
    queryset = Situado_Carga_Descarga.objects.all().order_by("-id").prefetch_related('vagones')
    serializer_class = SituadoCargaDescargaSerializers
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsUFCPermission] 
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_equipo = self.request.query_params.get("tipo_equipo")
        if tipo_equipo:
            if "," in tipo_equipo:
                tipos = tipo_equipo.split(",")
                queryset = queryset.filter(tipo_equipo__in=tipos)
        return queryset.prefetch_related('producto')  # Optimización para la relación M2M
    
    # Los métodos create, update, destroy, list permanecen igual
    # ya que el serializer ahora maneja la lógica de los productos
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_situado = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertado formulario en Situado carga o descarga: {objeto_situado.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_situado = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar formulario Situado: {objeto_situado.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        id_objeto_situado = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar formulario Situado carga y Descarga {id_objeto_situado}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de formularios Situados",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
class SituadoCargaDescarga_hoy_Viewset(viewsets.ModelViewSet):
    queryset = Situado_Carga_Descarga.objects.all()
    serializer_class = SituadoCargaDescargaSerializers
    
    def get_queryset(self):
        # Obtener la fecha actual (sin la hora)
        hoy = timezone.now().date()
        
        # Filtrar registros donde la fecha (truncada a día) sea igual a hoy
        return self.queryset.annotate(
            fecha_dia=TruncDate('fecha', output_field=DateField())
        ).filter(fecha_dia=hoy).order_by('-fecha')
    
    def list(self, request, *args, **kwargs):
        # Verificar permisos como en la vista original
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones situados hoy",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        
        return super().list(request, *args, **kwargs)
    

 #***********************************************************************************************************************   
    
class PendienteArrastreViewset(viewsets.ModelViewSet):
    queryset = arrastres.objects.all().prefetch_related('vagones')
    a=arrastres.objects.create
    serializer_class = PendienteArrastreSerializer
    permission_classes = [IsUFCPermission] 
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_pendiente = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertado formulario en Pendiente Arrastre: {objeto_pendiente.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_pendiente = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar formulario Pendiente Arrastre: {objeto_pendiente.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        id_objeto_pediente = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar formulario Pendiente Arrastre {id_objeto_pediente}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de Rotacion de Vagones",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
    
class PendienteArrastre_hoy_Viewset(viewsets.ModelViewSet):
    queryset = arrastres.objects.all()
    serializer_class = PendienteArrastreSerializer
    
    def get_queryset(self):
        # Obtener la fecha actual (sin la hora)
        hoy = timezone.now().date()
        
        # Filtrar registros donde la fecha (truncada a día) sea igual a hoy
        return self.queryset.annotate(
            fecha_dia=TruncDate('fecha', output_field=DateField())
        ).filter(fecha_dia=hoy).order_by('-fecha')
    
    def list(self, request, *args, **kwargs):
        # Verificar permisos como en la vista original
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones pendientes de arrastre hoy",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        
        return super().list(request, *args, **kwargs)
    
    
    
    
    
#*************Registro de vagones Dia*******************
class VagonesDiasViewSet(viewsets.ModelViewSet):
    queryset=vagones_dias.objects.all()
    serializer_class=vagones_dias_serializer    
    
    
#*************Empieza View Rotacion de Vagones **********************
class RotacionVagonesViewSet(viewsets.ModelViewSet):
    """
    Vista para gestionar registros de rotación de vagones.
    Permite listar, crear, actualizar y eliminar registros.
    """
    queryset = rotacion_vagones.objects.all()
    serializer_class = RotacionVagonesSerializer
    permission_classes = [IsUFCPermission] 

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto_rotacion = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertado formulario en Rotacion de vagones: {objeto_rotacion.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto_rotacion = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar formulario Rotacion de vagones: {objeto_rotacion.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        id_objeto_rotacion = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar formulario Rotacion de vagones {id_objeto_rotacion}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists() and not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de Rotacion de Vagones",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
    
""" class RotacionVagones_hoy_ViewSet(viewsets.ModelViewSet):
    queryset = rotacion_vagones.objects.all()
    serializer_class = RotacionVagonesSerializer
    
    def get_queryset(self):
        # Obtener la fecha actual (sin la hora)
        hoy = timezone.now().date()
        
        # Filtrar registros donde la fecha (truncada a día) sea igual a hoy
        return self.queryset.annotate(
            fecha_dia=TruncDate('creado_el', output_field=DateField())
        ).filter(fecha_dia=hoy).order_by('-creado_el')
    
    def list(self, request, *args, **kwargs):
        # Verificar permisos como en la vista original
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones en rotación hoy",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        
        return super().list(request, *args, **kwargs) """


#*************Termina View Rotacion de Vagones **********************



class VagonesAsociadosViewSet(viewsets.ModelViewSet):
    queryset = vagones_por_situar_situados_pendientes.objects.all()
    serializer_class = VagonesAsociadosSerializer
    permission_classes = [IsUFCPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrar por tipo de relación si se especifica
        relacion = self.request.query_params.get('relacion')
        relacion_id = self.request.query_params.get('relacion_id')
        
        if relacion and relacion_id:
            if relacion == 'por_situar':
                queryset = queryset.filter(por_situar_registros__id=relacion_id)
            elif relacion == 'arrastre':
                queryset = queryset.filter(arrastre_registros__id=relacion_id)
            elif relacion == 'situado':
                queryset = queryset.filter(situado_registros__id=relacion_id)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vagon_asociado = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertado vagon asociado: {vagon_asociado.id}",
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        vagon_asociado = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificado vagon asociado: {vagon_asociado.id}",
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        id_vagon = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminado vagon asociado {id_vagon}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorUFC').exists() and not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de vagones asociados",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
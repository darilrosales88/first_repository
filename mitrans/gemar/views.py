#4. Creacion de las vistas

#4.1 una variante para trabajar con los serializadores  es la propiedad viewsets
# de rest_framework, facilita el CRUD
from rest_framework import viewsets

#importacion de modelos
from .models import gemar_hecho_extraordinario,gemar_parte_hecho_extraordinario,gemar_programacion_maniobras

#importacion de serializadores asociados a los modelos
from .serializers import (gemar_hecho_extraordinario_serializer,gemar_parte_hecho_extraordinario_serializer,
                          gemar_programacion_maniobras,gemar_programacion_maniobras_serializer)

from Administracion.serializers import UserPermissionSerializer

from Administracion.models import Auditoria
from Administracion.serializers import AuditoriaSerializer, auditoria_filter

#importacion de verificacion de autenticacion, trabajo con grupos y asignacion de
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import Permission
#para la gestion de usuarios
from Administracion.models import CustomUser  # Importa tu modelo personalizado
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Administracion.serializers import GroupSerializer

#Para la gestion de los grupos a los que perteneceran los usuarios
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated  # Importa IsAuthenticated

from ufc.models import registro_vagones_cargados  # Importar el modelo de la app ufc

#para el filtrado
from django_filters.rest_framework import DjangoFilterBackend

#para usar el or
from django.db.models import Q


from django.utils import timezone

#para hacer la paginacion
#Para la paginacion
from rest_framework.pagination import PageNumberPagination

#Para el tratado de los permisos en el backend
from .permissions import IsAdminGemarPermission,IsVisualizadorGemarPermission

from datetime import datetime

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

class gemar_parte_hecho_extraordinario_view_set(viewsets.ModelViewSet):
    queryset = gemar_parte_hecho_extraordinario.objects.all().order_by('-id')
    serializer_class = gemar_parte_hecho_extraordinario_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nombre de informado_garante, se le pasa como parametro el campo por el que se va a filtrar
        search = self.request.query_params.get('fecha_entidad', None)

        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(entidad__icontains=search) | queryset.filter(fecha__operacion_icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre (que a su vez llama a perform_create)
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        parte_hecho_extraordinario = gemar_parte_hecho_extraordinario.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar parte de hecho extraordinario: {parte_hecho_extraordinario.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response
    
    def perform_create(self, serializer):
        user = self.request.user
        print(f"[VIEW] Usuario autenticado: {user.username}")
        
        # Obtener la entidad del usuario si existe
        entidad = user.entidad if hasattr(user, 'entidad') else None
        
        # Obtener la provincia de la entidad si existe
        provincia = entidad.provincia if entidad and hasattr(entidad, 'provincia') else None
        
        # Asignar valores al serializer
        instance = serializer.save(
            creado_por=user,
            entidad=entidad,
            provincia=provincia,
            estado_parte='Creado'
        )
    #Funcion para la actualizacion del estado del parte de HE
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Solo permitir actualizar el estado_parte
        if 'estado_parte' not in request.data:
            return Response(
                {"detail": "Se requiere el campo 'estado_parte'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Preparar datos para la actualización
        update_data = {'estado_parte': request.data['estado_parte']}
        
        # Si el nuevo estado es "Aprobado", asignar el usuario actual a aprobado_por
        if request.data['estado_parte'] == 'Aprobado':
            update_data['aprobado_por'] = request.user.id
        
        serializer = self.get_serializer(
            instance, 
            data=update_data, 
            partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Auditoría centralizada
        registrar_auditoria(request, f"Actualizar estado del parte de HE a {serializer.data['estado_parte']}")

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        parte_hecho_extraordinario = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, f"Modificar parte de hecho extraordinario: {parte_hecho_extraordinario.id}")

        #navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        #direccion_ip = request.META.get('REMOTE_ADDR')
        #Auditoria.objects.create(
            #usuario=request.user if request.user.is_authenticated else None,
            #accion=f"Modificar parte de hecho extraordinario: {parte_hecho_extraordinario.id}",
            #direccion_ip=direccion_ip,
            #navegador=navegador,
        #)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        id_hecho = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        registrar_auditoria(request, f"Eliminar parte de hecho extraordinario: {id_hecho}")

        #navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        #direccion_ip = request.META.get('REMOTE_ADDR')
        #Auditoria.objects.create(
        #    usuario=request.user if request.user.is_authenticated else None,
        #    accion=f"Eliminar parte de hecho extraordinario: {id_hecho}",
        #    direccion_ip=direccion_ip,
        #    navegador=navegador,
        #)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorGEMAR').exists() and not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de partes de hechos extraordinarios.")

        #navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        #direccion_ip = request.META.get('REMOTE_ADDR')
        #Auditoria.objects.create(
        #    usuario=request.user if request.user.is_authenticated else None,
        #    accion="Visualizar lista de partes de hechos extraordinarios.",
        #    direccion_ip=direccion_ip,
        #    navegador=navegador,
        #)

        return super().list(request, *args, **kwargs)
    
#/*****************************************************************************************************************************/
class gemar_hecho_extraordinario_view_set(viewsets.ModelViewSet):
    queryset = gemar_hecho_extraordinario.objects.all().order_by('-id')
    serializer_class = gemar_hecho_extraordinario_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nombre de informado_garante, se le pasa como parametro el campo por el que se va a filtrar
        search = self.request.query_params.get('informado_garante', None)

        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(informado__icontains=search) | queryset.filter(garante__icontains=search)

        return queryset
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hecho_extraordinario = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, f"Insertar hecho extraordinario: {hecho_extraordinario.id}")
        
        #navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        #direccion_ip = request.META.get('REMOTE_ADDR')
        #Auditoria.objects.create(
        #    usuario=request.user if request.user.is_authenticated else None,
         #   accion=f"Insertar hecho extraordinario: {hecho_extraordinario.id}",
        #    direccion_ip=direccion_ip,
        #    navegador=navegador,
        #)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        hecho_extraordinario = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, f"Modificar hecho extraordinario: {hecho_extraordinario.id}")

        #navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        #direccion_ip = request.META.get('REMOTE_ADDR')
        #Auditoria.objects.create(
        #    usuario=request.user if request.user.is_authenticated else None,
        #    accion=f"Modificar hecho extraordinario: {hecho_extraordinario.id}",
        #    direccion_ip=direccion_ip,
        #    navegador=navegador,
        #)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        id_hecho = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        registrar_auditoria(request, f"Eliminar hecho extraordinario: {id_hecho}")
        
        #navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        #direccion_ip = request.META.get('REMOTE_ADDR')
        #Auditoria.objects.create(
        #    usuario=request.user if request.user.is_authenticated else None,
        #    accion=f"Eliminar hecho extraordinario: {id_hecho}",
        #    direccion_ip=direccion_ip,
        #    navegador=navegador,
        #)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorGEMAR').exists() and not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de hechos extraordinarios.")
        
        #navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        #direccion_ip = request.META.get('REMOTE_ADDR')
        #Auditoria.objects.create(
        #    usuario=request.user if request.user.is_authenticated else None,
        #    accion="Visualizar lista de hechos extraordinarios.",
        #    direccion_ip=direccion_ip,
        #    navegador=navegador,
        #)

        return super().list(request, *args, **kwargs)
    

    #Muestra los hechos extraordinarios asociados al usuario autenticado(quien crea el parte)
    #La URL generada automáticamente por el decorador @action será: /gemar-hechos-extraordinarios/mis_hechos_extraordinarios/
    @action(detail=False, methods=['get'])
    def mis_hechos_extraordinarios(self, request):
        """
        Endpoint para obtener los hechos extraordinarios creados por el usuario autenticado
        que coincidan con la fecha de operación del parte existente.
        """
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=401)

        # Obtener la fecha actual (puede recibirse como parámetro también)
        fecha_operacion = request.query_params.get('fecha_operacion', None)
        
        try:
            if fecha_operacion:
                fecha_obj = datetime.strptime(fecha_operacion, '%Y-%m-%d').date()
            else:
                fecha_obj = timezone.now().date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)

        # Verificar si existe un parte para el usuario en la fecha especificada
        parte_existente = gemar_parte_hecho_extraordinario.objects.filter(
            creado_por=request.user,
            fecha_operacion__date=fecha_obj
        ).first()

        if not parte_existente:
            return Response({
                "existe_parte": False,
                "detalle": f"No existe un parte creado por el usuario para la fecha {fecha_obj}",
                "hechos": []
            }, status=200)

        # Obtener los hechos extraordinarios asociados al parte
        hechos = gemar_hecho_extraordinario.objects.filter(
            parte_hecho_extraordinario=parte_existente
        ).order_by('-fecha_operacion')

        # Serializar los resultados
        serializer = self.get_serializer(hechos, many=True)
        
        # Registrar la acción en auditoría
        registrar_auditoria(request, f"Visualizar hechos extraordinarios para parte del {fecha_obj}")
        
        #navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        #direccion_ip = request.META.get('REMOTE_ADDR')
        #Auditoria.objects.create(
        #    usuario=request.user,
        #    accion=f"Visualizar hechos extraordinarios para parte del {fecha_obj}",
        #    direccion_ip=direccion_ip,
        #    navegador=navegador,
        #)

        return Response({
            "existe_parte": True,
            "parte_id": parte_existente.id,
            "fecha_operacion": fecha_obj,
            "hechos": serializer.data
        })

        return Response(serializer.data)
    
 #/***********************************************************************************************************************  
  
#Verificando que exista el informe de HE creado antes de insertar
@api_view(['GET'])
def verificar_informe_he_existente(request):
    try:
        fecha_actual = request.query_params.get('fecha_actual')
        if not fecha_actual:
            return Response({"error": "Parámetro fecha_actual requerido"}, status=400)
        
        fecha_obj = datetime.strptime(fecha_actual, '%Y-%m-%d').date()
        user = request.user
        
        # Verificar que el usuario esté autenticado y tenga entidad asociada
        if not user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=401)
        
        if not hasattr(user, 'entidad') or not user.entidad:
            return Response({"error": "El usuario no tiene entidad asociada"}, status=400)
        
        # Construir el filtro con todos los criterios
        filtro = Q(fecha_actual__date=fecha_obj)

        # Filtrar por entidad del usuario
        filtro &= Q(entidad=user.entidad)
        
        # Si el usuario tiene provincia asociada, filtrar también por provincia
        if hasattr(user.entidad, 'provincia') and user.entidad.provincia:
            filtro &= Q(provincia=user.entidad.provincia)
            print("Aqui es donde mostrara lo que tiene el filtro ",filtro )
        
        # También podemos filtrar por creado_por si es relevante
            filtro &= Q(creado_por=user)
        
        existe = gemar_parte_hecho_extraordinario.objects.filter(filtro).exists()
        
        if existe:
            informe = gemar_parte_hecho_extraordinario.objects.filter(filtro).first()
            return Response({
                "existe": True,
                "id": informe.id,
                "fecha_actual": informe.fecha_actual,
                "estado": informe.estado_parte,
                "entidad": informe.entidad.id if informe.entidad else None,
                "provincia": informe.provincia.id if informe.provincia else None,
                "creado_por_id": informe.creado_por.id if informe.creado_por else None,
                "creado_por_nombre_usuario": informe.creado_por.username if informe.creado_por else None
            })     
        return Response({
            "existe": False,
            "detalle": f"No existe parte para la fecha {fecha_actual}, entidad {user.entidad} y provincia {getattr(user.entidad, 'provincia', None)}"
        })
        
    except ValueError:
        return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
#/*************************************************************************************************************************
class gemar_programacion_maniobras_view_set(viewsets.ModelViewSet):
    queryset = gemar_programacion_maniobras.objects.all().order_by('-id')
    serializer_class = gemar_programacion_maniobras_serializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('buque_puerto', None)

        if search is not None:
            queryset = queryset.filter(buque__icontains=search) | queryset.filter(puerto__nombre__icontains=search)

        return queryset
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        response = super().create(request, *args, **kwargs)
        parte_programacion = gemar_programacion_maniobras.objects.get(id=response.data['id'])
        
        registrar_auditoria(request, f"Insertar programación de maniobras: {parte_programacion.id}")
        return response
    
    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        response = super().update(request, *args, **kwargs)
        parte_programacion = self.get_object()
        
        registrar_auditoria(request, f"Modificar programación de maniobras: {parte_programacion.id}")
        return response

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        parte_programacion = self.get_object()
        id_parte = parte_programacion.id
        
        registrar_auditoria(request, f"Eliminar programación de maniobras: {id_parte}")
        
        self.perform_destroy(parte_programacion)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorGEMAR').exists() and not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        registrar_auditoria(request, "Visualizar lista de programación de maniobras.")
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def programacion_por_fecha(self, request):
        """
        Endpoint para obtener la programación de maniobras por fecha
        """
        fecha_str = request.query_params.get('fecha', None)
        
        try:
            if fecha_str:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            else:
                fecha = timezone.now().date()
                
            queryset = self.get_queryset().filter(
                Q(fecha_eta=fecha) | Q(fecha_ets=fecha)
            ).order_by('hora_eta', 'hora_ets')
            
            serializer = self.get_serializer(queryset, many=True)
            
            registrar_auditoria(request, f"Visualizar programación de maniobras para fecha {fecha}")
            
            return Response({
                "fecha": fecha,
                "resultados": serializer.data
            })
            
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)

#4. Creacion de las vistas
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from gemar.models import PartePBIP, CargaVieja, ExistenciaMercancia
from gemar.Administracion.permissions import IsGEMARUser, IsAdminUser

#4.1 una variante para trabajar con los serializadores  es la propiedad viewsets
# de rest_framework, facilita el CRUD
from rest_framework import viewsets
from rest_framework import serializers
from .models import ParteCombinado
#importacion de modelos
from .models import (gemar_hecho_extraordinario,gemar_parte_hecho_extraordinario,
                     gemar_programacion_maniobras,gemar_parte_programacion_maniobras,ParteCombinado) 

#importacion de serializadores asociados a los modelos
from .serializers import (ParteCombinadoSerializer, gemar_hecho_extraordinario_serializer,gemar_parte_hecho_extraordinario_serializer,
                          gemar_programacion_maniobras,gemar_programacion_maniobras_serializer,
                          gemar_parte_programacion_maniobras_serializer, PartePBIPSerializer, CargaViejaSerializer, 
                          ExistenciaMercanciaSerializer)


from Administracion.models import Auditoria

#importacion de verificacion de autenticacion, trabajo con grupos y asignacion de
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import action
#para la gestion de usuarios
from Administracion.models import CustomUser  # Importa tu modelo personalizado
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status

#para usar el or
from django.db.models import Q

from django.utils import timezone
from datetime import datetime, date, time

#Para la paginacion
from rest_framework.pagination import PageNumberPagination

#Para el tratado de los permisos en el backend
from .permissions import IsAdminGemarPermission,IsVisualizadorGemarPermission

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
        
        # Obtener el organismo de la entidad si existe
        organismo = entidad.osde_oace_organismo if entidad and hasattr(entidad, 'osde_oace_organismo') else None
        
        # Asignar valores al serializer
        instance = serializer.save(
            creado_por=user,
            entidad=entidad,
            provincia=provincia,
            organismo=organismo,  # Añadir esta línea
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

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        id_hecho = instance.id

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
class gemar_parte_programacion_maniobras_view_set(viewsets.ModelViewSet):
    queryset = gemar_parte_programacion_maniobras.objects.all().order_by('-id')
    serializer_class = gemar_parte_programacion_maniobras_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por fecha actual y entidad, se le pasa como parametro el campo por el que se va a filtrar
        search = self.request.query_params.get('fecha_entidad', None)

        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(fecha_actual__icontains=search) | queryset.filter(entidad_icontains=search)

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
        parte_programacion_maniobra = gemar_parte_programacion_maniobras.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar parte de programación de maniobras: {parte_programacion_maniobra.id}",
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
        
        # Obtener el organismo de la entidad si existe
        organismo = entidad.osde_oace_organismo if entidad and hasattr(entidad, 'osde_oace_organismo') else None
        
        # Asignar valores al serializer
        instance = serializer.save(
            creado_por=user,
            entidad=entidad,
            provincia=provincia,
            organismo=organismo,  # Añadir esta línea
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
        registrar_auditoria(request, f"Actualizar estado del parte de programación de maniobras {serializer.data['estado_parte']}")

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

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        id_hecho = instance.id

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorGEMAR').exists() and not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de partes de programación de maniobras.")

      

        return super().list(request, *args, **kwargs)
#**************************************************************************************************************************
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
    
    @action(detail=False, methods=['get'])
    def mis_programaciones_maniobras(self, request):
        """
        Endpoint para obtener las programaciones de maniobras creadas por el usuario autenticado
        que coincidan con la fecha de operación del parte existente.
        """
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=401)

        # Obtener la fecha actual (puede recibirse como parámetro también)
        fecha_actual = request.query_params.get('fecha_actual', None)
        
        try:
            if fecha_actual:
                fecha_obj = datetime.strptime(fecha_actual, '%Y-%m-%d').date()
            else:
                fecha_obj = timezone.now().date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)

        # Verificar si existe un parte para el usuario en la fecha especificada
        parte_existente = gemar_parte_programacion_maniobras.objects.filter(
            creado_por=request.user,
            fecha_actual__date=fecha_obj
        ).first()

        if not parte_existente:
            return Response({
                "existe_parte": False,
                "detalle": f"No existe un parte creado por el usuario para la fecha {fecha_obj}",
                "programaciones": []
            }, status=200)

        # Obtener las programaciones de maniobras asociadas al parte
        programaciones = gemar_programacion_maniobras.objects.filter(
            parte_programacion_maniobra=parte_existente
        ).order_by('-id')

        # Serializar los resultados
        serializer = self.get_serializer(programaciones, many=True)
        
        # Registrar la acción en auditoría
        registrar_auditoria(request, f"Visualizar programaciones de maniobras para parte de fecha {fecha_obj}")        

        return Response({
            "existe_parte": True,
            "parte_id": parte_existente.id,
            "fecha_actual": fecha_obj,
            "programaciones": serializer.data
        })
        
@api_view(['GET'])
def verificar_parte_programacion_maniobra_existente(request):
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
        
        # También podemos filtrar por creado_por si es relevante
            filtro &= Q(creado_por=user)
        
        existe = gemar_parte_programacion_maniobras.objects.filter(filtro).exists()        
        if existe:
            informe = gemar_parte_programacion_maniobras.objects.filter(filtro).first()
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
#**********************************************************************************************************************


#Lo que hizo Raider
class PartePBIPViewSet(viewsets.ModelViewSet):
    queryset = PartePBIP.objects.all().order_by('-fecha_creacion')
    serializer_class = PartePBIPSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsGEMARUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['buque', 'puerto', 'nivel', 'fecha_operacion', 'estado']
    search_fields = ['buque__nombre_embarcacion', 'puerto__nombre_puerto']
    ordering_fields = ['fecha_operacion', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrado por fecha si se proporciona
        fecha = self.request.query_params.get('fecha')
        
        if fecha:
            queryset = queryset.filter(fecha_operacion=fecha)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre (que a su vez llama a perform_create)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creado_por=request.user)
        headers = self.get_success_headers(serializer.data)
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar parte PBIP: {serializer.data['id']}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        user = self.request.user
        print(f"[VIEW] Usuario autenticado: {user.username}")
        
        # Asignar valores al serializer
        instance = serializer.save(
            creado_por=user,
            estado='CREADO'
        )

    #Funcion para la actualizacion del estado del parte de PBIP
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Solo permitir actualizar el estado
        if 'estado' not in request.data:
            return Response(
                {"detail": "Se requiere el campo 'estado'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Preparar datos para la actualización
        update_data = {'estado': request.data['estado']}
        
        # Si el nuevo estado es "APROBADO", asignar el usuario actual a aprobado_por
        if request.data['estado'] == 'APROBADO':
            update_data['aprobado_por'] = request.user.id
        
        serializer = self.get_serializer(
            instance, 
            data=update_data, 
            partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Auditoría centralizada
        registrar_auditoria(request, f"Actualizar estado del parte PBIP {serializer.data['estado']}")

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
        parte_pbip = serializer.save()

        # Registrar auditoría
        registrar_auditoria(request, f"Modificar parte PBIP: {parte_pbip.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        instance = self.get_object()
        id_parte = instance.id

        # Registrar auditoría antes de eliminar
        registrar_auditoria(request, f"Eliminar parte PBIP: {id_parte}")
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorGEMAR').exists() and not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de partes PBIP.")

        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def aprobar(self, request, pk=None):
        parte = self.get_object()
        parte.estado = 'APROBADO'
        parte.aprobado_por = request.user
        parte.save()
        
        # Registrar auditoría
        registrar_auditoria(request, f"Aprobar parte PBIP: {parte.id}")
        
        return Response({'status': 'Parte PBIP aprobado'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def listo(self, request, pk=None):
        parte = self.get_object()
        parte.estado = 'LISTO'
        parte.save()
        
        # Registrar auditoría
        registrar_auditoria(request, f"Marcar parte PBIP como listo: {parte.id}")
        
        return Response({'status': 'Parte PBIP marcado como listo'}, status=status.HTTP_200_OK)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def rechazar(self, request, pk=None):
        parte = self.get_object()
        parte.estado = 'RECHAZADO'
        parte.save()
        
        # Registrar auditoría
        registrar_auditoria(request, f"Rechazar parte PBIP: {parte.id}")
        
        return Response({'status': 'Parte PBIP rechazado'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def cancelar(self, request, pk=None):
        parte = self.get_object()
        parte.estado = 'CANCELADO'
        parte.save()
        
        # Registrar auditoría
        registrar_auditoria(request, f"Cancelar parte PBIP: {parte.id}")
        
        return Response({'status': 'Parte PBIP cancelado'}, status=status.HTTP_200_OK)

class CargaViejaViewSet(viewsets.ModelViewSet):
    queryset = CargaVieja.objects.all()
    serializer_class = CargaViejaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsGEMARUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parte', 'puerto', 'terminal', 'producto', 'organismo']
    search_fields = ['producto__nombre', 'manifiesto', 'organismo__nombre', 'puerto__nombre', 'terminal__nombre']
    ordering_fields = ['parte__fecha_operacion']
    ordering = ['-parte__fecha_operacion']

    def get_queryset(self):
        queryset = super().get_queryset()
        parte_id = self.request.query_params.get('parte_id')
        if parte_id:
            queryset = queryset.filter(parte_id=parte_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def aprobar(self, request, pk=None):
        carga = self.get_object()
        carga.estado = 'APROBADO'
        carga.aprobado_por = request.user
        carga.save()
        return Response({'status': 'Carga aprobada'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def rechazar(self, request, pk=None):
        carga = self.get_object()
        carga.estado = 'RECHAZADO'
        carga.save()
        return Response({'status': 'Carga rechazada'}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser | IsGEMARUser]
        return super().get_permissions()

class ExistenciaMercanciaViewSet(viewsets.ModelViewSet):
    queryset = ExistenciaMercancia.objects.all().order_by('-fecha_creacion')
    serializer_class = ExistenciaMercanciaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsGEMARUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['terminal', 'tipo', 'tipo_producto', 'producto', 'estado']
    search_fields = ['producto__nombre', 'terminal__nombre']
    ordering_fields = ['fecha_operacion', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrado por fecha si se proporciona
        fecha = self.request.query_params.get('fecha')
        
        if fecha:
            queryset = queryset.filter(fecha_operacion=fecha)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre (que a su vez llama a perform_create)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creado_por=request.user)
        headers = self.get_success_headers(serializer.data)
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar existencia mercancía: {serializer.data['id']}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        user = self.request.user
        print(f"[VIEW] Usuario autenticado: {user.username}")
        
        # Asignar valores al serializer
        instance = serializer.save(
            creado_por=user,
            estado='Creado'  # ✅ Cambiado a 'Creado' (formato título)
        )

    # Función para la actualización del estado del registro de existencia
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Solo permitir actualizar el estado
        if 'estado' not in request.data:
            return Response(
                {"detail": "Se requiere el campo 'estado'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Preparar datos para la actualización
        update_data = {'estado': request.data['estado']}
        
        # Si el nuevo estado es "Aprobado", asignar el usuario actual a aprobado_por
        if request.data['estado'] == 'Aprobado':  # ✅ Cambiado a 'Aprobado' (formato título)
            update_data['aprobado_por'] = request.user.id
        
        serializer = self.get_serializer(
            instance, 
            data=update_data, 
            partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Auditoría centralizada
        registrar_auditoria(request, f"Actualizar estado de existencia mercancía {serializer.data['estado']}")

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
        existencia = serializer.save()

        # Registrar auditoría
        registrar_auditoria(request, f"Modificar existencia mercancía: {existencia.id}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        instance = self.get_object()
        id_existencia = instance.id

        # Registrar auditoría antes de eliminar
        registrar_auditoria(request, f"Eliminar existencia mercancía: {id_existencia}")
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorGEMAR').exists() and not request.user.groups.filter(name='AdminGEMAR').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Registrar la acción en el modelo de Auditoria
        registrar_auditoria(request, "Visualizar lista de existencias de mercancía.")

        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def aprobar(self, request, pk=None):
        existencia = self.get_object()
        existencia.estado = 'Aprobado'  # ✅ Cambiado a 'Aprobado' (formato título)
        existencia.aprobado_por = request.user
        existencia.save()
        
        # Registrar auditoría
        registrar_auditoria(request, f"Aprobar existencia mercancía: {existencia.id}")
        
        return Response({'status': 'Existencia de mercancía aprobada'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def listo(self, request, pk=None):
        existencia = self.get_object()
        existencia.estado = 'Listo'  # ✅ Cambiado a 'Listo' (formato título)
        existencia.save()
        
        # Registrar auditoría
        registrar_auditoria(request, f"Marcar existencia mercancía como lista: {existencia.id}")
        
        return Response({'status': 'Existencia de mercancía marcada como lista'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def rechazar(self, request, pk=None):
        existencia = self.get_object()
        existencia.estado = 'Rechazado'  # ✅ Cambiado a 'Rechazado' (formato título)
        existencia.save()
        
        # Registrar auditoría
        registrar_auditoria(request, f"Rechazar existencia mercancía: {existencia.id}")
        
        return Response({'status': 'Existencia de mercancía rechazada'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def cancelar(self, request, pk=None):
        existencia = self.get_object()
        existencia.estado = 'Cancelado'  # ✅ Cambiado a 'Cancelado' (formato título)
        existencia.save()
        
        # Registrar auditoría
        registrar_auditoria(request, f"Cancelar existencia mercancía: {existencia.id}")
        
        return Response({'status': 'Existencia de mercancía cancelada'}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

class ResumenDiarioView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        fecha = request.query_params.get('fecha')
        if not fecha:
            return Response(
                {'error': 'El parámetro fecha es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener todos los partes del día
        partes_pbip = PartePBIP.objects.filter(fecha_operacion=fecha)
        cargas_viejas = CargaVieja.objects.filter(parte__fecha_operacion=fecha)
        existencias = ExistenciaMercancia.objects.filter(fecha_operacion=fecha)
        
        resumen = {
            'total_partes_pbip': partes_pbip.count(),
            'total_cargas_viejas': cargas_viejas.count(),
            'total_existencias_mercancia': existencias.count(),
            'partes_pbip': PartePBIPSerializer(partes_pbip, many=True).data,
            'cargas_viejas': CargaViejaSerializer(cargas_viejas, many=True).data,
            'existencias_mercancia': ExistenciaMercanciaSerializer(existencias, many=True).data
        }
        
        return Response(resumen)


# LISTA DE TODOS LOS PARTES (HE, PROGRAMACION DE MANIOBRAS, PBIP Y EXISTENCIAS MERCANCIA)
@api_view(['GET'])
def listar_partes_combinados(request):
    """
    Endpoint para listar todos los partes (hechos extraordinarios, programación de maniobras, PBIP y existencias de mercancía)
    ordenados por fecha_actual/fecha_operacion descendente (incluyendo hora).
    """
    try:
        # Obtener parámetros opcionales de filtrado
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)
        estado = request.query_params.get('estado', None)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        # Validar permisos
        if not request.user.groups.filter(name__in=['VisualizadorGEMAR', 'AdminGEMAR']).exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener partes de hechos extraordinarios CON TODAS LAS RELACIONES
        hechos_extraordinarios = gemar_parte_hecho_extraordinario.objects.all().select_related(
            'creado_por', 'aprobado_por', 'entidad', 'organismo', 'provincia'
        )
        
        # Obtener partes de programación de maniobras CON TODAS LAS RELACIONES
        programacion_maniobras = gemar_parte_programacion_maniobras.objects.all().select_related(
            'creado_por', 'aprobado_por', 'entidad', 'organismo', 'provincia'
        )
        
        # Obtener partes PBIP CON TODAS LAS RELACIONES
        partes_pbip = PartePBIP.objects.all().select_related(
            'creado_por', 'aprobado_por', 'buque', 'puerto'
        )
        
        # Obtener existencias de mercancía CON TODAS LAS RELACIONES
        existencias_mercancia = ExistenciaMercancia.objects.all().select_related(
            'creado_por', 'aprobado_por', 'terminal', 'producto', 'unidad_medida'
        )
        
        # Aplicar filtros si existen
        if fecha_inicio:
            try:
                fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                hechos_extraordinarios = hechos_extraordinarios.filter(fecha_actual__date__gte=fecha_inicio_obj)
                programacion_maniobras = programacion_maniobras.filter(fecha_actual__date__gte=fecha_inicio_obj)
                partes_pbip = partes_pbip.filter(fecha_operacion__gte=fecha_inicio_obj)
                existencias_mercancia = existencias_mercancia.filter(fecha_operacion__gte=fecha_inicio_obj)
            except ValueError:
                return Response({"error": "Formato de fecha_inicio inválido. Use YYYY-MM-DD"}, status=400)
        
        if fecha_fin:
            try:
                fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                hechos_extraordinarios = hechos_extraordinarios.filter(fecha_actual__date__lte=fecha_fin_obj)
                programacion_maniobras = programacion_maniobras.filter(fecha_actual__date__lte=fecha_fin_obj)
                partes_pbip = partes_pbip.filter(fecha_operacion__lte=fecha_fin_obj)
                existencias_mercancia = existencias_mercancia.filter(fecha_operacion__lte=fecha_fin_obj)
            except ValueError:
                return Response({"error": "Formato de fecha_fin inválido. Use YYYY-MM-DD"}, status=400)
        
        if estado:
                estado_lower = estado.lower()
    
    # Para Hecho Extraordinario y Programación Maniobras (primera mayúscula)
                estado_title = estado_lower.title()  # "creado" -> "Creado"
    
    # Para PBIP y Existencia Mercancía (todo mayúscula)
                estado_upper = estado_lower.upper()  # "creado" -> "CREADO"
    
                hechos_extraordinarios = hechos_extraordinarios.filter(estado_parte=estado_title)
                programacion_maniobras = programacion_maniobras.filter(estado_parte=estado_title)
                partes_pbip = partes_pbip.filter(estado=estado_upper)
                existencias_mercancia = existencias_mercancia.filter(estado=estado_upper)
        
        # Serializar los datos - USAR LOS SERIALIZERS CORRECTOS
        hechos_serializer = gemar_parte_hecho_extraordinario_serializer(hechos_extraordinarios, many=True)
        programacion_serializer = gemar_parte_programacion_maniobras_serializer(programacion_maniobras, many=True)
        pbip_serializer = PartePBIPSerializer(partes_pbip, many=True)
        existencias_serializer = ExistenciaMercanciaSerializer(existencias_mercancia, many=True)
        
        # Combinar los resultados
        combined_data = []
        for hecho in hechos_extraordinarios:
            combined_data.append({
        'id': hecho.id,
        'tipo_parte': 'HECHO_EXTRAORDINARIO',
        # ... otros campos ...
        'detalle_url': f'/gemar/hechos-extraordinarios/{hecho.id}/detalle'
    })

        for programacion in programacion_maniobras:
            combined_data.append({
        'id': programacion.id,
        'tipo_parte': 'PROGRAMACION_MANIOBRAS',
        # ... otros campos ...
        'detalle_url': f'/gemar/programacion-maniobras/{programacion.id}/detalle'
    })

        for parte in partes_pbip:
            combined_data.append({
            'id': parte.id,
            'tipo_parte': 'PBIP',
            # ... otros campos ...
            'detalle_url': f'/gemar/partes-pbip/{parte.id}/detalle'
        })

        for existencia in existencias_mercancia:
            combined_data.append({
            'id': existencia.id,
            'tipo_parte': 'EXISTENCIA_MERCANCIA',
            # ... otros campos ...
            'detalle_url': f'/gemar/existencias-mercancia/{existencia.id}/detalle'
        })
        # Transformar datos de hechos extraordinarios (VERSIÓN CORREGIDA)
        for hecho in hechos_extraordinarios:
            combined_data.append({
                'id': hecho.id,
                'tipo_parte': 'HECHO_EXTRAORDINARIO',
                'fecha_actual': hecho.fecha_actual,
                'estado_parte': hecho.estado_parte,
                'creado_por_name': hecho.creado_por.username if hecho.creado_por else 'N/A',
                'aprobado_por_name': hecho.aprobado_por.username if hecho.aprobado_por else '-',
                'entidad_name': hecho.entidad.nombre if hecho.entidad else 'N/A',
                'organismo_name': hecho.organismo.nombre if hecho.organismo else 'N/A',
                'provincia_name': hecho.provincia.nombre_provincia if hecho.provincia else 'N/A',
                #'detalles': {
                    #'descripcion': hecho.descripcion_hecho or 'Hecho Extraordinario',
                    #'tipo_hecho': hecho.tipo_hecho or ''
                #}
            })
        
        # Transformar datos de programación de maniobras (VERSIÓN CORREGIDA)
        for programacion in programacion_maniobras:
            combined_data.append({
                'id': programacion.id,
                'tipo_parte': 'PROGRAMACION_MANIOBRAS',
                'fecha_actual': programacion.fecha_actual,
                'estado_parte': programacion.estado_parte,
                'creado_por_name': programacion.creado_por.username if programacion.creado_por else 'N/A',
                'aprobado_por_name': programacion.aprobado_por.username if programacion.aprobado_por else '-',
                'entidad_name': programacion.entidad.nombre if programacion.entidad else 'N/A',
                'organismo_name': programacion.organismo.nombre if programacion.organismo else 'N/A',
                'provincia_name': programacion.provincia.nombre_provincia if programacion.provincia else 'N/A',
                #'detalles': {
                    #'descripcion': programacion.descripcion_maniobras or 'Programación de Maniobras',
                    #'tipo_maniobras': programacion.tipo_maniobras or ''
                #}
            })
        
        # Transformar datos PBIP (VERSIÓN CORREGIDA)
        for parte in partes_pbip:
            combined_data.append({
                'id': parte.id,
                'tipo_parte': 'PBIP',
                'fecha_actual': parte.fecha_creacion,
                'estado_parte': parte.estado,
                'creado_por_name': parte.creado_por.username if parte.creado_por else 'N/A',
                'aprobado_por_name': parte.aprobado_por.username if parte.aprobado_por else '-',
                #'entidad_name': parte.buque.nombre_embarcacion if parte.buque else 'N/A',
                #'organismo_name': parte.puerto.nombre_puerto if parte.puerto else 'N/A',
                'provincia_name': programacion.provincia.nombre_provincia if programacion.provincia else 'N/A',
                'detalles': {
                    'nivel': parte.nivel or '',
                    'descripcion': 'Parte PBIP'
                }
            })
        
        # Transformar datos de existencias de mercancía (VERSIÓN CORREGIDA)
        for existencia in existencias_mercancia:
            combined_data.append({
                'id': existencia.id,
                'tipo_parte': 'EXISTENCIA_MERCANCIA',
                'fecha_actual': existencia.fecha_operacion,
                'estado_parte': existencia.estado_registro,
                'creado_por_name': existencia.creado_por.username if existencia.creado_por else 'N/A',
                'aprobado_por_name': existencia.aprobado_por.username if existencia.aprobado_por else '-',
                #'entidad_name': existencia.terminal.nombre_terminal if existencia.terminal else 'N/A',
                #'organismo_name': existencia.producto.t_producto if existencia.producto else 'N/A',
                'provincia_name': programacion.provincia.nombre_provincia if programacion.provincia else 'N/A',
                'detalles': {
                    'tipo': getattr(existencia, 'tipo_display', '') if hasattr(existencia, 'tipo_display') else '',
                    'tipo_producto': getattr(existencia, 'tipo_producto_display', '') if hasattr(existencia, 'tipo_producto_display') else '',
                    'existencia': existencia.existencia or '',
                    'unidad_medida': existencia.unidad_medida.unidad_medida if existencia.unidad_medida else '',
                    'descripcion': 'Existencia de Mercancía'
                }
            })
          # Función para normalizar fechas para ordenamiento
        def normalizar_fecha_para_ordenamiento(fecha):
            """
            Normaliza cualquier tipo de fecha (datetime, date) a datetime para ordenamiento consistente.
            Si es date, lo convierte a datetime a medianoche.
            """
            if fecha is None:
                return datetime.min
            elif isinstance(fecha, datetime):
                return fecha
            elif isinstance(fecha, date):
                return datetime.combine(fecha, time.min)
            else:
                return datetime.min
            
         # Ordenar por fecha_actual descendente (más reciente primero)
        combined_data_sorted = sorted(
            combined_data,
            key=lambda x: normalizar_fecha_para_ordenamiento(x.get('fecha_actual')),
            reverse=True
        )
        
        # Paginación manual
        start = (page - 1) * page_size
        end = start + page_size
        
        paginated_data = combined_data_sorted[start:end]
        
        # Registrar auditoría
        registrar_auditoria(request, "Visualización de lista combinada de partes (HE, Maniobras, PBIP y Existencias Mercancía)")
        
        return Response({
            "count": len(combined_data_sorted),
            "next": end < len(combined_data_sorted),
            "previous": page > 1,
            "page": page,
            "page_size": page_size,
            "results": paginated_data
        })
        
    except Exception as e:
        import traceback
        # Log del error para debugging
        print(f"Error en listar_partes_combinados: {str(e)}")
        print(traceback.format_exc())
        return Response({
            "error": "Error interno del servidor",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_parte_combinado(request, pk):
    """
    Obtiene el detalle de un parte combinado específico
    """
    try:
        # Buscar el parte combinado por ID
        parte = get_object_or_404(ParteCombinado, pk=pk)
        
        # Debug: imprimir información del parte
        print(f"Parte ID: {parte.id}, Tipo: {parte.tipo_parte}")
        print(f"Entidad: {parte.entidad}, Organismo: {parte.organismo}, Provincia: {parte.provincia}")
        
        # Serializar los datos
        serializer = ParteCombinadoSerializer(parte)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except ParteCombinado.DoesNotExist:
        return Response(
            {'error': 'Parte combinado no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Log detallado del error
        import traceback
        print(f"Error detallado: {str(e)}")
        print(traceback.format_exc())
        
        return Response(
            {'error': 'Error interno del servidor'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_estado_parte(request, pk):
    """
    Actualiza el estado de un parte combinado
    """
    try:
        parte = get_object_or_404(ParteCombinado, pk=pk)
        nuevo_estado = request.data.get('estado_parte')
        
        if not nuevo_estado:
            return Response(
                {'error': 'El campo estado_parte es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar que el estado sea uno de los permitidos
        estados_permitidos = ['creado', 'aprobado', 'rechazado', 'listo']
        if nuevo_estado.lower() not in estados_permitidos:
            return Response(
                {'error': f'Estado no válido. Los estados permitidos son: {estados_permitidos}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Actualizar el estado
        parte.estado_parte = nuevo_estado.lower()
        parte.save()
        
        # Serializar y retornar la respuesta
        serializer = ParteCombinadoSerializer(parte)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except ParteCombinado.DoesNotExist:
        return Response(
            {'error': 'Parte combinado no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_parte_combinado(request, pk):
    """
    Elimina un parte combinado
    """
    try:
        parte = get_object_or_404(ParteCombinado, pk=pk)
        
        # Verificar permisos adicionales si es necesario
        if parte.estado_parte != 'creado':
            return Response(
                {'error': 'Solo se pueden eliminar partes en estado "creado"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        parte.delete()
        return Response(
            {'message': 'Parte combinado eliminado correctamente'}, 
            status=status.HTTP_200_OK
        )
        
    except ParteCombinado.DoesNotExist:
        return Response(
            {'error': 'Parte combinado no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
# VISTAS ESPECÍFICAS PARA DETALLES DE CADA TIPO DE PARTE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_hecho_extraordinario(request, pk):
    """Detalle específico de un hecho extraordinario"""
    try:
        parte = get_object_or_404(gemar_parte_hecho_extraordinario, pk=pk)
        serializer = gemar_parte_hecho_extraordinario_serializer(parte)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_programacion_maniobras(request, pk):
    """Detalle específico de programación de maniobras"""
    try:
        parte = get_object_or_404(gemar_parte_programacion_maniobras, pk=pk)
        serializer = gemar_parte_programacion_maniobras_serializer(parte)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_pbip(request, pk):
    """Detalle específico de parte PBIP"""
    try:
        parte = get_object_or_404(PartePBIP, pk=pk)
        serializer = PartePBIPSerializer(parte)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_existencia_mercancia(request, pk):
    """Detalle específico de existencia de mercancía"""
    try:
        parte = get_object_or_404(ExistenciaMercancia, pk=pk)
        serializer = ExistenciaMercanciaSerializer(parte)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def actualizar_estado_existencia(request, pk):
    """
    Actualiza el estado de una existencia de mercancía
    """
    try:
        existencia = get_object_or_404(ExistenciaMercancia, pk=pk)
        nuevo_estado = request.data.get('estado_registro')
        
        if not nuevo_estado:
            return Response(
                {'error': 'El campo estado_registro es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar que el estado sea uno de los permitidos
        estados_permitidos = ['creado', 'aprobado', 'rechazado', 'listo']
        if nuevo_estado.lower() not in estados_permitidos:
            return Response(
                {'error': f'Estado no válido. Los estados permitidos son: {estados_permitidos}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Actualizar el estado (en mayúsculas para coincidir con tu modelo)
        existencia.estado_registro = nuevo_estado.upper()
        
        # ✅ ACTUALIZAR QUIÉN REALIZÓ LA ACCIÓN
        if nuevo_estado.lower() == 'aprobado':
            existencia.aprobado_por = request.user
        # Puedes agregar lógica similar para otros estados si es necesario
        
        existencia.save()
        
        # Serializar y retornar la respuesta
        serializer = ExistenciaMercanciaSerializer(existencia)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except ExistenciaMercancia.DoesNotExist:
        return Response(
            {'error': 'Existencia de mercancía no encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
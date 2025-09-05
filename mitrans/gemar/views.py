#4. Creacion de las vistas
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from gemar.models import PartePBIP, CargaVieja, ExistenciaMercancia
from gemar.Administracion.permissions import IsGEMARUser, IsAdminUser
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view


#4.1 una variante para trabajar con los serializadores  es la propiedad viewsets
# de rest_framework, facilita el CRUD

#importacion de modelos
from .models import (
    gemar_hecho_extraordinario, gemar_parte_hecho_extraordinario, 
    gemar_programacion_maniobras, gemar_parte_programacion_maniobras,
    PartePBIP, CargaVieja, ExistenciaMercancia,
    RegistroPBIP, ParteCargaVieja, RegistroCargaVieja, 
    ParteExistenciaMercancia, RegistroExistenciaMercancia
)
from .serializers import (
    gemar_hecho_extraordinario_serializer, 
    gemar_parte_hecho_extraordinario_serializer,
    gemar_programacion_maniobras_serializer, 
    gemar_parte_programacion_maniobras_serializer,
    PartePBIPSerializer, 
    RegistroPBIPSerializer,
    ParteCargaViejaSerializer,
    RegistroCargaViejaSerializer,
    ParteExistenciaMercanciaSerializer,
    RegistroExistenciaMercanciaSerializer
)


from Administracion.decorators import audit_log
from Administracion.models import Auditoria

#importacion de verificacion de autenticacion, trabajo con grupos y asignacion de
from rest_framework.decorators import api_view
#para la gestion de usuarios


#para usar el or

from django.utils import timezone
from datetime import datetime

#Para la paginacion

#Para el tratado de los permisos en el backend
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
    
    audit_log("Crear")
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
    @audit_log("Eliminado")
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

    @audit_log("Visualizar")
    def list(self, request, *args, **kwargs):
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
class SinRestriccionPermission(permissions.BasePermission):
    """
    Permiso que permite acceso sin restricciones a los partes específicos
    """
    def has_permission(self, request, view):
        # Permitir acceso sin restricciones para los métodos GET
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Para métodos no seguros, verificar si el usuario está autenticado
        return request.user and request.user.is_authenticated

# Views para los nuevos modelos
class PartePBIPViewSet(viewsets.ModelViewSet):
    queryset = PartePBIP.objects.all()
    serializer_class = PartePBIPSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['buque', 'puerto', 'nivel', 'estado', 'fecha_operacion']
    search_fields = ['buque__nombre_embarcacion', 'puerto__nombre_puerto'] 
    ordering_fields = ['fecha_creacion', 'fecha_operacion']
    ordering = ['-fecha_creacion']

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        parte = self.get_object()
        if parte.estado == 'APROBADO':
            return Response({'error': 'El parte ya está aprobado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        parte.estado = 'APROBADO'
        parte.aprobado_por = request.user
        parte.save()
        
        return Response({'status': 'Parte aprobado'})

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        parte = self.get_object()
        if parte.estado == 'CANCELADO':
            return Response({'error': 'El parte ya está cancelado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        parte.estado = 'CANCELADO'
        parte.save()
        
        return Response({'status': 'Parte cancelado'})

    @action(detail=True, methods=['get'])
    def registros(self, request, pk=None):
        parte = self.get_object()
        registros = parte.registros.all()
        serializer = RegistroPBIPSerializer(registros, many=True)
        return Response(serializer.data)

class RegistroPBIPViewSet(viewsets.ModelViewSet):
    queryset = RegistroPBIP.objects.all()
    serializer_class = RegistroPBIPSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['buque', 'puerto', 'nivel', 'fecha_operacion']
    search_fields = ['buque__nombre', 'puerto__nombre']
    ordering_fields = ['fecha_operacion']
    ordering = ['-fecha_operacion']

class ParteCargaViejaViewSet(viewsets.ModelViewSet):
    queryset = ParteCargaVieja.objects.all()
    serializer_class = ParteCargaViejaSerializer
    permission_classes = [AllowAny]  
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'fecha_operacion']
    search_fields = ['creado_por__username']
    ordering_fields = ['fecha_creacion', 'fecha_operacion']
    ordering = ['-fecha_creacion']

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        parte = self.get_object()
        if parte.estado == 'APROBADO':
            return Response({'error': 'El parte ya está aprobado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        parte.estado = 'APROBADO'
        parte.aprobado_por = request.user
        parte.save()
        
        return Response({'status': 'Parte aprobado'})

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        parte = self.get_object()
        if parte.estado == 'CANCELADO':
            return Response({'error': 'El parte ya está cancelado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        parte.estado = 'CANCELADO'
        parte.save()
        
        return Response({'status': 'Parte cancelado'})

    @action(detail=True, methods=['get'])
    def registros(self, request, pk=None):
        parte = self.get_object()
        registros = parte.registros.all()
        serializer = RegistroCargaViejaSerializer(registros, many=True)
        return Response(serializer.data)

class RegistroCargaViejaFilter(filters.FilterSet):
    fecha_operacion = filters.DateFilter(field_name='parte__fecha_operacion', lookup_expr='exact')
    puerto = filters.CharFilter(field_name='puerto__nombre_puerto', lookup_expr='icontains')  # Corregido
    terminal = filters.CharFilter(field_name='terminal__nombre_terminal', lookup_expr='icontains')  # Corregido
    producto = filters.CharFilter(field_name='producto__nombre_producto', lookup_expr='icontains')  # Corregido
    manifiesto = filters.CharFilter(lookup_expr='icontains')
    organismo = filters.CharFilter(field_name='organismo__nombre', lookup_expr='icontains')

    class Meta:
        model = RegistroCargaVieja
        fields = ['fecha_operacion', 'puerto', 'terminal', 'producto', 'manifiesto', 'organismo']

class RegistroCargaViejaViewSet(viewsets.ModelViewSet):
    queryset = RegistroCargaVieja.objects.all()
    serializer_class = RegistroCargaViejaSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RegistroCargaViejaFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por fecha de operación
        fecha_operacion = self.request.query_params.get('fecha_operacion')
        if fecha_operacion:
            try:
                fecha = datetime.strptime(fecha_operacion, '%Y-%m-%d').date()
                queryset = queryset.filter(parte__fecha_operacion=fecha)
            except ValueError:
                pass
        
        # Filtro por puerto
        puerto_id = self.request.query_params.get('puerto_id')
        if puerto_id:
            queryset = queryset.filter(puerto_id=puerto_id)
        
        # Filtro por terminal
        terminal_id = self.request.query_params.get('terminal_id')
        if terminal_id:
            queryset = queryset.filter(terminal_id=terminal_id)
        
        # Filtro por producto
        producto_id = self.request.query_params.get('producto_id')
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        
        # Filtro por organismo
        organismo_id = self.request.query_params.get('organismo_id')
        if organismo_id:
            queryset = queryset.filter(organismo_id=organismo_id)
        
        # Filtro por manifiesto
        manifiesto = self.request.query_params.get('manifiesto')
        if manifiesto:
            queryset = queryset.filter(manifiesto__icontains=manifiesto)
        
        return queryset.select_related(
            'parte', 'puerto', 'terminal', 'producto', 'organismo'
        )

class ParteExistenciaMercanciaViewSet(viewsets.ModelViewSet):
    queryset = ParteExistenciaMercancia.objects.all()
    serializer_class = ParteExistenciaMercanciaSerializer
    permission_classes = [SinRestriccionPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'fecha_operacion']
    search_fields = ['creado_por__username']
    ordering_fields = ['fecha_creacion', 'fecha_operacion']
    ordering = ['-fecha_creacion']

    @action(detail=True, methods=['post'])
    def aprobar(self, request, pk=None):
        parte = self.get_object()
        if parte.estado == 'APROBADO':
            return Response({'error': 'El parte ya está aprobado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        parte.estado = 'APROBADO'
        parte.aprobado_por = request.user
        parte.save()
        
        return Response({'status': 'Parte aprobado'})

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        parte = self.get_object()
        if parte.estado == 'CANCELADO':
            return Response({'error': 'El parte ya está cancelado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        parte.estado = 'CANCELADO'
        parte.save()
        
        return Response({'status': 'Parte cancelado'})

    @action(detail=True, methods=['get'])
    def registros(self, request, pk=None):
        parte = self.get_object()
        registros = parte.registros.all()
        serializer = RegistroExistenciaMercanciaSerializer(registros, many=True)
        return Response(serializer.data)

class RegistroExistenciaMercanciaViewSet(viewsets.ModelViewSet):
    queryset = RegistroExistenciaMercancia.objects.all()
    serializer_class = RegistroExistenciaMercanciaSerializer
    permission_classes = [SinRestriccionPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['terminal', 'producto', 'tipo', 'tipo_producto']
    
    # Corregir los campos de búsqueda para usar los campos de relación correctos
    search_fields = ['producto__nombre_producto', 'terminal__nombre_terminal']
    
    ordering_fields = ['producto__nombre_producto', 'terminal__nombre_terminal']
    ordering = ['producto__nombre_producto']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por fecha de operación
        fecha_operacion = self.request.query_params.get('fecha_operacion')
        if fecha_operacion:
            try:
                fecha = datetime.strptime(fecha_operacion, '%Y-%m-%d').date()
                queryset = queryset.filter(parte__fecha_operacion=fecha)
            except ValueError:
                pass
        
        return queryset.select_related('producto', 'terminal', 'parte')


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
            'total_existencias': existencias.count(),
            'partes_pbip': PartePBIPSerializer(partes_pbip, many=True).data,
            'cargas_viejas': CargaViejaSerializer(cargas_viejas, many=True).data,
            'existencias': ExistenciaMercanciaSerializer(existencias, many=True).data
        }
        
        return Response(resumen)
#LISTA DE TODOS LOS PARTES (HE, PROGRAMACION DE MANIOBRAS Y PBIP)
@api_view(['GET'])
def listar_partes_combinados(request):
    """
    Endpoint para listar todos los partes (hechos extraordinarios, programación de maniobras y PBIP)
    ordenados por fecha_actual/fecha_operacion descendente (incluyendo hora).
    """
    try:
        # Obtener parámetros opcionales de filtrado
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)
        estado = request.query_params.get('estado', None)
        
        # Validar permisos
        if not request.user.groups.filter(name__in=['VisualizadorGEMAR', 'AdminGEMAR']).exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener partes de hechos extraordinarios
        hechos_extraordinarios = gemar_parte_hecho_extraordinario.objects.all()
        # Obtener partes de programación de maniobras
        programacion_maniobras = gemar_parte_programacion_maniobras.objects.all()
        # Obtener partes PBIP
        partes_pbip = PartePBIP.objects.all()
        
        # Aplicar filtros si existen
        if fecha_inicio:
            try:
                fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                hechos_extraordinarios = hechos_extraordinarios.filter(fecha_actual__date__gte=fecha_inicio_obj)
                programacion_maniobras = programacion_maniobras.filter(fecha_actual__date__gte=fecha_inicio_obj)
                partes_pbip = partes_pbip.filter(fecha_operacion__gte=fecha_inicio_obj)
            except ValueError:
                return Response({"error": "Formato de fecha_inicio inválido. Use YYYY-MM-DD"}, status=400)
        
        if fecha_fin:
            try:
                fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                hechos_extraordinarios = hechos_extraordinarios.filter(fecha_actual__date__lte=fecha_fin_obj)
                programacion_maniobras = programacion_maniobras.filter(fecha_actual__date__lte=fecha_fin_obj)
                partes_pbip = partes_pbip.filter(fecha_operacion__lte=fecha_fin_obj)
            except ValueError:
                return Response({"error": "Formato de fecha_fin inválido. Use YYYY-MM-DD"}, status=400)
        
        if estado:
            hechos_extraordinarios = hechos_extraordinarios.filter(estado_parte=estado)
            programacion_maniobras = programacion_maniobras.filter(estado_parte=estado)
            partes_pbip = partes_pbip.filter(estado=estado)
        
        # Serializar los datos
        hechos_serializer = gemar_parte_hecho_extraordinario_serializer(hechos_extraordinarios, many=True)
        programacion_serializer = gemar_parte_programacion_maniobras_serializer(programacion_maniobras, many=True)
        pbip_serializer = PartePBIPSerializer(partes_pbip, many=True)
        
        # Combinar los resultados
        combined_data = hechos_serializer.data + programacion_serializer.data
        
        # Transformar datos PBIP para mantener consistencia con los otros partes
        pbip_data = []
        for parte in pbip_serializer.data:
            pbip_data.append({
                'id': parte['id'],
                'tipo_parte': 'PBIP',
                'fecha_actual': parte['fecha_operacion'],  # Usamos fecha_operacion como fecha_actual
                'estado_parte': parte['estado'],
                'creado_por': parte['creado_por'],
                'aprobado_por': parte['aprobado_por'],
                'buque': parte['buque'],
                'puerto': parte['puerto'],
                'detalles': {
                    'nivel': parte['nivel'],
                    'descripcion': 'Parte PBIP'  # Campo adicional para consistencia
                }
            })
        
        combined_data += pbip_data
        
        # Ordenar por fecha_actual descendente (más reciente primero)
        combined_data_sorted = sorted(
            combined_data,
            key=lambda x: x['fecha_actual'],
            reverse=True
        )
        
        # Registrar auditoría
        registrar_auditoria(request, "Visualización de lista combinada de partes (HE, Maniobras y PBIP)")
        
        return Response({
            "count": len(combined_data_sorted),
            "results": combined_data_sorted
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def listar_partes_combinados(request):
    """
    Endpoint para listar todos los partes (hechos extraordinarios, programación de maniobras y PBIP)
    ordenados por fecha_actual/fecha_operacion descendente (incluyendo hora).
    """
    try:
        # Obtener parámetros opcionales de filtrado
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)
        estado = request.query_params.get('estado', None)
        
        # Validar permisos
        if not request.user.groups.filter(name__in=['VisualizadorGEMAR', 'AdminGEMAR']).exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener partes de hechos extraordinarios
        hechos_extraordinarios = gemar_parte_hecho_extraordinario.objects.all()
        # Obtener partes de programación de maniobras
        programacion_maniobras = gemar_parte_programacion_maniobras.objects.all()
        # Obtener partes PBIP
        partes_pbip = PartePBIP.objects.all()
        # Obtener partes de carga vieja
        partes_carga_vieja = ParteCargaVieja.objects.all()
        # Obtener partes de existencia mercancía
        partes_existencia_mercancia = ParteExistenciaMercancia.objects.all()
        
        # Aplicar filtros si existen
        if fecha_inicio:
            try:
                fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                hechos_extraordinarios = hechos_extraordinarios.filter(fecha_actual__date__gte=fecha_inicio_obj)
                programacion_maniobras = programacion_maniobras.filter(fecha_actual__date__gte=fecha_inicio_obj)
                partes_pbip = partes_pbip.filter(fecha_operacion__gte=fecha_inicio_obj)
                partes_carga_vieja = partes_carga_vieja.filter(fecha_operacion__gte=fecha_inicio_obj)
                partes_existencia_mercancia = partes_existencia_mercancia.filter(fecha_operacion__gte=fecha_inicio_obj)
            except ValueError:
                return Response({"error": "Formato de fecha_inicio inválido. Use YYYY-MM-DD"}, status=400)
        
        if fecha_fin:
            try:
                fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                hechos_extraordinarios = hechos_extraordinarios.filter(fecha_actual__date__lte=fecha_fin_obj)
                programacion_maniobras = programacion_maniobras.filter(fecha_actual__date__lte=fecha_fin_obj)
                partes_pbip = partes_pbip.filter(fecha_operacion__lte=fecha_fin_obj)
                partes_carga_vieja = partes_carga_vieja.filter(fecha_operacion__lte=fecha_fin_obj)
                partes_existencia_mercancia = partes_existencia_mercancia.filter(fecha_operacion__lte=fecha_fin_obj)
            except ValueError:
                return Response({"error": "Formato de fecha_fin inválido. Use YYYY-MM-DD"}, status=400)
        
        if estado:
            hechos_extraordinarios = hechos_extraordinarios.filter(estado_parte=estado)
            programacion_maniobras = programacion_maniobras.filter(estado_parte=estado)
            partes_pbip = partes_pbip.filter(estado=estado)
            partes_carga_vieja = partes_carga_vieja.filter(estado=estado)
            partes_existencia_mercancia = partes_existencia_mercancia.filter(estado=estado)
        
        # Serializar los datos
        hechos_serializer = gemar_parte_hecho_extraordinario_serializer(hechos_extraordinarios, many=True)
        programacion_serializer = gemar_parte_programacion_maniobras_serializer(programacion_maniobras, many=True)
        pbip_serializer = PartePBIPSerializer(partes_pbip, many=True)
        carga_vieja_serializer = ParteCargaViejaSerializer(partes_carga_vieja, many=True)
        existencia_serializer = ParteExistenciaMercanciaSerializer(partes_existencia_mercancia, many=True)
        
        # Combinar los resultados
        combined_data = []
        
        # Transformar datos de hechos extraordinarios
        for parte in hechos_serializer.data:
            combined_data.append({
                'id': parte['id'],
                'tipo_parte': 'Hecho Extraordinario',
                'fecha_actual': parte['fecha_actual'],
                'estado_parte': parte['estado_parte'],
                'creado_por': parte['creado_por'],
                'aprobado_por': parte['aprobado_por'],
                'entidad': parte['entidad'],
                'provincia': parte['provincia'],
                'detalles': {
                    'descripcion': 'Parte de Hecho Extraordinario'
                }
            })
        
        # Transformar datos de programación de maniobras
        for parte in programacion_serializer.data:
            combined_data.append({
                'id': parte['id'],
                'tipo_parte': 'Programación de Maniobras',
                'fecha_actual': parte['fecha_actual'],
                'estado_parte': parte['estado_parte'],
                'creado_por': parte['creado_por'],
                'aprobado_por': parte['aprobado_por'],
                'entidad': parte['entidad'],
                'provincia': parte['provincia'],
                'detalles': {
                    'descripcion': 'Parte de Programación de Maniobras'
                }
            })
        
        # Transformar datos PBIP
        for parte in pbip_serializer.data:
            combined_data.append({
                'id': parte['id'],
                'tipo_parte': 'PBIP',
                'fecha_actual': parte['fecha_operacion'],
                'estado_parte': parte['estado'],
                'creado_por': parte['creado_por'],
                'aprobado_por': parte['aprobado_por'],
                'buque': parte['buque'],
                'puerto': parte['puerto'],
                'detalles': {
                    'nivel': parte['nivel'],
                    'descripcion': 'Parte PBIP'
                }
            })
        
        # Transformar datos de carga vieja
        for parte in carga_vieja_serializer.data:
            combined_data.append({
                'id': parte['id'],
                'tipo_parte': 'Carga Vieja',
                'fecha_actual': parte['fecha_operacion'],
                'estado_parte': parte['estado'],
                'creado_por': parte['creado_por'],
                'aprobado_por': parte['aprobado_por'],
                'detalles': {
                    'descripcion': 'Parte de Carga Vieja'
                }
            })
        
        # Transformar datos de existencia mercancía
        for parte in existencia_serializer.data:
            combined_data.append({
                'id': parte['id'],
                'tipo_parte': 'Existencia Mercancía',
                'fecha_actual': parte['fecha_operacion'],
                'estado_parte': parte['estado'],
                'creado_por': parte['creado_por'],
                'aprobado_por': parte['aprobado_por'],
                'detalles': {
                    'descripcion': 'Parte de Existencia de Mercancía'
                }
            })
        
        # Ordenar por fecha_actual descendente (más reciente primero)
        combined_data_sorted = sorted(
            combined_data,
            key=lambda x: x['fecha_actual'],
            reverse=True
        )
        
        # Registrar auditoría
        registrar_auditoria(request, "Visualización de lista combinada de partes")
        
        return Response({
            "count": len(combined_data_sorted),
            "results": combined_data_sorted
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)
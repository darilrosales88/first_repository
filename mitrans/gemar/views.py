#4. Creacion de las vistas
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import filters
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

#importacion de modelos, aqui es todo
from .models import (gemar_hecho_extraordinario,gemar_parte_hecho_extraordinario,
                     gemar_programacion_maniobras,gemar_parte_programacion_maniobras,
                     gemar_parte_carga_descarga,gemar_carga_descarga,gemar_producto_carga_descarga,
                     gemar_turno_carga_descarga,gemar_incidencia_por_turno_carga_descarga,
                     gemar_informe_diario_enc,gemar_maniobras_portuarias_enc,gemar_afectaciones_maniobras_portuarias_enc,
                     gemar_carga_seca_enc,gemar_remolcadores_maniobras_enc,gemar_remolcador_carga_liquida_enc,
                     gemar_remolcador_cabotaje_auxiliar_enc) 

#importacion de serializadores asociados a los modelos
from .serializers import (gemar_hecho_extraordinario_serializer,gemar_parte_hecho_extraordinario_serializer,
                          gemar_programacion_maniobras,gemar_programacion_maniobras_serializer,
                          gemar_parte_carga_descarga_serializer,gemar_carga_descarga_serializer,
                          gemar_producto_carga_descarga_serializer,gemar_turno_carga_descarga_serializer,
                          gemar_incidencia_por_turno_carga_descarga_serializer,gemar_informe_diario_enc_serializer,
                          gemar_parte_programacion_maniobras_serializer,gemar_maniobras_portuarias_enc_serializer,
                          gemar_afectaciones_maniobras_portuarias_enc_serializer,gemar_carga_seca_enc_serializer,
                          gemar_remolcadores_maniobras_enc_serializer,gemar_remolcador_carga_liquida_enc_serializer,
                          gemar_remolcador_cabotaje_auxiliar_enc_serializer, PartePBIPSerializer, ParteCargaViejaSerializer,
                          ParteExistenciaMercanciaSerializer)
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
class gemar_parte_carga_descarga_view_set(viewsets.ModelViewSet):
    queryset = gemar_parte_carga_descarga.objects.all().order_by('-id')
    serializer_class = gemar_parte_carga_descarga_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por fecha actual y entidad, se le pasa como parametro el campo por el que se va a filtrar
        search = self.request.query_params.get('fecha_entidad', None)

        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(fecha_actual__icontains=search) | queryset.filter(entidad__icontains=search)

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
        parte_carga_descarga = gemar_parte_carga_descarga.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar parte de carga-descarga: {parte_carga_descarga.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response
    
    def perform_create(self, serializer):
        user = self.request.user
        
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
    #Funcion para la actualizacion del estado del parte de carga-descarga
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
        registrar_auditoria(request, f"Actualizar estado del parte de carga-descarga {serializer.data['estado_parte']}")

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
        parte_carga_descarga = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de partes de carga-descarga.")

      

        return super().list(request, *args, **kwargs)
#**********************************************************************************************************************
class gemar_carga_descarga_view_set(viewsets.ModelViewSet):
    queryset = gemar_carga_descarga.objects.all().order_by('-id')
    serializer_class = gemar_carga_descarga_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por operacion, buque o terminal, se le pasa como parametro el campo por el que se va a filtrar
        search = self.request.query_params.get('operacion_buque_terminal', None)

        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(operacion__icontains=search) | queryset.filter(buque__nombre_embarcacion__icontains=search) | queryset.filter(terminal__nombre_terminal__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_carga_descarga = gemar_parte_carga_descarga.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar registro de carga-descarga: {obj_carga_descarga.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_carga_descarga = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de registros de carga-descarga.")

      

        return super().list(request, *args, **kwargs)
#**********************************************************************************************************************
class gemar_producto_carga_descarga_view_set(viewsets.ModelViewSet):
    queryset = gemar_producto_carga_descarga.objects.all().order_by('-id')
    serializer_class = gemar_producto_carga_descarga_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por producto o estado
        search = self.request.query_params.get('producto_estado', None)

        if search is not None:
            queryset = queryset.filter(producto__nombre_producto__icontains=search) | queryset.filter(estado__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_producto_carga_descarga = gemar_parte_carga_descarga.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar producto de carga-descarga: {obj_producto_carga_descarga.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_producto_carga_descarga = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de productos de carga-descarga.")

      

        return super().list(request, *args, **kwargs)
#**********************************************************************************************************************
class gemar_turno_carga_descarga_view_set(viewsets.ModelViewSet):
    queryset = gemar_turno_carga_descarga.objects.all().order_by('-id')
    serializer_class = gemar_turno_carga_descarga_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por producto o estado
        search = self.request.query_params.get('turno_cantidad_toneladas', None)

        if search is not None:
            queryset = queryset.filter(turno__icontains=search) | queryset.filter(cantidad_toneladas__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_turno_carga_descarga = gemar_turno_carga_descarga.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar turno de carga-descarga: {obj_turno_carga_descarga.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_turno_carga_descarga = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de turnos de carga-descarga.")      

        return super().list(request, *args, **kwargs)
#**********************************************************************************************************************
class gemar_incidencia_por_turno_carga_descarga_view_set(viewsets.ModelViewSet):
    queryset = gemar_incidencia_por_turno_carga_descarga.objects.all().order_by('-id')
    serializer_class = gemar_incidencia_por_turno_carga_descarga_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por producto o estado
        search = self.request.query_params.get('turno_incidencia', None)

        if search is not None:
            queryset = queryset.filter(turno__icontains=search) | queryset.filter(incidencia__nombre_incidencia__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_incidencia_turno_carga_descarga = gemar_incidencia_por_turno_carga_descarga_serializer.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar incidencia por turnos de carga-descarga: {obj_incidencia_turno_carga_descarga.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_incidencia_turno_carga_descarga = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de incidencias por turno de carga-descarga.")      

        return super().list(request, *args, **kwargs)
#**********************************************************************************************************************

#########**********************PARTE INFORME DIARIO ENC********************##########
class gemar_informe_diario_enc_view_set(viewsets.ModelViewSet):
    queryset = gemar_informe_diario_enc.objects.all().order_by('-id')
    serializer_class = gemar_informe_diario_enc_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por fecha actual y entidad, se le pasa como parametro el campo por el que se va a filtrar
        search = self.request.query_params.get('fecha_entidad', None)

        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(fecha_actual__icontains=search) | queryset.filter(entidad__icontains=search)

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
        informe_diario_enc = gemar_informe_diario_enc.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar informe diario ENC: {informe_diario_enc.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response
    
    def perform_create(self, serializer):
        user = self.request.user
        
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
    #Funcion para la actualizacion del estado del parte de carga-descarga
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
        registrar_auditoria(request, f"Actualizar estado del informe diario ENC a  {serializer.data['estado_parte']}")

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
        parte_carga_descarga = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de partes diarios de ENC.")

      

        return super().list(request, *args, **kwargs)
    
#**********************************************************************************************************************
class gemar_maniobras_portuarias_enc_view_set(viewsets.ModelViewSet):
    queryset = gemar_maniobras_portuarias_enc.objects.all().order_by('-id')
    serializer_class = gemar_maniobras_portuarias_enc_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por producto o estado
        search = self.request.query_params.get('buque_puerto', None)

        if search is not None:
            queryset = queryset.filter(buque__nombre_embarcacion__icontains=search) | queryset.filter(puerto__nombre_puerto__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_maniobra_portuaria_enc = gemar_maniobras_portuarias_enc_serializer.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar maniobra portuaria ENC: {obj_maniobra_portuaria_enc.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_maniobra_portuaria_enc = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de maniobras portuarias ENC.")      

        return super().list(request, *args, **kwargs)

#**********************************************************************************************************************
class gemar_afectaciones_maniobras_portuarias_enc_view_set(viewsets.ModelViewSet):
    queryset = gemar_afectaciones_maniobras_portuarias_enc.objects.all().order_by('-id')
    serializer_class = gemar_afectaciones_maniobras_portuarias_enc_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por producto o estado
        search = self.request.query_params.get('buque_puerto', None)

        if search is not None:
            queryset = queryset.filter(buque__nombre_embarcacion__icontains=search) | queryset.filter(puerto__nombre_puerto__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_afectacion_maniobra_portuaria_enc = gemar_afectaciones_maniobras_portuarias_enc_serializer.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar afectación de maniobra portuaria ENC: {obj_afectacion_maniobra_portuaria_enc.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_maniobra_portuaria_enc = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de afectaciones de maniobras portuarias ENC.")      

        return super().list(request, *args, **kwargs)

#**********************************************************************************************************************
class gemar_carga_seca_enc_view_set(viewsets.ModelViewSet):
    queryset = gemar_carga_seca_enc.objects.all().order_by('-id')
    serializer_class = gemar_carga_seca_enc_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por unidad basica o puerto
        search = self.request.query_params.get('unidad_basica_puerto', None)

        if search is not None:
            queryset = queryset.filter(unidad_basica__nombre__icontains=search) | queryset.filter(puerto_ubicado__nombre_puerto__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_carga_seca_enc = gemar_carga_seca_enc_serializer.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar carga seca ENC: {obj_carga_seca_enc.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_carga_seca_enc = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de cargas secas ENC.")      

        return super().list(request, *args, **kwargs)

#**********************************************************************************************************************
class gemar_remolcadores_maniobras_enc_view_set(viewsets.ModelViewSet):
    queryset = gemar_remolcadores_maniobras_enc.objects.all().order_by('-id')
    serializer_class = gemar_remolcadores_maniobras_enc_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por unidad basica o puerto
        search = self.request.query_params.get('unidad_basica_puerto', None)

        if search is not None:
            queryset = queryset.filter(unidad_basica__nombre__icontains=search) | queryset.filter(puerto_ubicado__nombre_puerto__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_remolcador_maniobra_enc = gemar_remolcadores_maniobras_enc_serializer.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar remolcador de maniobra ENC: {obj_remolcador_maniobra_enc.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_carga_seca_enc = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de remolcadores de maniobras ENC.")      

        return super().list(request, *args, **kwargs)

#**********************************************************************************************************************
class gemar_remolcador_carga_liquida_enc_view_set(viewsets.ModelViewSet):
    queryset = gemar_remolcador_carga_liquida_enc.objects.all().order_by('-id')
    serializer_class = gemar_remolcador_carga_liquida_enc_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por unidad basica o puerto
        search = self.request.query_params.get('unidad_basica_puerto', None)

        if search is not None:
            queryset = queryset.filter(unidad_basica__nombre__icontains=search) | queryset.filter(puerto_ubicado__nombre_puerto__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_remolcador_carga_liquida_enc = gemar_remolcador_carga_liquida_enc_serializer.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar remolcador de caga líquida ENC: {obj_remolcador_carga_liquida_enc.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_remolcador_carga_liquida_enc = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de remolcadores de carga líquida ENC.")      

        return super().list(request, *args, **kwargs)

#**********************************************************************************************************************
class gemar_remolcador_cabotaje_auxiliar_enc_view_set(viewsets.ModelViewSet):
    queryset = gemar_remolcador_cabotaje_auxiliar_enc.objects.all().order_by('-id')
    serializer_class = gemar_remolcador_cabotaje_auxiliar_enc_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por unidad basica o puerto
        search = self.request.query_params.get('unidad_basica_puerto', None)

        if search is not None:
            queryset = queryset.filter(unidad_basica__nombre__icontains=search) | queryset.filter(puerto_ubicado__nombre_puerto__icontains=search)

        return queryset
    
   
    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminGEMAR').exists():            
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Llama al método create del padre
        response = super().create(request, *args, **kwargs)
        
        # Obtiene la instancia creada (puedes acceder a ella a través del serializer)
        obj_remolcador_cabotaje_aux_enc = gemar_remolcador_cabotaje_auxiliar_enc_serializer.objects.get(id=response.data['id'])
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar remolcador de cabotaje y auxiliar ENC: {obj_remolcador_cabotaje_aux_enc.id}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return response   

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
        obj_remolcador_cabotaje_aux_enc = serializer.save()

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
        registrar_auditoria(request, "Visualizar lista de remolcadores de cabotaje y auxiliar ENC.")      

        return super().list(request, *args, **kwargs)

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
    
class RegistroPBIPViewSet(viewsets.ModelViewSet):
    queryset = RegistroPBIP.objects.all()
    serializer_class = RegistroPBIPSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['buque', 'puerto', 'nivel', 'fecha_operacion']
    search_fields = ['buque__nombre', 'puerto__nombre']
    ordering_fields = ['fecha_operacion']
    ordering = ['-fecha_operacion']


###################Tuve que comentar estas 2 serializadores que no tenian los modelos implementados de seguro por problemas con el merge
################### Raydel implemento, Partes, Registro.
# class CargaViejaViewSet(viewsets.ModelViewSet):
#     queryset = CargaVieja.objects.all()
#     serializer_class = CargaViejaSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser | IsGEMARUser]
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['parte', 'puerto', 'terminal', 'producto', 'organismo']
#     search_fields = ['producto__nombre', 'manifiesto', 'organismo__nombre', 'puerto__nombre', 'terminal__nombre']
#     ordering_fields = ['parte__fecha_operacion']
#     ordering = ['-parte__fecha_operacion']

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         parte_id = self.request.query_params.get('parte_id')
#         if parte_id:
#             queryset = queryset.filter(parte_id=parte_id)
#         return queryset

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save(creado_por=self.request.user)

#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
#     def aprobar(self, request, pk=None):
#         carga = self.get_object()
#         carga.estado = 'APROBADO'
#         carga.aprobado_por = request.user
#         carga.save()
#         return Response({'status': 'Carga aprobada'}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
#     def rechazar(self, request, pk=None):
#         carga = self.get_object()
#         carga.estado = 'RECHAZADO'
#         carga.save()
#         return Response({'status': 'Carga rechazada'}, status=status.HTTP_200_OK)

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             self.permission_classes = [IsAuthenticated, IsAdminUser | IsGEMARUser]
#         return super().get_permissions()

# class ExistenciaMercanciaViewSet(viewsets.ModelViewSet):
#     queryset = ExistenciaMercancia.objects.all()
#     serializer_class = ExistenciaMercanciaSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser | IsGEMARUser]
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['terminal', 'tipo', 'tipo_producto', 'producto', 'estado_registro']
#     search_fields = ['producto__nombre', 'terminal__nombre']
#     ordering_fields = ['fecha_operacion', 'fecha_creacion']
#     ordering = ['-fecha_operacion']

#     def perform_create(self, serializer):
#         serializer.save(creado_por=self.request.user)

#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
#     def aprobar(self, request, pk=None):
#         existencia = self.get_object()
#         existencia.estado_registro = 'APROBADO'
#         existencia.aprobado_por = request.user
#         existencia.save()
#         return Response({'status': 'Existencia aprobada'}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
#     def rechazar(self, request, pk=None):
#         existencia = self.get_object()
#         existencia.estado_registro = 'RECHAZADO'
#         existencia.save()
#         return Response({'status': 'Existencia rechazada'}, status=status.HTTP_200_OK)

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             self.permission_classes = [IsAuthenticated, IsAdminUser]
#         return super().get_permissions()

#######################################

#### ExistenciaMercancia
class ParteExistenciaMercanciaViewSet(viewsets.ModelViewSet):
    queryset = ParteExistenciaMercancia.objects.all()
    serializer_class = ParteExistenciaMercanciaSerializer
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['terminal', 'producto', 'tipo', 'tipo_producto']
    search_fields = ['producto__nombre', 'terminal__nombre']
    ordering_fields = ['producto__nombre', 'terminal__nombre']
    ordering = ['producto__nombre']
### Existencia Mercancia

#### Carga Vieja
class RegistroCargaViejaViewSet(viewsets.ModelViewSet):
    queryset = RegistroCargaVieja.objects.all()
    serializer_class = RegistroCargaViejaSerializer
    permission_classes = [AllowAny]  # Cambiado a AllowAny
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['puerto', 'terminal', 'producto', 'organismo', 'fecha_operacion']  # Campo añadido
    search_fields = ['producto__nombre', 'manifiesto']
    ordering_fields = ['manifiesto', 'producto__nombre', 'fecha_operacion']  # Campo añadido
    ordering = ['manifiesto']
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

##### Carga Vieja


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
            'cargas_viejas': ParteCargaViejaSerializer(cargas_viejas, many=True).data,
            'existencias': ParteExistenciaMercanciaSerializer(existencias, many=True).data
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

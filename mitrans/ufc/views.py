#4.1 una variante para trabajar con los serializadores  es la propiedad viewsets
# de rest_framework, facilita el CRUD
from rest_framework import viewsets,generics,permissions
from rest_framework.pagination import PageNumberPagination
#importacion de modelos
from .models import vagon_cargado_descargado,productos_vagones_cargados_descargados,en_trenes,producto_en_vagon
from .models import registro_vagones_cargados
from .models import por_situar,Situado_Carga_Descarga,arrastres
#importacion de serializadores asociados a los modelos
from .serializers import vagon_cargado_descargado_filter,vagon_cargado_descargado_serializer,producto_vagon_serializer
from .serializers import producto_vagon_cargado_descargado_filter,productos_vagones_cargados_descargados_serializer,en_trenes_serializer
from .serializers import PorSituarCargaDescargaSerializer,SituadoCargaDescargaSerializers,PendienteArrastreSerializer
from .serializers import registro_vagones_cargados_serializer,registro_vagones_cargados_filter

from Administracion.models import Auditoria

from rest_framework.response import Response
from rest_framework import status

#para el filtrado
from django_filters.rest_framework import DjangoFilterBackend

#para usar el or
from django.db.models import Q


from django.utils import timezone
#para usar el or

#Actualizando el ModelViewSet para usar diferentes permisos según la acción
from .permissions import IsAdminUFCPermission,IsVisualizadorUFCPermission

from rest_framework.decorators import action  # Importa el decorador action



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




#/*********************************************************************************************************************************************
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

    def create(self, request, *args, **kwargs):
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
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminUFC').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
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
#para productos de vagones cargados/descargados
class productos_vagones_cargados_descargados_view_set(viewsets.ModelViewSet):
    queryset = productos_vagones_cargados_descargados.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = productos_vagones_cargados_descargados_serializer    

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('producto_contenido', None)

        if search is not None:
            #filtrado por origen y por tipo de equipo ferroviario
            queryset = queryset.filter( Q(producto__icontains=search) | Q(contenido__icontains=search) 
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
        objeto_producto_vagon_cargado_descargado = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Insertar producto de vagón cargado/descargado: {objeto_producto_vagon_cargado_descargado.id}",
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
        objeto_producto_vagon_cargado_descargado = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Modificar producto de vagón cargado/descargado: {objeto_producto_vagon_cargado_descargado.id}",
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
        id_objeto_producto_vagon_cargado_descargado = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar producto de vagón cargado/descargado: {id_objeto_producto_vagon_cargado_descargado}",
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
            accion="Visualizar lista de productos de vagones cargados/descargados",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
    
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



class en_trenes_paginator(PageNumberPagination):
    page_size = 10  # Número de registros por página
    page_size_query_param = 'page_size'
    max_page_size = 100
class en_trenes_view_set(viewsets.ModelViewSet):
    queryset = en_trenes.objects.all().order_by('-id') # Definir el queryset
    serializer_class = en_trenes_serializer
    pagination_class = en_trenes_paginator

    ordering_fields = ['id'] 
    ordering = ['-id']  # Orden por defecto (descendente por id)    

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('origen_destino', None)

        if search_term:
            # Filtra por coincidencia en cualquiera de los campos
            queryset = queryset.select_related('producto').filter(
            Q(origen__icontains=search_term) |
            Q(destino__icontains=search_term)|
            Q(producto__producto__nombre_producto__icontains=search_term)|
            Q(numero_identificacion_locomotora__icontains=search_term)         
     )
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



class producto_vagon_view_set(viewsets.ModelViewSet):
    queryset = producto_en_vagon.objects.all().order_by('-id') # Definir el queryset
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



#Voy a agregar los modulos de auditoria a los que hizo Karmal
class PorSituarCargaDescargaViewSet(viewsets.ModelViewSet):
    queryset = por_situar.objects.all().order_by("-id")
    serializer_class = PorSituarCargaDescargaSerializer
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_equipo = self.request.query_params.get("tipo_equipo")
        if tipo_equipo:
            # Si el parámetro es una lista (ej: ?tipo_equipo=camion,furgon)
            if "," in tipo_equipo:
                tipos = tipo_equipo.split(",")
                queryset = queryset.filter(tipo_equipo__in=tipos)
        return queryset
    

    def create(self, request, *args, **kwargs):
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
            accion=f"Modificar formulario Situar carga o descarga: {objeto_por_situar.id}",
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

    
    
    
    


class SituadoCargaDescargaViewset(viewsets.ModelViewSet):
    queryset= Situado_Carga_Descarga.objects.all().order_by("-id")
    serializer_class = SituadoCargaDescargaSerializers
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_equipo = self.request.query_params.get("tipo_equipo")
        if tipo_equipo:
            # Si el parámetro es una lista (ej: ?tipo_equipo=camion,furgon)
            if "," in tipo_equipo:
                tipos = tipo_equipo.split(",")
                queryset = queryset.filter(tipo_equipo__in=tipos)
        return queryset
    
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

    
    
class PendienteArrastreViewset(viewsets.ModelViewSet):
    queryset = arrastres.objects.all()
    a=arrastres.objects.create
    serializer_class = PendienteArrastreSerializer


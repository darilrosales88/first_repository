#4.1 una variante para trabajar con los serializadores  es la propiedad viewsets
# de rest_framework, facilita el CRUD
from rest_framework import viewsets,generics,permissions
from rest_framework.pagination import PageNumberPagination
#importacion de modelos
from .models import vagon_cargado_descargado,productos_vagones_cargados_descargados,en_trenes,producto_en_vagon
from .models import por_situar_carga_descarga,Situado_Carga_Descarga,arrastre_pendientes
#importacion de serializadores asociados a los modelos
from .serializers import vagon_cargado_descargado_filter,vagon_cargado_descargado_serializer,producto_vagon_serializer
from .serializers import producto_vagon_cargado_descargado_filter,productos_vagones_cargados_descargados_serializer,en_trenes_serializer
from .serializers import PorSituarCargaDescargaSerializer,SituadoCargaDescargaSerializers,PendienteArrastreSerializer

from Administracion.models import Auditoria

from rest_framework.response import Response
from rest_framework import status

#para el filtrado
from django_filters.rest_framework import DjangoFilterBackend

#para usar el or
from django.db.models import Q


from django.utils import timezone
#para usar el or



# Verifica si el usuario tiene el rol "ufc"
class IsUFCPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ROLES_PERMITIDO=['ufc','admin']
        return request.user.role in ROLES_PERMITIDO




#/*********************************************************************************************************************************************
class vagon_cargado_descargado_view_set(viewsets.ModelViewSet):
    queryset = vagon_cargado_descargado.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = vagon_cargado_descargado_serializer
    permission_classes = [IsUFCPermission] 
    
    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('origen_t_e_ferroviario', None)

        if search is not None:
            #filtrado por origen y por tipo de equipo ferroviario
            queryset = queryset.filter( Q(origen__icontains=search) | Q(tipo_equipo_ferroviario_name__icontains=search) 
            )

        return queryset

    def create(self, request, *args, **kwargs):
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
        instance = self.get_object()
        id_objeto_vagon_cargado_descargado = instance.id

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            direccion_ip=direccion_ip,
            accion=f"Eliminar vagón cargado/descargado: {id_objeto_vagon_cargado_descargado}",
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
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
#/*********************************************************************************************************************************************
class productos_vagones_cargados_descargados_view_set(viewsets.ModelViewSet):
    queryset = productos_vagones_cargados_descargados.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = productos_vagones_cargados_descargados_serializer
    permission_classes = [IsUFCPermission]

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('producto_contenido', None)

        if search is not None:
            #filtrado por origen y por tipo de equipo ferroviario
            queryset = queryset.filter( Q(producto__icontains=search) | Q(contenido__icontains=search) 
            )

        return queryset

    def create(self, request, *args, **kwargs):
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
    
#/********************************************************EN_TRENES*********************************************************************



class en_trenes_paginator(PageNumberPagination):
    page_size = 10  # Número de registros por página
    page_size_query_param = 'page_size'
    max_page_size = 100
class en_trenes_view_set(viewsets.ModelViewSet):
    queryset = en_trenes.objects.all().order_by('-id') # Definir el queryset
    serializer_class = en_trenes_serializer
    pagination_class = en_trenes_paginator
    permission_classes = [IsUFCPermission]
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
    queryset = por_situar_carga_descarga.objects.all()
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

    def update(self, request, *args, **kwargs):
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
    queryset= Situado_Carga_Descarga.objects.all()
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
    queryset = arrastre_pendientes.objects.all()
    a=arrastre_pendientes.objects.create
    serializer_class = PendienteArrastreSerializer
    
    
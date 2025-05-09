#4. Creacion de las vistas

#4.1 una variante para trabajar con los serializadores  es la propiedad viewsets
# de rest_framework, facilita el CRUD
from rest_framework import viewsets

#importacion de modelos
from .models import nom_pais,nom_provincia,nom_municipio,nom_tipo_maniobra_portuaria,nom_contenedor,nom_cargo
from .models import nom_territorio,nom_puerto,nom_terminal,nom_atraque,nom_unidad_medida,nom_osde_oace_organismo,nom_entidades
from .models import nom_destino,nom_tipo_equipo_ferroviario,nom_embarcacion,nom_equipo_ferroviario,nom_estado_tecnico
from .models import nom_producto,nom_tipo_embalaje,nom_incidencia,nom_tipo_estructura_ubicacion,nom_estructura_ubicacion

#importacion de serializadores asociados a los modelos
from .serializers import nom_pais_serializer,nom_provincia_serializer,nom_municipio_serializer
from .serializers import nom_tipo_maniobra_portuaria_serializer,nom_contenedor_serializer,nom_cargo_serializer
from .serializers import nom_territorio_serializer,nom_puerto_serializer,nom_terminal_serializer
from .serializers import nom_atraque_serializer,nom_unidad_medida_serializer,nom_osde_oace_organismo_serializer,nom_osde_oace_organismo_filter,nom_entidades_serializer
from .serializers import nom_destino_serializer,nom_tipo_equipo_ferroviario_serializer,nom_embarcacion_serializer
from .serializers import nom_equipo_ferroviario_serializer,nom_estado_tecnico_serializer,nom_producto_serializer,nom_entidades_filter
from .serializers import nom_tipo_embalaje_serializer,nom_incidencia_serializer,nom_tipo_estructura_ubicacion_serializer,nom_estructura_ubicacion_serializer
from Administracion.serializers import UserPermissionSerializer

from Administracion.models import Auditoria
from Administracion.serializers import AuditoriaSerializer, auditoria_filter

#importacion de verificacion de autenticacion, trabajo con grupos y asignacion de
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
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
from .permissions import IsAdminNomenladoresPermission,IsVisualizadorNomencladoresPermission



#asignando a permission_classes los permisos asociados
def get_permissions(self):
    if self.action in ['create', 'update', 'partial_update', 'destroy']:
        permission_classes = [IsAdminNomenladoresPermission]
    else:  # Para list y retrieve
        # Permitir tanto a AdminNomencladores como a VisualizadorNomencladores visualizar
        permission_classes = [IsAdminNomenladoresPermission | IsVisualizadorNomencladoresPermission]
    return [permission() for permission in permission_classes]

          
    #*****************************************************************************************************************************
#4.2 declaramos la vista para serializar el modelo nom_pais
class nom_pais_view_set(viewsets.ModelViewSet):
    queryset = nom_pais.objects.all().order_by('-id')
    serializer_class = nom_pais_serializer

    

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nacionalidad de pais, se le pasa como parametro el campo por el que se va a filtrar,
        # nom_pais_nacionalidad, declarado en el nom_pais_filter del archivo serializers.py
        nacionalidad_pais = self.request.query_params.get('nom_pais_nacionalidad')
        if nacionalidad_pais:
            #nacionalidad es el nombre del campo del modelo nom_pais
            queryset = queryset.filter(nacionalidad = nacionalidad_pais)

        #LA OTRA PARTE DEL FILTRADO
        # el otro campo por el que estoy filtrando, nombre_p, declarado en el nom_pais_filter del archivo serializers.py
        #voy a capturar ese valor que me llega desde el serializador y lo voy a comparar con el campo nombre_pais del modelo nom_pais
        #preguntando si ese valor entrado por le usuario esta contenido en el valor del campo nombre_pais
        search = self.request.query_params.get('nombre_p', None)


        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(nombre_pais__icontains=search)
           # queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)

        return queryset
    
    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pais = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar país: {pais.nombre_pais}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        pais = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar país: {pais.nombre_pais}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        nombre_pais = instance.nombre_pais

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar país: {nombre_pais}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de países",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)

#/*********************************************************************************************************************************************
class nom_provincia_view_set(viewsets.ModelViewSet):
    queryset = nom_provincia.objects.all().order_by('-id')
    serializer_class = nom_provincia_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nombre de nombre_provincia, se le pasa como parametro el campo por el que se va a filtrar
        search = self.request.query_params.get('nombre_prov', None)

        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(nombre_provincia__icontains=search)
           # queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)

        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provincia = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar provincia: {provincia.nombre_provincia}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        provincia = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar provincia: {provincia.nombre_provincia}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_provincia = instance.nombre_provincia

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar provincia: {nombre_provincia}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de provincias",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_municipio_view_set(viewsets.ModelViewSet):
    queryset = nom_municipio.objects.all().order_by('-id')
    serializer_class = nom_municipio_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nombre codigo, se le pasa como parametro el campo por el que se va a filtrar, codigo
        codigo_m = self.request.query_params.get('municipio_codigo')
        if codigo_m:
            queryset = queryset.filter(codigo=codigo_m)

        # Filtrado por nombre de nombre_municipio, se le pasa como parametro el campo por el que se va a filtrar, nombre_municipio
        search = self.request.query_params.get('nombre_munic', None)

        if search is not None: #preguntamos si la variable search no está vacía
            queryset = queryset.filter(nombre_municipio__icontains=search)
        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        municipio = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar país: {municipio.nombre_municipio}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        municipio = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar municipio: {municipio.nombre_municipio}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_municipio = instance.nombre_municipio

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar municipio: {nombre_municipio}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de municipios",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************

CustomUser = get_user_model()  # Obtén el modelo de usuario personalizado

class nom_tipo_maniobra_portuaria_view_set(viewsets.ModelViewSet):
    queryset = nom_tipo_maniobra_portuaria.objects.all().order_by('-id')
    serializer_class = nom_tipo_maniobra_portuaria_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de estructura de ubicacion
        search = self.request.query_params.get('nombre_y_tipo_maniobra', None)

        if search is not None:

            queryset = queryset.filter( Q(nombre_maniobra__icontains=search) | Q(tipo_maniobra__icontains=search)
            )

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tipo_maniobra = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar tipo de maniobra portuaria: {tipo_maniobra.nombre_maniobra}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tipo_maniobra = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar tipo de maniobra portuaria: {tipo_maniobra.nombre_maniobra}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_maniobra = instance.nombre_maniobra

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar tipo de maniobra portuaria: {nombre_maniobra}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de tipos de maniobras portuarias",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_contenedor_view_set(viewsets.ModelViewSet):
    queryset = nom_contenedor.objects.all().order_by('-id_contenedor')
    serializer_class = nom_contenedor_serializer
    #El método get_object utiliza el campo lookup_field para obtener la instancia correcta. Por defecto, lookup_field es pk, 
    #pero en 3este caso, la clave primaria es id_contenedor. Por eso en el ModelViewSet este campo debe estar igualado a id_contenedor
    lookup_field = 'id_contenedor'  # Especifica el campo de búsqueda

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        print('Eliminando contenedor con ID:', kwargs.get('pk'));  # Verifica el ID

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar contenedor con ID {kwargs.get('pk')}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        return super().destroy(request, *args, **kwargs);

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('id_tipo_longitud', None)

        if search is not None:

            queryset = queryset.filter( Q(id_contenedor__icontains=search) | Q(longitud__icontains=search) | Q(tipo_contenedor__icontains=search)
            )

        return queryset
    
    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contenedor = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar contenedor con ID {contenedor.id_contenedor}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        contenedor = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar contenedor con ID {contenedor.id_contenedor}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de municipios",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_cargo_view_set(viewsets.ModelViewSet):
    queryset = nom_cargo.objects.all().order_by('-id')
    serializer_class = nom_cargo_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nombre del cargo
        search = self.request.query_params.get('n_cargo', None)

        if search is not None:
            queryset = queryset.filter(nombre_cargo__icontains=search)
        return queryset
    
    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cargo = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar cargo: {cargo.nombre_cargo}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        cargo = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar cargo: {cargo.nombre_cargo}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_cargo = instance.nombre_cargo

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar cargo: {nombre_cargo}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista cargos",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_territorio_view_set(viewsets.ModelViewSet):
    queryset = nom_territorio.objects.all().order_by('-id')
    serializer_class = nom_territorio_serializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('nomb_territorio', None)
        if search is not None:
            queryset = queryset.filter(nombre_territorio__icontains=search)
        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        territorio = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar Territorio: {territorio.nombre_territorio}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        territorio = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar territorio: {territorio.nombre_territorio}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_territorio= instance.nombre_territorio

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar territorio: {nombre_territorio}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de territorios",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)    
            
#/*********************************************************************************************************************************************
class nom_puerto_view_set(viewsets.ModelViewSet):
    queryset = nom_puerto.objects.all().order_by('id')  # Ordenar por defecto por el campo 'id'
    serializer_class = nom_puerto_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de estructura de ubicacion
        search = self.request.query_params.get('nombre_pais', None)

        if search is not None:

            queryset = queryset.filter( Q(nombre_puerto__icontains=search) | Q(pais_name__icontains=search) 
            | Q(codigo_producto__exact=search) )      

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        puerto = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar puerto: {puerto.nombre_puerto}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        puerto = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar puerto: {puerto.nombre_puerto}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_puerto= instance.nombre_puerto

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar puerto: {nombre_puerto}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de puertos",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs) 
#/*********************************************************************************************************************************************
class nom_terminal_view_set(viewsets.ModelViewSet):
    queryset = nom_terminal.objects.all().order_by('id')  # Ordenar por defecto por el campo 'id'
    serializer_class = nom_terminal_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de estructura de ubicacion
        search = self.request.query_params.get('puerto_nombre_terminal', None)

        if search is not None:

            queryset = queryset.filter( Q(nombre_terminal__icontains=search) | Q(puerto_name__icontains=search) 
            | Q(codigo_producto__exact=search) )      

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        terminal = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar terminal: {terminal.nombre_terminal}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        terminal = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar terminal: {terminal.nombre_terminal}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_terminal= instance.nombre_terminal

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar terminal: {nombre_terminal}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de terminales",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs) 
#/*********************************************************************************************************************************************
#funcion declarada en el views.py una sola vez, sera usada en cada view_set
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15  # Número de registros por página
    page_size_query_param = 'page_size'
    max_page_size = 100

class nom_atraque_view_set(viewsets.ModelViewSet):
    queryset = nom_atraque.objects.all().order_by('id')  # Ordenar por defecto por el campo 'id',hay que hacerlo con 
    #todos los view_set que seran paginados
    serializer_class = nom_atraque_serializer
    #funcion declarada para la paginacion aqui en el views.py

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nombre_atraque
        search = self.request.query_params.get('nombre_atraque', None)

        if search is not None:
            queryset = queryset.filter(nombre_atraque__icontains=search)
        
        return queryset.order_by('id')  # Asegurar que el QuerySet esté ordenado,hacer esto en cada get_queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        atraque = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar atraque: {atraque.nombre_atraque}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        atraque = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar atraque: {atraque.nombre_atraque}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_atraque= instance.nombre_atraque

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar atraque: {nombre_atraque}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de atraques",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_unidad_medida_view_set(viewsets.ModelViewSet):
    queryset = nom_unidad_medida.objects.all().order_by('-id')
    serializer_class = nom_unidad_medida_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de estructura de ubicacion
        search = self.request.query_params.get('magnitud_um_simbolo', None)

        if search is not None:

            queryset = queryset.filter( Q(magnitud__icontains=search) | Q(unidad_medida__icontains=search) 
            | Q(simbolo__exact=search) )      

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unidad_medida = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar unidad de medida: {unidad_medida.unidad_medida}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        unidad_medida = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar unidad de medida: {unidad_medida.unidad_medida}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        unidad_medida= instance.unidad_medida

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar unidad de medida: {unidad_medida}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de unidades de medida",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_osde_oace_organismo_view_set(viewsets.ModelViewSet):
    queryset = nom_osde_oace_organismo.objects.all().order_by('-id')
    serializer_class = nom_osde_oace_organismo_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = nom_osde_oace_organismo_filter
    def get_queryset(self):
        queryset = super().get_queryset()
        #filtrado por codigo_reeup
        cod_r = self.request.query_params.get('cod_reeup')
        if cod_r:
            queryset = queryset.filter(codigo_reeup=cod_r)

        # Filtrado por nombre del OSDE/OACE/Organismo
        search = self.request.query_params.get('nombre', None)

        if search is not None:
            queryset = queryset.filter(nombre__icontains=search)
        return queryset
    
    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        o_o_organismo = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar OSDE/OACE u Organismo: {o_o_organismo.nombre}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        o_o_organismo = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar OSDE/OACE u Organismo: {o_o_organismo.nombre}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_o_o_o= instance.nombre

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar OSDE/OACE u Organismo: {nombre_o_o_o}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de OSDE/OACE u Organismos",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_entidades_view_set(viewsets.ModelViewSet):
    queryset = nom_entidades.objects.all().order_by('id')  # Ordenar por defecto por el campo 'id' Esto estaba mal implementado estaba buscando en nom_atraques'
    serializer_class = nom_entidades_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = nom_entidades_filter

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('nombre_abrev_osde', None)

        if search is not None:

            queryset = queryset.filter( Q(nombre__icontains=search) | Q(abreviatura__icontains=search) | Q(osde_oace_organismo__icontains=search)
            )

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        entidad = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar entidad: {entidad.nombre}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        entidad = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar entidad: {entidad.nombre}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        entidad_nombre= instance.nombre

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar entidad: {entidad_nombre}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de entidades",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)

#funcion para verificar si un juego de datos ya existe en la tabla de la BD
@api_view(['GET'])
def verificar_codigo_reeup(request):
    codigo_reeupp = request.query_params.get('codigo_reeup')

    if not codigo_reeupp:
        return Response({"error": "Se requiere el parámetro 'codigo_reeup'."}, status=400)

    existe = nom_entidades.objects.filter(codigo_reeup=codigo_reeupp).exists()
    return Response({"exists": existe})#retorna un booleano

#retorna solo las entidades cuyo tipo sean de acceso comercial o de ccd
class entidades_acceso_comercial_ccdView(APIView):
    def get(self, request):
        # Filtrar las entidades cuyo tipo_entidad sea "acceso_comercial" o "CCD"
        entidades = nom_entidades.objects.filter(tipo_entidad__in=['acceso_comercial', 'ccd'])
        
        # Serializar los datos
        serializer = nom_entidades_serializer(entidades, many=True)
        
        # Devolver la respuesta
        return Response(serializer.data, status=status.HTTP_200_OK)
#/*********************************************************************************************************************************************
class nom_destino_view_set(viewsets.ModelViewSet):
    queryset = nom_destino.objects.all().order_by('-id')
    serializer_class = nom_destino_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('cliente_destino', None)

        if search is not None:

            queryset = queryset.filter( Q(cliente__icontains=search) | Q(destino__icontains=search)
            )

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        destino = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar destino: {destino.destino}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        destino = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar destino: {destino.destino}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        destino = instance.destino

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar destino: {destino}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de destinos",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)

#funcion para verificar si un juego de datos ya existe en la tabla de la BD
@api_view(['GET'])
def verificar_destino(request):
    cliente = request.query_params.get('cliente')
    destino = request.query_params.get('destino')

    if not cliente or not destino:
        return Response({"error": "Se requieren los parámetros 'cliente' y 'destino'."}, status=400)

    existe = nom_destino.objects.filter(cliente=cliente, destino=destino).exists()
    return Response({"exists": existe})#retorna un booleano
#/*********************************************************************************************************************************************
class nom_tipo_equipo_ferroviario_view_set(viewsets.ModelViewSet):
    queryset = nom_tipo_equipo_ferroviario.objects.all().order_by('-id')
    serializer_class = nom_tipo_equipo_ferroviario_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de equipo, descripcion y tipo_combustible
        search = self.request.query_params.get('busqueda_tipo_equipo__tipo_carga', None)

        if search is not None: #preguntamos si la variable search no está vacía

          #si no lo está el queryset es alguna coincidencia con el campo descripcion, 
          #tipo de equipo, o exactamente el valor del campo tipo_combustible
            queryset = queryset.filter(tipo_equipo__icontains=search) | queryset.filter(tipo_carga__icontains=search)

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tipo_equipo = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar tipo de equipo ferroviario: {tipo_equipo.tipo_equipo}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tipo_equipo = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar tipo de equipo ferroviario: {tipo_equipo.tipo_equipo}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        tipo_equipo = instance.tipo_equipo

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar tipo de equipo ferroviario: {tipo_equipo}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de tipos de equipos ferroviarios",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)

#retorna los tipos de equipo
class tipo_equipo_ferroviario_no_locomotora(APIView):
    def get(self, request):
        # Excluir los tipos de equipos ferroviarios cuyo tipo sea "locomotora"
        tipos_equipos = nom_tipo_equipo_ferroviario.objects.exclude(tipo_equipo='locomotora')
        
        # Obtener el parámetro de tipo_combustible de la URL si existe
        tipo_combustible = request.query_params.get('tipo_combustible', None)
        
        # Si se proporciona un tipo de combustible, filtrar por él
        if tipo_combustible:
            tipos_equipos = tipos_equipos.filter(tipo_combustible=tipo_combustible)
        
        # Serializar los datos
        serializer = nom_tipo_equipo_ferroviario_serializer(tipos_equipos, many=True)
        
        # Devolver la respuesta
        return Response(serializer.data, status=status.HTTP_200_OK)
#/*********************************************************************************************************************************************
class nom_embarcacion_view_set(viewsets.ModelViewSet):
    queryset = nom_embarcacion.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = nom_embarcacion_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('nombre_tipo_nacionalidad', None)

        if search is not None:

            queryset = queryset.filter( Q(nombre_embarcacion__icontains=search) | Q(tipo_embarcacion_name__icontains=search) | Q(nacionalidad_name__icontains=search)
            )

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        embarcacion = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar embarcación: {embarcacion.nombre_embarcacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        embarcacion = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar embarcación: {embarcacion.nombre_embarcacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_embarcacion = instance.nombre_embarcacion

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar embarcación: {nombre_embarcacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de embarcaciones",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************

#retorna todos los equipos ferroviarios excepto los de tipo "Locomotora", y que no se encuentren presentes
#en la tabla de vagones registrado asociada al estado cargado_descargado
class equipo_ferroviario_no_locomotora(APIView):
    def get(self, request):
        tipos_no_locomotoras = nom_tipo_equipo_ferroviario.objects.exclude(tipo_equipo='locomotora')
        
        # Filtro adicional si se proporciona tipo_equipo
        tipo_equipo = request.query_params.get('tipo_equipo', None)
        if tipo_equipo:
            tipos_no_locomotoras = tipos_no_locomotoras.filter(id=tipo_equipo)

        # Usamos subquery para mejor rendimiento
        vagones_registrados = registro_vagones_cargados.objects.exclude(
            Q(no_id__isnull=True) | Q(no_id__exact='')
        ).values('no_id')
        
        equipos_no_locomotoras = nom_equipo_ferroviario.objects.filter(
            tipo_equipo__in=tipos_no_locomotoras
        )
        #.exclude(   numero_identificacion__in=vagones_registrados) Esto lo tuve que comentar para poder hacer que me salieran los equipos *******
        
        serializer = nom_equipo_ferroviario_serializer(equipos_no_locomotoras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class nom_equipo_ferroviario_view_set(viewsets.ModelViewSet):
    queryset = nom_equipo_ferroviario.objects.all().order_by('-id')  # Definir el queryset
    serializer_class = nom_equipo_ferroviario_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.query_params.get('id_tipo_equipo_territorio', None)
        if search:
            try:
                # Intenta convertir el término de búsqueda a un entero para buscar por ID
                search_term_as_int = int(search)
                queryset = queryset.select_related('tipo_equipo').filter(Q(tipo_equipo_id=search_term_as_int))
                return queryset
            except ValueError:
                search_term_as_int = None
                
            queryset = queryset.select_related('tipo_equipo').filter(Q(tipo_equipo__tipo_equipo__icontains=search) |Q(territorio__icontains=search) | Q(numero_identificacion__icontains=search)
            )
        #Fixed bug para buscar locomotoras cuando se usa select_related('campo_asociado_a_ForeignKEY')
        return queryset
    
    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        equipo_ferroviario = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar equipo ferroviario: {equipo_ferroviario.numero_identificacion}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        equipo_ferroviario = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar equipo ferroviario: {equipo_ferroviario.numero_identificacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        numero_identificacion= instance.numero_identificacion

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar equipo ferroviario: {numero_identificacion}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de equipos ferroviarios",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
    


#/*********************************************************************************************************************************************


class nom_estado_tecnico_view_set(viewsets.ModelViewSet):
    queryset = nom_estado_tecnico.objects.all().order_by('-id')
    serializer_class = nom_estado_tecnico_serializer
    lookup_field = 'codigo_estado_tecnico'  # Especifica el campo a usar como clave primaria

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        print('Eliminando estado tecnico con ID:', kwargs.get('pk'));  # Verifica el ID
        return super().destroy(request, *args, **kwargs);

    def get_queryset(self):
        queryset = super().get_queryset()
        cod_estado = self.request.query_params.get('codigo_estado')
        if cod_estado:            
            queryset = queryset.filter(codigo_estado_tecnico=cod_estado) | queryset.filter(nombre_estado_tecnico__icontains=cod_estado)
        return queryset 

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        estado_tecnico = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar estado técnico: {estado_tecnico.nombre_estado_tecnico}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        estado_tecnico = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar estado técnico: {estado_tecnico.nombre_estado_tecnico}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_estado_tecnico = instance.nombre_estado_tecnico

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar estado técnico: {nombre_estado_tecnico}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de estados técnicos",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)

#/*********************************************************************************************************************************************
class nom_producto_view_set(viewsets.ModelViewSet):
    queryset = nom_producto.objects.all().order_by('nombre_producto')  # Orden obligatorio
    serializer_class = nom_producto_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de estructura de ubicacion
        search = self.request.query_params.get('nombre_tipo_codigo_producto', None)

        if search is not None:

            queryset = queryset.filter( Q(nombre_producto__icontains=search) | Q(tipo_producto__icontains=search) 
            | Q(codigo_producto__exact=search) )      

        return queryset


        # Filtrado por nombre, descripcion y codigo
        search = self.request.query_params.get('nombre_descripcion_codigo_producto', None)

        if search is not None:

            queryset = queryset.filter(nombre_producto__icontains=search) | queryset.filter(descripcion__icontains = search) | queryset.filter(codigo_producto__exact = search)

        return queryset
    
    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        producto = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar producto: {producto.nombre_producto}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        producto = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar producto: {producto.nombre_producto}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_producto= instance.nombre_producto

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar producto: {nombre_producto}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de productos",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************

class nom_tipo_embalaje_view_set(viewsets.ModelViewSet):
    queryset = nom_tipo_embalaje.objects.all().order_by('-id')
    serializer_class = nom_tipo_embalaje_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de embalaje
        search = self.request.query_params.get('nombre_tipo_embalaje', None)

        if search is not None:

            queryset = queryset.filter(nombre_tipo_embalaje__icontains=search)

        return queryset
    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tipo_embalaje = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar tipo de embalaje: {tipo_embalaje.nombre_tipo_embalaje}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tipo_embalaje = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar tipo de embalaje: {tipo_embalaje.nombre_tipo_embalaje}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_tipo_embalaje= instance.nombre_tipo_embalaje

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar tipo de embalaje: {nombre_tipo_embalaje}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de tipos de embalaje",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_incidencia_view_set(viewsets.ModelViewSet):
    queryset = nom_incidencia.objects.all().order_by('-id')
    serializer_class = nom_incidencia_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de estructura de ubicacion
        search = self.request.query_params.get('nombre_codigo', None)

        if search is not None:

            queryset = queryset.filter( Q(codigo_incidencia__icontains=search) | Q(nombre_incidencia__icontains=search)
            )

        return queryset
    
    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        incidencia = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar incidencia: {incidencia.nombre_incidencia}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        incidencia = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar incidencia: {incidencia.nombre_incidencia}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_incidencia= instance.nombre_incidencia

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar incidencia: {nombre_incidencia}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de incidencias",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_tipo_estructura_ubicacion_view_set(viewsets.ModelViewSet):
    queryset = nom_tipo_estructura_ubicacion.objects.all().order_by('-id')
    serializer_class = nom_tipo_estructura_ubicacion_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por tipo de estructura de ubicacion
        search = self.request.query_params.get('nombre_tipo_estructura_ubicacion', None)

        if search is not None:

            queryset = queryset.filter(nombre_tipo_estructura_ubicacion__icontains = search)

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tipo_estructura = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar tipo de estructura de ubicación: {tipo_estructura.nombre_tipo_estructura_ubicacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tipo_estructura = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar tipo de estructura de ubicación: {tipo_estructura.nombre_tipo_estructura_ubicacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_tipo_estructura = instance.nombre_tipo_estructura_ubicacion

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar tipo de estructura de ubicación: {nombre_tipo_estructura}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de tipos de estructura de ubicación",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)
#/*********************************************************************************************************************************************
class nom_estructura_ubicacion_view_set(viewsets.ModelViewSet):
    queryset = nom_estructura_ubicacion.objects.all().order_by('-id')
    serializer_class = nom_estructura_ubicacion_serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtrado por nombre de estructura de ubicación
        search = self.request.query_params.get('nombre_estructura', None)

        if search is not None:
            queryset = queryset.filter(nombre_estructura_ubicacion__icontains=search)

        return queryset

    def create(self, request, *args, **kwargs):
        #permisos de acceso a la operacion
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        estructura = serializer.save() 

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Insertar estructura de ubicación: {estructura.nombre_estructura_ubicacion}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        estructura = serializer.save()

        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Modificar estructura de ubicación: {estructura.nombre_estructura_ubicacion}",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance = self.get_object()
        nombre_estructura_ubicacion= instance.nombre_estructura_ubicacion

        # Registrar la acción en el modelo de Auditoria antes de eliminar
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion=f"Eliminar estructura de ubicación: {nombre_estructura_ubicacion}",
            direccion_ip=direccion_ip,
            navegador=navegador, 
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='VisualizadorNomencladores').exists() and not request.user.groups.filter(name='AdminNomencladores').exists():
            return Response(
                {"detail": "No tiene permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Registrar la acción en el modelo de Auditoria
        navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')
        direccion_ip = request.META.get('REMOTE_ADDR')
        Auditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            accion="Visualizar lista de estructuras de ubicación",
            direccion_ip=direccion_ip,
            navegador=navegador,
        )

        return super().list(request, *args, **kwargs)


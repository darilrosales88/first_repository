# gemar/views.py
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
from gemar.serializers import (
    PartePBIPSerializer, CargaViejaSerializer, ExistenciaMercanciaSerializer
)
from Administracion.permissions import IsGEMARUser, IsUFCUser, IsAdminUser

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
        # Filtro por fecha si se proporciona
        fecha = self.request.query_params.get('fecha')
        if fecha:
            queryset = queryset.filter(fecha_operacion=fecha)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creado_por=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def aprobar(self, request, pk=None):
        parte = self.get_object()
        parte.estado = 'APROBADO'
        parte.aprobado_por = request.user
        parte.save()
        return Response({'status': 'Parte PBIP aprobado'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def rechazar(self, request, pk=None):
        parte = self.get_object()
        parte.estado = 'RECHAZADO'
        parte.save()
        return Response({'status': 'Parte PBIP rechazado'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def cancelar(self, request, pk=None):
        parte = self.get_object()
        parte.estado = 'CANCELADO'
        parte.save()
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
    queryset = ExistenciaMercancia.objects.all()
    serializer_class = ExistenciaMercanciaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsGEMARUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['terminal', 'tipo', 'tipo_producto', 'producto', 'estado_registro']
    search_fields = ['producto__nombre', 'terminal__nombre']
    ordering_fields = ['fecha_operacion', 'fecha_creacion']
    ordering = ['-fecha_operacion']

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def aprobar(self, request, pk=None):
        existencia = self.get_object()
        existencia.estado_registro = 'APROBADO'
        existencia.aprobado_por = request.user
        existencia.save()
        return Response({'status': 'Existencia aprobada'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsGEMARUser | IsAdminUser])
    def rechazar(self, request, pk=None):
        existencia = self.get_object()
        existencia.estado_registro = 'RECHAZADO'
        existencia.save()
        return Response({'status': 'Existencia rechazada'}, status=status.HTTP_200_OK)

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
            'total_existencias': existencias.count(),
            'partes_pbip': PartePBIPSerializer(partes_pbip, many=True).data,
            'cargas_viejas': CargaViejaSerializer(cargas_viejas, many=True).data,
            'existencias': ExistenciaMercanciaSerializer(existencias, many=True).data
        }
        
        return Response(resumen)
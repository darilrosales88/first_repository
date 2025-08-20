from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from .models import en_trenes, producto_UFC
from nomencladores.models import (
    nom_tipo_equipo_ferroviario, 
    nom_equipo_ferroviario,
    nom_producto,
    nom_tipo_embalaje,
    nom_unidad_medida
)
from django.contrib.auth.models import Group

class EnTrenesTests(APITestCase):
    def setUp(self):
        # Crear usuario de prueba
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='ufc'
        )
        
        # Crear usuario visualizador
        self.viewer_user = User.objects.create_user(
            username='viewer',
            email='viewer@test.com',
            password='viewer123',
            role='ufc'
        )
        
        # Crear grupos
        self.admin_group = Group.objects.create(name='AdminUFC')
        self.viewer_group = Group.objects.create(name='VisualizadorUFC')
        
        # Asignar usuarios a grupos
        self.user.groups.add(self.admin_group)
        self.viewer_user.groups.add(self.viewer_group)
        
        # Crear datos necesarios para las pruebas
        self.tipo_equipo = nom_tipo_equipo_ferroviario.objects.create(
            tipo_equipo='locomotora',
            tipo_carga='carga_general',
            longitud=10.0,
            peso_neto_sin_carga=100.0,
            peso_maximo_con_carga=200.0
        )
        
        self.equipo = nom_equipo_ferroviario.objects.create(
            tipo_equipo=self.tipo_equipo,
            numero_identificacion='12345'
        )

        # Configurar cliente API
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_crear_tren(self):
        """Test para crear un nuevo tren"""
        url = reverse('en-trenes-list')
        data = {
            'locomotora': self.equipo.id,
            'tipo_origen': 'puerto',
            'origen': 'Puerto Test',
            'tipo_equipo': self.tipo_equipo.id,
            'estado': 'cargado',
            'tipo_destino': 'ac_ccd',
            'destino': 'Destino Test',
            'cantidad_vagones': 1,
            'equipo_vagon': self.equipo.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(en_trenes.objects.count(), 1)
        self.assertEqual(en_trenes.objects.get().origen, 'Puerto Test')

    def test_listar_trenes(self):
        """Test para listar trenes"""
        # Crear un tren de prueba
        en_trenes.objects.create(
            locomotora=self.equipo,
            tipo_origen='puerto',
            origen='Puerto Test',
            tipo_equipo=self.tipo_equipo,
            estado='cargado',
            tipo_destino='ac_ccd',
            destino='Destino Test',
            cantidad_vagones=1,
            equipo_vagon=self.equipo
        )
        
        url = reverse('en-trenes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filtrar_trenes(self):
        """Test para probar el filtrado de trenes"""
        # Crear dos trenes con diferentes orígenes
        en_trenes.objects.create(
            locomotora=self.equipo,
            tipo_origen='puerto',
            origen='Puerto A',
            tipo_equipo=self.tipo_equipo,
            estado='cargado',
            tipo_destino='ac_ccd',
            destino='Destino Test',
            cantidad_vagones=1,
            equipo_vagon=self.equipo
        )
        
        en_trenes.objects.create(
            locomotora=self.equipo,
            tipo_origen='puerto',
            origen='Puerto B',
            tipo_equipo=self.tipo_equipo,
            estado='cargado',
            tipo_destino='ac_ccd',
            destino='Destino Test',
            cantidad_vagones=1,
            equipo_vagon=self.equipo
        )
        
        url = reverse('en-trenes-list')
        response = self.client.get(f'{url}?search=Puerto A')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['origen'], 'Puerto A')

    def test_actualizar_tren(self):
        """Test para actualizar un tren existente"""
        tren = en_trenes.objects.create(
            locomotora=self.equipo,
            tipo_origen='puerto',
            origen='Puerto Original',
            tipo_equipo=self.tipo_equipo,
            estado='cargado',
            tipo_destino='ac_ccd',
            destino='Destino Test',
            cantidad_vagones=1,
            equipo_vagon=self.equipo
        )
        
        url = reverse('en-trenes-detail', kwargs={'pk': tren.pk})
        data = {
            'locomotora': self.equipo.id,
            'tipo_origen': 'puerto',
            'origen': 'Puerto Modificado',
            'tipo_equipo': self.tipo_equipo.id,
            'estado': 'cargado',
            'tipo_destino': 'ac_ccd',
            'destino': 'Destino Test',
            'cantidad_vagones': 2,
            'equipo_vagon': self.equipo.id
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(en_trenes.objects.get(pk=tren.pk).origen, 'Puerto Modificado')
        self.assertEqual(en_trenes.objects.get(pk=tren.pk).cantidad_vagones, 2)

    def test_eliminar_tren(self):
        """Test para eliminar un tren"""
        tren = en_trenes.objects.create(
            locomotora=self.equipo,
            tipo_origen='puerto',
            origen='Puerto Test',
            tipo_equipo=self.tipo_equipo,
            estado='cargado',
            tipo_destino='ac_ccd',
            destino='Destino Test',
            cantidad_vagones=1,
            equipo_vagon=self.equipo
        )
        
        url = reverse('en-trenes-detail', kwargs={'pk': tren.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(en_trenes.objects.count(), 0)

    def test_permisos_visualizador(self):
        """Test para verificar permisos de visualizador"""
        self.client.force_authenticate(user=self.viewer_user)
        
        # Intentar crear un tren (debe fallar)
        url = reverse('en-trenes-list')
        data = {
            'locomotora': self.equipo.id,
            'tipo_origen': 'puerto',
            'origen': 'Puerto Test',
            'tipo_equipo': self.tipo_equipo.id,
            'estado': 'cargado',
            'tipo_destino': 'ac_ccd',
            'destino': 'Destino Test',
            'cantidad_vagones': 1,
            'equipo_vagon': self.equipo.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verificar que puede listar trenes
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProductoUFCTests(APITestCase):
    def setUp(self):
        # Crear usuario de prueba
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='ufc'
        )
        
        # Crear grupo AdminUFC y agregar usuario
        self.admin_group = Group.objects.create(name='AdminUFC')
        self.user.groups.add(self.admin_group)
        
        # Crear datos necesarios para las pruebas
        self.producto = nom_producto.objects.create(
            nombre_producto='Producto Test',
            codigo_producto='TEST001'
        )
        
        self.tipo_embalaje = nom_tipo_embalaje.objects.create(
            clave='Embalaje Test'
        )
        
        self.unidad_medida = nom_unidad_medida.objects.create(
            unidad_medida='Unidad Test'
        )
        
        # Configurar cliente API
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_crear_producto(self):
        """Test para crear un nuevo producto"""
        url = reverse('producto-vagon-list')
        data = {
            'producto': self.producto.id,
            'tipo_embalaje': self.tipo_embalaje.id,
            'unidad_medida': self.unidad_medida.id,
            'cantidad': 100,
            'estado': 'lleno',
            'contiene': 'alimentos'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(producto_UFC.objects.count(), 1)
        self.assertEqual(producto_UFC.objects.get().cantidad, 100)

    def test_actualizar_producto(self):
        """Test para actualizar un producto existente"""
        producto_ufc = producto_UFC.objects.create(
            producto=self.producto,
            tipo_embalaje=self.tipo_embalaje,
            unidad_medida=self.unidad_medida,
            cantidad=100,
            estado='lleno',
            contiene='alimentos'
        )
        
        url = reverse('producto-vagon-detail', kwargs={'pk': producto_ufc.pk})
        data = {
            'producto': self.producto.id,
            'tipo_embalaje': self.tipo_embalaje.id,
            'unidad_medida': self.unidad_medida.id,
            'cantidad': 200,
            'estado': 'lleno',
            'contiene': 'alimentos'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(producto_UFC.objects.get(pk=producto_ufc.pk).cantidad, 200)

    def test_listar_productos(self):
        """Test para listar productos"""
        # Crear productos de prueba
        producto_UFC.objects.create(
            producto=self.producto,
            tipo_embalaje=self.tipo_embalaje,
            unidad_medida=self.unidad_medida,
            cantidad=100,
            estado='lleno',
            contiene='alimentos'
        )
        
        url = reverse('producto-vagon-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_eliminar_producto(self):
        """Test para eliminar un producto"""
        producto_ufc = producto_UFC.objects.create(
            producto=self.producto,
            tipo_embalaje=self.tipo_embalaje,
            unidad_medida=self.unidad_medida,
            cantidad=100,
            estado='lleno',
            contiene='alimentos'
        )
        
        url = reverse('producto-vagon-detail', kwargs={'pk': producto_ufc.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(producto_UFC.objects.count(), 0)

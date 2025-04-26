from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from .models import en_trenes, producto_UFC
from nomencladores.models import nom_tipo_equipo_ferroviario, nom_equipo_ferroviario
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
        
        # Crear grupo AdminUFC y agregar usuario
        self.admin_group = Group.objects.create(name='AdminUFC')
        self.user.groups.add(self.admin_group)
        
        # Crear datos necesarios para las pruebas
        self.tipo_equipo = nom_tipo_equipo_ferroviario.objects.create(
            tipo_equipo='locomotora',
            tipo_carga='carga_general'
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

from django.test import TestCase
from django.contrib.auth import get_user_model
from ufc.models import ufc_informe_ccd
from nomencladores.models import nom_provincia, nom_entidades,nom_pais,nom_osde_oace_organismo,nom_territorio
from Administracion.models import CustomUser
import logging

log=logging.Logger(name="###LOG:")

class UFCInformeCCDTestCase(TestCase):
      
    def setUp(self):
        #Creado logger
        #Crear pais
        self.pais= nom_pais.objects.create(
            nacionalidad="CUB",
            nombre_pais="Cuba"
        )
        log.info("Creado el pais")
        
        
        # Crear una provincia para las pruebas
        self.provincia = nom_provincia.objects.create(
            codigo="01",
            pais=self.pais,
            nombre_provincia="Habana",    
        )
        log.info("Creada la provincia")
        
        self.oasde=nom_osde_oace_organismo.objects.create(
            nombre="Paquito",
            abreviatura="Paquito",
            codigo_reeup="12245"
        )
        
        self.territorio=nom_territorio.objects.create(
            nombre_territorio= "Centro",
            abreviatura="Centro"
        )
        
        # Crear una entidad para las pruebas
        self.entidad = nom_entidades.objects.create(
            nombre="Paquito",
            abreviatura="Paqt",
            codigo_reeup="544112",
            osde_oace_organismo=self.oasde,       
            provincia=self.provincia,
            tipo_entidad="otros",
            territorio=self.territorio,
        )

        # Crear un usuario para las pruebas
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            entidad=self.entidad
        )
    
    def test_crear_pais(self):
        """
        Prueba la creacion del pais
        """
        self.pais= nom_pais.objects.create(
            nacionalidad="JAP",
            nombre_pais="Japan"
        )
        self.assertIsInstance(self.pais,nom_pais)
    
        log.info("Creado el pais")
    
    def test_crear_informe_ccd(self):
        """
        Prueba la creación de una instancia de ufc_informe_ccd.
        """
        informe = ufc_informe_ccd.objects.create(
            creado_por=self.user,
            comentarios="Este es un comentario de prueba."
        )

        # Verificar que la instancia fue creada
        self.assertIsInstance(informe, ufc_informe_ccd)

        # Verificar que la entidad y la provincia se asignaron correctamente desde el usuario
        self.assertEqual(informe.entidad, self.entidad)
        self.assertEqual(informe.provincia, self.provincia)

        # Verificar el estado inicial del parte
        self.assertEqual(informe.estado_parte, "Creado")

        # Verificar los comentarios
        self.assertEqual(informe.comentarios, "Este es un comentario de prueba.")

    def test_str_method(self):
        """
        Prueba el método __str__ del modelo ufc_informe_ccd.
        """
        informe = ufc_informe_ccd.objects.create(
            creado_por=self.user
        )
        expected_str = f"Fecha de operación {informe.fecha_operacion} - fecha actual: {informe.fecha_actual}"
        self.assertEqual(str(informe), expected_str)

    def test_aprobacion_informe(self):
        """
        Prueba la aprobación de un informe.
        """
        aprobador = CustomUser.objects.create_user(
            username="aprobador",
            password="testpassword"
        )
        informe = ufc_informe_ccd.objects.create(
            creado_por=self.user
        )
        informe.aprobado_por = aprobador
        informe.estado_parte = "Aprobado"
        informe.save()

        self.assertEqual(informe.estado_parte, "Aprobado")
        self.assertEqual(informe.aprobado_por, aprobador)


import random
from django.core.management.base import BaseCommand
from faker import Faker
from nomencladores.models import (
    nom_contenedor, nom_cargo, nom_territorio,
    nom_unidad_medida, nom_osde_oace_organismo,
    nom_tipo_equipo_ferroviario,
    nom_estado_tecnico, nom_producto, nom_tipo_embalaje, nom_incidencia,
    nom_tipo_estructura_ubicacion
)

fake = Faker()

class Command(BaseCommand):
    help = 'Genera 100 registros aleatorios para cada modelo'

    def handle(self, *args, **kwargs):
        
        self.populate_nom_incidencia()
        

        self.stdout.write(self.style.SUCCESS('Todos los modelos han sido poblados exitosamente.'))



    def populate_nom_incidencia(self):
        for _ in range(100):
            nom_incidencia.objects.create(
                codigo_incidencia=fake.bothify(text='??##'),
                nombre_incidencia=fake.word(),
                tipo_imputable=random.choice([ti[0] for ti in nom_incidencia.t_imputable]),
            )

    
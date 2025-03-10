import random
from django.core.management.base import BaseCommand
from .models import nom_contenedor  # Asegúrate de importar tu modelo correctamente

class Command(BaseCommand):
    help = 'Genera 100 registros aleatorios para la tabla nom_contenedor'

    def handle(self, *args, **kwargs):
        # Opciones para tipo_contenedor y longitud
        tipos_contenedor = [tc[0] for tc in nom_contenedor.t_contenedor]
        longitudes = [lg[0] for lg in nom_contenedor.longit]

        for i in range(100):
            # Generar un id_contenedor válido
            letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
            numeros = ''.join(random.choices('0123456789', k=7))
            id_contenedor = f"{letras}{numeros}"

            # Generar un código ISO válido
            codigo_iso = f"{random.randint(10, 99)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(0, 9)}"

            # Crear el registro
            nom_contenedor.objects.create(
                id_contenedor=id_contenedor,
                tipo_contenedor=random.choice(tipos_contenedor),
                longitud=random.choice(longitudes),
                codigo_iso=codigo_iso,
            )

        self.stdout.write(self.style.SUCCESS('100 registros creados exitosamente.'))
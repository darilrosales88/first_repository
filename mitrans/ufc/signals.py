from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import (ufc_informe_operativo,                     
                     vagones_productos,
                     Situado_Carga_Descarga,
                     por_situar,
                     vagon_cargado_descargado,
                     registro_vagones_cargados,
                     en_trenes,
                     arrastres,
                     rotacion_vagones


)
from django.db import transaction

@receiver(pre_save, sender=ufc_informe_operativo)
def borrar_registros_antiguos(sender, instance, **kwargs):
    """
    Borra los registros con fecha diferente al día actual de los modelos cuando se crea un nuevo informe
    operativo .
    """
    if instance.pk is None:  # Solo para nuevos registros
        hoy = timezone.now().date()
        
        # Verificar si ya existe un informe con la fecha de hoy
        existe_informe_hoy = sender.objects.filter(
            fecha_operacion__date=hoy
        ).exists()
        
        if not existe_informe_hoy:
            # Borrar todos los registros de ambos modelos
            with transaction.atomic():
                vagon_cargado_descargado.objects.all().delete()
                vagones_productos.objects.all().delete()
                Situado_Carga_Descarga.objects.all().delete()
                por_situar.objects.all().delete()
                registro_vagones_cargados.objects.all().delete()
                en_trenes.objects.all().delete()
                arrastres.objects.all().delete()
                rotacion_vagones.objects.all().delete()

                
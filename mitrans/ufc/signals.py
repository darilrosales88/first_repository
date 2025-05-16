from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime
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
from django.db.models import Sum
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
                
@receiver(post_delete,sender=vagon_cargado_descargado)
@receiver(post_save, sender=vagon_cargado_descargado)
def actualizar_rotacion(sender,instance,**kwargs):
    """
    Se ejecuta después de guardar un vagon_cargado_descargado.
    Busca o crea un registro en rotacion_vagones asociado al tipo de equipo ferroviario.
    Actualiza: plan_carga, real_carga, plan_rotacion, real_rotacion
    """
    print("Se creo un registro cargado")
    if not instance.tipo_equipo_ferroviario:
        print("El registro no tiene tipo de equipo ferroviario.")
        return
    tipo_equipo = instance.tipo_equipo_ferroviario
    
    rotaciones=rotacion_vagones.objects.filter(tipo_equipo_ferroviario=tipo_equipo)
    for rotacion in rotaciones:
            actualizar_datos_rotacion(rotacion, tipo_equipo)
            rotacion.save()
            print(f"Se actualizó el registro de rotación: {rotacion.id}")

    # Filtrar solo los vagones cargados/descargados para este tipo de equipo

def actualizar_datos_rotacion(rotacion, tipo_equipo):

    # Filtrar los vagones cargados/descargados para este tipo de equipo
    hoy=timezone.now().date()
    registros = vagon_cargado_descargado.objects.filter(
        tipo_equipo_ferroviario=tipo_equipo,
        operacion='carga',
        fecha__date=hoy
    )
    total_plan_carga =registros.aggregate(Sum("plan_diario_carga_descarga"))['plan_diario_carga_descarga__sum'] or 0
    total_real_carga = registros.aggregate(Sum('real_carga_descarga'))['real_carga_descarga__sum'] or 0
    en_servicio = rotacion.en_servicio or 1  # Evitar división por cero

    # Actualizar campos de rotación
    rotacion.plan_carga = total_plan_carga
    rotacion.real_carga = total_real_carga
    rotacion.plan_rotacion = round(total_plan_carga / en_servicio, 2) if en_servicio else 0
    rotacion.real_rotacion = round(total_real_carga / en_servicio, 2) if en_servicio else 0
    
    


@receiver(post_save, sender=vagon_cargado_descargado)
@receiver(post_save, sender=Situado_Carga_Descarga)
@receiver(post_save, sender=por_situar)
@receiver(post_save, sender=arrastres)
@receiver(post_save, sender=en_trenes)
@receiver(post_save, sender=vagones_productos)
@receiver(post_save, sender=rotacion_vagones)
def asignar_informe_operativo(sender, instance, created, **kwargs):
    if created and not instance.informe_operativo:
        fecha_registro = instance.fecha.date() if hasattr(instance, 'fecha') else datetime.now().date()
        informe = ufc_informe_operativo.objects.get(
            fecha_operacion__date=fecha_registro
        )
        instance.informe_operativo = informe
        instance.save()
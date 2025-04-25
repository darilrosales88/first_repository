from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import vagones_productos, vagon_cargado_descargado, Situado_Carga_Descarga

#@receiver([post_save, post_delete], sender=vagon_cargado_descargado)
#@receiver([post_save, post_delete], sender=Situado_Carga_Descarga)
def actualizar_campos_calculados(sender, instance, **kwargs):
    """
    Actualiza los campos calculados en vagones_productos cuando cambian los modelos relacionados
    """
    # Filtramos los productos relacionados con esta instancia
    productos_relacionados = instance.producto.all() if hasattr(instance, 'producto') else []
    
    # Actualizamos todos los vagones_productos afectados
    for vagon in vagones_productos.objects.filter(
        origen=instance.origen,
        producto__in=productos_relacionados
    ).distinct():
        # Cálculos (igual que en tu código original)
        vagon.plan_dia = vagon_cargado_descargado.objects.filter(
            operacion='carga',
            origen=vagon.origen,
            producto__in=vagon.producto.all()
        ).aggregate(total=Sum('plan_diario_carga_descarga'))['total'] or 0
        
        vagon.vagones_situados = Situado_Carga_Descarga.objects.filter(
            operacion='carga',
            origen=vagon.origen,
            producto__producto__in=vagon.producto.all()
        ).aggregate(total=Sum('situados'))['total'] or 0
        
        vagon.vagones_cargados = vagon_cargado_descargado.objects.filter(
            operacion='carga',
            origen=vagon.origen,
            producto__in=vagon.producto.all()
        ).aggregate(total=Sum('real_carga_descarga'))['total'] or 0
        
        vagon.plan_aseguramiento_proximos_dias = vagon.vagones_cargados
        vagon.save(update_fields=[
            'plan_dia',
            'vagones_situados',
            'vagones_cargados',
            'plan_aseguramiento_proximos_dias'
        ])
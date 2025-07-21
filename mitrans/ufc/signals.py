from datetime import date
from django.db import models 
from django.db.models.signals import pre_save, post_save, post_delete,pre_delete
from django.db.models import Sum, Prefetch,Subquery, OuterRef
from django.db.models.functions import TruncDate
from django.db import transaction
from django.dispatch import receiver
from django.utils import timezone
from nomencladores.models import nom_equipo_ferroviario
from .models import (
    ufc_informe_operativo,
    vagones_productos,
    Situado_Carga_Descarga,
    por_situar,
    vagon_cargado_descargado,
    vagones_dias,
    registro_vagones_cargados,
    en_trenes,
    arrastres,
    rotacion_vagones,
    producto_UFC,
)
from ufc.serializers import actualizar_estado_equipo_ferroviario

# @receiver(pre_save, sender=ufc_informe_operativo)
# def resetear_estados(sender, instance, **kwargs):
#     """
#     Borra los registros con fecha diferente al día actual de los modelos cuando se crea un nuevo informe
#     operativo .
#     """
#     if instance.pk is None:  # Solo para nuevos registros
#         hoy = timezone.now().date()

#         # Verificar si ya existe un informe con la fecha de hoy
#         existe_informe_hoy = sender.objects.filter(fecha_operacion__date=hoy).exists()

#         if not existe_informe_hoy:
#             # Borrar todos los registros de ambos modelos
#             equipos=[]
#             registros_cargados=vagon_cargado_descargado.objects.all()
#             for registro in registros_cargados:
#                 equipos.append()
#             vagones_productos.objects.all()
#             Situado_Carga_Descarga.objects.all()
#             por_situar.objects.all()
#             registro_vagones_cargados.objects.all()
#             en_trenes.objects.all()
#             arrastres.objects.all()


@receiver(post_save, sender=ufc_informe_operativo)
@receiver(pre_delete, sender=ufc_informe_operativo)
def actualizar_estado_vagones(sender, instance:ufc_informe_operativo, **kwargs):
    """
    Signal que actualiza el estado de los vagones asociados cuando cambia estado_parte
    del informe operativo, considerando todas las relaciones posibles.
    """
    #print(kwargs,sender)
    # Solo ejecutar si es una actualización y estado_parte está en los campos actualizados
    if(not kwargs.get('origin')):
        if kwargs.get('created', False) or instance.estado_parte=="Creado":
            return
    #print(kwargs,sender)
    with transaction.atomic():
        # Bloquear el informe para evitar condiciones de carrera
        informe = ufc_informe_operativo.objects.select_for_update().get(pk=instance.pk)
        updated=0
        # 1. Vagones a través de por_situar -> vagones_dias
####-----------Aqui se pone a disponible Los estados de Por Situar, Situados, Pendiente---------########        
        vagones_ids = vagones_dias.objects.filter(
        por_situar_vagones_dias__informe_operativo=informe,
    ).values_list('equipo_ferroviario_id', flat=True)
        
        vagones_partes = nom_equipo_ferroviario.objects.filter(id__in=list(vagones_ids))
        updated += vagones_partes.update(estado_actual='Disponible')
    #     vagones_por_situar=nom_equipo_ferroviario.objects.filter(
    #     registro_por_dias__por_situar_vagones_dias__informe_operativo_id=informe.id
    # ).distinct()
        
        vagones_ids = vagones_dias.objects.filter(
        situados_vagones_dias__informe_operativo=informe,
    ).values_list('equipo_ferroviario_id', flat=True)
        print(vagones_ids)
        vagones_partes = nom_equipo_ferroviario.objects.filter(id__in=list(vagones_ids))
        updated += vagones_partes.update(estado_actual='Disponible')


        vagones_ids = vagones_dias.objects.filter(
        arrastre_vagones_dias__informe_operativo=informe,
    ).values_list('equipo_ferroviario_id', flat=True)
        
        vagones_partes = nom_equipo_ferroviario.objects.filter(id__in=list(vagones_ids))
        updated += vagones_partes.update(estado_actual='Disponible')
####-----------Aqui se pone a disponible Los estado Cargado/Descargado---------########       
        # Obtener los números de identificación de los vagones asociados
        vagones_cargados=nom_equipo_ferroviario.objects.filter(
        numero_identificacion__in=Subquery(
            registro_vagones_cargados.objects.filter(
                registro_vagones_cargados__informe_operativo=informe
            ).values_list('no_id', flat=True)
        )
    )
        #vagones_cargados = nom_equipo_ferroviario.objects.filter(id__in=list(vagones_cargados))
        updated += vagones_cargados.update(estado_actual='Disponible')
        
        
        # 2. Vagones a través de la relación ManyToMany en en_trenes
####-----------Aqui se pone a disponible Los estado En Trenes---------########     
        vagones_en_trenes = nom_equipo_ferroviario.objects.filter(
            en_trenes_vagones__informe_operativo=informe
        ).distinct()
        #print (vagones_partes,vagones_ids)
        
        
        updated += vagones_en_trenes.update(estado_actual='Disponible')
        
        # Opcional: Registrar el cambio
        if updated > 0:
            print(f"Informe {informe.id}: {updated} vagones actualizados a Disponible")
            

@receiver(post_save, sender=ufc_informe_operativo)
def set_entidad_from_creator(sender, instance, **kwargs):
    print("set_entidad_from_creator signal triggered")
    print(instance.entidad, instance.creado_por)
    print(instance)
    
    if not instance.entidad and instance.creado_por:
        instance.entidad = instance.creado_por.entidad


@receiver(post_delete, sender=vagon_cargado_descargado)
@receiver(post_save, sender=vagon_cargado_descargado)
def actualizar_rotacion(sender, instance, **kwargs):
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
    informe=instance.informe_operativo

    rotaciones = rotacion_vagones.objects.filter(tipo_equipo_ferroviario=tipo_equipo, informe_operativo=informe)
    for rotacion in rotaciones:
        actualizar_datos_rotacion(rotacion, tipo_equipo, informe)
        rotacion.save()
        print(f"Se actualizó el registro de rotación: {rotacion.id}")

    # Filtrar solo los vagones cargados/descargados para este tipo de equipo


def actualizar_datos_rotacion(rotacion, tipo_equipo,informe):

    # Filtrar los vagones cargados/descargados para este tipo de equipo
    hoy = timezone.now().date()
    registros = vagon_cargado_descargado.objects.filter(
        tipo_equipo_ferroviario=tipo_equipo, operacion="carga", fecha__date=hoy,informe_operativo=informe
    )
    total_plan_carga = (
        registros.aggregate(Sum("plan_diario_carga_descarga"))[
            "plan_diario_carga_descarga__sum"
        ]
        or 0
    )
    total_real_carga = (
        registros.aggregate(Sum("real_carga_descarga"))["real_carga_descarga__sum"] or 0
    )
    en_servicio = rotacion.en_servicio or 1  # Evitar división por cero

    # Actualizar campos de rotación
    rotacion.plan_carga = total_plan_carga
    rotacion.real_carga = total_real_carga
    rotacion.plan_rotacion = (
        round(total_plan_carga / en_servicio, 2) if en_servicio else 0
    )
    rotacion.real_rotacion = (
        round(total_real_carga / en_servicio, 2) if en_servicio else 0
    )




# funcion que calcula de forma automatica los campos del parte ufc_informe_operativo
@receiver(post_save, sender=vagon_cargado_descargado)
@receiver(post_save, sender=Situado_Carga_Descarga)
@receiver(post_save, sender=vagones_productos)
def calcular_informe_operativo_diario(sender, instance, created, **kwargs):
    """
    Calcula y actualiza los datos del informe operativo diario.
    Se ejecuta después de guardar un vagon_cargado_descargado.
    """
    try:
        # Usamos una transacción atómica para evitar inconsistencias
        with transaction.atomic():
            # Obtener la fecha actual (sin la hora)
            hoy = date.today()

            informe = (
                ufc_informe_operativo.objects.filter(fecha_operacion__date=hoy)
                .order_by("-fecha_operacion")
                .first()
            )

            # 1. Sumatoria de plan_mensual de vagones_productos (solo del día actual)
            plan_mensual_total = (
                vagones_productos.objects.filter(fecha__date=hoy).aggregate(
                    total=Sum("plan_mensual")
                )["total"]
                or 0
            )

            # 2. Sumatoria de plan_diario_carga_descarga (solo del día actual)
            plan_diario_total = (
                vagon_cargado_descargado.objects.filter(fecha__date=hoy).aggregate(
                    total=Sum("plan_diario_carga_descarga")
                )["total"]
                or 0
            )

            # 3. Sumatoria de real_carga_descarga (solo del día actual)
            real_total = (
                vagon_cargado_descargado.objects.filter(fecha__date=hoy).aggregate(
                    total=Sum("real_carga_descarga")
                )["total"]
                or 0
            )

            # 4. Sumatoria de situados (solo del día actual) - Versión compatible
            situados_total = 0
            situados_qs = Situado_Carga_Descarga.objects.filter(fecha__date=hoy).only(
                "situados"
            )

            for situado in situados_qs:
                try:
                    situados_total += int(situado.situados) if situado.situados else 0
                except (ValueError, TypeError):
                    continue

            # 5. Sumatoria de plan_acumulado_actual (solo del día actual)
            plan_acumulado_actual = (
                vagones_productos.objects.filter(fecha__date=hoy).aggregate(
                    total=Sum("plan_acumulado_actual")
                )["total"]
                or 0
            )

            # 6. Sumatoria de real_acumulado_actual (solo del día actual)
            real_acumulado_actual = (
                vagones_productos.objects.filter(fecha__date=hoy).aggregate(
                    total=Sum("real_acumulado_actual")
                )["total"]
                or 0
            )

            # Actualizar el informe con los valores calculados
            informe.plan_mensual_total = plan_mensual_total
            informe.plan_diario_total_vagones_cargados = plan_diario_total
            informe.real_total_vagones_cargados = real_total
            informe.total_vagones_situados = situados_total
            informe.plan_total_acumulado_actual = plan_acumulado_actual
            informe.real_total_acumulado_actual = real_acumulado_actual
            informe.save()

    except Exception as e:
        # En producción, usa logging.getLogger(__name__).error(...)
        print(f"Error al calcular el informe operativo: {str(e)}")
        # No relanzamos la excepción para no interrumpir el flujo principal


# ejecutar la funcion de actualizacion de los campos del parte cuando se elimina uno de los registros de los modelos que la activan
# Cuando se elimine un registro de unode  esos modelos, se llama a la función recalcular_informe_operativo_al_eliminar
# Esta función a su vez llamará a calcular_informe_operativo_diario con created=False (ya que no es una creación)
# La función original recalculará todos los valores del informe operativo basándose en los registros restantes
@receiver(post_delete, sender=vagon_cargado_descargado)
@receiver(post_delete, sender=Situado_Carga_Descarga)
@receiver(post_delete, sender=vagones_productos)
def recalcular_informe_operativo_al_eliminar(sender, instance, **kwargs):
    """
    Recalcula el informe operativo cuando se elimina un registro de los modelos relacionados
    """
    calcular_informe_operativo_diario(sender, instance, created=False, **kwargs)




# funcion que calcula automaticamente los valores de los campos de vagones_productos
@receiver(post_save, sender=vagon_cargado_descargado)
@receiver(post_save, sender=Situado_Carga_Descarga)
def actualizar_campos_automaticos_vagones_productos(sender, instance, **kwargs):
    """Actualiza los campos automáticos en vagones_productos cuando hay cambios
    en los modelos relacionados vagon_cargado_descargado, Situado_Carga_Descarga"""

    # Obtener la fecha actual
    hoy = timezone.now().date()

    # Verificar si es el primer día del mes
    es_primer_dia_mes = hoy.day == 1

    # Obtener el año actual
    año_actual = hoy.year

    # Verificar si hay otros informes operativos en el año actual
    informes_año_actual = ufc_informe_operativo.objects.filter(
        fecha_operacion__year=año_actual
    ).exclude(fecha_operacion__date=hoy)

    es_unico_informe_año = not informes_año_actual.exists()

    with transaction.atomic():
        # Obtener todos los objetos vagones_productos que necesitan actualización
        objetos_actualizar = vagones_productos.objects.all()

        for vagon_producto in objetos_actualizar:
            # Actualizar campos básicos
            plan_dia = (
                vagon_cargado_descargado.objects.filter(operacion="carga").aggregate(
                    total=Sum("plan_diario_carga_descarga")
                )["total"]
                or 0
            )

            vagones_cargados = (
                vagon_cargado_descargado.objects.filter(operacion="carga",).aggregate(
                    total=Sum("real_carga_descarga")
                )["total"]
                or 0
            )

            vagones_situados = (
                Situado_Carga_Descarga.objects.filter(operacion="carga",).aggregate(
                    total=Sum("situados")
                )["total"]
                or 0
            )

            plan_aseguramiento = (
                vagon_cargado_descargado.objects.filter(operacion="carga",).aggregate(
                    total=Sum("real_carga_descarga")
                )["total"]
                or 0
            )

            # Lógica para campos acumulados según los casos especificados
            if es_unico_informe_año and es_primer_dia_mes:
                # Caso 3: Único informe en el año y es primer día del mes
                vagon_producto.plan_acumulado_dia_anterior = 0
                vagon_producto.real_acumulado_dia_anterior = 0
                vagon_producto.plan_acumulado_actual = (
                    vagon_producto.plan_acumulado_dia_anterior + plan_dia
                )
                vagon_producto.real_acumulado_actual = (
                    vagon_producto.real_acumulado_dia_anterior + vagones_cargados
                )
                vagon_producto.plan_acumulado_anual = (
                    vagon_producto.plan_acumulado_anual + plan_dia
                )
                vagon_producto.real_acumulado_anual = (
                    vagon_producto.real_acumulado_anual + vagones_cargados
                )

            elif es_unico_informe_año and not es_primer_dia_mes:
                # Caso 4: Único informe en el año pero no es primer día del mes
                vagon_producto.plan_acumulado_actual = (
                    vagon_producto.plan_acumulado_dia_anterior + plan_dia
                )
                vagon_producto.real_acumulado_actual = (
                    vagon_producto.real_acumulado_dia_anterior + vagones_cargados
                )
                vagon_producto.plan_acumulado_anual = (
                    vagon_producto.plan_acumulado_anual + plan_dia
                )
                vagon_producto.real_acumulado_anual = (
                    vagon_producto.real_acumulado_anual + vagones_cargados
                )

            elif not es_unico_informe_año and es_primer_dia_mes:
                # Caso 5: No es único informe en el año pero es primer día del mes
                vagon_producto.plan_acumulado_dia_anterior = 0
                vagon_producto.real_acumulado_dia_anterior = 0
                vagon_producto.plan_acumulado_actual = (
                    vagon_producto.plan_acumulado_dia_anterior + plan_dia
                )
                vagon_producto.real_acumulado_actual = (
                    vagon_producto.real_acumulado_dia_anterior + vagones_cargados
                )
                vagon_producto.plan_acumulado_anual = (
                    vagon_producto.plan_acumulado_anual + plan_dia
                )
                vagon_producto.real_acumulado_anual = (
                    vagon_producto.real_acumulado_anual + vagones_cargados
                )

            else:
                # Caso 6: No es único informe en el año ni es primer día del mes
                vagon_producto.plan_acumulado_actual = (
                    vagon_producto.plan_acumulado_dia_anterior + plan_dia
                )
                vagon_producto.real_acumulado_actual = (
                    vagon_producto.real_acumulado_dia_anterior + vagones_cargados
                )
                vagon_producto.plan_acumulado_anual = (
                    vagon_producto.plan_acumulado_anual + plan_dia
                )
                vagon_producto.real_acumulado_anual = (
                    vagon_producto.real_acumulado_anual + vagones_cargados
                )

            # Actualizar campos básicos
            vagon_producto.plan_dia = plan_dia
            vagon_producto.vagones_situados = vagones_situados
            vagon_producto.vagones_cargados = vagones_cargados
            vagon_producto.plan_aseguramiento_proximos_dias = plan_aseguramiento

            # Validar campos obligatorios
            campos_obligatorios = [
                "plan_mensual",
                "plan_anual",
                "plan_acumulado_dia_anterior",
                "real_acumulado_dia_anterior",
                "plan_acumulado_actual",
                "real_acumulado_actual",
                "plan_acumulado_anual",
                "real_acumulado_anual",
            ]

            campos_vacios = [
                campo
                for campo in campos_obligatorios
                if getattr(vagon_producto, campo) is None
            ]

            if campos_vacios:
                print(
                    f"Advertencia: Los siguientes campos están vacíos en el registro {vagon_producto.id}: {', '.join(campos_vacios)}"
                )

            # Guardar todos los cambios
            vagon_producto.save()


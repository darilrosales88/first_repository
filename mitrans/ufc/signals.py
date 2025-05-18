from datetime import date

from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Sum, Prefetch
from django.db.models.functions import TruncDate
from django.db import transaction
from django.dispatch import receiver
from django.utils import timezone
from .models import (
    ufc_informe_operativo,
    vagones_productos,
    Situado_Carga_Descarga,
    por_situar,
    vagon_cargado_descargado,
    registro_vagones_cargados,
    en_trenes,
    arrastres,
    rotacion_vagones,
    HistorialArrastres,
    HistorialVagonCargadoDescargado,
    HistorialVagonesProductos,
    HistorialVagonPorSituar,
    producto_UFC,
    HistorialEnTrenes,
    HistorialRotacionVagones,
    HistorialSituadoCargaDescarga,
)


@receiver(pre_save, sender=ufc_informe_operativo)
def borrar_registros_antiguos(sender, instance, **kwargs):
    """
    Borra los registros con fecha diferente al día actual de los modelos cuando se crea un nuevo informe
    operativo .
    """
    if instance.pk is None:  # Solo para nuevos registros
        hoy = timezone.now().date()

        # Verificar si ya existe un informe con la fecha de hoy
        existe_informe_hoy = sender.objects.filter(fecha_operacion__date=hoy).exists()

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

    rotaciones = rotacion_vagones.objects.filter(tipo_equipo_ferroviario=tipo_equipo)
    for rotacion in rotaciones:
        actualizar_datos_rotacion(rotacion, tipo_equipo)
        rotacion.save()
        print(f"Se actualizó el registro de rotación: {rotacion.id}")

    # Filtrar solo los vagones cargados/descargados para este tipo de equipo


def actualizar_datos_rotacion(rotacion, tipo_equipo):

    # Filtrar los vagones cargados/descargados para este tipo de equipo
    hoy = timezone.now().date()
    registros = vagon_cargado_descargado.objects.filter(
        tipo_equipo_ferroviario=tipo_equipo, operacion="carga", fecha__date=hoy
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


# Señal para crear el historial al guardar
@receiver(post_save, sender=rotacion_vagones)
def crear_historial_rotacion_vagones(sender, instance, created, **kwargs):
    if not created:
        return

    def _crear_historial():
        fecha_registro = instance.fecha.date()

        informe = (
            ufc_informe_operativo.objects.annotate(
                fecha_op=TruncDate("fecha_operacion")
            )
            .filter(fecha_op=fecha_registro)
            .first()
        )

        if not informe:
            return

        # Obtener el registro completo con relaciones
        registro_completo = rotacion_vagones.objects.select_related(
            "tipo_equipo_ferroviario"
        ).get(pk=instance.pk)

        # Serializar datos principales
        datos_rotacion = {
            "id": registro_completo.id,
            "tipo_equipo": {
                "id": registro_completo.tipo_equipo_ferroviario.id,
                "nombre": registro_completo.tipo_equipo_ferroviario.get_tipo_equipo_display(),
            },
            "en_servicio": registro_completo.en_servicio,
            "plan_carga": registro_completo.plan_carga,
            "real_carga": registro_completo.real_carga,
            "plan_rotacion": registro_completo.plan_rotacion,
            "real_rotacion": registro_completo.real_rotacion,
            "fecha": str(registro_completo.fecha),
            "actualizado_el": str(registro_completo.actualizado_el),
        }

        HistorialRotacionVagones.objects.create(
            informe_operativo=informe, datos_rotacion=datos_rotacion
        )

    transaction.on_commit(_crear_historial)


# Señal para eliminar el historial
@receiver(post_delete, sender=rotacion_vagones)
def eliminar_historial_rotacion_vagones(sender, instance, **kwargs):
    try:
        HistorialRotacionVagones.objects.filter(
            datos_rotacion__icontains={"id": instance.id}
        ).delete()
    except Exception as e:
        print(f"Error eliminando historial de rotación de vagones: {str(e)}")


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


# Señal para crear el historial cuando se crea un arrastre
@receiver(post_save, sender=arrastres)
def crear_historial_arrastre(sender, instance, created, **kwargs):
    """
    Crea un historial de arrastre asociado al informe operativo de su fecha
    """
    if not created:  # Solo nos interesan las creaciones nuevas
        return

    def _crear_historial_arrastre_despues_de_guardar():
        # Obtener solo la fecha (sin hora) del arrastre
        fecha_arrastre = instance.fecha.date()

        # Buscar si existe un informe operativo para esta fecha
        informe = (
            ufc_informe_operativo.objects.annotate(
                fecha_op=TruncDate("fecha_operacion")
            )
            .filter(fecha_op=fecha_arrastre)
            .first()
        )

        if not informe:
            return  # No hacer nada si no hay informe para esta fecha

        # Obtener el arrastre con todas sus relaciones
        arrastre_completo = arrastres.objects.prefetch_related(
            "producto__producto", "producto__tipo_embalaje", "producto__unidad_medida"
        ).get(pk=instance.pk)

        # Serializar datos del arrastre
        datos_arrastre = {
            "id": arrastre_completo.id,
            "tipo_origen": arrastre_completo.tipo_origen,
            "origen": arrastre_completo.origen,
            "tipo_equipo": arrastre_completo.tipo_equipo,
            "estado": arrastre_completo.estado,
            "cantidad_vagones": arrastre_completo.cantidad_vagones,
            "tipo_destino": arrastre_completo.tipo_destino,
            "destino": arrastre_completo.destino,
            "fecha": str(arrastre_completo.fecha),
        }

        # Serializar productos relacionados
        productos = []
        for producto in arrastre_completo.producto.all():
            productos.append(
                {
                    "id": producto.id,
                    "producto_name": producto.producto.nombre_producto,
                    "tipo_embalaje_name": producto.tipo_embalaje.nombre_tipo_embalaje
                    if producto.tipo_embalaje
                    else None,
                    "unidad_medida_simbolo": producto.unidad_medida.simbolo
                    if producto.unidad_medida
                    else None,
                    "cantidad": producto.cantidad,
                    "estado": producto.estado,
                    "contiene": producto.contiene,
                }
            )

        # Crear registro de historial
        HistorialArrastres.objects.create(
            informe_operativo=informe,
            datos_arrastre=datos_arrastre,
            datos_productos=productos,
        )

    # Usamos transaction.on_commit para ejecutar después de que la transacción se complete
    transaction.on_commit(_crear_historial_arrastre_despues_de_guardar)


# Señal para eliminar el historial cuando se elimina un arrastre
@receiver(post_delete, sender=arrastres)
def eliminar_historial_arrastre(sender, instance, **kwargs):
    """
    Elimina el registro de historial asociado cuando se elimina un arrastre
    """
    try:
        # Buscar el historial que contiene datos de este arrastre
        historiales = HistorialArrastres.objects.filter(
            datos_arrastre__icontains={"id": instance.id}
        )

        # Eliminar todos los registros de historial encontrados
        historiales.delete()

    except Exception as e:
        print(f"Error al eliminar historial del arrastre {instance.id}: {str(e)}")


# funcion que se encarga de almacenar el historial de vagon_cargado_descargado, la activa la creacion del modelo padre
@receiver(post_save, sender=ufc_informe_operativo)
def crear_historial_vagones_al_aprobar(sender, instance, created, **kwargs):
    """
    Crea historial de todos los vagones cargados/descargados cuando se aprueba el informe operativo
    """
    if instance.estado_parte == "Aprobado":
        # Obtener la fecha del informe operativo (sin hora)
        fecha_informe = instance.fecha_operacion.date()

        # Obtener todos los vagones cargados/descargados de esta fecha
        vagones = (
            vagon_cargado_descargado.objects.filter(fecha__date=fecha_informe)
            .select_related("tipo_equipo_ferroviario")
            .prefetch_related(
                "producto__producto",
                "producto__tipo_embalaje",
                "producto__unidad_medida",
                "registros_vagones",
            )
        )

        # Crear historial para cada vagon
        for vagon in vagones:
            # Serializar datos del vagon
            datos_vagon = {
                "id": vagon.id,
                "tipo_origen": vagon.tipo_origen,
                "origen": vagon.origen,
                "tipo_equipo_ferroviario_id": vagon.tipo_equipo_ferroviario.id
                if vagon.tipo_equipo_ferroviario
                else None,
                "tipo_equipo_ferroviario_name": vagon.tipo_equipo_ferroviario.get_tipo_equipo_display()
                if vagon.tipo_equipo_ferroviario
                else None,
                "estado": vagon.get_estado_display(),
                "operacion": vagon.operacion,
                "plan_diario_carga_descarga": vagon.plan_diario_carga_descarga,
                "real_carga_descarga": vagon.real_carga_descarga,
                "tipo_destino": vagon.tipo_destino,
                "destino": vagon.destino,
                "causas_incumplimiento": vagon.causas_incumplimiento,
                "fecha": str(vagon.fecha),
            }

            # Serializar productos relacionados
            productos = []
            for producto in vagon.producto.all():
                productos.append(
                    {
                        "id": producto.id,
                        "producto_name": producto.producto.nombre_producto,
                        "tipo_embalaje_name": producto.tipo_embalaje.nombre_tipo_embalaje
                        if producto.tipo_embalaje
                        else None,
                        "unidad_medida_simbolo": producto.unidad_medida.simbolo
                        if producto.unidad_medida
                        else None,
                        "cantidad": producto.cantidad,
                        "estado": producto.get_estado_display(),
                        "contiene": producto.contiene,
                    }
                )

            # Serializar registros de vagones relacionados
            registros = []
            for registro in vagon.registros_vagones.all():
                registros.append(
                    {
                        "id": registro.id,
                        "no_id": registro.no_id,
                        "fecha_despacho": str(registro.fecha_despacho)
                        if registro.fecha_despacho
                        else None,
                        "tipo_origen": registro.tipo_origen,
                        "origen": registro.origen,
                        "fecha_llegada": str(registro.fecha_llegada)
                        if registro.fecha_llegada
                        else None,
                        "observaciones": registro.observaciones,
                    }
                )

            # Crear o actualizar registro de historial
            HistorialVagonCargadoDescargado.objects.update_or_create(
                informe_operativo=instance,
                defaults={
                    "datos_vagon": datos_vagon,
                    "datos_productos": productos,
                    "datos_registros_vagones": registros,
                },
            )


# Elimina el registro del historial asociado al vagon que se esta eliminando
@receiver(post_delete, sender=vagon_cargado_descargado)
def eliminar_historial_vagon_cargado_descargado(sender, instance, **kwargs):
    """
    Elimina el registro de historial asociado cuando se elimina un vagon_cargado_descargado
    """
    try:
        # Buscar el historial que contiene datos de este vagon
        # datos_vagon__id es la forma correcta de buscar por el campo específico id dentro del JSONField.
        historiales = HistorialVagonCargadoDescargado.objects.filter(
            datos_vagon__id=instance.id  # Sintaxis correcta para buscar en JSON
        )

        # Eliminar todos los registros de historial encontrados
        historiales.delete()

    except Exception as e:
        print(f"Error al eliminar historial del vagon {instance.id}: {str(e)}")


# Señal para crear el historial cuando se crea un Situado_Carga_Descarga
@receiver(post_save, sender=Situado_Carga_Descarga)
def crear_historial_situado(sender, instance, created, **kwargs):
    if not created:
        return

    def _crear_historial():
        # 1. Obtener el situado con relaciones FRESCAS de la base de datos
        situado = Situado_Carga_Descarga.objects.prefetch_related(
            Prefetch(
                "producto",
                queryset=producto_UFC.objects.select_related(
                    "producto", "tipo_embalaje", "unidad_medida"
                ),
            )
        ).get(pk=instance.pk)

        # 2. Debug avanzado - Verificar conexión M2M en BD
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT producto_ufc_id 
                FROM ufc_situado_carga_descarga_producto 
                WHERE situado_carga_descarga_id = %s
            """,
                [instance.id],
            )
            ids_productos = cursor.fetchall()
            print(f"Productos en tabla M2M: {ids_productos}")

        # 3. Serialización a prueba de errores
        productos_data = []
        print(situado, situado.producto)
        for p in situado.producto.all():
            try:
                productos_data.append(
                    {
                        "id": p.id,
                        "producto": {
                            "id": p.producto.id,
                            "nombre": p.producto.nombre_producto,
                            "codigo": p.producto.codigo_producto,
                        },
                        "embalaje": {
                            "id": p.tipo_embalaje.id,
                            "nombre": p.tipo_embalaje.nombre_tipo_embalaje,
                        }
                        if p.tipo_embalaje
                        else None,
                        "unidad_medida": {
                            "id": p.unidad_medida.id,
                            "nombre": p.unidad_medida.unidad_medida,
                            "simbolo": p.unidad_medida.simbolo,
                        }
                        if p.unidad_medida
                        else None,
                        "cantidad": p.cantidad,
                        "estado": p.estado,
                        "contiene": p.contiene,
                    }
                )
            except Exception as e:
                print(f"Error serializando producto {p.id}: {str(e)}")
                continue

        # 4. Creación condicional del historial
        if not productos_data:
            print(
                f"ADVERTENCIA CRÍTICA: Situado {instance.id} tiene productos en el serializer pero no en la señal"
            )
            return

        HistorialSituadoCargaDescarga.objects.create(
            informe_operativo=ufc_informe_operativo.objects.filter(
                fecha_operacion__date=instance.fecha.date()
            ).first(),
            datos_situado={
                "id": instance.id,
                "tipo_origen": instance.tipo_origen,
                "origen": instance.origen,
                "tipo_equipo": instance.tipo_equipo,
                "estado": instance.estado,
                "operacion": instance.operacion,
                "fecha": str(instance.fecha),
                "situados": instance.situados,
                "pendiente_proximo_dia": instance.pendiente_proximo_dia,
                "observaciones": instance.observaciones,
            },
            datos_productos=productos_data,
        )

    # Retardo opcional para asegurar consistencia (solo en desarrollo)
    import os

    if os.environ.get("DEBUG") == "True":
        import time

        time.sleep(0.5)

    transaction.on_commit(_crear_historial)


# Señal para eliminar el historial cuando se elimina un Situado_Carga_Descarga
@receiver(post_delete, sender=Situado_Carga_Descarga)
def eliminar_historial_situado(sender, instance, **kwargs):
    """
    Elimina el registro de historial asociado cuando se elimina un Situado_Carga_Descarga
    """
    try:
        # Buscar el historial que contiene datos de este situado
        historiales = HistorialSituadoCargaDescarga.objects.filter(
            datos_situado__icontains={"id": instance.id}
        )

        # Eliminar todos los registros de historial encontrados
        historiales.delete()

    except Exception as e:
        print(f"Error al eliminar historial del situado {instance.id}: {str(e)}")


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


# Señal para crear el historial al guardar
@receiver(post_save, sender=vagones_productos)
def crear_historial_vagones_productos(sender, instance, created, **kwargs):
    if not created:
        return

    def _crear_historial_vagones_productos():
        fecha_registro = instance.fecha.date()

        informe = (
            ufc_informe_operativo.objects.annotate(
                fecha_op=TruncDate("fecha_operacion")
            )
            .filter(fecha_op=fecha_registro)
            .first()
        )

        if not informe:
            return

        # Obtener los productos directamente desde la instancia
        productos = instance.producto.all()

        # Serializar datos principales
        datos_principales = {
            "id": instance.id,
            "fecha": str(instance.fecha),
            "tipo_origen": instance.tipo_origen,
            "origen": instance.origen,
            "tipo_producto": instance.tipo_producto,
            "tipo_combustible": instance.tipo_combustible,
            "tipo_equipo": instance.tipo_equipo_ferroviario.get_tipo_equipo_display()
            if instance.tipo_equipo_ferroviario
            else None,
            "plan_mensual": instance.plan_mensual,
            "plan_dia": instance.plan_dia,
            "vagones_situados": instance.vagones_situados,
            "vagones_cargados": instance.vagones_cargados,
            "plan_anual": instance.plan_anual,
            "plan_acumulado_actual": instance.plan_acumulado_actual,
            "real_acumulado_actual": instance.real_acumulado_actual,
            "plan_acumulado_anual": instance.plan_acumulado_anual,
            "real_acumulado_anual": instance.real_acumulado_anual,
            "plan_aseguramiento_proximos_dias": instance.plan_aseguramiento_proximos_dias,
            "plan_acumulado": instance.plan_acumulado_dia_anterior,
            "real_acumulado": instance.real_acumulado_dia_anterior,
            "observaciones": instance.observaciones,
        }

        # Serializar productos - versión mejorada
        productos_serializados = []
        if productos.exists():  # Verificar si hay productos
            for prod in productos:
                producto_data = {
                    "id": prod.id,
                    "producto": prod.producto.nombre_producto
                    if prod.producto
                    else None,
                    "tipo_embalaje": prod.tipo_embalaje.nombre_tipo_embalaje
                    if prod.tipo_embalaje
                    else None,
                    "unidad_medida": prod.unidad_medida.simbolo
                    if prod.unidad_medida
                    else None,
                    "cantidad": prod.cantidad,
                    "estado": prod.estado,
                    "contiene": prod.contiene,
                }
                productos_serializados.append(producto_data)

        # Debug: Verificar datos antes de guardar
        print("Productos a serializar:", productos_serializados)

        HistorialVagonesProductos.objects.create(
            informe_operativo=informe,
            datos_vagon_producto=datos_principales,
            datos_productos=productos_serializados,
        )

    transaction.on_commit(_crear_historial_vagones_productos)


# Señal para eliminar el historial de HistorialVagonesProductos asociado al id de vagones_productos
@receiver(post_delete, sender=vagones_productos)
def eliminar_historial_vagones_productos(sender, instance, **kwargs):
    """
    Elimina el registro de historial asociado cuando se elimina un vagones_productos
    """
    try:
        # Buscar el historial que contiene datos de este vagon
        # datos_vagon_producto__id es la forma correcta de buscar por el campo específico id dentro del JSONField.
        historiales = HistorialVagonesProductos.objects.filter(
            datos_vagon_producto__id=instance.id  # Sintaxis correcta para buscar en JSON
        )

        # Eliminar todos los registros de historial encontrados
        historiales.delete()

    except Exception as e:
        print(f"Error al eliminar historial del vagon {instance.id}: {str(e)}")


# Señal para crear el historial cuando se crea un en_trenes
@receiver(post_save, sender=en_trenes)
def crear_historial_en_trenes(sender, instance, created, **kwargs):
    """
    Crea un historial de en_trenes asociado al informe operativo de su fecha
    """
    if not created:  # Solo nos interesan las creaciones nuevas
        return

    def _crear_historial_en_trenes_despues_de_guardar():
        # Obtener solo la fecha (sin hora) del tren
        fecha_tren = instance.fecha.date()

        # Buscar si existe un informe operativo para esta fecha
        informe = (
            ufc_informe_operativo.objects.annotate(
                fecha_op=TruncDate("fecha_operacion")
            )
            .filter(fecha_op=fecha_tren)
            .first()
        )

        if not informe:
            return  # No hacer nada si no hay informe para esta fecha

        # Obtener el tren con todas sus relaciones
        tren_completo = (
            en_trenes.objects.select_related("locomotora", "tipo_equipo")
            .prefetch_related(
                "producto__producto",
                "producto__tipo_embalaje",
                "producto__unidad_medida",
                "equipo_vagon",
            )
            .get(pk=instance.pk)
        )

        # Serializar datos del tren
        datos_tren = {
            "id": tren_completo.id,
            "locomotora_id": tren_completo.locomotora.id
            if tren_completo.locomotora
            else None,
            "locomotora_numero": tren_completo.locomotora.numero_identificacion
            if tren_completo.locomotora
            else None,
            "fecha": str(tren_completo.fecha),
            "numero_identificacion_locomotora": tren_completo.numero_identificacion_locomotora,
            "tipo_equipo_id": tren_completo.tipo_equipo.id
            if tren_completo.tipo_equipo
            else None,
            "tipo_equipo_name": tren_completo.tipo_equipo.get_tipo_equipo_display()
            if tren_completo.tipo_equipo
            else None,
            "estado": tren_completo.estado,
            "tipo_origen": tren_completo.tipo_origen,
            "origen": tren_completo.origen,
            "tipo_destino": tren_completo.tipo_destino,
            "destino": tren_completo.destino,
            "cantidad_vagones": tren_completo.cantidad_vagones,
            "observaciones": tren_completo.observaciones,
        }

        # Serializar productos relacionados
        productos = []
        for producto in tren_completo.producto.all():
            productos.append(
                {
                    "id": producto.id,
                    "producto_name": producto.producto.nombre_producto,
                    "tipo_embalaje_name": producto.tipo_embalaje.nombre_tipo_embalaje
                    if producto.tipo_embalaje
                    else None,
                    "unidad_medida_simbolo": producto.unidad_medida.simbolo
                    if producto.unidad_medida
                    else None,
                    "cantidad": producto.cantidad,
                    "estado": producto.estado,
                    "contiene": producto.contiene,
                }
            )

        # Serializar vagones relacionados
        vagones = []
        for vagon in tren_completo.equipo_vagon.all():
            vagones.append(
                {
                    "id": vagon.id,
                    "numero_identificacion": vagon.numero_identificacion,
                    "tipo_equipo": vagon.tipo_equipo.tipo_equipo
                    if vagon.tipo_equipo
                    else None,
                    "estado_actual": vagon.estado_actual,
                }
            )

        # Crear registro de historial
        HistorialEnTrenes.objects.create(
            informe_operativo=informe,
            datos_tren=datos_tren,
            datos_productos=productos,
            datos_vagones=vagones,
        )

    # Usamos transaction.on_commit para ejecutar después de que la transacción se complete
    transaction.on_commit(_crear_historial_en_trenes_despues_de_guardar)


# Señal para eliminar el historial cuando se elimina un en_trenes
@receiver(post_delete, sender=en_trenes)
def eliminar_historial_en_trenes(sender, instance, **kwargs):
    """
    Elimina el registro de historial asociado cuando se elimina un en_trenes
    """
    try:
        # Buscar el historial que contiene datos de este tren
        historiales = HistorialEnTrenes.objects.filter(
            datos_tren__icontains={"id": instance.id}
        )

        # Eliminar todos los registros de historial encontrados
        historiales.delete()

    except Exception as e:
        print(f"Error al eliminar historial del tren {instance.id}: {str(e)}")


# Señal para crear el historial cuando se crea un por_situar
@receiver(post_save, sender=por_situar)
def crear_historial_por_situar(sender, instance, created, **kwargs):
    """
    Versión mejorada que garantiza el correcto guardado de productos relacionados
    """
    if not created:
        return

    def _crear_historial_por_situar_despues_de_guardar():
        try:
            # Obtener fecha sin hora
            fecha_vagon = instance.fecha.date()

            # Buscar informe operativo correspondiente
            informe = (
                ufc_informe_operativo.objects.annotate(
                    fecha_op=TruncDate("fecha_operacion")
                )
                .filter(fecha_op=fecha_vagon)
                .first()
            )

            if not informe:
                print(f"No se encontró informe operativo para la fecha {fecha_vagon}")
                return

            # Obtener productos directamente desde la instancia
            productos = instance.producto.all()

            # Serializar datos principales del por_situar
            datos_vagon = {
                "id": instance.id,
                "tipo_origen": instance.tipo_origen,
                "origen": instance.origen,
                "tipo_equipo": instance.tipo_equipo,
                "estado": instance.estado,
                "operacion": instance.operacion,
                "por_situar": instance.por_situar,
                "fecha": str(instance.fecha),
                "observaciones": instance.observaciones,
            }

            # Serializar productos - versión robusta
            productos_serializados = []
            if productos.exists():  # Verificar si hay productos
                for producto in productos:
                    producto_data = {
                        "id": producto.id,
                        "producto_name": producto.producto.nombre_producto
                        if producto.producto
                        else None,
                        "tipo_embalaje_name": producto.tipo_embalaje.nombre_tipo_embalaje
                        if producto.tipo_embalaje
                        else None,
                        "unidad_medida_simbolo": producto.unidad_medida.simbolo
                        if producto.unidad_medida
                        else None,
                        "cantidad": producto.cantidad,
                        "estado": producto.estado,
                        "contiene": producto.contiene,
                    }
                    productos_serializados.append(producto_data)

            # Debug: Verificar datos antes de guardar
            print(f"Datos a serializar - Productos: {len(productos_serializados)}")

            # Crear registro de historial
            HistorialVagonPorSituar.objects.create(
                informe_operativo=informe,
                datos_vagon=datos_vagon,
                datos_productos=productos_serializados,
            )

        except Exception as e:
            print(f"Error al crear historial por_situar: {str(e)}")
            # Puedes agregar aquí notificaciones adicionales o logging

    # Ejecutar después de commit
    transaction.on_commit(_crear_historial_por_situar_despues_de_guardar)


# Señal para eliminar el historial cuando se elimina un por_situar
@receiver(post_delete, sender=por_situar)
def eliminar_historial_por_situar(sender, instance, **kwargs):
    """
    Elimina el registro de historial asociado cuando se elimina un por_situar
    """
    try:
        # Buscar el historial que contiene datos de este por_situar
        historiales = HistorialVagonPorSituar.objects.filter(
            datos_vagon__icontains={"id": instance.id}
        )

        # Eliminar todos los registros de historial encontrados
        historiales.delete()

    except Exception as e:
        print(f"Error al eliminar historial del por_situar {instance.id}: {str(e)}")

from django.db import models
from nomencladores.models import nom_tipo_equipo_ferroviario,nom_producto,nom_tipo_embalaje,nom_unidad_medida,nom_equipo_ferroviario
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum,Prefetch
# Usamos un delay para asegurar que las relaciones ManyToMany estén establecidas 
from django.db import transaction
from django.db.models.functions import TruncDate
from django.utils import timezone



#Modelo para el informe operativo
class ufc_informe_operativo(models.Model):    

    fecha_operacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de operación")
    fecha_actual = models.DateTimeField(auto_now=True, verbose_name="Fecha actual")
    plan_mensual_total = models.IntegerField(editable=False,default=0)
    plan_diario_total_vagones_cargados = models.IntegerField(editable=False,default=0)
    real_total_vagones_cargados = models.IntegerField(editable=False,default=0)
    total_vagones_situados = models.IntegerField(editable=False,default=0)
    plan_total_acumulado_actual = models.IntegerField(editable=False,default=0)
    real_total_acumulado_actual = models.IntegerField(editable=False,default=0)
    estado_parte = models.CharField(default="Creado",max_length=14)

    class Meta:
        permissions = [
            ("puede_rechazar_informe", "Puede rechazar informes operativos"),
            ("puede_aprobar_informe", "Puede aprobar informes operativos"),
            ("puede_cambiar_a_listo", "Puede cambiar el estado del informe a listo"),
        ]
        verbose_name = "Parte informe operativo"
        verbose_name_plural = "Parte informe operativo"
        ordering = ["-fecha_operacion"]

    def __str__(self):
        return f"Fecha de operación {self.fecha_operacion} - fecha actual: {self.fecha_actual}" 




#*************************************************************************************************************************
    
#productos asociados a vagones en trenes
class producto_UFC(models.Model):
   
    ESTADO_CHOICES = [
        ('vacio', 'Vacío'),
        ('lleno', 'Lleno'),
    ]
    CONTIENE_CHOICES = [
        ('alimentos', 'Alimentos'),
        ('prod_varios', 'Productos Varios'),
    ]
   
   
    producto = models.ForeignKey(nom_producto, on_delete=models.CASCADE)
    tipo_embalaje = models.ForeignKey(nom_tipo_embalaje, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(nom_unidad_medida, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado=models.CharField(choices=ESTADO_CHOICES, null=True, blank=True, max_length=20)
    contiene=models.CharField(choices=CONTIENE_CHOICES, null=True, blank=True, max_length=20)
    
    class Meta:
        verbose_name = "Producto UFC"
        verbose_name_plural = "Productos en UFC"
        #unique_together = [['cliente', 'destino']] 

    
    def __str__(self):
        return f"tipo de producto {self.get_contiene_display()} - {self.producto.nombre_producto}"
    
    @property
    def embalaje_display(self):
        return self.tipo_embalaje if self.tipo_embalaje else "Sin especificar"
    
    @property
    def unidad_medida_display(self):
        return self.unidad_medida if self.unidad_medida else "Sin especificar"
    @property
    def producto_display(self):
        return f"{self.producto.nombre_producto} - {self.embalaje_display}"
    
#productos asociados al estado vagones cargados/descargados

#Modelo creado para los productos asociados al modelo vagones y productos

# Modelo para representar el estado vagones cargados/descargados

# modelo para registrar los vagones asociados al estado vagones cargados/descargados
class registro_vagones_cargados(models.Model):
    # Opciones para el campo tipo_origen
    TIPO_ORIGEN_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso comercial/CCD'),
    ]

    no_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Número de identificación",
        help_text="Valores definidos en el nomenclador de equipos ferroviarios (excepto 'Locomotora')"
    )
    
    fecha_despacho = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de despacho"
    )
    
    tipo_origen = models.CharField(choices=TIPO_ORIGEN_CHOICES, max_length = 50,null=True,blank=True)
    
    origen = models.CharField(max_length=40,null=True,blank=True)
    
    fecha_llegada = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de llegada"
    )
    
    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones",
        help_text="Admite letras, números y caracteres especiales"
    )

    class Meta:
        verbose_name = "Registro de vagón cargado"
        verbose_name_plural = "Registros de vagones cargados"

    def __str__(self):
        return f"Vagón {self.no_id}" if self.no_id else "Registro sin ID"
    
    
class vagon_cargado_descargado(models.Model):
    TIPO_ORIGEN_DESTINO_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso comercial/CCD'),
    ]
    
    ESTADO_CHOICES = [
        ('vacio', 'Vacío'),
        ('cargado', 'Cargado'),
    ]
    
    OPERACION_CHOICES = [
        ('carga', 'Carga'),
        ('descarga', 'Descarga'),
    ]
    
    TIPO_DESTINO_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso comercial/CCD'),
    ]
    
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro", editable=False)
    tipo_origen = models.CharField(choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length = 50)
    origen = models.CharField(max_length=40)
    tipo_equipo_ferroviario = models.ForeignKey(nom_tipo_equipo_ferroviario, on_delete=models.CASCADE)
    estado = models.CharField(choices=ESTADO_CHOICES, max_length = 50)    
    operacion = models.CharField(choices=OPERACION_CHOICES, editable=True, max_length = 50)
    plan_diario_carga_descarga = models.IntegerField()
    real_carga_descarga = models.IntegerField(default = 0, editable=False)
    tipo_destino = models.CharField(choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length = 50)
    destino = models.CharField(max_length=40)
    causas_incumplimiento = models.TextField(null=False, blank=True, default='', max_length=100)
    # Cambiamos ForeignKey a ManyToManyField, es posible que un vagon tenga mas de un producto
    producto = models.ManyToManyField(
        producto_UFC,
        blank=True,
        related_name='vagones_cargados'
    )

    registros_vagones = models.ManyToManyField(
        registro_vagones_cargados,
        blank=True,
        related_name='registro_vagones_cargados',
        verbose_name="Registros de vagones asociados"
    )

    class Meta:
        verbose_name_plural = "Vagones cargados/descargados"
        verbose_name = "Vagón cargado/descargado"  

    def delete(self, *args, **kwargs):
        try:
            from nomencladores.models import nom_equipo_ferroviario
            
            # Procesar en pequeñas transacciones independientes
            registros = list(self.registros_vagones.all())
            
            for registro in registros:
                try:
                    with transaction.atomic():
                        equipo = nom_equipo_ferroviario.objects.filter(
                            numero_identificacion=registro.no_id
                        ).first()
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                except Exception as e:
                    print(f"Error al actualizar equipo {registro.no_id}: {str(e)}")
                    continue
            
            # Eliminar relaciones (operaciones menos críticas)
            self.registros_vagones.clear()
            self.producto.clear()
            
            # Eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico: {str(e)}")
            raise
    
#Modelo para almacenar el historial de vagon_cargado_descargado y sus relaciones
class HistorialVagonCargadoDescargado(models.Model):
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo, 
        on_delete=models.CASCADE,
        related_name='historiales_vagones'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    datos_vagon = models.JSONField()  # Almacena todos los datos del vagon_cargado_descargado
    datos_productos = models.JSONField()  # Almacena datos de productos relacionados
    datos_registros_vagones = models.JSONField()  # Almacena datos de registros_vagones_cargados
    
    class Meta:
        verbose_name = "Historial de vagón cargado/descargado"
        verbose_name_plural = "Historiales de vagones cargados/descargados"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Historial para informe {self.informe_operativo.id} - {self.fecha_creacion}"

#funcion que se encarga de almacenar el historial de vagon_cargado_dscargado, la activa la creacion del modelo padre
@receiver(post_save, sender=vagon_cargado_descargado)
def crear_historial_vagones_cargados_descargados(sender, instance, created, **kwargs):
    """
    Crea un historial del vagon cargado/descargado asociado al informe operativo de su fecha
    """
    if not created:  # Solo nos interesan las creaciones nuevas
        return
    
    def _crear_historial_Cargado_descargado_despues_de_guardar():
        # Obtener solo la fecha (sin hora) del vagon
        fecha_vagon = instance.fecha.date()
        
        # Buscar si existe un informe operativo para esta fecha
        informe = ufc_informe_operativo.objects.annotate(
            fecha_op=TruncDate('fecha_operacion')
        ).filter(fecha_op=fecha_vagon).first()
        
        if not informe:
            return  # No hacer nada si no hay informe para esta fecha
        
        # Obtener el vagon con todas sus relaciones
        vagon_completo = vagon_cargado_descargado.objects.select_related(
            'tipo_equipo_ferroviario'
        ).prefetch_related(
            'producto__producto',
            'producto__tipo_embalaje',
            'producto__unidad_medida',
            'registros_vagones'
        ).get(pk=instance.pk)
        
        # Serializar datos del vagon
        datos_vagon = {
            'id': vagon_completo.id,
            'tipo_origen': vagon_completo.tipo_origen,
            'origen': vagon_completo.origen,
            'tipo_equipo_ferroviario_id': vagon_completo.tipo_equipo_ferroviario.id if vagon_completo.tipo_equipo_ferroviario else None,
            'tipo_equipo_ferroviario_name': vagon_completo.tipo_equipo_ferroviario.get_tipo_equipo_display() if vagon_completo.tipo_equipo_ferroviario else None,
            'estado': vagon_completo.estado,
            'operacion': vagon_completo.operacion,
            'plan_diario_carga_descarga': vagon_completo.plan_diario_carga_descarga,
            'real_carga_descarga': vagon_completo.real_carga_descarga,
            'tipo_destino': vagon_completo.tipo_destino,
            'destino': vagon_completo.destino,
            'causas_incumplimiento': vagon_completo.causas_incumplimiento,
            'fecha': str(vagon_completo.fecha)
        }
        
        # Serializar productos relacionados
        productos = []
        for producto in vagon_completo.producto.all():
            productos.append({
                    'id': producto.id,
                    'producto_name': producto.producto.nombre_producto,
                    'tipo_embalaje_name': producto.tipo_embalaje.nombre_tipo_embalaje if producto.tipo_embalaje else None,
                    'unidad_medida_simbolo': producto.unidad_medida.simbolo if producto.unidad_medida else None,
                    'cantidad': producto.cantidad,
                    'estado': producto.estado,
                    'contiene': producto.contiene
            })
        
        # Serializar registros de vagones relacionados
        registros = []
        for registro in vagon_completo.registros_vagones.all():
            registros.append({
                'id': registro.id,
                'no_id': registro.no_id,
                'fecha_despacho': str(registro.fecha_despacho) if registro.fecha_despacho else None,
                'tipo_origen': registro.tipo_origen,
                'origen': registro.origen,
                'fecha_llegada': str(registro.fecha_llegada) if registro.fecha_llegada else None,
                'observaciones': registro.observaciones
            })
        
        # Crear registro de historial
        HistorialVagonCargadoDescargado.objects.create(
            informe_operativo=informe,
            datos_vagon=datos_vagon,
            datos_productos=productos,
            datos_registros_vagones=registros
        )

    # Usamos transaction.on_commit para ejecutar después de que la transacción se complete
    transaction.on_commit(_crear_historial_Cargado_descargado_despues_de_guardar)

#Elimina el registro del historial asociado al vagon que se esta eliminando
@receiver(post_delete, sender=vagon_cargado_descargado)
def eliminar_historial_vagon_cargado_descargado(sender, instance, **kwargs):
    """
    Elimina el registro de historial asociado cuando se elimina un vagon_cargado_descargado
    """
    try:
        # Buscar el historial que contiene datos de este vagon
        historiales = HistorialVagonCargadoDescargado.objects.filter(
            datos_vagon__icontains={'id': instance.id}
        )
        
        # Eliminar todos los registros de historial encontrados
        historiales.delete()
        
    except Exception as e:
        print(f"Error al eliminar historial del vagon {instance.id}: {str(e)}")
#************************************************************************************************************************
#Modelo Situado
class Situado_Carga_Descarga(models.Model):
    
    t_origen = (
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso Comercial')
    )
    
    tipo_origen = models.CharField(max_length=100, choices=t_origen, verbose_name="Tipo de origen", blank=True, null=True)
    origen = models.CharField(max_length=200, verbose_name="Origen")
    
    t_equipo = (
        ('casilla', 'Casilla'),
        ('caj_gon', 'Cajones o Góndola'),
        ('planc_plat', 'Plancha o Plataforma'),
        ('Plan_porta_cont', 'Plancha porta contenedores'),
        ('cist_liquidos', 'Cisterna para líquidos'),
        ('cist_solidos', 'Cisterna para sólidos'),
        ('tolva_g_mineral', 'Tolva granelera(mineral)'),
        ('tolva_g_agric', 'Tolva granelera(agrícola)'),
        ('tolva_g_cemento', 'Tolva para cemento'),
        ('volqueta', 'Volqueta'),
        ('Vagon_ref', 'Vagón refrigerado'),
        ('jaula', 'Jaula'),
        ('locomotora', 'Locomotora'),
        ('tren', 'Tren'),
    )
    
    tipo_equipo = models.CharField(max_length=200, choices=t_equipo, verbose_name="Tipo de equipo", blank=True, null=True)
    
    status =(
        ('vacio', 'Vacio'),
        ('cargado', 'Cargado')
    )
    
    estado = models.CharField(max_length=200, choices=status, verbose_name="Estado", blank=True, null=True)
    
    t_operacion = (
        ('carga', 'Carga'),
        ('descarga', 'Descarga')
    )
    
    operacion = models.CharField(max_length=200, choices=t_operacion, verbose_name="Operacion", blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro", editable=False)
    producto = models.ManyToManyField(
        producto_UFC,
        blank=True,
        related_name="situados",
        verbose_name="Productos"
    )
    
    situados = models.CharField(
        max_length=10,
        verbose_name="Cantidad de situados",
        default="0",
        validators=[
            RegexValidator(
                regex='^[0-9]+$',
                message='Solo se permiten números positivos',
                code='invalid_situados'
            )
        ]
    )
    
    pendiente_proximo_dia = models.CharField(
        max_length=10,
        verbose_name="Pendientes para el próximo día",
        default="0",
        validators=[
            RegexValidator(
                regex='^[0-9]+$',
                message='Solo se permiten números positivos',
                code='invalid_pendientes'
            )
        ]
    )
    
    observaciones = models.TextField(
        verbose_name="Observaciones",
        help_text="Ingrese observaciones adicionales. Admite letras, números y caracteres especiales.",
        blank=True,  # Permite que el campo esté vacío
        null=True,   # Permite valores nulos en la base de datos
    )

    class Meta:
        verbose_name = "Situado "
        verbose_name_plural = "Situados"
        ordering = ['tipo_origen', 'origen']

    def __str__(self):
        return f"{self.tipo_origen} - {self.origen} - {self.tipo_equipo}"
    
# Modelo para el historial de Situado_Carga_Descarga
class HistorialSituadoCargaDescarga(models.Model):
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo, 
        on_delete=models.CASCADE,
        related_name='historiales_situados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    datos_situado = models.JSONField()  # Almacena todos los datos del situado
    datos_productos = models.JSONField(
        null=True,  # Permite NULL
        blank=True,  # Permite vacío
        default=list  # Valor por defecto como lista vacía
    )  # Almacena datos de productos relacionados
    
    class Meta:
        verbose_name = "Historial de situado"
        verbose_name_plural = "Historiales de situados"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Historial de situado para informe {self.informe_operativo.id} - {self.fecha_creacion}"

# Señal para crear el historial cuando se crea un Situado_Carga_Descarga
@receiver(post_save, sender=Situado_Carga_Descarga)
def crear_historial_situado(sender, instance, created, **kwargs):
    if not created:
        return

    def _crear_historial():
        # 1. Obtener el situado con relaciones FRESCAS de la base de datos
        situado = Situado_Carga_Descarga.objects.prefetch_related(
            Prefetch('producto', queryset=producto_UFC.objects.select_related(
                'producto', 'tipo_embalaje', 'unidad_medida'
            ))
        ).get(pk=instance.pk)

        # 2. Debug avanzado - Verificar conexión M2M en BD
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT producto_ufc_id 
                FROM ufc_situado_carga_descarga_producto 
                WHERE situado_carga_descarga_id = %s
            """, [instance.id])
            ids_productos = cursor.fetchall()
            print(f"Productos en tabla M2M: {ids_productos}")

        # 3. Serialización a prueba de errores
        productos_data = []
        print(situado,situado.producto)
        for p in situado.producto.all():
            try:
                productos_data.append({
                    'id': p.id,
                    'producto': {
                        'id': p.producto.id,
                        'nombre': p.producto.nombre_producto,
                        'codigo': p.producto.codigo_producto
                    },
                    'embalaje': {
                        'id': p.tipo_embalaje.id,
                        'nombre': p.tipo_embalaje.nombre_tipo_embalaje
                    } if p.tipo_embalaje else None,
                    'unidad_medida': {
                        'id': p.unidad_medida.id,
                        'nombre': p.unidad_medida.unidad_medida,
                        'simbolo': p.unidad_medida.simbolo
                    } if p.unidad_medida else None,
                    'cantidad': p.cantidad,
                    'estado': p.estado,
                    'contiene': p.contiene
                })
            except Exception as e:
                print(f"Error serializando producto {p.id}: {str(e)}")
                continue

        # 4. Creación condicional del historial
        if not productos_data:
            print(f"ADVERTENCIA CRÍTICA: Situado {instance.id} tiene productos en el serializer pero no en la señal")
            return

        HistorialSituadoCargaDescarga.objects.create(
            informe_operativo=ufc_informe_operativo.objects.filter(
                fecha_operacion__date=instance.fecha.date()
            ).first(),
            datos_situado={
                'id': instance.id,
                'tipo_origen': instance.tipo_origen,
                'origen': instance.origen,
                'tipo_equipo': instance.tipo_equipo,
                'estado': instance.estado,
                'operacion': instance.operacion,
                'fecha': str(instance.fecha),
                'situados': instance.situados,
                'pendiente_proximo_dia': instance.pendiente_proximo_dia,
                'observaciones': instance.observaciones
            },
            datos_productos=productos_data
        )

    # Retardo opcional para asegurar consistencia (solo en desarrollo)
    import os
    if os.environ.get('DEBUG') == 'True':
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
            datos_situado__icontains={'id': instance.id}
        )
        
        # Eliminar todos los registros de historial encontrados
        historiales.delete()
        
    except Exception as e:
        print(f"Error al eliminar historial del situado {instance.id}: {str(e)}")
    
#**************************************************************************************************
#Modelo destinado a vagones y productos
class vagones_productos(models.Model):
    TIPO_ORIGEN_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso comercial/CCD'),
    ]
    
    TIPO_PRODUCTO_CHOICES = [
        ('producto', 'Producto'),
        ('contenedor', 'Contenedor'),
        ('combustible', 'Combustible'),
    ]
    TIPO_COMBUSTIBLE_CHOICES = [
        ('combustible_blanco', 'Combustible blanco'),
        ('combustible_negro', 'Combustible negro'),
        ('combustible_turbo', 'Combustible turbo'),
        ('-', '-'),
    ]

    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro", editable=False)
    tipo_origen = models.CharField(choices=TIPO_ORIGEN_CHOICES, max_length = 50)
    origen = models.CharField(max_length=40)
    tipo_producto = models.CharField(choices=TIPO_PRODUCTO_CHOICES, max_length = 20,blank=True,null=True)
    tipo_combustible = models.CharField(choices=TIPO_COMBUSTIBLE_CHOICES, max_length = 20,blank=True,null=True)
    tipo_equipo_ferroviario = models.ForeignKey(nom_tipo_equipo_ferroviario, on_delete=models.CASCADE,blank=True,null=True)
    plan_mensual = models.IntegerField()
    plan_dia = models.IntegerField(editable=False,default=0)
    vagones_situados = models.IntegerField(editable=False,default=0)
    vagones_cargados = models.IntegerField(editable=False,default=0)
    plan_acumulado_actual = models.IntegerField(editable=False,default=0)
    real_acumulado_actual = models.IntegerField(editable=False,default=0)
    plan_acumulado_anual = models.IntegerField(editable=False,default=0)
    real_acumulado_anual = models.IntegerField(editable=False,default=0)
    plan_aseguramiento_proximos_dias = models.IntegerField(editable=False,default=0,blank=True)
    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones",
        help_text="Admite letras, números y caracteres especiales"
    )

    #ManyToManyField, es posible que un vagon tenga mas de un producto
    producto = models.ManyToManyField(
        producto_UFC,
        blank=True,
        related_name='vagones_productos'
    )
    plan_anual = models.IntegerField()
    plan_acumulado_dia_anterior = models.IntegerField()
    real_acumulado_dia_anterior = models.IntegerField()

    class Meta:
        verbose_name_plural = "Vagones y productos"
        verbose_name = "Vagón y producto"
         

    def __str__(self):
        # Obtener todos los productos relacionados
        productos = self.producto.all()
        
        # Crear una lista con los nombres de los productos,el primer producto es el objeto local,
        #el segundo es el nombre del atrib en el modelo al que se llama de tipo nom_producto
        nombres_productos = [str(producto.producto.nombre_producto) for producto in productos]
        
        # Unir los nombres con comas si hay más de uno
        productos_str = ", ".join(nombres_productos) if nombres_productos else "Sin productos"        
        return f"Vagones y productos: {productos_str}"   

#Actualizando el resto de los campos de forma automatica, se activa cuando se inserta un registro en vagones_productos
@receiver([post_save, post_delete], sender=vagon_cargado_descargado)
@receiver([post_save, post_delete], sender=Situado_Carga_Descarga)
def actualizar_campos_automaticos_vagones_productos(sender, instance, **kwargs):    
    '''Actualiza los campos automáticos en vagones_productos cuando hay cambios
    en los modelos relacionados vagon_cargado_descargado, Situado_Carga_Descarga'''
    
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
            plan_dia = vagon_cargado_descargado.objects.filter(
                operacion='carga'
            ).aggregate(total=Sum('plan_diario_carga_descarga'))['total'] or 0
            
            vagones_cargados = vagon_cargado_descargado.objects.filter(
                operacion='carga',
            ).aggregate(total=Sum('real_carga_descarga'))['total'] or 0
            
            vagones_situados = Situado_Carga_Descarga.objects.filter(
                operacion='carga',
            ).aggregate(total=Sum('situados'))['total'] or 0
            
            plan_aseguramiento = vagon_cargado_descargado.objects.filter(
                operacion='carga',
            ).aggregate(total=Sum('real_carga_descarga'))['total'] or 0
            
            # Lógica para campos acumulados según los casos especificados
            if es_unico_informe_año and es_primer_dia_mes:
                # Caso 3: Único informe en el año y es primer día del mes
                vagon_producto.plan_acumulado_dia_anterior = 0
                vagon_producto.real_acumulado_dia_anterior = 0
                vagon_producto.plan_acumulado_actual = vagon_producto.plan_acumulado_dia_anterior + plan_dia
                vagon_producto.real_acumulado_actual = vagon_producto.real_acumulado_dia_anterior + vagones_cargados
                vagon_producto.plan_acumulado_anual = vagon_producto.plan_acumulado_anual + plan_dia
                vagon_producto.real_acumulado_anual = vagon_producto.real_acumulado_anual + vagones_cargados
                
            elif es_unico_informe_año and not es_primer_dia_mes:
                # Caso 4: Único informe en el año pero no es primer día del mes
                vagon_producto.plan_acumulado_actual = vagon_producto.plan_acumulado_dia_anterior + plan_dia
                vagon_producto.real_acumulado_actual = vagon_producto.real_acumulado_dia_anterior + vagones_cargados
                vagon_producto.plan_acumulado_anual = vagon_producto.plan_acumulado_anual + plan_dia
                vagon_producto.real_acumulado_anual = vagon_producto.real_acumulado_anual + vagones_cargados
                
            elif not es_unico_informe_año and es_primer_dia_mes:
                # Caso 5: No es único informe en el año pero es primer día del mes
                vagon_producto.plan_acumulado_dia_anterior = 0
                vagon_producto.real_acumulado_dia_anterior = 0
                vagon_producto.plan_acumulado_actual = vagon_producto.plan_acumulado_dia_anterior + plan_dia
                vagon_producto.real_acumulado_actual = vagon_producto.real_acumulado_dia_anterior + vagones_cargados
                vagon_producto.plan_acumulado_anual = vagon_producto.plan_acumulado_anual + plan_dia
                vagon_producto.real_acumulado_anual = vagon_producto.real_acumulado_anual + vagones_cargados
                
            else:
                # Caso 6: No es único informe en el año ni es primer día del mes
                vagon_producto.plan_acumulado_actual = vagon_producto.plan_acumulado_dia_anterior + plan_dia
                vagon_producto.real_acumulado_actual = vagon_producto.real_acumulado_dia_anterior + vagones_cargados
                vagon_producto.plan_acumulado_anual = vagon_producto.plan_acumulado_anual + plan_dia
                vagon_producto.real_acumulado_anual = vagon_producto.real_acumulado_anual + vagones_cargados
            
            # Actualizar campos básicos
            vagon_producto.plan_dia = plan_dia
            vagon_producto.vagones_situados = vagones_situados
            vagon_producto.vagones_cargados = vagones_cargados
            vagon_producto.plan_aseguramiento_proximos_dias = plan_aseguramiento
            
            # Validar campos obligatorios
            campos_obligatorios = [
                'plan_mensual', 'plan_anual', 'plan_acumulado_dia_anterior',
                'real_acumulado_dia_anterior', 'plan_acumulado_actual',
                'real_acumulado_actual', 'plan_acumulado_anual', 'real_acumulado_anual'
            ]
            
            campos_vacios = [campo for campo in campos_obligatorios if getattr(vagon_producto, campo) is None]
            
            if campos_vacios:
                print(f"Advertencia: Los siguientes campos están vacíos en el registro {vagon_producto.id}: {', '.join(campos_vacios)}")
            
            # Guardar todos los cambios
            vagon_producto.save()

  # Modelo para el historial de vagones_productos
class HistorialVagonesProductos(models.Model):
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo, 
        on_delete=models.CASCADE,
        related_name='historiales_vagones_productos'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    datos_vagon_producto = models.JSONField()  # Datos principales del registro
    datos_productos = models.JSONField()      # Productos relacionados
    
    class Meta:
        verbose_name = "Historial de vagón-producto"
        verbose_name_plural = "Historiales de vagones-productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Historial vagon-producto para informe {self.informe_operativo.id}"

# Señal para crear el historial al guardar
@receiver(post_save, sender=vagones_productos)
def crear_historial_vagones_productos(sender, instance, created, **kwargs):
    if not created:
        return

    def _crear_historial_vagones_productos():
        fecha_registro = instance.fecha.date()
        
        informe = ufc_informe_operativo.objects.annotate(
            fecha_op=TruncDate('fecha_operacion')
        ).filter(fecha_op=fecha_registro).first()
        
        if not informe:
            return

        # Obtener los productos directamente desde la instancia
        productos = instance.producto.all()
        
        # Serializar datos principales
        datos_principales = {
            'id': instance.id,
            'fecha': str(instance.fecha),
            'tipo_origen': instance.tipo_origen,
            'origen': instance.origen,
            'tipo_producto': instance.tipo_producto,
            'tipo_combustible': instance.tipo_combustible,
            'tipo_equipo': instance.tipo_equipo_ferroviario.get_tipo_equipo_display() if instance.tipo_equipo_ferroviario else None,
            'plan_mensual': instance.plan_mensual,
            'plan_dia': instance.plan_dia,
            'vagones_situados': instance.vagones_situados,
            'vagones_cargados': instance.vagones_cargados,
            'plan_anual': instance.plan_anual,
            'plan_acumulado_actual': instance.plan_acumulado_actual,
            'real_acumulado_actual': instance.real_acumulado_actual,
            'plan_acumulado_anual': instance.plan_acumulado_anual,
            'real_acumulado_anual': instance.real_acumulado_anual,
            'plan_aseguramiento_proximos_dias': instance.plan_aseguramiento_proximos_dias,
            'plan_acumulado': instance.plan_acumulado_dia_anterior,
            'real_acumulado': instance.real_acumulado_dia_anterior,
            'observaciones': instance.observaciones
        }

        # Serializar productos - versión mejorada
        productos_serializados = []
        if productos.exists():  # Verificar si hay productos
            for prod in productos:
                producto_data = {
                    'id': prod.id,
                    'producto': prod.producto.nombre_producto if prod.producto else None,
                    'tipo_embalaje': prod.tipo_embalaje.nombre_tipo_embalaje if prod.tipo_embalaje else None,
                    'unidad_medida': prod.unidad_medida.simbolo if prod.unidad_medida else None,
                    'cantidad': prod.cantidad,
                    'estado': prod.estado,
                    'contiene': prod.contiene
                }
                productos_serializados.append(producto_data)

        # Debug: Verificar datos antes de guardar
        print("Productos a serializar:", productos_serializados)

        HistorialVagonesProductos.objects.create(
            informe_operativo=informe,
            datos_vagon_producto=datos_principales,
            datos_productos=productos_serializados
        )

    transaction.on_commit(_crear_historial_vagones_productos)
# Señal para eliminar el historial
@receiver(post_delete, sender=vagones_productos)
def eliminar_historial_vagones_productos(sender, instance, **kwargs):
    try:
        HistorialVagonesProductos.objects.filter(
            datos_vagon_producto__icontains={'id': instance.id}
        ).delete()
    except Exception as e:
        print(f"Error eliminando historial de vagones-productos: {str(e)}") 

#************************************************************************************************************************************
#Modelo para representar en_trenes
class en_trenes(models.Model):
    
    TIPO_ORIGEN_DESTINO_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso comercial/CCD'),
    ]
    
    TIPO_EQUIPO_CHOICES=nom_tipo_equipo_ferroviario.t_equipo
    
    ESTADO_CHOICES = [
        ('vacio', 'Vacío'),
        ('cargado', 'Cargado'),
    ]

  
  #Cuando vayas a crear varias instancias con la misma ForeignKey hay que agregar "related_name"
  #Agregar "default" en los campos que tengan el parametro "choise"
    locomotora = models.ForeignKey(
        nom_equipo_ferroviario,
        on_delete=models.CASCADE,
        verbose_name="Locomotora asignada",
        help_text="Seleccione una locomotora.",
        related_name="trenes_locomotora",
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro", editable=False)
    numero_identificacion_locomotora = models.CharField(
        max_length=10,
        verbose_name="Número de identificación de la locomotora",
        blank=True,
        null=True,
    )
    tipo_equipo=models.ForeignKey(nom_tipo_equipo_ferroviario, on_delete=models.CASCADE,default="", max_length=50)
    estado = models.CharField(default="" ,choices=ESTADO_CHOICES, max_length = 50)
    producto = models.ManyToManyField(
        producto_UFC,
        blank=True,
        related_name="en_trenes",
        verbose_name="Productos"
    )
    
    tipo_origen = models.CharField(default="",choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length = 50)
    origen = models.CharField(default='',max_length=40)
    
    tipo_destino = models.CharField(default="",choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length = 50)
    destino = models.CharField(default='',max_length=40)
    cantidad_vagones=models.IntegerField(default=1,verbose_name="Cantidad de vagones")
    equipo_vagon=models.ManyToManyField(
        nom_equipo_ferroviario,
        blank=True,
        related_name="en_trenes_vagones",
        verbose_name="Productos"
    )
    observaciones = models.TextField(
        verbose_name="Observaciones",
        help_text="Ingrese observaciones adicionales. Admite letras, números y caracteres especiales.",
        blank=True,  # Permite que el campo esté vacío
        null=True,   # Permite valores nulos en la base de datos
    )
    def save(self, *args, **kwargs):
        # Llenar el campo numero_identificacion_locomotora con el valor de la locomotora relacionada
        if self.locomotora:
            self.numero_identificacion_locomotora = self.locomotora.numero_identificacion
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Tren"
        verbose_name_plural="Trenes"
         
    
    def __str__(self):
        return f"En trenes {self.id} -{self.numero_identificacion_locomotora}- {self.get_estado_display()}"
    
# Modelo para el historial de en_trenes
class HistorialEnTrenes(models.Model):
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo, 
        on_delete=models.CASCADE,
        related_name='historiales_en_trenes'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    datos_tren = models.JSONField()  # Almacena todos los datos del tren
    datos_productos = models.JSONField()  # Almacena datos de productos relacionados
    datos_vagones = models.JSONField()  # Almacena datos de los vagones relacionados
    
    class Meta:
        verbose_name = "Historial de tren"
        verbose_name_plural = "Historiales de trenes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Historial de tren para informe {self.informe_operativo.id} - {self.fecha_creacion}"

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
        informe = ufc_informe_operativo.objects.annotate(
            fecha_op=TruncDate('fecha_operacion')
        ).filter(fecha_op=fecha_tren).first()
        
        if not informe:
            return  # No hacer nada si no hay informe para esta fecha
        
        # Obtener el tren con todas sus relaciones
        tren_completo = en_trenes.objects.select_related(
            'locomotora',
            'tipo_equipo'
        ).prefetch_related(
            'producto__producto',
            'producto__tipo_embalaje',
            'producto__unidad_medida',
            'equipo_vagon'
        ).get(pk=instance.pk)
        
        # Serializar datos del tren
        datos_tren = {
            'id': tren_completo.id,
            'locomotora_id': tren_completo.locomotora.id if tren_completo.locomotora else None,
            'locomotora_numero': tren_completo.locomotora.numero_identificacion if tren_completo.locomotora else None,
            'fecha': str(tren_completo.fecha),
            'numero_identificacion_locomotora': tren_completo.numero_identificacion_locomotora,
            'tipo_equipo_id': tren_completo.tipo_equipo.id if tren_completo.tipo_equipo else None,
            'tipo_equipo_name': tren_completo.tipo_equipo.get_tipo_equipo_display() if tren_completo.tipo_equipo else None,
            'estado': tren_completo.estado,
            'tipo_origen': tren_completo.tipo_origen,
            'origen': tren_completo.origen,
            'tipo_destino': tren_completo.tipo_destino,
            'destino': tren_completo.destino,
            'cantidad_vagones': tren_completo.cantidad_vagones,
            'observaciones': tren_completo.observaciones
        }
        
        # Serializar productos relacionados
        productos = []
        for producto in tren_completo.producto.all():
            productos.append({
                'id': producto.id,
                'producto_name': producto.producto.nombre_producto,
                'tipo_embalaje_name': producto.tipo_embalaje.nombre_tipo_embalaje if producto.tipo_embalaje else None,
                'unidad_medida_simbolo': producto.unidad_medida.simbolo if producto.unidad_medida else None,
                'cantidad': producto.cantidad,
                'estado': producto.estado,
                'contiene': producto.contiene
            })
        
        # Serializar vagones relacionados
        vagones = []
        for vagon in tren_completo.equipo_vagon.all():
            vagones.append({
                'id': vagon.id,
                'numero_identificacion': vagon.numero_identificacion,
                'tipo_equipo': vagon.tipo_equipo.tipo_equipo if vagon.tipo_equipo else None,
                'estado_actual': vagon.estado_actual
            })
        
        # Crear registro de historial
        HistorialEnTrenes.objects.create(
            informe_operativo=informe,
            datos_tren=datos_tren,
            datos_productos=productos,
            datos_vagones=vagones
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
            datos_tren__icontains={'id': instance.id}
        )
        
        # Eliminar todos los registros de historial encontrados
        historiales.delete()
        
    except Exception as e:
        print(f"Error al eliminar historial del tren {instance.id}: {str(e)}")

#***********************************************************************************************************************

class por_situar(models.Model):
    
    t_origen = (
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso Comercial')
    )
    
    tipo_origen = models.CharField(max_length=100, choices=t_origen, verbose_name="Tipo de origen")
    origen = models.CharField(max_length=200, verbose_name="Origen")
    
    t_equipo = (
        ('casilla', 'Casilla'),
        ('caj_gon', 'Cajones o Góndola'),
        ('planc_plat', 'Plancha o Plataforma'),
        ('Plan_porta_cont', 'Plancha porta contenedores'),
        ('cist_liquidos', 'Cisterna para líquidos'),
        ('cist_solidos', 'Cisterna para sólidos'),
        ('tolva_g_mineral', 'Tolva granelera(mineral)'),
        ('tolva_g_agric', 'Tolva granelera(agrícola)'),
        ('tolva_g_cemento', 'Tolva para cemento'),
        ('volqueta', 'Volqueta'),
        ('Vagon_ref', 'Vagón refrigerado'),
        ('jaula', 'Jaula'),
        ('locomotora', 'Locomotora'),
        ('tren', 'Tren'),
    )
    
    tipo_equipo = models.CharField(max_length=200, choices=t_equipo, verbose_name="Tipo de equipo")
    
    status =(
        ('vacio', 'Vacio'),
        ('cargado', 'Cargado')
    )
    
    estado = models.CharField(max_length=200, choices=status, verbose_name="Estado")
    
    t_operacion = (
        ('carga', 'Carga'),
        ('descarga', 'Descarga')
    )
    
    operacion = models.CharField(max_length=200, choices=t_operacion, verbose_name="Operacion")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro", editable=False)
    producto = models.ManyToManyField(
        producto_UFC,
        blank=True,
        related_name="por_situar",
        verbose_name="Productos"
    )
    
    por_situar = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex='^-?\d+$',
                message='Solo se permiten números enteros (ej: 5, -10).',
                code='numero_invalido'
            )
        ],
        verbose_name="Por situar"
    )

    observaciones = models.TextField(
        verbose_name="Observaciones",
        help_text="Ingrese observaciones adicionales. Admite letras, números y caracteres especiales.",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Por situar"
        verbose_name_plural = "Por situar"
        ordering = ['tipo_origen', 'origen']

    def __str__(self):
        return f"{self.tipo_origen} - {self.origen} - {self.tipo_equipo}"
    
#clase asociada al historial de por_situar

class HistorialVagonPorSituar(models.Model):
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo, 
        on_delete=models.CASCADE,
        related_name='historiales_por_situar'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    datos_vagon = models.JSONField()  # Almacena todos los datos del por_situar
    datos_productos = models.JSONField()  # Almacena datos de productos relacionados
    
    class Meta:
        verbose_name = "Historial de vagón por situar"
        verbose_name_plural = "Historiales de vagones por situar"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Historial por situar para informe {self.informe_operativo.id} - {self.fecha_creacion}"

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
            informe = ufc_informe_operativo.objects.annotate(
                fecha_op=TruncDate('fecha_operacion')
            ).filter(fecha_op=fecha_vagon).first()
            
            if not informe:
                print(f"No se encontró informe operativo para la fecha {fecha_vagon}")
                return

            # Obtener productos directamente desde la instancia
            productos = instance.producto.all()
            
            # Serializar datos principales del por_situar
            datos_vagon = {
                'id': instance.id,
                'tipo_origen': instance.tipo_origen,
                'origen': instance.origen,
                'tipo_equipo': instance.tipo_equipo,
                'estado': instance.estado,
                'operacion': instance.operacion,
                'por_situar': instance.por_situar,
                'fecha': str(instance.fecha),
                'observaciones': instance.observaciones
            }
            
            # Serializar productos - versión robusta
            productos_serializados = []
            if productos.exists():  # Verificar si hay productos
                for producto in productos:
                    producto_data = {
                        'id': producto.id,
                        'producto_name': producto.producto.nombre_producto if producto.producto else None,
                        'tipo_embalaje_name': producto.tipo_embalaje.nombre_tipo_embalaje if producto.tipo_embalaje else None,
                        'unidad_medida_simbolo': producto.unidad_medida.simbolo if producto.unidad_medida else None,
                        'cantidad': producto.cantidad,
                        'estado': producto.estado,
                        'contiene': producto.contiene
                    }
                    productos_serializados.append(producto_data)
            
            # Debug: Verificar datos antes de guardar
            print(f"Datos a serializar - Productos: {len(productos_serializados)}")
            
            # Crear registro de historial
            HistorialVagonPorSituar.objects.create(
                informe_operativo=informe,
                datos_vagon=datos_vagon,
                datos_productos=productos_serializados
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
            datos_vagon__icontains={'id': instance.id}
        )
        
        # Eliminar todos los registros de historial encontrados
        historiales.delete()
        
    except Exception as e:
        print(f"Error al eliminar historial del por_situar {instance.id}: {str(e)}")

    
#**********************************************************************************************************************
class arrastres(models.Model):
    
    TIPO_ORIGEN_DESTINO_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', ' comercial/AccesoCCD'),
    ]
    
    tipo_origen = models.CharField(
        default="",
        choices=TIPO_ORIGEN_DESTINO_CHOICES, 
        max_length=50,
        verbose_name="Tipo de origen"
    )
    
    origen = models.CharField(
        default='',
        max_length=40,
        verbose_name="Origen"
    )
    
    TIPO_EQUIPO_CHOICES = (
        ('casilla', 'Casilla'),
        ('caj_gon', 'Cajones o Góndola'),
        ('planc_plat', 'Plancha o Plataforma'),
        ('Plan_porta_cont', 'Plancha porta contenedores'),
        ('cist_liquidos', 'Cisterna para líquidos'),
        ('cist_solidos', 'Cisterna para sólidos'),
        ('tolva_g_mineral', 'Tolva granelera(mineral)'),
        ('tolva_g_agric', 'Tolva granelera(agrícola)'),
        ('tolva_g_cemento', 'Tolva para cemento'),
        ('volqueta', 'Volqueta'),
        ('Vagon_ref', 'Vagón refrigerado'),
        ('jaula', 'Jaula'),
        ('locomotora', 'Locomotora'),
        ('tren', 'Tren'),
    )
    
    tipo_equipo = models.CharField(
        max_length=200, 
        choices=TIPO_EQUIPO_CHOICES, 
        verbose_name="Tipo de equipo", 
        blank=True, 
        null=True
    )
    
    ESTADO_CHOICES = (
        ('vacio', 'Vacio'),
        ('cargado', 'Cargado')
    )
    
    estado = models.CharField(
        max_length=200, 
        choices=ESTADO_CHOICES, 
        verbose_name="Estado", 
        blank=True, 
        null=True
    )
    
    producto = models.ManyToManyField(
        producto_UFC,
        blank=True,
        related_name="arrastres",
        verbose_name="Productos_UFC"
    )
    cantidad_vagones = models.CharField(
        max_length=10, 
        verbose_name="Cantidad de vagones",
    )
    
    tipo_destino = models.CharField(
        default="",
        choices=TIPO_ORIGEN_DESTINO_CHOICES, 
        max_length=50,
        verbose_name="Tipo de destino"
    )
    
    destino = models.CharField(
        default='',
        max_length=40,
        verbose_name="Destino"
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro", editable=False)
    class Meta:
        verbose_name = "arrastre"
        verbose_name_plural = "Arrastres"
     #   db_table = "arrastres"  # Esto asegura que la tabla se llame exactamente "arrastres"
     #no quiero que la tabla se llame arrastres, quiero que se llame ufc_arrastre
    
    def __str__(self):
        return f"Arrastre Pendiente{self.id} - {self.origen}"
    
# Modelo para el historial de arrastres
class HistorialArrastres(models.Model):
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo, 
        on_delete=models.CASCADE,
        related_name='historiales_arrastres'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    datos_arrastre = models.JSONField()  # Almacena todos los datos del arrastre
    datos_productos = models.JSONField()  # Almacena datos de productos relacionados
    
    class Meta:
        verbose_name = "Historial de arrastre"
        verbose_name_plural = "Historiales de arrastres"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Historial de arrastre para informe {self.informe_operativo.id} - {self.fecha_creacion}"

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
        informe = ufc_informe_operativo.objects.annotate(
            fecha_op=TruncDate('fecha_operacion')
        ).filter(fecha_op=fecha_arrastre).first()
        
        if not informe:
            return  # No hacer nada si no hay informe para esta fecha
        
        # Obtener el arrastre con todas sus relaciones
        arrastre_completo = arrastres.objects.prefetch_related(
            'producto__producto',
            'producto__tipo_embalaje',
            'producto__unidad_medida'
        ).get(pk=instance.pk)
        
        # Serializar datos del arrastre
        datos_arrastre = {
            'id': arrastre_completo.id,
            'tipo_origen': arrastre_completo.tipo_origen,
            'origen': arrastre_completo.origen,
            'tipo_equipo': arrastre_completo.tipo_equipo,
            'estado': arrastre_completo.estado,
            'cantidad_vagones': arrastre_completo.cantidad_vagones,
            'tipo_destino': arrastre_completo.tipo_destino,
            'destino': arrastre_completo.destino,
            'fecha': str(arrastre_completo.fecha)
        }
        
        # Serializar productos relacionados
        productos = []
        for producto in arrastre_completo.producto.all():
            productos.append({
                'id': producto.id,
                'producto_name': producto.producto.nombre_producto,
                'tipo_embalaje_name': producto.tipo_embalaje.nombre_tipo_embalaje if producto.tipo_embalaje else None,
                'unidad_medida_simbolo': producto.unidad_medida.simbolo if producto.unidad_medida else None,
                'cantidad': producto.cantidad,
                'estado': producto.estado,
                'contiene': producto.contiene
            })
        
        # Crear registro de historial
        HistorialArrastres.objects.create(
            informe_operativo=informe,
            datos_arrastre=datos_arrastre,
            datos_productos=productos
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
            datos_arrastre__icontains={'id': instance.id}
        )
        
        # Eliminar todos los registros de historial encontrados
        historiales.delete()
        
    except Exception as e:
        print(f"Error al eliminar historial del arrastre {instance.id}: {str(e)}")

#************************************************************************************************************************
    
    
class rotacion_vagones(models.Model):
    tipo_equipo_ferroviario = models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.CASCADE,
        related_name="tipo_equipo_rotacion",
        verbose_name="Equipo ferroviario"
    )
    
  #  registro_vagones=models.ManyToManyField(vagon_cargado_descargado, blank=True,related_name="vagones_rotacion", verbose_name="Registro de rotacion de vagones")
    en_servicio = models.PositiveIntegerField(verbose_name="En servicio")
    plan_carga = models.PositiveIntegerField(verbose_name="Plan carga")
    real_carga = models.PositiveIntegerField(verbose_name="Real carga")
    plan_rotacion = models.PositiveIntegerField(verbose_name="Plan rotación")
    real_rotacion = models.PositiveIntegerField(verbose_name="Real rotación")

    creado_el = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    actualizado_el = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Registro de rotación"
        verbose_name_plural = "Registros de rotación"
        ordering = ["-creado_el"]

    def __str__(self):
        return f"{self.tipo_equipo_ferroviario.tipo_equipo} - Servicio: {self.en_servicio}"
    
# Modelo para el historial de rotacion_vagones
class HistorialRotacionVagones(models.Model):
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo,
        on_delete=models.CASCADE,
        related_name='historiales_rotacion_vagones'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    datos_rotacion = models.JSONField()  # Almacena todos los datos de rotación
    
    class Meta:
        verbose_name = "Historial de rotación de vagones"
        verbose_name_plural = "Historiales de rotaciones de vagones"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Historial rotación vagones para informe {self.informe_operativo.id}"

# Señal para crear el historial al guardar
@receiver(post_save, sender=rotacion_vagones)
def crear_historial_rotacion_vagones(sender, instance, created, **kwargs):
    if not created:
        return

    def _crear_historial():
        fecha_registro = instance.creado_el.date()
        
        informe = ufc_informe_operativo.objects.annotate(
            fecha_op=TruncDate('fecha_operacion')
        ).filter(fecha_op=fecha_registro).first()
        
        if not informe:
            return

        # Obtener el registro completo con relaciones
        registro_completo = rotacion_vagones.objects.select_related(
            'tipo_equipo_ferroviario'
        ).get(pk=instance.pk)

        # Serializar datos principales
        datos_rotacion = {
            'id': registro_completo.id,
            'tipo_equipo': {
                'id': registro_completo.tipo_equipo_ferroviario.id,
                'nombre': registro_completo.tipo_equipo_ferroviario.get_tipo_equipo_display(),
            },
            'en_servicio': registro_completo.en_servicio,
            'plan_carga': registro_completo.plan_carga,
            'real_carga': registro_completo.real_carga,
            'plan_rotacion': registro_completo.plan_rotacion,
            'real_rotacion': registro_completo.real_rotacion,
            'creado_el': str(registro_completo.creado_el),
            'actualizado_el': str(registro_completo.actualizado_el)
        }

        HistorialRotacionVagones.objects.create(
            informe_operativo=informe,
            datos_rotacion=datos_rotacion
        )

    transaction.on_commit(_crear_historial)

# Señal para eliminar el historial
@receiver(post_delete, sender=rotacion_vagones)
def eliminar_historial_rotacion_vagones(sender, instance, **kwargs):
    try:
        HistorialRotacionVagones.objects.filter(
            datos_rotacion__icontains={'id': instance.id}
        ).delete()
    except Exception as e:
        print(f"Error eliminando historial de rotación de vagones: {str(e)}")
    
    
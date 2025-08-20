from django.db import models
from Administracion.models import CustomUser
from nomencladores.models import( nom_producto,nom_tipo_embalaje,nom_unidad_medida,
                                 nom_entidades,nom_incidencia,nom_provincia,nom_terminal,nom_atraque,
                                 nom_tipo_maniobra_portuaria,nom_puerto,nom_osde_oace_organismo
                                 )

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete,pre_delete

from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from Administracion.models import CustomUser
from nomencladores.models import nom_producto, nom_tipo_embalaje, nom_unidad_medida, nom_entidades, nom_incidencia, nom_provincia
from rest_framework.decorators import api_view
from rest_framework.response import Response
class gemar_parte_hecho_extraordinario(models.Model):
    tipo_parte = models.CharField(
        default="Parte de hecho extraordinario", 
        max_length=14
    )    
    fecha_operacion = models.DateTimeField( 
        verbose_name="Fecha de operación",
        auto_now_add=False
    )
    fecha_actual = models.DateTimeField(
        auto_now=True, 
        verbose_name="Fecha actual"
    )
    
    estado_parte = models.CharField(
        default="Creado", 
        max_length=14
    )
    provincia = models.ForeignKey(
        nom_provincia, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Provincia"
    )
    creado_por = models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True, null=True, verbose_name="Creado por: ", related_name="gemar_informe_creador" )
    
    aprobado_por = models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True, null=True, verbose_name="Aprobado por: ", related_name="gemar_informe_aprobador" )
    
    entidad = models.ForeignKey(
        nom_entidades,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Entidad"
    )   
    
    organismo = models.ForeignKey(
        nom_osde_oace_organismo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Organismo",
        editable=False  # No se edita manualmente
    )

    def save(self, *args, **kwargs):
        # Solo para asegurar que los campos no sean nulos si vienen de la vista
        super().save(*args, **kwargs)

    class Meta: 
        permissions = [
            ("gemar_puede_rechazar_informe", "Puede rechazar partes de hechos extraordinarios"),
            ("gemar_puede_aprobar_informe", "Puede aprobar partes de hechos extraordinarios"),
            ("gemar_puede_cambiar_informe_a_listo", "Puede cambiar el estado del informe de hechos extraordinarios a listo"),
        ]
               
        verbose_name = "Parte de hecho extraordinario"
        verbose_name_plural = "Partes de hechos extraordinarios"
        ordering = ["-fecha_operacion"]
    
    def __str__(self):
        return f"Fecha actual: {self.fecha_actual} - fecha de operación {self.fecha_operacion}"
    

 #/*********************************************************************************************************************   
#modelo para el hecho extraordinario como tal
class gemar_hecho_extraordinario(models.Model):
    T_INVOLUCRADO_CHOICES = [
        ("puerto", "Puerto"),
        ("entidad", "Entidad"),
        ("buque", "Buque"),
    ]  

    TIPO_ORIGEN_CHOICES = [
        ("puerto", "Puerto"),
        ("entidad", "Entidad"),
    ] 

    TIPO_DIFERENCIA_CHOICES = [
        ("sobrante", "Sobrante"),
        ("faltante", "Faltante"),
    ]  

    AVERIA_CHOICES = [
        ("si", "Sí"),
        ("no", "No"),
    ]

    fecha_operacion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de operación", unique=True
    )
    fecha_actual = models.DateTimeField(
        auto_now=True, verbose_name="Fecha actual", unique=True
    )
    informado = models.CharField(max_length=200, verbose_name="Informado")
    garante = models.ForeignKey(nom_entidades,on_delete=models.CASCADE,blank=True, null=True, 
                                related_name="gemar_garante",verbose_name="Garante o dueño")
    tipo_involucrado = models.CharField(choices=T_INVOLUCRADO_CHOICES, max_length=20, default="puerto")
    involucrado = models.CharField(max_length=40, null=True, blank=True)
    tipo_origen = models.CharField(
        choices=TIPO_ORIGEN_CHOICES, max_length=50)

    origen = models.CharField(max_length=40)
    destino = models.CharField(max_length=40)
    producto_involucrado = models.ForeignKey(nom_producto,on_delete=models.CASCADE, verbose_name="Producto involucrado")
    embalaje = models.ForeignKey(nom_tipo_embalaje,on_delete=models.CASCADE, verbose_name="Embalaje")
    unidad_medida = models.ForeignKey(nom_unidad_medida,on_delete=models.CASCADE, verbose_name="Unidad de medida")
    tipo_diferencia = models.CharField(choices=TIPO_DIFERENCIA_CHOICES, max_length=20, default="Tipo de diferencia")
    kg_diferencia = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    cantidad_diferencia = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    valor_diferencia = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    averia = models.CharField(max_length=2, choices=AVERIA_CHOICES, blank=True, null=True, default="no")
    kg_averia = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    cantidad_averia = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    valor_averia = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    incidencia_involucrada = models.ForeignKey(nom_incidencia,on_delete=models.CASCADE, verbose_name="Incidencia involucrada")
    descripcion_hecho = models.CharField(max_length=500,blank=True,null=True) 

    parte_hecho_extraordinario = models.ForeignKey(
        gemar_parte_hecho_extraordinario,
        on_delete=models.CASCADE,
        related_name='hechos_extraordinarios',
        null=True, blank=True
    )   

    class Meta:   
        unique_together = ('garante', 'producto_involucrado','origen','destino','tipo_diferencia','descripcion_hecho')           
        verbose_name = "Hecho extraordinario"
        verbose_name_plural = "Hechos extraordinarios"
        ordering = ["-fecha_actual"]
    
   
    def __str__(self):
        return self.tipo_diferencia
    #******************************************************************************************************************************
class gemar_parte_programacion_maniobras(models.Model): 
    tipo_parte = models.CharField(
        default="Parte de programación de maniobras", 
        max_length=14
    ) 
    fecha_operacion = models.DateTimeField(
        verbose_name="Fecha de operación",
        auto_now_add=False,          
    )
    fecha_actual = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha actual"
    )
    
    estado_parte = models.CharField(
        default="Creado",
        max_length=14
    )
    provincia = models.ForeignKey(
        nom_provincia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Provincia"
    )
    creado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
        blank=True, null=True, verbose_name="Creado por: ",
        related_name="gemar_parte_programacion_maniobras_creador")
    
    aprobado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
        blank=True, null=True, verbose_name="Aprobado por: ",
        related_name="gemar_parte_programacion_maniobras_aprobador")
    
    entidad = models.ForeignKey(
        nom_entidades,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Entidad",
        editable=False  # No se edita manualmente
    )
    
    organismo = models.ForeignKey(
        nom_osde_oace_organismo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Organismo",
        editable=False  # No se edita manualmente
    )

    class Meta:
        permissions = [
            ("gemar_puede_rechazar_parte_programacion_maniobras", "Puede rechazar partes de programación de maniobras"),
            ("gemar_puede_aprobar_parte_programacion_maniobras", "Puede aprobar partes de programación de maniobras"),
            ("gemar_puede_cambiar__parte_programacion_maniobras_a_listo", "Puede cambiar el estado del de programación de maniobras a listo"),
        ]
                
        verbose_name = "Parte de programación de maniobras"
        verbose_name_plural = "Partes de programación de maniobras"
        ordering = ["-fecha_actual"]
    
    def __str__(self):
        return f"Fecha actual: {self.fecha_actual} - fecha de operación {self.fecha_operacion}"
#************************************************************************************************************************************

class gemar_programacion_maniobras(models.Model):
    # Opciones para campos de selección
    FORMATO_HORA_CHOICES = [
        (1, '24 horas'),
        (2, 'AM/PM'),
        (3, 'SIN DETERMINAR'),
    ]
    
    AM_PM_CHOICES = [
        (1, 'AM'),
        (2, 'PM'),
    ]
    
    # Campos principales
    puerto = models.ForeignKey(
        'nomencladores.nom_puerto',
        on_delete=models.PROTECT,
        verbose_name='Puerto',
        related_name='partes_programacion_puerto'  # Nombre único para la relación inversa
    )
    
    terminal = models.ForeignKey(
        'nomencladores.nom_terminal',
        on_delete=models.PROTECT,
        verbose_name='Terminal',
        related_name='partes_programacion_terminal'
    )
    
    atraque = models.ForeignKey(
        'nomencladores.nom_atraque',
        on_delete=models.PROTECT,
        verbose_name='Atraque',
        related_name='partes_programacion_atraque'
    )
    
    buque = models.CharField(
        max_length=255,
        verbose_name='Buque',
        blank=False,
        null=False
    )
    
    puerto_procedencia = models.ForeignKey(
        'nomencladores.nom_puerto',
        on_delete=models.PROTECT,
        verbose_name='Puerto procedencia',
        blank=True,
        null=True,
        related_name='partes_programacion_puerto_procedencia'  # Nombre único diferente
    )
    
    tipo_maniobra = models.ForeignKey(
        'nomencladores.nom_tipo_maniobra_portuaria',
        on_delete=models.PROTECT,
        verbose_name='Tipo de maniobra',
        related_name='partes_programacion_tipo_maniobra'
    )
    
    # Campos ETA (Estimated Time of Arrival)
    formato_eta = models.CharField(max_length=5,
        choices=FORMATO_HORA_CHOICES,
        verbose_name='Formato ETA'
    )
    
    fecha_eta = models.DateField(
        verbose_name='Fecha ETA',
        blank=True,
        null=True
    )
    
    hora_eta = models.TimeField(
        verbose_name='Hora ETA',
        blank=True,
        null=True
    )
    
    hora_eta_am_pm = models.CharField(max_length=5,
        choices=AM_PM_CHOICES,
        verbose_name='Hora ETA (AM/PM)',
        blank=True,
        null=True
    )
    
    # Campos ETS (Estimated Time of Sailing)
    formato_ets = models.CharField(max_length=5,
        choices=FORMATO_HORA_CHOICES,
        verbose_name='Formato ETS'
    )
    
    fecha_ets = models.DateField(
        verbose_name='Fecha ETS',
        blank=True,
        null=True
    )
    
    hora_ets = models.TimeField(
        verbose_name='Hora ETS',
        blank=True,
        null=True
    )
    
    hora_ets_am_pm = models.CharField(max_length=5,
        choices=AM_PM_CHOICES,
        verbose_name='Hora ETS (AM/PM)',
        blank=True,
        null=True
    )
    
    # Otros campos
    cantidad_remolcadores = models.PositiveSmallIntegerField(
        verbose_name='Cantidad de remolcadores',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    
    observaciones = models.TextField(
        verbose_name='Observaciones',
        blank=True,
        null=True
    )

    parte_programacion_maniobra = models.ForeignKey(
        gemar_parte_programacion_maniobras,
        on_delete=models.CASCADE,
        related_name='parte_programacion_maniobra',
        null=True, blank=True
    )
    
    # Metadata
    class Meta:
        verbose_name = 'Programación de maniobras'
        verbose_name_plural = 'Programación de maniobras'
        ordering = ['-fecha_eta']  # Ordenar por fecha ETA descendente por defecto
    
    def __str__(self):
        return f"Buque {self.buque} - puerto {self.puerto} ({self.fecha_eta})"
    

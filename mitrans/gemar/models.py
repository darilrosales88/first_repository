from django.db import models
from django.conf import settings
from Administracion.models import CustomUser
from nomencladores.models import( nom_atraque, nom_estado_tecnico, nom_pais, nom_producto,nom_tipo_embalaje,nom_unidad_medida,
                                 nom_entidades,nom_incidencia,nom_provincia,nom_terminal,nom_puerto,nom_osde_oace_organismo,nom_embarcacion
                                 )


from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from nomencladores.models import (
    nom_embarcacion as Buque, nom_puerto, nom_terminal, nom_producto, 
    nom_osde_oace_organismo, nom_tipo_embalaje, nom_unidad_medida
)
from Administracion.models import CustomUser
from django.utils import timezone
from django.db import models
from Administracion.models import CustomUser
from nomencladores.models import nom_producto, nom_tipo_embalaje, nom_unidad_medida, nom_entidades, nom_incidencia, nom_provincia
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
# CHOICES GLOBALES (reutilizables)
TIPO_PARTE_CHOICES = [
    ('HECHO_EXTRAORDINARIO', 'Hecho Extraordinario'),
    ('PROGRAMACION_MANIOBRAS', 'Programación Maniobras'),
    ('PBIP', 'PBIP'),
    ('EXISTENCIA_MERCANCIA', 'Existencia Mercancía'),
]
class gemar_parte_hecho_extraordinario(models.Model):
    tipo_parte = models.CharField(
        default="Parte de hecho extraordinario", 
        max_length=100
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
        ("1", '24 horas'),
        ("2", 'AM/PM'),
        ("3", 'SIN DETERMINAR'),
    ]
    
    AM_PM_CHOICES = [
        ("1", 'AM'),
        ("2", 'PM'),
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
    
class PartePBIP(models.Model):
    
    # Opciones para campos de selección
    NIVEL_CHOICES = [
        (1, 'Nivel 1'),
        (2, 'Nivel 2'),
        (3, 'Nivel 3'),
    ]
    
    ESTADO_CHOICES = [
        ('Creado', 'Creado'),      # ← Formato título
        ('Listo', 'Listo'),        # ← Formato título  
        ('Aprobado', 'Aprobado'),  # ← Formato título (debe coincidir)
        ('Rechazado', 'Rechazado'), # ← Formato título
        
    ]
    
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='Creado'
    )

    # Campos de fecha y hora
    fecha_operacion = models.DateField(
        verbose_name=_('Fecha de operación'),
        help_text=_('Fecha en que se realiza la operación portuaria')
    )
    
    fecha_creacion = models.DateTimeField(
        verbose_name=_('Fecha de creación'),
        auto_now_add=True,
        help_text=_('Fecha y hora en que se creó el registro')
    )
    
    

    # Relaciones con otros modelos
    buque = models.ForeignKey(
        Buque,
        on_delete=models.PROTECT,
        verbose_name=_('Buque'),
        related_name='partes_pbip_buque'
    )
    
    puerto = models.ForeignKey(
        nom_puerto,
        on_delete=models.PROTECT,
        verbose_name=_('Puerto'),
        related_name='partes_pbip_puerto'
    )
    
    creado_por = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name=_('Creado por'),
        related_name='partes_pbip_creados'
    )
    
    aprobado_por = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name=_('Aprobado por'),
        null=True,
        blank=True,
        related_name='partes_pbip_aprobados'
    )

    # Campos de estado y nivel
    nivel = models.IntegerField(
        verbose_name=_('Nivel de seguridad'),
        choices=NIVEL_CHOICES,
        help_text=_('Nivel de protección establecido para la operación')
    )
    
    estado = models.CharField(
        verbose_name=_('Estado del parte'),
        max_length=20,
        choices=ESTADO_CHOICES,
        default='CREADO',
        help_text=_('Estado actual del parte PBIP')
    )

    # Metadata
    class Meta:
        verbose_name = _('Parte PBIP')
        verbose_name_plural = _('Partes PBIP')
        unique_together = ('buque', 'puerto', 'nivel', 'fecha_operacion')
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['fecha_operacion']),
            models.Index(fields=['estado']),
            models.Index(fields=['nivel']),
        ]

    # Métodos
    def __str__(self):
        return f"PBIP - {self.buque.nombre} - {self.puerto.nombre} - Nivel {self.get_nivel_display()}"

    def clean(self):
        """
        Validación para asegurar que la fecha de operación no sea futura
        """
        if self.fecha_operacion and self.fecha_operacion > timezone.now().date():
            raise ValidationError({
                'fecha_operacion': _('La fecha de operación no puede ser futura.')
            })
            
    def save(self, *args, **kwargs):
        """
        Sobreescritura del método save para incluir validaciones adicionales
        """
        self.full_clean()
        super().save(*args, **kwargs)

# gemar/models.py (actualización de CargaVieja)
class CargaVieja(models.Model):
    parte = models.ForeignKey(PartePBIP, on_delete=models.CASCADE, related_name='cargas_viejas')
    puerto = models.ForeignKey(nom_puerto, on_delete=models.PROTECT, verbose_name=_('Puerto'))
    terminal = models.ForeignKey(nom_terminal, on_delete=models.PROTECT, verbose_name=_('Terminal'))
    producto = models.ForeignKey(nom_producto, on_delete=models.PROTECT, verbose_name=_('Producto'))
    manifiesto = models.CharField(_('Manifiesto'), max_length=100)
    toneladas_ayer = models.DecimalField(_('Toneladas ayer'), max_digits=10, decimal_places=2)
    toneladas_hoy = models.DecimalField(_('Toneladas hoy'), max_digits=10, decimal_places=2)
    organismo = models.ForeignKey(nom_osde_oace_organismo, on_delete=models.PROTECT, verbose_name=_('Organismo'))
    dias_almacen = models.IntegerField(_('Días en almacén'))
    plan = models.DecimalField(_('Plan'), max_digits=10, decimal_places=2)
    real = models.DecimalField(_('Real'), max_digits=10, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(_('Observaciones'), null=True, blank=True)
    estado = models.CharField(_('Estado'), max_length=20, default='CREADO', choices=[
        ('CREADO', 'Creado'),
        ('APROBADO', 'Aprobado'),
        ('CANCELADO', 'Cancelado'),
    ])
    aprobado_por = models.ForeignKey(
        CustomUser, 
        on_delete=models.PROTECT, 
        verbose_name=_('Aprobado por'),
        null=True,
        blank=True,
        related_name='cargas_viejas_aprobadas'
    )

    class Meta:
        verbose_name = _('Carga Vieja')
        verbose_name_plural = _('Cargas Viejas')
        unique_together = ('parte', 'puerto', 'terminal', 'producto', 'manifiesto', 'organismo')

    def __str__(self):
        return f"Carga Vieja - {self.producto.nombre} - {self.manifiesto}"

    def clean(self):
        if self.toneladas_ayer < 0 or self.toneladas_hoy < 0:
            raise ValidationError(_('Las toneladas no pueden ser negativas.'))
        if self.dias_almacen < 0:
            raise ValidationError(_('Los días en almacén no pueden ser negativos.'))

class ExistenciaMercancia(models.Model):
    # Opciones para campos de selección
    TIPO_CHOICES = [
        (1, 'Importación'),
        (2, 'Exportación'),
    ]
    
    TIPO_PRODUCTO_CHOICES = [
        (1, 'Producto'),
        (2, 'Contenedor'),
    ]
    
    ESTADO_CONTENEDOR_CHOICES = [
        (1, 'Vacío'),
        (2, 'Lleno'),
    ]
    
    CONTENIDO_CHOICES = [
        (1, 'Alimentos'),
        (2, 'Productos varios'),
    ]
    
    ESTADO_REGISTRO_CHOICES = [  # ← Este para estado_registro (string)
        ('CREADO', 'Creado'),
        ('LISTO', 'Listo'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    estado_registro = models.CharField(
        max_length=20,
        choices=ESTADO_REGISTRO_CHOICES,
        default='Creado'
    )
    # Campos de fecha
    fecha_operacion = models.DateField(
        verbose_name=_('Fecha de operación'),
        help_text=_('Fecha en que se registra la existencia de mercancía')
    )
    
    fecha_creacion = models.DateTimeField(
        verbose_name=_('Fecha de creación'),
        auto_now_add=True,
        help_text=_('Fecha y hora en que se creó el registro')
    )

    # Relaciones con otros modelos
    terminal = models.ForeignKey(
        nom_terminal,
        on_delete=models.PROTECT,
        verbose_name=_('Terminal'),
        related_name='existencias_terminal'
    )
    
    producto = models.ForeignKey(
        nom_producto,
        on_delete=models.PROTECT,
        verbose_name=_('Producto'),
        related_name='existencias_producto'
    )
    
    tipo_embalaje = models.ForeignKey(
        nom_tipo_embalaje,
        on_delete=models.PROTECT,
        verbose_name=_('Tipo de embalaje'),
        null=True,
        blank=True,
        related_name='existencias_tipo_embalaje'
    )
    
    unidad_medida = models.ForeignKey(
        nom_unidad_medida,
        on_delete=models.PROTECT,
        verbose_name=_('Unidad de medida'),
        related_name='existencias_unidad_medida'
    )
    
    creado_por = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name=_('Creado por'),
        related_name='existencias_creadas'
    )
    
    aprobado_por = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name=_('Aprobado por'),
        null=True,
        blank=True,
        related_name='existencias_aprobadas'
    )

    # Campos de tipo y estado
    tipo = models.IntegerField(
        verbose_name=_('Tipo'),
        choices=TIPO_CHOICES,
        help_text=_('Tipo de operación (Importación/Exportación)')
    )
    
    tipo_producto = models.IntegerField(
        verbose_name=_('Tipo de producto'),
        choices=TIPO_PRODUCTO_CHOICES,
        help_text=_('Tipo de producto (Producto/Contenedor)')
    )
    
    estado = models.IntegerField(
        verbose_name=_('Estado del contenedor'),
        choices=ESTADO_CONTENEDOR_CHOICES,
        null=True,
        blank=True,
        help_text=_('Estado del contenedor (Vacío/Lleno)')
    )
    
    contiene = models.IntegerField(
        verbose_name=_('Contenido del contenedor'),
        choices=CONTENIDO_CHOICES,
        null=True,
        blank=True,
        help_text=_('Contenido del contenedor (si está lleno)')
    )
    
    estado_registro = models.CharField(
        verbose_name=_('Estado del registro'),
        max_length=20,
        choices=ESTADO_REGISTRO_CHOICES,
        default='CREADO',  # ← Formato título (igual que PartePBIP)
        help_text=_('Estado actual del registro de existencia')
    )

    # Campos numéricos
    existencia = models.DecimalField(
        verbose_name=_('Existencia'),
        max_digits=10,
        decimal_places=2,
        help_text=_('Cantidad de mercancía existente')
    )

    # Metadata
    class Meta:
        verbose_name = _('Existencia de Mercancía')
        verbose_name_plural = _('Existencias de Mercancías')
        unique_together = ('fecha_operacion', 'terminal', 'tipo', 'producto', 'tipo_embalaje', 'unidad_medida')
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['fecha_operacion']),
            models.Index(fields=['tipo']),
            models.Index(fields=['tipo_producto']),
            models.Index(fields=['estado_registro']),
        ]

    # Métodos
    def __str__(self):
        return f"Existencia - {self.get_tipo_display()} - {self.producto.nombre}"

    def clean(self):
        """
        Validaciones complejas del modelo
        """
        # Validación de fecha de operación
        if self.fecha_operacion and self.fecha_operacion > timezone.now().date():
            raise ValidationError({
                'fecha_operacion': _('La fecha de operación no puede ser futura.')
            })
            
        # Validación para contenedores
        if self.tipo_producto == 2:  # Contenedor
            if not self.estado:
                raise ValidationError({
                    'estado': _('Para contenedores debe especificar el estado.')
                })
            if self.estado == 2 and not self.contiene:  # Lleno
                raise ValidationError({
                    'contiene': _('Para contenedores llenos debe especificar qué contienen.')
                })
        else:
            # Limpiar campos de contenedor si no es contenedor
            self.estado = None
            self.contiene = None
            
        # Validación de cantidad no negativa
        if self.existencia < 0:
            raise ValidationError({
                'existencia': _('La cantidad no puede ser negativa.')
            })
            
    def save(self, *args, **kwargs):
        """
        Sobreescritura del método save para incluir validaciones adicionales
        """
        self.full_clean()
        super().save(*args, **kwargs)

    # Métodos de display para choices
    def get_tipo_display(self):
        return dict(self.TIPO_CHOICES).get(self.tipo, '')
        
    def get_tipo_producto_display(self):
        return dict(self.TIPO_PRODUCTO_CHOICES).get(self.tipo_producto, '')
        
    def get_estado_display(self):
        return dict(self.ESTADO_CONTENEDOR_CHOICES).get(self.estado, '') if self.estado else ''
        
    def get_contiene_display(self):
        return dict(self.CONTENIDO_CHOICES).get(self.contiene, '') if self.contiene else ''
        
    def get_estado_registro_display(self):
        return dict(self.ESTADO_REGISTRO_CHOICES).get(self.estado_registro, '')
    
class ParteCombinado(models.Model):
    TIPO_PARTE_CHOICES = [
        ('HECHO_EXTRAORDINARIO', 'Hecho Extraordinario'),
        ('PROGRAMACION_MANIOBRAS', 'Programación Maniobras'),
        ('PBIP', 'PBIP'),
        ('EXISTENCIA_MERCANCIA', 'Existencia Mercancía'),
    ]

    ESTADO_PARTE_CHOICES = [
        ('creado', 'Creado'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('listo', 'Listo'),
    ]
    
    tipo_parte = models.CharField(max_length=50, choices=TIPO_PARTE_CHOICES)
    fecha_actual = models.DateTimeField(auto_now_add=True)
    estado_parte = models.CharField(max_length=20, choices=ESTADO_PARTE_CHOICES, default='creado')
    
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partes_creados')
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='partes_aprobados')
    
    # RELACIONES OPCIONALES CON LOS MODELOS EXISTENTES
    entidad = models.ForeignKey(nom_entidades, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Entidad")
    organismo = models.ForeignKey(nom_osde_oace_organismo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Organismo")
    provincia = models.ForeignKey(nom_provincia, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Provincia")
    
    # CAMPOS DE TEXTO COMO BACKUP (opcional)
    entidad_nombre = models.CharField(max_length=100, blank=True)
    organismo_nombre = models.CharField(max_length=100, blank=True)
    provincia_nombre = models.CharField(max_length=100, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_tipo_parte_display()} - {self.fecha_actual.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
    # Sincronizar nombres desde las relaciones
        if self.entidad:
            self.entidad_nombre = self.entidad.nombre
        if self.organismo:
            self.organismo_nombre = self.organismo.nombre
        if self.provincia:
        # Verifica el nombre correcto del campo en nom_provincia
            self.provincia_nombre = getattr(self.provincia, 'nombre_provincia', 
                                       getattr(self.provincia, 'nombre', ''))
    
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Parte Combinado"
        verbose_name_plural = "Partes Combinados"
        ordering = ['-fecha_creacion']

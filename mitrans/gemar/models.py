# gemar/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from nomencladores.models import (
    nom_embarcacion as Buque, nom_puerto, nom_terminal, nom_producto, 
    nom_osde_oace_organismo, nom_tipo_embalaje, nom_unidad_medida
)
from Administracion.models import CustomUser
from django.utils import timezone

class PartePBIP(models.Model):
    NIVEL_CHOICES = [
        (1, 'Nivel 1'),
        (2, 'Nivel 2'),
        (3, 'Nivel 3'),
    ]

    fecha_operacion = models.DateField(_('Fecha de operación'))
    fecha_creacion = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    buque = models.ForeignKey(Buque, on_delete=models.PROTECT, verbose_name=_('Buque'))
    puerto = models.ForeignKey(nom_puerto, on_delete=models.PROTECT, verbose_name=_('Puerto'))
    fecha_hora = models.DateTimeField(_('Fecha y hora'))
    nivel = models.IntegerField(_('Nivel'), choices=NIVEL_CHOICES)
    creado_por = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_('Creado por'))
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
        related_name='partes_pbip_aprobados'
    )

    class Meta:
        verbose_name = _('Parte PBIP')
        verbose_name_plural = _('Partes PBIP')
        unique_together = ('buque', 'puerto', 'nivel', 'fecha_operacion')

    def __str__(self):
        return f"PBIP - {self.buque.nombre} - {self.puerto.nombre} - {self.get_nivel_display()}"

    def clean(self):
        if self.fecha_operacion > timezone.now().date():
            raise ValidationError(_('La fecha de operación no puede ser futura.'))

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

    fecha_operacion = models.DateField(_('Fecha de operación'))
    fecha_creacion = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    terminal = models.ForeignKey(nom_terminal, on_delete=models.PROTECT, verbose_name=_('Terminal'))
    tipo = models.IntegerField(_('Tipo'), choices=TIPO_CHOICES)
    tipo_producto = models.IntegerField(_('Tipo de producto'), choices=TIPO_PRODUCTO_CHOICES)
    producto = models.ForeignKey(nom_producto, on_delete=models.PROTECT, verbose_name=_('Producto'))
    tipo_embalaje = models.ForeignKey(nom_tipo_embalaje, on_delete=models.PROTECT, verbose_name=_('Tipo de embalaje'), null=True, blank=True)
    unidad_medida = models.ForeignKey(nom_unidad_medida, on_delete=models.PROTECT, verbose_name=_('Unidad de medida'))
    estado = models.IntegerField(_('Estado'), choices=ESTADO_CONTENEDOR_CHOICES, null=True, blank=True)
    contiene = models.IntegerField(_('Contiene'), choices=CONTENIDO_CHOICES, null=True, blank=True)
    existencia = models.DecimalField(_('Existencia'), max_digits=10, decimal_places=2)
    creado_por = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_('Creado por'))
    estado_registro = models.CharField(_('Estado'), max_length=20, default='CREADO', choices=[
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
        related_name='existencias_aprobadas'
    )

    class Meta:
        verbose_name = _('Existencia de Mercancía')
        verbose_name_plural = _('Existencias de Mercancías')
        unique_together = ('fecha_operacion', 'terminal', 'tipo', 'producto', 'tipo_embalaje', 'unidad_medida')

    def __str__(self):
        return f"Existencia - {self.get_tipo_display()} - {self.producto.nombre}"

    def clean(self):
        if self.tipo_producto == 2:  # Contenedor
            if not self.estado:
                raise ValidationError(_('Para contenedores debe especificar el estado.'))
            if self.estado == 2 and not self.contiene:  # Lleno
                raise ValidationError(_('Para contenedores llenos debe especificar qué contienen.'))
        else:
            self.estado = None
            self.contiene = None
            
        if self.existencia < 0:
            raise ValidationError(_('La existencia no puede ser negativa.'))
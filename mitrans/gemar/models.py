from django.db import models
from Administracion.models import CustomUser
from nomencladores.models import( nom_producto,nom_tipo_embalaje,nom_unidad_medida,
                                 nom_entidades,nom_incidencia,nom_provincia
                                 )
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete,pre_delete

#Modelo para el informe de hecho extraordinario

from django.db import models
from Administracion.models import CustomUser
from nomencladores.models import nom_producto, nom_tipo_embalaje, nom_unidad_medida, nom_entidades, nom_incidencia, nom_provincia

class gemar_parte_hecho_extraordinario(models.Model):    
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

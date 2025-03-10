from django.db import models
from nomencladores.models import nom_puerto,nom_tipo_equipo_ferroviario,nom_producto,nom_tipo_embalaje,nom_unidad_medida

#productos asociados a vagones cargados/descargados
class productos_vagones_cargados_descargados(models.Model):
    TIPO_PROD_CHOICES = [
        ('producto', 'Producto'),
        ('contenedor', 'Contenedor'),
    ]

    ESTADO_CHOICES = [
        ('vacio', 'Vacío'),
        ('lleno', 'lleno'),
    ]

    CONTIENE_CHOICES = [
        ('alimentos', 'Alimentos'),
        ('productos_varios', 'Productos varios'),
    ]

    tipo_producto = models.CharField(choices=TIPO_PROD_CHOICES, max_length = 20)
    producto = models.ForeignKey(nom_producto, on_delete=models.CASCADE)
    tipo_embalaje = models.ForeignKey(nom_tipo_embalaje, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(nom_unidad_medida, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado = models.CharField(choices=ESTADO_CHOICES, null=True, blank=True, max_length = 20)
    contiene = models.CharField(choices=CONTIENE_CHOICES, null=True, blank=True, max_length = 20)

    class Meta:
        verbose_name = "Producto de vagón cargado/descargado"
        verbose_name_plural = "Productos de vagones cargados/descargados"
        #unique_together = [['cliente', 'destino']] 

    
    def __str__(self):
        return f"tipo de producto {self.get_tipo_producto_display()} - {self.producto.nombre_producto}"

# Modelo para representar los vagones cargados/descargados
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
    
    tipo_origen = models.CharField(choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length = 50)
    origen = models.CharField(max_length=40)
    tipo_equipo_ferroviario = models.ForeignKey(nom_tipo_equipo_ferroviario, on_delete=models.CASCADE)
    estado = models.CharField(choices=ESTADO_CHOICES, max_length = 50)    
    operacion = models.CharField(choices=OPERACION_CHOICES, editable=False, max_length = 50)
    plan_diario_carga_descarga = models.IntegerField()
    real_carga_descarga = models.IntegerField(default = 0, editable=False)
    tipo_destino = models.CharField(choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length = 50)
    destino = models.CharField(max_length=40)
    causas_incumplimiento = models.TextField(null=True, blank=True, max_length = 100)
    producto = models.ForeignKey(productos_vagones_cargados_descargados, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Vagones cargados/descargados"
        #unique_together = [['cliente', 'destino']]
        verbose_name = "Vagón cargado/descargado"
         

    
    def __str__(self):
        return f"Vagón {self.id} - {self.get_estado_display()}"


    
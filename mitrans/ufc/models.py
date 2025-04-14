from django.db import models
from nomencladores.models import nom_puerto,nom_tipo_equipo_ferroviario,nom_producto,nom_tipo_embalaje,nom_unidad_medida,nom_equipo_ferroviario
from nomencladores.models import nom_destino
from django.core.validators import RegexValidator



#productos asociados a vagones cargados/descargados

class producto_en_vagon(models.Model):
   
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
        verbose_name = "Producto en vagon"
        verbose_name_plural = "Producto en vagones"
        #unique_together = [['cliente', 'destino']] 

    
    def __str__(self):
        return f"tipo de producto {self.get_contiene_display()} - {self.producto.nombre_producto}"
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
    operacion = models.CharField(choices=OPERACION_CHOICES, editable=True, max_length = 50)
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
    numero_identificacion_locomotora = models.CharField(
        max_length=10,
        verbose_name="Número de identificación de la locomotora",
        blank=True,
        null=True,
    )
    tipo_equipo=models.ForeignKey(nom_tipo_equipo_ferroviario, on_delete=models.CASCADE,default="", max_length=50)
    estado = models.CharField(default="" ,choices=ESTADO_CHOICES, max_length = 50)
    producto = models.ForeignKey(producto_en_vagon,default='', on_delete=models.CASCADE,null=True, blank=True)
    
    
    tipo_origen = models.CharField(default="",choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length = 50)
    origen = models.CharField(default='',max_length=40)
    
    tipo_destino = models.CharField(default="",choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length = 50)
    destino = models.CharField(default='',max_length=40)
    cantidad_vagones=models.IntegerField(default=1,verbose_name="Cantidad de vagones")
    equipo_vagon=models.ForeignKey(nom_equipo_ferroviario, on_delete=models.CASCADE)
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
    
    producto = models.ForeignKey(nom_producto, null=False, blank=False, on_delete=models.CASCADE)
    
    por_situar = models.CharField( max_length=10, validators=[ RegexValidator(
                regex='^-?\d+$',  # Acepta positivos y negativos
                message='Solo se permiten números enteros (ej: 5, -10).',
                code='numero_invalido'
            )
        ]
    )
    observaciones = models.TextField(
        verbose_name="Observaciones",
        help_text="Ingrese observaciones adicionales. Admite letras, números y caracteres especiales.",
        blank=True,  # Permite que el campo esté vacío
        null=True,   # Permite valores nulos en la base de datos
    )

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
    
    producto = models.ForeignKey(nom_producto, null=False, blank=False, on_delete=models.CASCADE)
    
    situados = models.CharField( max_length=10, validators=[ RegexValidator(
                regex='^-?\d+$',  # Acepta positivos y negativos
                message='Solo se permiten números enteros (ej: 5, -10).',
                code='numero_invalido'
            )
        ]
    )
    
    pendiente_proximo_dia = models.CharField( max_length=10, validators=[ RegexValidator(
                regex='^-?\d+$',  # Acepta positivos y negativos
                message='Solo se permiten números enteros (ej: 5, -10).',
                code='numero_invalido'
            )
        ]
    )
    
    observaciones = models.TextField(
        verbose_name="Observaciones",
        help_text="Ingrese observaciones adicionales. Admite letras, números y caracteres especiales.",
        blank=True,  # Permite que el campo esté vacío
        null=True,   # Permite valores nulos en la base de datos
    )
    
class arrastres(models.Model):
    
    TIPO_ORIGEN_DESTINO_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso comercial/CCD'),
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
    
    producto = models.ForeignKey(
        nom_producto, 
        on_delete=models.CASCADE, 
        null=False, 
        blank=False, 
        verbose_name="Producto"
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
    
    class Meta:
        verbose_name = "arrastre"
        verbose_name_plural="Arrastres"
    
    
    
    def __str__(self):
        return f"Arrastre Pendiente{self.id} - {self.origen}"
    
    
    
    
    
    
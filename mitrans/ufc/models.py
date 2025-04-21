from django.db import models
from nomencladores.models import nom_puerto,nom_tipo_equipo_ferroviario,nom_producto,nom_tipo_embalaje,nom_unidad_medida,nom_equipo_ferroviario
from nomencladores.models import nom_destino
from django.core.validators import RegexValidator



#productos asociados a vagones en trenes
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
    
#productos asociados al estado vagones cargados/descargados
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

#Modelo creado para los productos asociados al modelo vagones y productos
class productos_vagones_productos(models.Model):
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
        verbose_name = "Producto de vagones y productos"
        verbose_name_plural = "Productos de vagones y productos"
        #unique_together = [['cliente', 'destino']] 

    
    def __str__(self):
        return f"tipo de producto {self.get_tipo_producto_display()} - {self.producto.nombre_producto}"
# Modelo para representar el estado vagones cargados/descargados
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
    # Cambiamos ForeignKey a ManyToManyField, es posible que un vagon tenga mas de un producto
    producto = models.ManyToManyField(
        productos_vagones_cargados_descargados,
        blank=True,
        related_name='vagones_asociados'
    )

    registros_vagones = models.ManyToManyField(
        'registro_vagones_cargados',
        blank=True,
        related_name='vagon_principal',
        verbose_name="Registros de vagones asociados"
    )

    class Meta:
        verbose_name_plural = "Vagones cargados/descargados"
        verbose_name = "Vagón cargado/descargado"   

    def delete(self, *args, **kwargs):
        # Eliminar primero los registros_vagones asociados
        self.registros_vagones.all().delete()
        # Luego eliminar el registro padre
        super().delete(*args, **kwargs)     

    def __str__(self):
        return f"Vagón {self.id} - {self.get_estado_display()}"
    
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
        db_table = "registro_vagones_cargados"

    def __str__(self):
        return f"Vagón {self.no_id}" if self.no_id else "Registro sin ID"
    
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
    ]
    TIPO_COMBUSTIBLE_CHOICES = [
        ('combustible_blanco', 'Combustible blanco'),
        ('combustible_negro', 'Combustible negro'),
        ('combustible_turbo', 'Combustible turbo'),
    ]

    
    tipo_origen = models.CharField(choices=TIPO_ORIGEN_CHOICES, max_length = 50)
    origen = models.CharField(max_length=40)
    tipo_producto = models.CharField(choices=TIPO_PRODUCTO_CHOICES, max_length = 20,blank=True,null=True)
    tipo_combustible = models.CharField(choices=TIPO_COMBUSTIBLE_CHOICES, max_length = 20,blank=True,null=True)
    tipo_equipo_ferroviario = models.ForeignKey(nom_tipo_equipo_ferroviario, on_delete=models.CASCADE,blank=True,null=True)
    plan_mensual = models.IntegerField()
    plan_dia = models.IntegerField(editable=False,default=0)
    vagones_situados = models.IntegerField(editable=False,default=0)
    vagones_cargados = models.IntegerField(editable=False,default=0)
    plan_aseguramiento_proximos_dias = models.IntegerField(editable=False,default=0)
    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones",
        help_text="Admite letras, números y caracteres especiales"
    )

    #ManyToManyField, es posible que un vagon tenga mas de un producto
    producto = models.ManyToManyField(
        productos_vagones_productos,
        blank=True,
        related_name='producto_vagones_productos'
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
    
    producto = models.ForeignKey(
        producto_en_vagon,
        on_delete=models.SET_NULL,  # Cambiado a SET_NULL para mayor seguridad
        null=True,
        blank=True,
        related_name="producto_por_situar",
        verbose_name="Producto"
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
    
    producto = models.ForeignKey(producto_en_vagon, null=True, blank=True, on_delete=models.CASCADE)
    
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
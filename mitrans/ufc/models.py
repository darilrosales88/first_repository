from django.db import models
from nomencladores.models import( nom_tipo_equipo_ferroviario,nom_producto,
                                 nom_tipo_embalaje,nom_unidad_medida,
                                 nom_equipo_ferroviario,nom_provincia   
                                 )
from Administracion.models import CustomUser
from django.core.validators import RegexValidator
# Usamos un delay para asegurar que las relaciones ManyToMany estén establecidas 
from django.db import transaction





#Modelo para el informe operativo
class ufc_informe_operativo(models.Model):    

    fecha_operacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de operación", unique=True)
    fecha_actual = models.DateTimeField(auto_now=True, verbose_name="Fecha actual", unique=True)
    plan_mensual_total = models.IntegerField(default=0)
    plan_diario_total_vagones_cargados = models.IntegerField(default=0)
    real_total_vagones_cargados = models.IntegerField(default=0)
    total_vagones_situados = models.IntegerField(default=0)
    plan_total_acumulado_actual = models.IntegerField(default=0)
    real_total_acumulado_actual = models.IntegerField(default=0)
    estado_parte = models.CharField(default="Creado",max_length=14)
    provincia=models.ForeignKey(nom_provincia,on_delete=models.CASCADE,blank=True, null=True, verbose_name="Provincia")
    creado_por=models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True, null=True, verbose_name="Creado por: ", related_name="informe_creador" )
    aprobado_por=models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True,null=True, verbose_name="Aprobado por: ", related_name="informe_aprobador")

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

class vagones_dias(models.Model):
    equipo_ferroviario=models.ForeignKey(nom_equipo_ferroviario,on_delete=models.CASCADE,related_name="registro_por_dias",verbose_name="Vagones por Dias", null=True,blank=True)
    cant_dias=models.PositiveSmallIntegerField(verbose_name="Cantidad de Dias")


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

    informe_operativo = models.ForeignKey(
        ufc_informe_operativo,
        on_delete=models.CASCADE,
        related_name='vagones_cargados_descargados',
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Vagones cargados/descargados"
        verbose_name = "Vagón cargado/descargado"  

    def delete(self, *args, **kwargs):
        try:
            from nomencladores.models import nom_equipo_ferroviario
            
            # Obtener todos los registros asociados antes de eliminarlos
            registros_asociados = list(self.registros_vagones.all())
            
            # Actualizar estado de equipos y eliminar registros asociados
            for registro in registros_asociados:
                try:
                    with transaction.atomic():
                        # Actualizar estado del equipo
                        equipo = nom_equipo_ferroviario.objects.filter(
                            numero_identificacion=registro.no_id
                        ).first()
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                        
                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.no_id}: {str(e)}")
                    continue
            
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.registros_vagones.clear()
            self.producto.clear()
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
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



#************************************************************************************************************************
#Modelo Situado
class Situado_Carga_Descarga(models.Model):
    
    TIPO_ORIGEN_DESTINO_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso comercial/CCD'),
    ]
    
    tipo_origen = models.CharField(max_length=100, choices=TIPO_ORIGEN_DESTINO_CHOICES, verbose_name="Tipo de origen", blank=True, null=True)
    origen = models.CharField(max_length=200, verbose_name="Origen")
    
    
    
    tipo_equipo=models.ForeignKey(nom_tipo_equipo_ferroviario, on_delete=models.SET_NULL,null=True, blank=True,default="", max_length=50)
    #tipo_equipo=models.CharField(max_length=100)
    equipo_vagon=models.ManyToManyField(
        vagones_dias,
        blank=True,
        related_name="situados_vagones_dias",
        verbose_name="Equipos Situados"
    )
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
    
    
    
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo,
        on_delete=models.CASCADE,
        related_name='situados',
        null=True, blank=True
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
        
    def delete(self, *args, **kwargs):
        try:
            from nomencladores.models import nom_equipo_ferroviario
            
            # Obtener todos los registros asociados antes de eliminarlos
            registros_asociados = list(self.equipo_vagon.all())
            
            # Actualizar estado de equipos y eliminar registros asociados
            for registro in registros_asociados:
                try:
                    with transaction.atomic():
                        # Actualizar estado del equipo
                        equipo = nom_equipo_ferroviario.objects.filter(
                            numero_identificacion=registro.no_id
                        ).first()
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                        
                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.no_id}: {str(e)}")
                    continue
            
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.equipo_vagon.clear()
            self.producto.clear()
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
            raise

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
    plan_anual = models.IntegerField(default=0)
    plan_acumulado_dia_anterior = models.IntegerField()
    real_acumulado_dia_anterior = models.IntegerField()
    
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo,
        on_delete=models.CASCADE,
        related_name='vagones_productos',
        null=True, blank=True
    )


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


#************************************************************************************************************************************
#Modelo para representar en_trenes
class en_trenes(models.Model):
    
    TIPO_ORIGEN_DESTINO_CHOICES = [
        ('puerto', 'Puerto'),
        ('ac_ccd', 'Acceso comercial/CCD'),
    ]
    
    #TIPO_EQUIPO_CHOICES=nom_tipo_equipo_ferroviario.t_equipo
    
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
        verbose_name="Vagones en Trenes"
    )
    observaciones = models.TextField(
        verbose_name="Observaciones",
        help_text="Ingrese observaciones adicionales. Admite letras, números y caracteres especiales.",
        blank=True,  # Permite que el campo esté vacío
        null=True,   # Permite valores nulos en la base de datos
    )
    
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo,
        on_delete=models.CASCADE,
        related_name='en_trenes',
        null=True, blank=True
    )

    
    def save(self, *args, **kwargs):
        # Llenar el campo numero_identificacion_locomotora con el valor de la locomotora relacionada
        if self.locomotora:
            self.numero_identificacion_locomotora = self.locomotora.numero_identificacion
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Tren"
        verbose_name_plural="Trenes"
         
    def delete(self, *args, **kwargs):
        try:
            from nomencladores.models import nom_equipo_ferroviario
            
            # Obtener todos los registros asociados antes de eliminarlos
            registros_asociados = list(self.equipo_vagon.all())
            
            # Actualizar estado de equipos y eliminar registros asociados
            for registro in registros_asociados:
                try:
                    with transaction.atomic():
                        # Actualizar estado del equipo
                        equipo = nom_equipo_ferroviario.objects.filter(
                            numero_identificacion=registro.no_id
                        ).first()
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                        
                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.no_id}: {str(e)}")
                    continue
            
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.equipo_vagon.clear()
            self.producto.clear()
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
    
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
    
    tipo_equipo = models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.SET_NULL,
        verbose_name="Tipo de equipo", 
        blank=True, 
        null=True
    )
    
    equipo_vagon=models.ManyToManyField(
        vagones_dias,
        blank=True,
        related_name="por_situar_vagones_dias",
        verbose_name="Equipos por Situar"
    )
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
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo,
        on_delete=models.CASCADE,
        related_name='por_situar',
        null=True, blank=True
    )


    class Meta:
        verbose_name = "Por situar"
        verbose_name_plural = "Por situar"
        ordering = ['tipo_origen', 'origen']

    def delete(self, *args, **kwargs):
        try:
            from nomencladores.models import nom_equipo_ferroviario
            
            # Obtener todos los registros asociados antes de eliminarlos
            registros_asociados = list(self.equipo_vagon.all())
            
            # Actualizar estado de equipos y eliminar registros asociados
            for registro in registros_asociados:
                try:
                    with transaction.atomic():
                        # Actualizar estado del equipo
                        equipo = nom_equipo_ferroviario.objects.filter(
                            numero_identificacion=registro.no_id
                        ).first()
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                        
                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.no_id}: {str(e)}")
                    continue
            
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.equipo_vagon.clear()
            self.producto.clear()
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
    
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
    
    tipo_equipo = models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.SET_NULL,
        verbose_name="Tipo de equipo", 
        blank=True, 
        null=True
    )
    
    equipo_vagon=models.ManyToManyField(
        vagones_dias,
        blank=True,
        related_name="arrastre_vagones_dias",
        verbose_name="Equipos en Arrastre"
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
    
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo,
        on_delete=models.CASCADE,
        related_name='arrastres',
        null=True, blank=True
    )

    class Meta:
        verbose_name = "arrastre"
        verbose_name_plural = "Arrastres"
     #   db_table = "arrastres"  # Esto asegura que la tabla se llame exactamente "arrastres"
     #no quiero que la tabla se llame arrastres, quiero que se llame ufc_arrastre
    
    
    def delete(self, *args, **kwargs):
        try:
            from nomencladores.models import nom_equipo_ferroviario
            
            # Obtener todos los registros asociados antes de eliminarlos
            registros_asociados = list(self.equipo_vagon.all())
            
            # Actualizar estado de equipos y eliminar registros asociados
            for registro in registros_asociados:
                try:
                    with transaction.atomic():
                        # Actualizar estado del equipo
                        equipo = nom_equipo_ferroviario.objects.filter(
                            numero_identificacion=registro.no_id
                        ).first()
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                        
                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.no_id}: {str(e)}")
                    continue
            
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.equipo_vagon.clear()
            self.producto.clear()
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
    
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
    plan_rotacion = models.FloatField(verbose_name="Plan rotación")
    real_rotacion = models.FloatField(verbose_name="Real rotación")

    fecha = models.DateTimeField(auto_now_add=True,  verbose_name="Fecha de registro")
    actualizado_el = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    
    informe_operativo = models.ForeignKey(
        ufc_informe_operativo,
        on_delete=models.CASCADE,
        related_name='rotacion',
        null=True, blank=True
    )


    class Meta:
        verbose_name = "Registro de rotación"
        verbose_name_plural = "Registros de rotación"
        ordering = ["-fecha"]

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

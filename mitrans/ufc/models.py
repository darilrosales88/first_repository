from django.db import models, transaction
from django.core.validators import RegexValidator

from Administracion.models import CustomUser
from nomencladores.models import( nom_tipo_equipo_ferroviario,nom_producto,
                                 nom_tipo_embalaje,nom_unidad_medida,
                                 nom_equipo_ferroviario,nom_provincia,
                                 nom_entidades   
                                 )





#Modelo para el informe operativo
class ufc_informe_operativo(models.Model):    

    fecha_operacion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de operación", unique=True
    )
    fecha_actual = models.DateTimeField(
        auto_now=True, verbose_name="Fecha actual", unique=True
    )
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
    entidad = models.ForeignKey(
        nom_entidades,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Entidad de donde proviene el parte"
    )
    class Meta:
        permissions = [
            ("puede_rechazar_informe", "Puede rechazar informes operativos"),
            ("puede_aprobar_informe", "Puede aprobar informes operativos"),
            ("puede_cambiar_a_listo", "Puede cambiar el estado del informe a listo"),
        ]
        verbose_name = "Parte informe operativo"
        verbose_name_plural = "Parte informe operativo"
        ordering = ["-fecha_operacion"]
    
    def save(self, *args, **kwargs):
        # Asignar entidad del creador si no está establecida
        if not self.entidad and self.creado_por:
            self.entidad = self.creado_por.entidad
            self.provincia=self.creado_por.entidad.provincia
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Fecha de operación {self.fecha_operacion} - fecha actual: {self.fecha_actual}"

#*************************************************************************************************************************

class vagones_dias(models.Model):
    equipo_ferroviario=models.ForeignKey(nom_equipo_ferroviario,on_delete=models.CASCADE,related_name="registro_por_dias",verbose_name="Vagones por Dias", null=True,blank=True)
    cant_dias=models.PositiveSmallIntegerField(verbose_name="Cantidad de Dias")


#productos asociados a vagones en trenes
class producto_UFC(models.Model):

    ESTADO_CHOICES = [
        ("vacio", "Vacío"),
        ("lleno", "Lleno"),
    ]
    CONTIENE_CHOICES = [
        ("alimentos", "Alimentos"),
        ("prod_varios", "Productos Varios"),
    ]

    producto = models.ForeignKey(nom_producto, on_delete=models.CASCADE)
    tipo_embalaje = models.ForeignKey(nom_tipo_embalaje, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(nom_unidad_medida, on_delete=models.CASCADE)
    
    tipo_equipo=models.ForeignKey(nom_tipo_equipo_ferroviario,on_delete=models.CASCADE,null=True,blank=True)
    
    cantidad = models.IntegerField()
    estado = models.CharField(
        choices=ESTADO_CHOICES, null=True, blank=True, max_length=20
    )
    contiene = models.CharField(
        choices=CONTIENE_CHOICES, null=True, blank=True, max_length=20
    )

    class Meta:
        verbose_name = "Producto UFC"
        verbose_name_plural = "Productos en UFC"
        # unique_together = [['cliente', 'destino']]

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


# productos asociados al estado vagones cargados/descargados

# Modelo creado para los productos asociados al modelo vagones y productos

# Modelo para representar el estado vagones cargados/descargados

# modelo para registrar los vagones asociados al estado vagones cargados/descargados
class registro_vagones_cargados(models.Model):
    # Opciones para el campo tipo_origen
    TIPO_ORIGEN_CHOICES = [
        ("puerto", "Puerto"),
        ("ac_ccd", "Acceso comercial/CCD"),
    ]

    no_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        
        verbose_name="Número de identificación",
        help_text="Valores definidos en el nomenclador de equipos ferroviarios (excepto 'Locomotora')",
    )

    fecha_despacho = models.DateField(
        null=True, blank=True, verbose_name="Fecha de despacho"
    )

    tipo_origen = models.CharField(
        choices=TIPO_ORIGEN_CHOICES, max_length=50, null=True, blank=True
    )

    origen = models.CharField(max_length=40, null=True, blank=True)

    fecha_llegada = models.DateField(
        null=True, blank=True, verbose_name="Fecha de llegada"
    )

    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones",
        help_text="Admite letras, números y caracteres especiales",
    )

    class Meta:
        verbose_name = "Registro de vagón cargado"
        verbose_name_plural = "Registros de vagones cargados"

    def __str__(self):
        return f"Vagón {self.no_id}" if self.no_id else "Registro sin ID"


class vagon_cargado_descargado(models.Model):
    TIPO_ORIGEN_DESTINO_CHOICES = [
        ("puerto", "Puerto"),
        ("ac_ccd", "Acceso comercial/CCD"),
    ]

    ESTADO_CHOICES = [
        ("vacio", "Vacío"),
        ("cargado", "Cargado"),
    ]

    OPERACION_CHOICES = [
        ("carga", "Carga"),
        ("descarga", "Descarga"),
    ]

    TIPO_DESTINO_CHOICES = [
        ("puerto", "Puerto"),
        ("ac_ccd", "Acceso comercial/CCD"),
    ]

    fecha = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de registro", editable=False
    )
    tipo_origen = models.CharField(choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length=50)
    origen = models.CharField(max_length=40)
    tipo_equipo_ferroviario = models.ForeignKey(
        nom_tipo_equipo_ferroviario, on_delete=models.CASCADE
    )
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=50)
    operacion = models.CharField(
        choices=OPERACION_CHOICES, editable=True, max_length=50
    )
    plan_diario_carga_descarga = models.IntegerField()
    real_carga_descarga = models.IntegerField(default=0, editable=False)
    tipo_destino = models.CharField(choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length=50)
    destino = models.CharField(max_length=40)
    causas_incumplimiento = models.TextField(
        null=False, blank=True, default="", max_length=100
    )
    # Cambiamos ForeignKey a ManyToManyField, es posible que un vagon tenga mas de un producto
    producto = models.ForeignKey(
        producto_UFC, blank=True, related_name="vagones_cargados", on_delete=models.SET_NULL,null=True
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
                            equipo.estado_actual = "Disponible"
                            equipo.save()

                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.no_id}: {str(e)}")
                    continue

            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.registros_vagones.clear()

            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)

        except Exception as e:
            print(
                f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}"
            )
            raise




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

    fecha = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de registro", editable=False
    )
    producto = models.ForeignKey(
        producto_UFC, blank=True, related_name="situados", verbose_name="Productos situados a la carga/descarga",on_delete=models.SET_NULL,null=True
    )

    situados = models.CharField(
        max_length=10,
        verbose_name="Cantidad de situados",
        default="0",
        validators=[
            
            RegexValidator(
                regex="^[0-9]+$",
                message="Solo se permiten números positivos",
                code="invalid_situados",
            )
        ],
    )

    pendiente_proximo_dia = models.CharField(
        max_length=10,
        verbose_name="Pendientes para el próximo día",
        default="0",
        validators=[
            RegexValidator(
                regex="^[0-9]+$",
                message="Solo se permiten números positivos",
                code="invalid_pendientes",
            )
        ],
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
        null=True,  # Permite valores nulos en la base de datos
    )

    class Meta:
        verbose_name = "Situado "
        verbose_name_plural = "Situados"
        ordering = ['tipo_origen', 'origen']
        
    def delete(self, *args, **kwargs):
        try:
            
            # Obtener todos los registros asociados antes de eliminarlos
            registros_asociados = list(self.equipo_vagon.all())
            
            # Actualizar estado de equipos y eliminar registros asociados
            for registro in registros_asociados:
                try:
                    with transaction.atomic():
                        # Actualizar estado del equipo
                        equipo =registro.equipo_ferroviario
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                        
                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.id}: {str(e)}")
                    continue
            
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.equipo_vagon.clear()
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
            

    def __str__(self):
        return f"{self.tipo_origen} - {self.origen} - {self.tipo_equipo}"






#**************************************************************************************************
#Modelo destinado a vagones y productos
class vagones_productos(models.Model):
    TIPO_ORIGEN_CHOICES = [
        ("puerto", "Puerto"),
        ("ac_ccd", "Acceso comercial/CCD"),
    ]

    TIPO_PRODUCTO_CHOICES = [
        ("producto", "Producto"),
        ("contenedor", "Contenedor"),
        ("combustible", "Combustible"),
    ]
    TIPO_COMBUSTIBLE_CHOICES = [
        ("combustible_blanco", "Combustible blanco"),
        ("combustible_negro", "Combustible negro"),
        ("combustible_turbo", "Combustible turbo"),
        ("-", "-"),
    ]

    fecha = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de registro", editable=False
    )
    tipo_origen = models.CharField(choices=TIPO_ORIGEN_CHOICES, max_length=50)
    origen = models.CharField(max_length=40)
    tipo_producto = models.CharField(
        choices=TIPO_PRODUCTO_CHOICES, max_length=20, blank=True, null=True
    )
    tipo_combustible = models.CharField(
        choices=TIPO_COMBUSTIBLE_CHOICES, max_length=20, blank=True, null=True
    )
    tipo_equipo_ferroviario = models.ForeignKey(
        nom_tipo_equipo_ferroviario, on_delete=models.CASCADE, blank=True, null=True
    )
    plan_mensual = models.IntegerField()
    plan_dia = models.IntegerField(editable=False, default=0)
    vagones_situados = models.IntegerField(editable=False, default=0)
    vagones_cargados = models.IntegerField(editable=False, default=0)
    plan_acumulado_actual = models.IntegerField(editable=False, default=0)
    real_acumulado_actual = models.IntegerField(editable=False, default=0)
    plan_acumulado_anual = models.IntegerField(editable=False, default=0)
    real_acumulado_anual = models.IntegerField(editable=False, default=0)
    plan_aseguramiento_proximos_dias = models.IntegerField(
        editable=False, default=0, blank=True
    )
    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones",
        help_text="Admite letras, números y caracteres especiales",
    )

    # ManyToManyField, es posible que un vagon tenga mas de un producto
    producto = models.ForeignKey(
        producto_UFC, blank=True, related_name="vagones_productos", on_delete=models.SET_NULL,null=True
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
        
        return f"Vagones y productos: {self.producto}"




#************************************************************************************************************************************
#Modelo para representar en_trenes
class en_trenes(models.Model):

    TIPO_ORIGEN_DESTINO_CHOICES = [
        ("puerto", "Puerto"),
        ("ac_ccd", "Acceso comercial/CCD"),
    ]
    
    #TIPO_EQUIPO_CHOICES=nom_tipo_equipo_ferroviario.t_equipo
    
    ESTADO_CHOICES = [
        ("vacio", "Vacío"),
        ("cargado", "Cargado"),
    ]

    # Cuando vayas a crear varias instancias con la misma ForeignKey hay que agregar "related_name"
    # Agregar "default" en los campos que tengan el parametro "choise"
    locomotora = models.ForeignKey(
        nom_equipo_ferroviario,
        on_delete=models.CASCADE,
        verbose_name="Locomotora asignada",
        help_text="Seleccione una locomotora.",
        related_name="trenes_locomotora",
    )
    fecha = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de registro", editable=False
    )
    numero_identificacion_locomotora = models.CharField(
        max_length=10,
        verbose_name="Número de identificación de la locomotora",
        blank=True,
        null=True,
    )
    tipo_equipo = models.ForeignKey(
        nom_tipo_equipo_ferroviario, on_delete=models.CASCADE, default="", max_length=50
    )
    estado = models.CharField(default="", choices=ESTADO_CHOICES, max_length=50)
    producto = models.ForeignKey(
        producto_UFC, blank=True, related_name="en_trenes", verbose_name="Productos en Trenes",on_delete=models.SET_NULL,null=True
    )

    tipo_origen = models.CharField(
        default="", choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length=50
    )
    origen = models.CharField(default="", max_length=40)

    tipo_destino = models.CharField(
        default="", choices=TIPO_ORIGEN_DESTINO_CHOICES, max_length=50
    )
    destino = models.CharField(default="", max_length=40)
    cantidad_vagones = models.IntegerField(
        default=1, verbose_name="Cantidad de vagones"
    )
    equipo_vagon = models.ManyToManyField(
        nom_equipo_ferroviario,
        blank=True,
        related_name="en_trenes_vagones",
        verbose_name="Vagones en Trenes"
    )
    observaciones = models.TextField(
        verbose_name="Observaciones",
        help_text="Ingrese observaciones adicionales. Admite letras, números y caracteres especiales.",
        blank=True,  # Permite que el campo esté vacío
        null=True,  # Permite valores nulos en la base de datos
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
            self.numero_identificacion_locomotora = (
                self.locomotora.numero_identificacion
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tren"
        verbose_name_plural="Trenes"

        constraints = [models.UniqueConstraint(
            fields = [
                "tipo_equipo",
                "estado",
                "origen",
                "destino",
            ],
            name="unique_train_register",
        )]

    def delete(self, *args, **kwargs):
        try:
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.equipo_vagon.clear()
        
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
    
    def __str__(self):
        return f"En trenes {self.id} -{self.numero_identificacion_locomotora}- {self.get_estado_display()}"



#***********************************************************************************************************************

class por_situar(models.Model):

    t_origen = (("puerto", "Puerto"), ("ac_ccd", "Acceso Comercial"))

    tipo_origen = models.CharField(
        max_length=100, choices=t_origen, verbose_name="Tipo de origen"
    )
    origen = models.CharField(max_length=200, verbose_name="Origen")

    t_equipo = (
        ("casilla", "Casilla"),
        ("caj_gon", "Cajones o Góndola"),
        ("planc_plat", "Plancha o Plataforma"),
        ("Plan_porta_cont", "Plancha porta contenedores"),
        ("cist_liquidos", "Cisterna para líquidos"),
        ("cist_solidos", "Cisterna para sólidos"),
        ("tolva_g_mineral", "Tolva granelera(mineral)"),
        ("tolva_g_agric", "Tolva granelera(agrícola)"),
        ("tolva_g_cemento", "Tolva para cemento"),
        ("volqueta", "Volqueta"),
        ("Vagon_ref", "Vagón refrigerado"),
        ("jaula", "Jaula"),
        ("locomotora", "Locomotora"),
        ("tren", "Tren"),
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

    t_operacion = (("carga", "Carga"), ("descarga", "Descarga"))

    operacion = models.CharField(
        max_length=200, choices=t_operacion, verbose_name="Operacion"
    )
    fecha = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de registro", editable=False
    )
    producto = models.ForeignKey(
        producto_UFC, blank=True, related_name="por_situar", verbose_name="Productos por Situar", on_delete=models.SET_NULL, null=True
    )

    por_situar = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex="^-?\d+$",
                message="Solo se permiten números enteros (ej: 5, -10).",
                code="numero_invalido",
            )
        ],
        verbose_name="Por situar",
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
            
            # Obtener todos los registros asociados antes de eliminarlos
            registros_asociados = list(self.equipo_vagon.all())
            
            # Actualizar estado de equipos y eliminar registros asociados
            for registro in registros_asociados:
                try:
                    with transaction.atomic():
                        # Actualizar estado del equipo
                        equipo =registro.equipo_ferroviario
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                        
                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.id}: {str(e)}")
                    continue
            
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.equipo_vagon.clear()
        
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
    
    def __str__(self):
        return f"{self.tipo_origen} - {self.origen} - {self.tipo_equipo}"







    
#**********************************************************************************************************************
class arrastres(models.Model):

    TIPO_ORIGEN_DESTINO_CHOICES = [
        ("puerto", "Puerto"),
        ("ac_ccd", " comercial/AccesoCCD"),
    ]

    tipo_origen = models.CharField(
        default="",
        choices=TIPO_ORIGEN_DESTINO_CHOICES,
        max_length=50,
        verbose_name="Tipo de origen",
    )

    origen = models.CharField(default="", max_length=40, verbose_name="Origen")

    TIPO_EQUIPO_CHOICES = (
        ("casilla", "Casilla"),
        ("caj_gon", "Cajones o Góndola"),
        ("planc_plat", "Plancha o Plataforma"),
        ("Plan_porta_cont", "Plancha porta contenedores"),
        ("cist_liquidos", "Cisterna para líquidos"),
        ("cist_solidos", "Cisterna para sólidos"),
        ("tolva_g_mineral", "Tolva granelera(mineral)"),
        ("tolva_g_agric", "Tolva granelera(agrícola)"),
        ("tolva_g_cemento", "Tolva para cemento"),
        ("volqueta", "Volqueta"),
        ("Vagon_ref", "Vagón refrigerado"),
        ("jaula", "Jaula"),
        ("locomotora", "Locomotora"),
        ("tren", "Tren"),
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
    OPERACION_CHOICES=[('carga', 'Carga'),
        ('descarga', 'Descarga')
    ]
    estado = models.CharField(
        max_length=200,
        choices=ESTADO_CHOICES,
        verbose_name="Estado",
        blank=True,
        null=True,
    )
    operacion=models.CharField(
        max_length=200,
        choices=OPERACION_CHOICES,
        verbose_name="Operacion",
        blank=True,
        null=True,
    )

    producto = models.ForeignKey(
        producto_UFC, blank=True, related_name="arrastres", verbose_name="Productos Arrastres", on_delete=models.SET_NULL,null=True
    )
    cantidad_vagones = models.CharField(
        max_length=10,
        verbose_name="Cantidad de vagones",
    )

    tipo_destino = models.CharField(
        default="",
        choices=TIPO_ORIGEN_DESTINO_CHOICES,
        max_length=50,
        verbose_name="Tipo de destino",
    )
    
    destino = models.CharField(
        default='',
        max_length=40,
        verbose_name="Destino"
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro", editable=False)

    observaciones = models.TextField(
        verbose_name="Observaciones",
        help_text="Ingrese observaciones adicionales. Admite letras, números y caracteres especiales.",
        blank=True,
        null=True,
    )
    
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
            
            # Obtener todos los registros asociados antes de eliminarlos
            registros_asociados = list(self.equipo_vagon.all())
            
            # Actualizar estado de equipos y eliminar registros asociados
            for registro in registros_asociados:
                try:
                    with transaction.atomic():
                        # Actualizar estado del equipo
                        equipo =registro.equipo_ferroviario
                        
                        if equipo:
                            equipo.estado_actual = 'Disponible'
                            equipo.save()
                        
                        # Eliminar el registro asociado
                        registro.delete()
                except Exception as e:
                    print(f"Error al procesar registro {registro.id}: {str(e)}")
                    continue
            
            # Limpiar relaciones ManyToMany (aunque ya deberían estar vacías)
            self.equipo_vagon.clear()
        
            
            # Finalmente eliminar el registro principal
            super().delete(*args, **kwargs)
            
        except Exception as e:
            print(f"Error crítico al eliminar vagon_cargado_descargado {self.id}: {str(e)}")
    
    def __str__(self):
        return f"{self.tipo_origen} - {self.origen} - {self.tipo_equipo}"




#************************************************************************************************************************
    
    
class rotacion_vagones(models.Model):
    tipo_equipo_ferroviario = models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.CASCADE,
        related_name="tipo_equipo_rotacion",
        verbose_name="Equipo ferroviario",
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

        constraints = [models.UniqueConstraint(
            fields = [
                "tipo_equipo_ferroviario",
                "informe_operativo",
            ],
            name="unique_train_rotation"
        )]

    def __str__(self):
        return (
            f"{self.tipo_equipo_ferroviario.tipo_equipo} - Servicio: {self.en_servicio}"
        )





#************************************************************************************************************************
#/**********************Aqui empieza CCDxPRODUCTO****************************

TIPO_ORIGEN_DESTINO_CHOICES = [
        ('ac', 'Acceso comercial'),
        ('ccd', 'Centro de carga/descarga'),
    ]

ESTADOS = [
        ('vacio', 'Vacío'),
        ('cargado', 'Cargado'),
    ]

OPERACIONES = [('carga', 'Carga'), ('descarga', 'Descarga')]


class ufc_informe_ccd(models.Model):    
    """Modelo para registrar informes CCD por producto"""
    ESTADOS_PARTE=[('creado', 'Creado'), ('aprobado', 'Aprobado'), ('listo', 'Listo'), ('rechazado', 'Rechazado')]
    fecha_operacion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de operación", unique=True
    )
    fecha_actual = models.DateTimeField(
        auto_now=True, verbose_name="Fecha actual", unique=True
    )
    fecha_creacion = models.DateField(
        auto_now=True, verbose_name="Fecha actual", editable=False
    )
    estado_parte = models.CharField(default="creado",max_length=14, choices=ESTADOS_PARTE, verbose_name="Estado del parte")
    comentarios= models.TextField(
        null=True,
        blank=True,
        verbose_name="Comentarios",
        help_text="Admite letras, números y caracteres especiales",
    )
    provincia=models.ForeignKey(nom_provincia,on_delete=models.CASCADE,blank=True, null=True, verbose_name="Provincia")
    creado_por=models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True, null=True, verbose_name="Creado por: ", related_name="informe_ccd_creador" )
    aprobado_por=models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True,null=True, verbose_name="Aprobado por: ", related_name="informe_ccd_aprobador")
    entidad = models.ForeignKey(
        nom_entidades,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Entidad de donde proviene el parte"
    )
    class Meta:
        verbose_name = "Parte CCD por Producto"
        verbose_name_plural = "Partes CCD por Producto"
        ordering = ["-fecha_operacion"]
        permissions = [
            ("puede_rechazar_informe", "Puede rechazar informes CCD"),
            ("puede_aprobar_informe", "Puede aprobar informes CCD"),
            ("puede_cambiar_a_listo", "Puede cambiar el estado del informe CCD a listo"),
        ]
        constraints=[models.UniqueConstraint(
            fields = [
                "creado_por",
                "fecha_creacion",
            ],
            name="unique_ccd_creado_por__fecha_creacion",
        )]
    def save(self, *args, **kwargs):
        # Asignar entidad del creador si no está establecida
        if not self.entidad and self.creado_por:
            self.entidad = self.creado_por.entidad
            self.provincia=self.creado_por.entidad.provincia
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"ID:informe {self.pk} - Fecha de operación {self.fecha_operacion} - Entidad: {self.entidad}"




class ccd_producto(models.Model):
    """Modelo de Producto CCD"""

    ESTADO_CHOICES = [
        ("vacio", "Vacío"),
        ("lleno", "Lleno"),
    ]
    CONTIENE_CHOICES = [
        ("alimentos", "Alimentos"),
        ("prod_varios", "Productos Varios"),
    ]

    producto = models.ForeignKey(nom_producto, on_delete=models.CASCADE,null=True)
    tipo_embalaje = models.ForeignKey(nom_tipo_embalaje, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(nom_unidad_medida, on_delete=models.CASCADE)
    tipo_equipo=models.ForeignKey(nom_tipo_equipo_ferroviario,on_delete=models.CASCADE,null=True,blank=True)
    
    cantidad = models.IntegerField()
    estado = models.CharField(
        choices=ESTADO_CHOICES, null=True, blank=True, max_length=20
    )
    contiene = models.CharField(
        choices=CONTIENE_CHOICES, null=True, blank=True, max_length=20
    )

    class Meta:
        verbose_name = "Producto CCD"
        verbose_name_plural = "Productos en CCD"

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


class ccd_casillas_productos(models.Model):
    informe_ccd= models.ForeignKey(
        ufc_informe_ccd,
        on_delete=models.CASCADE,
        related_name="casillas_ccd",
        null=False, blank=False,
        verbose_name="Informe CCD asociado"
    ) 
    acceso= models.ForeignKey(
        nom_entidades,
        on_delete=models.CASCADE,
        related_name="casillas_ccd",
        null=True, blank=True,
        verbose_name="Acceso o Centro Carga/Descarga"
    )
    total_ayer=models.IntegerField(default=0,verbose_name="Casillas Ayer")
    entro_hoy=models.IntegerField(default=0,verbose_name="Casillas entraron Hoy")
    total_general=models.IntegerField(default=0,verbose_name="Total General de Casillas") 
    plan_carga=models.IntegerField(default=0,verbose_name="Plan de Carga") 
    plan_descarga=models.IntegerField(default=0,verbose_name="Plan de Descarga") 
    recepcion=models.IntegerField(default=0,verbose_name="Recepciones") 
    reexpedciones=models.IntegerField(default=0,verbose_name="Reexpediciones") 
    
    class Meta:
        verbose_name="CCD Casillas por Centro Carga/Descarga"

    def save(self, *args, **kwargs):
        # Asignar entidad del creador si no está establecida

        self.total_general= self.entro_hoy + self.total_ayer
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"CCD Casillas:{self.pk} -> Informe {self.informe_ccd}"
    
class ccd_situados(models.Model):
    informe_ccd= models.ForeignKey(
        ufc_informe_ccd,
        on_delete=models.CASCADE,
        related_name="situados_ccd",
        null=False, blank=False,
        verbose_name="Informe CCD asociado"
    )
    acceso= models.ForeignKey(
        nom_entidades,
        on_delete=models.CASCADE,
        related_name="situados_ccd",
        null=True, blank=True,
        verbose_name="Acceso o Centro Carga/Descarga"
    )
    tipo_equipo= models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.CASCADE,
        related_name="situados_ccd",
        null=False, blank=False,
        verbose_name="Tipo de equipo ferroviario",
        help_text="Seleccione el tipo de equipo ferroviario asociado a la carga o descarga",
    
    )
    estado= models.CharField(
        max_length=10,
        choices=ESTADOS,
        verbose_name="Estado del equipo",
        default="vacio",
        blank=True
    )
    operacion= models.CharField(
        max_length=10,
        choices=OPERACIONES,
        verbose_name="Tipo de operación",
        default="carga"
    )
    real_carga_descarga=models.FloatField(
        default=0,
        verbose_name="Real carga/descarga",
        null=True, blank=True,
        help_text="Cantidad real de carga o descarga realizada",
    )
    causas_incumplimiento=models.TextField(
        blank=True,null=True,
        verbose_name="Causas del incumplimiento"
    )
    producto = models.ForeignKey(
        ccd_producto, blank=True, related_name="situados_ccd", verbose_name="Productos Situados CCD", on_delete=models.SET_NULL,null=True
    )
    equipo_vagon=models.ManyToManyField(
        vagones_dias,
        blank=True,
        related_name="situados_ccd",
        verbose_name="Equipos en Situados CCD"
    )
    fecha_registro=models.DateField(auto_created=True)
       
    class Meta:
        verbose_name="CCD Equipos Situados"
        #Validacion #14 del RF_CCD
        constraints=[models.UniqueConstraint(
            fields = [
                "producto",
                "tipo_equipo",
                "acceso",
                "informe_ccd",
            ],
            name="unique_ccd_situados_register",
        )]
    
    def __str__(self):
        return f"CCD Situado ID:{self.id} -> Informe {self.informe_ccd}"
    #### esta partiendo la entrada de los datos
    #### SEGUN GPT ESTAS VALIDACIONES DEBERIAN SER EN EL SERIALIZER, VAMOS A VER QUE TAL PORQUE AL SERIALIZAR NO ME DEJA HACER VALIDACIONES
    # def clean(self):
    #     super().clean()
    #     if self.tipo_equipo and getattr(self.tipo_equipo, "tipo_equipo", "").lower() == "locomotora":
    #         raise ValidationError("No se permite seleccionar 'locomotora' como tipo de equipo ferroviario.")
    
    
    
    

class ccd_por_situar(models.Model):
    informe_ccd= models.ForeignKey(
        ufc_informe_ccd,
        on_delete=models.CASCADE,
        related_name="por_situar_ccd",
        null=False, blank=False,
        verbose_name="Informe CCD asociado"
    )
    acceso= models.ForeignKey(
        nom_entidades,
        on_delete=models.CASCADE,
        related_name="por_situar_ccd",
        null=True, blank=True,
        verbose_name="Acceso o Centro Carga/Descarga"
    )
    tipo_equipo= models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.CASCADE,
        related_name="por_situar_ccd",
        null=False, blank=False,
        verbose_name="Tipo de equipo ferroviario",
        help_text="Seleccione el tipo de equipo ferroviario asociado a la carga o descarga",
    
    )
    estado= models.CharField(
        max_length=10,
        choices=ESTADOS,
        verbose_name="Estado del equipo",
        default="vacio"
    )
    operacion= models.CharField(
        max_length=10,
        choices=OPERACIONES,
        verbose_name="Tipo de operación",
        default="carga"
    )
    cantidad_vagones=models.IntegerField(
        default=0,
        verbose_name="Cantidad de Vagones",
        null=True, blank=True,
        help_text="Cantidad de Vagones",
    )
    causas_incumplimiento=models.TextField(
        blank=True,null=True,
        verbose_name="Causas del incumplimiento"
    )
    producto = models.ForeignKey(
        ccd_producto, blank=True, related_name="por_situar_ccd", verbose_name="Productos Por Situar CCD", on_delete=models.SET_NULL,null=True
    )
    equipo_vagon=models.ManyToManyField(
        vagones_dias,
        blank=True,
        related_name="por_situar_ccd",
        verbose_name="Equipos Por Situar CCD"
    )
    fecha_registro=models.DateField(auto_created=True)
       
    class Meta:
        verbose_name="CCD Equipos Por Situar"
        verbose_name_plural="CCD Equipos Por Situar"
    
    def __str__(self):
        return f"CCD Por Situar ID:{self.pk} -> Informe {self.informe_ccd}"
       
    # def clean(self):
    #     super().clean()
    #     if self.cantidad_vagones and self.cantidad_vagones!=self.equipo_vagon.count():
    #         raise ValidationError("El campo cantidad de vagones tiene que ser igual a la cantidad de vagones pasados como listas")
    #     if self.tipo_equipo and getattr(self.tipo_equipo, "tipo_equipo", "").lower() == "locomotora":
    #         raise ValidationError("No se permite seleccionar 'locomotora' como tipo de equipo ferroviario.")
    
    
    
class ccd_arrastres(models.Model):
   
    informe_ccd= models.ForeignKey(
        ufc_informe_ccd,
        on_delete=models.CASCADE,
        related_name="arrastres_ccd",
        null=False, blank=False,
        verbose_name="Informe CCD asociado"
    )
    acceso= models.ForeignKey(
        nom_entidades,
        on_delete=models.CASCADE,
        related_name="arrastres_ccd",
        null=True, blank=True,
        verbose_name="Acceso o Centro Carga/Descarga",
        help_text="Seleccione el acceso o centro de carga/descarga asociado al arrastre",
    )
    tipo_equipo= models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.CASCADE,
        related_name="arrastres_ccd",
        null=False, blank=False,
        verbose_name="Tipo de equipo ferroviario",
        help_text="Seleccione el tipo de equipo ferroviario asociado a la carga o descarga",
    
    )
    estado= models.CharField(
        max_length=10,
        choices=ESTADOS,
        verbose_name="Estado del equipo",
        default="vacio"
    )
    cantidad_vagones=models.IntegerField(
        default=0,
        verbose_name="Cantidad de Vagones",
        null=True, blank=True,
        help_text="Cantidad de Vagones",
    )
    observaciones=models.TextField(
        blank=True,null=True,
        verbose_name="Observaciones"
    )
    producto = models.ForeignKey(
        ccd_producto, blank=True, related_name="arrastres_ccd", verbose_name="Productos Arrastre CCD", on_delete=models.SET_NULL,null=True
    )
 
    equipo_vagon=models.ManyToManyField(
        vagones_dias,
        blank=True,
        related_name="arrastres_ccd",
        verbose_name="Equipos en Arrastre CCD"
    )
    fecha_registro=models.DateField(auto_created=True)
       
    class Meta:
        verbose_name="CCD Equipos Pendientes al Arrastre"
        #Validacion #14 del RF_CCD
        constraints=[models.UniqueConstraint(
            fields = [
                "producto",
                "tipo_equipo",
                "acceso",
                "informe_ccd",
            ],
            name="unique_ccd_arrastres_register",
        )]

    def __str__(self):
        return f"CCD Pendiente Arrastre ID:{self.producto} -> Informe {self.informe_ccd.pk}"
       
    # def clean_fields(self):
    #     super().clean_fields()
    #     if self.cantidad_vagones and self.cantidad_vagones!=self.equipo_vagon.count():
    #         raise ValidationError("El campo cantidad de vagones tiene que ser igual a la cantidad de vagones pasados como listas")
    #     if self.tipo_equipo and getattr(self.tipo_equipo, "tipo_equipo", "").lower() == "locomotora":
    #         raise ValidationError("No se permite seleccionar 'locomotora' como tipo de equipo ferroviario.")


class ccd_en_trenes(models.Model):
    informe_ccd= models.ForeignKey(
        ufc_informe_ccd,
        on_delete=models.CASCADE,
        related_name="en_trenes_ccd",
        null=False, blank=False,
        verbose_name="Informe CCD asociado"
    )
    acceso= models.ForeignKey(
        nom_entidades,
        on_delete=models.CASCADE,
        related_name="en_trenes_ccd",
        null=True, blank=True,
        verbose_name="Acceso o Centro Carga/Descarga"
    )
    tipo_equipo= models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.CASCADE,
        related_name="en_trenes_ccd",
        null=False, blank=False,
        verbose_name="Tipo de equipo ferroviario",
        help_text="Seleccione el tipo de equipo ferroviario asociado a Trenes",
    
    )
    estado= models.CharField(
        max_length=10,
        choices=ESTADOS,
        verbose_name="Estado del equipo",
        default="vacio"
    )
    cantidad_vagones=models.IntegerField(
        default=0,
        verbose_name="Cantidad de Vagones",
        null=True, blank=True,
        help_text="Cantidad de Vagones",
    )
    observaciones=models.TextField(
        blank=True,null=True,
        verbose_name="Obsevaciones"
    )
    producto = models.ForeignKey(
        ccd_producto, blank=True, related_name="en_trenes_ccd", verbose_name="Productos En Trenes CCD", on_delete=models.SET_NULL,null=True
    )
    equipo_vagon=models.ManyToManyField(
        nom_equipo_ferroviario,
        blank=True,
        related_name="en_trenes_ccd",
        verbose_name="Equipos en Trenes CCD"
    )
    fecha_registro=models.DateField(auto_created=True)
       
    class Meta:
        verbose_name="CCD Equipos En Trenes"
        #Validacion #14 del RF_CCD
        constraints=[models.UniqueConstraint(
            fields = [
                "producto",
                "tipo_equipo",
                "acceso",
                "informe_ccd",
            ],
            name="unique_ccd_en_trenes_register",
        )]

    def __str__(self):
        return f"CCD En Trenes ID:{self.pk} -> Informe {self.informe_ccd}"
       
    # def clean(self):
    #     super().clean()
    #     if self.cantidad_vagones and self.cantidad_vagones!=self.equipo_vagon.count():
    #         raise ValidationError("El campo cantidad de vagones tiene que ser igual a la cantidad de vagones pasados como listas")
    #     if self.tipo_equipo and getattr(self.tipo_equipo, "tipo_equipo", "").lower() == "locomotora":
    #         raise ValidationError("No se permite seleccionar 'locomotora' como tipo de equipo ferroviario.")




class ccd_registro_vagones_cd(models.Model):
    # Opciones para el campo tipo_origen
    TIPO_ORIGEN_CHOICES = [
        ("ac_cd", "Acceso Comercial"),
        ("puerto", "Puerto"),
    ]

    equipo_ferroviario=models.ForeignKey(nom_equipo_ferroviario, on_delete=models.CASCADE,null=False,blank=False,verbose_name="Campo de equipo Ferroviario", related_name="registro_equipo_ccd")
    
    no_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        
        verbose_name="Número de identificación",
        help_text="Valores definidos en el nomenclador de equipos ferroviarios (excepto 'Locomotora')",
    )

    fecha_despacho = models.DateField(
        null=True, blank=True, verbose_name="Fecha de despacho"
    )

    tipo_origen = models.CharField(
        choices=TIPO_ORIGEN_CHOICES, max_length=50, null=True, blank=True
    )

    origen = models.CharField(max_length=40, null=True, blank=True, verbose_name="Campo Origen")

    fecha_llegada = models.DateField(
        null=True, blank=True, verbose_name="Fecha de llegada"
    )

    incidencias=models.BooleanField(verbose_name="Campo asociado si tiene alguna incidencia")

    observaciones=models.JSONField(verbose_name="Este campo guardaria una lista de [Faltante,Sobrante, Averias, Peso Origen, Peso Destino]", blank=True,null=True, default=None)
    
    class Meta:
        verbose_name = "Registro de vagón cargado"
        verbose_name_plural = "Registros de vagones cargados"

    def __str__(self):
        return f"Vagón {self.no_id}" if self.no_id else "Registro sin ID"

    # def clean(self):
    #     super().clean()
    #     self.no_id= self.equipo_ferrvoviario.numero_identificacion
    #     if self.incidencias and not self.observaciones:
    #         raise ValidationError("Si el registro tiene incidencias los campos de incidencia no puede ser Null")
        
    


class ccd_vagones_cd(models.Model):
    informe_ccd= models.ForeignKey(
        ufc_informe_ccd,
        on_delete=models.CASCADE,
        related_name="vagones_cd_ccd",
        null=True, blank=True,
        verbose_name="Informe CCD asociado"
    )
    acceso= models.ForeignKey(
        nom_entidades,
        on_delete=models.CASCADE,
        related_name="vagones_cd_ccd",
        null=True, blank=True,
        verbose_name="Acceso o Centro Carga/Descarga"
    )
    tipo_equipo= models.ForeignKey(
        nom_tipo_equipo_ferroviario,
        on_delete=models.CASCADE,
        related_name="vagones_cd_ccd",
        null=True, blank=True,
        verbose_name="Tipo de equipo ferroviario",
        help_text="Seleccione el tipo de equipo ferroviario asociado a Trenes",
    
    )
    estado= models.CharField(
        max_length=10,
        choices=ESTADOS,
        verbose_name="Estado del equipo",
        default="vacio"
    )
    operacion=models.CharField(
        max_length=15,
        choices=OPERACIONES,
        verbose_name="Operacion realizada",
        default=""
    )
    real_carga_descarga=models.FloatField(
        default=0,
        verbose_name="Real carga/descarga",
        null=True, blank=True,
        help_text="Cantidad real de carga o descarga realizada",
    )
    causa_incumplimiento=models.TextField(
        blank=True,null=True,
        verbose_name="Causas del incumplimiento de la carga/descarga"
    )
    producto = models.ForeignKey(
        ccd_producto, blank=True, related_name="vagones_cd_ccd", verbose_name="Productos En Trenes CCD", on_delete=models.SET_NULL,null=True
    )
    equipo_vagon=models.ManyToManyField(
        ccd_registro_vagones_cd,
        blank=True,
        related_name="vagones_cd_ccd",
        verbose_name="Equipos Vagones Cargados/Descargados"
    )
    fecha_registro=models.DateField(auto_created=True,blank=True,null=True)
    
    class Meta:
        verbose_name="CCD Vagones Cargados/Descargados"
        #Validacion #14 del RF_CCD
        constraints=[models.UniqueConstraint(
            fields = [
                "producto",
                "tipo_equipo",
                "acceso",
                "informe_ccd",
            ],
            name="unique_ccd_vagones_cd_register",
        )]

    def __str__(self):
        return f"CCD Vagones C/D ID:{self.pk} -> Informe {self.informe_ccd}"
from django.db import models
from Administracion.models import CustomUser
from nomencladores.models import( nom_atraque, nom_estado_tecnico, nom_pais, nom_producto,nom_tipo_embalaje,nom_unidad_medida,
                                 nom_entidades,nom_incidencia,nom_provincia,nom_terminal,nom_puerto,nom_osde_oace_organismo,
                                 nom_embarcacion,nom_tipo_maniobra_portuaria
                                 )


from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from nomencladores.models import (
    nom_embarcacion as Buque
)
from django.utils import timezone
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
#***************************************************************************************************************************
"""GEMAR PARTE DIARIO CARGA-DESCARGA"""
class gemar_parte_carga_descarga(models.Model):
    tipo_parte = models.CharField(
        default="Parte de carga-descarga", 
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
    creado_por = models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True, null=True, 
                                   verbose_name="Creado por: ", related_name="gemar_informe_carga_descarga_creador" )
    
    aprobado_por = models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True, null=True, 
                                     verbose_name="Aprobado por: ", related_name="gemar_informe_carga_descarga_aprobador" )
    
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
            ("gemar_carga_descarga_puede_rechazar_informe", "Puede rechazar partes de carga-descarga"),
            ("gemar_carga_descarga_puede_aprobar_informe", "Puede aprobar partes de carga-descarga"),
            ("gemar_carga_descarga_puede_cambiar_informe_a_listo", "Puede cambiar el estado del parte de carga-descarga a listo"),
        ]
               
        verbose_name = "Parte de carga-descarga"
        verbose_name_plural = "Partes de carga-descarga"
        ordering = ["-fecha_operacion"]
    
    def __str__(self):
        return f"Fecha actual: {self.fecha_actual} - fecha de operación {self.fecha_operacion}"
    
# ************************************************************************************************************************** 
class gemar_carga_descarga(models.Model):
    OPERACION_CHOICES = [
        ("descarga", 'Descarga'),
        ("carga", 'Carga'),
    ]

    CATEGORIA_CHOICES = [
        ("I", 'Importación'),
        ("E", 'Exportación'),
        ("CR", 'Cabotaje recibido'),
        ("CE", 'Cabotaje expedido'),
        ("T", 'Trasbordo'),
        ("A", 'Alijo'),
    ]

    operacion = models.CharField(max_length=10,
        choices=OPERACION_CHOICES,
        verbose_name='Operación'
    )

    puerto = models.ForeignKey(
        nom_puerto, 
        on_delete=models.CASCADE,
        verbose_name="Puerto"
    )

    terminal = models.ForeignKey(
        nom_terminal, 
        on_delete=models.CASCADE,
        verbose_name="Terminal"
    )

    atraque = models.ForeignKey(
        nom_atraque, 
        on_delete=models.CASCADE,
        verbose_name="Atraque"
    )

    buque = models.ForeignKey(
        nom_embarcacion, 
        on_delete=models.CASCADE,
        verbose_name="Buque"
    )  

    categoria = models.CharField(max_length=10,
        choices=CATEGORIA_CHOICES,
        verbose_name='Categoría'
    ) 

    manifiesto = models.CharField(max_length=100, verbose_name="Manifiesto") 

    segundo_puerto = models.ForeignKey(
        nom_puerto, 
        on_delete=models.CASCADE,
        related_name="segundo_puerto",
        verbose_name="Segundo puerto"
    )

    toneladas_manifestadas = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Toneladas manifestadas")

    fecha_arribo = models.DateTimeField(verbose_name="Fecha actual" )
    fecha_comienzo = models.DateTimeField(verbose_name="Fecha de comienzo" )
    fecha_terminacion = models.DateTimeField(verbose_name="Fecha de terminación")
    etf = models.DateTimeField(verbose_name="ETF")
    tiempo_vencimiento = models.DateTimeField(verbose_name="Tiempo de vencimiento")

    rate = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Rate")
    plan = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Plan")
    acumulado_ayer = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Acumulado de ayer")
    real_toneladas = models.DecimalField(max_digits=10,decimal_places=2, editable=False,default=0, verbose_name="Real toneladas")
    observaciones = models.TextField(
        verbose_name='Observaciones',
        blank=True,
        null=True
    )

    parte_carga_descarga = models.ForeignKey(
        gemar_parte_carga_descarga,
        on_delete=models.CASCADE,
        related_name='carga_descarga',
        null=True, blank=True
    )

# **************************************************************************************************************************
class gemar_producto_carga_descarga(models.Model):

    TIPO_PRODUCTO_CHOICES = [
        ("producto", "Producto"),
        ("contenedor", "Contenedor"),
    ]

    ESTADO_CHOICES = [
        ("vacio", "Vacío"),
        ("cargado", "Cargado"),
    ]

    tipo_producto = models.CharField(
        choices=TIPO_PRODUCTO_CHOICES, max_length=20)    

    producto = models.ForeignKey(nom_producto, on_delete=models.CASCADE)
    tipo_embalaje = models.ForeignKey(nom_tipo_embalaje, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(nom_unidad_medida, on_delete=models.CASCADE)

    estado = models.CharField(
        choices=ESTADO_CHOICES, max_length=20,blank=True,null=True) 
    
    cantidad = models.IntegerField(blank=True,null=True)

    parte_carga_descarga = models.ForeignKey(
        gemar_parte_carga_descarga,
        on_delete=models.CASCADE,
        related_name='producto_carga_descarga')

    
    

    class Meta:
        verbose_name = "Producto de carga-descarga"
        verbose_name_plural = "Productos de carga-descarga"

    def __str__(self):
        return f"producto {self.get_tipo_producto_display()} - {self.producto.nombre_producto}"

    @property
    def embalaje_display(self):
        return self.tipo_embalaje if self.tipo_embalaje else "Sin especificar"

    @property
    def unidad_medida_display(self):
        return self.unidad_medida if self.unidad_medida else "Sin especificar"

    @property
    def producto_display(self):
        return f"{self.producto.nombre_producto} - {self.embalaje_display}"
# **************************************************************************************************************************   
class gemar_turno_carga_descarga(models.Model):   
    TURNO_CHOICES = [
        ("turno_madrugada", "Turno madrugada"),
        ("turno_manana", "Turno mañana"),
        ("turno_tarde", "Turno tarde"),  ]        
        

    turno = models.CharField(
        choices=TURNO_CHOICES, max_length = 40) 
    
    cantidad_toneladas = models.DecimalField(unique=True,max_digits=10,decimal_places=2)
    cantidad_brigadas = models.IntegerField()

    parte_carga_descarga = models.ForeignKey(
        gemar_parte_carga_descarga,
        on_delete=models.CASCADE,
        related_name='turno_carga_descarga')   
    

    class Meta:
        verbose_name = "Turno de la carga-descarga"
        verbose_name_plural = "Turnos de la carga-descarga"

    def __str__(self):
        return f"turno {self.get_turno_display()} - cantidad {self.cantidad_toneladas}"   
# **************************************************************************************************************************  
class gemar_incidencia_por_turno_carga_descarga(models.Model):   
    TURNO_CHOICES = [
        ("turno_uno", "Turno 1"),
        ("turno_dos", "Turno 2"),
        ("turno_tres", "Turno 3"),  ]        
        

    turno = models.CharField(
        choices=TURNO_CHOICES, max_length = 40)
     
    incidencia = models.ForeignKey(
        nom_incidencia,
        on_delete=models.CASCADE)
    
    tiempo_ocurrencia = models.TimeField()

    parte_carga_descarga = models.ForeignKey(
        gemar_parte_carga_descarga,
        on_delete=models.CASCADE,
        related_name='incidencia_por_turno_carga_descarga')   
    

    class Meta:
        verbose_name = "Incidencia por turno de la carga-descarga"
        verbose_name_plural = "Incidencias por turno de la carga-descarga"

    def __str__(self):
        return f"turno {self.get_turno_display()} - tiempo ocurrencia {self.tiempo_ocurrencia}"   
# **************************************************************************************************************************  

"""GEMAR INFORME DIARIO ENC"""
class gemar_informe_diario_enc(models.Model):
    tipo_parte = models.CharField(
        default="Informe diario ENC", 
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
    creado_por = models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True, null=True, 
                                   verbose_name="Creado por: ", related_name="gemar_informe_diario_enc_creador" )
    
    aprobado_por = models.ForeignKey(CustomUser,on_delete=models.CASCADE, blank=True, null=True, 
                                     verbose_name="Aprobado por: ", related_name="gemar_informe_diario_enc_aprobador" )
    
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
    total_remolcadores_maniobras = models.IntegerField(default=0,editable=False)
    total_embarcaciones_carga_seca = models.IntegerField(default=0,editable=False)
    total_embarcaciones_suministro_agua = models.IntegerField(default=0,editable=False)
    total_remolcadores_suministro_combustible = models.IntegerField(default=0,editable=False)
    total_remolcadores_cabotaje = models.IntegerField(default=0,editable=False)
    total_remolcadores_flota_auxiliar = models.IntegerField(default=0,editable=False)

    remolcadores_maniobra_operando = models.IntegerField(default=0,editable=False)
    remolcadores_maniobra_sin_operar = models.IntegerField(default=0,editable=False)
    remolcadores_maniobra_reparando = models.IntegerField(default=0,editable=False)
    remolcadores_maniobra_fuera_servicio = models.IntegerField(default=0,editable=False)
    remolcadores_maniobra_pendiente_reparacion = models.IntegerField(default=0,editable=False)
    cdt_remolcadores_maniobra = models.IntegerField(default=0,editable=False)

    remolcadores_carga_seca_operando = models.IntegerField(default=0,editable=False)
    remolcadores_carga_seca_sin_operar = models.IntegerField(default=0,editable=False)
    remolcadores_carga_seca_reparando = models.IntegerField(default=0,editable=False)
    remolcadores_carga_seca_fuera_servicio = models.IntegerField(default=0,editable=False)
    remolcadores_carga_seca_pendiente_reparacion = models.IntegerField(default=0,editable=False)
    cdt_remolcadores_carga_seca = models.IntegerField(default=0,editable=False)

    remolcadores_suministro_agua_operando = models.IntegerField(default=0,editable=False)
    remolcadores_suministro_agua_sin_operar = models.IntegerField(default=0,editable=False)
    remolcadores_suministro_agua_reparando = models.IntegerField(default=0,editable=False)
    remolcadores_suministro_agua_fuera_servicio = models.IntegerField(default=0,editable=False)
    remolcadores_suministro_agua_pendiente_reparacion = models.IntegerField(default=0,editable=False)
    cdt_remolcadores_suministro_agua = models.IntegerField(default=0,editable=False)

    remolcadores_suministro_combustible_operando = models.IntegerField(default=0,editable=False)
    remolcadores_suministro_combustible_sin_operar = models.IntegerField(default=0,editable=False)
    remolcadores_suministro_combustible_reparando = models.IntegerField(default=0,editable=False)
    remolcadores_suministro_combustible_fuera_servicio = models.IntegerField(default=0,editable=False)
    remolcadores_suministro_combustible_pendiente_reparacion = models.IntegerField(default=0,editable=False)
    cdt_remolcadores_suministro_combustible = models.IntegerField(default=0,editable=False)

    remolcadores_cabotaje_operando = models.IntegerField(default=0,editable=False)
    remolcadores_cabotaje_sin_operar = models.IntegerField(default=0,editable=False)
    remolcadores_cabotaje_reparando = models.IntegerField(default=0,editable=False)
    remolcadores_cabotaje_fuera_servicio = models.IntegerField(default=0,editable=False)
    remolcadores_cabotaje_pendiente_reparacion = models.IntegerField(default=0,editable=False)
    cdt_remolcadores_cabotaje = models.IntegerField(default=0,editable=False)

    remolcadores_flota_auxiliar_operando = models.IntegerField(default=0,editable=False)
    remolcadores_flota_auxiliar_sin_operar = models.IntegerField(default=0,editable=False)
    remolcadores_flota_auxiliar_reparando = models.IntegerField(default=0,editable=False)
    remolcadores_flota_auxiliar_fuera_servicio = models.IntegerField(default=0,editable=False)
    remolcadores_flota_auxiliar_pendiente_reparacion = models.IntegerField(default=0,editable=False)
    cdt_remolcadores_flota_auxiliar = models.IntegerField(default=0,editable=False)

    def save(self, *args, **kwargs):
        # Solo para asegurar que los campos no sean nulos si vienen de la vista
        super().save(*args, **kwargs)

    class Meta: 
        permissions = [
            ("gemar_informe_diario_enc_puede_rechazar_informe", "Puede rechazar informe diario ENC"),
            ("gemar_informe_diario_enc_puede_aprobar_informe", "Puede aprobar informe diario ENC"),
            ("gemar_informe_diario_enc_puede_cambiar_informe_a_listo", "Puede cambiar el estado del informe diario ENC a listo"),
        ]
               
        verbose_name = "Informe diario ENC"
        verbose_name_plural = "Informes diarios ENC"
        ordering = ["-fecha_operacion"]
    
    def __str__(self):
        return f"Fecha actual: {self.fecha_actual} - fecha de operación {self.fecha_operacion}"
    
# **************************************************************************************************************************
class gemar_maniobras_portuarias_enc(models.Model):
    puerto = models.ForeignKey(nom_puerto, on_delete=models.CASCADE, verbose_name="Puerto")
    buque = models.ForeignKey(nom_embarcacion, on_delete=models.CASCADE, verbose_name="Buque",
                             related_name='buque',limit_choices_to={'tipo_embarcacion': 'buque'})
    tipo_maniobra = models.ForeignKey(nom_tipo_maniobra_portuaria, on_delete=models.CASCADE, verbose_name="Tipo de maniobra portuaria")
    hora_inicio = models.TimeField(verbose_name = "Hora de inicio")
    hora_fin = models.TimeField(verbose_name = "Hora de fin")
    observaciones = models.TextField(max_length=250,blank=True,null=True)
    # Campo de selección múltiple para remolcadores
    remolcadores = models.ManyToManyField(
        nom_embarcacion,
        related_name='remolcadores',
        verbose_name="Remolcadores",
        limit_choices_to={'tipo_embarcacion': 'remolcador'},
        blank=True,  # Opcional: permite que el campo esté vacío
        help_text="Seleccione los remolcadores participantes"
    )
    parte_diario_enc = models.ForeignKey(
        gemar_informe_diario_enc,
        on_delete=models.CASCADE,
        related_name='maniobras_portuarias')
    
    class Meta:
        verbose_name = "Maniobra portuaria ENC"
        verbose_name_plural = "Maniobras portuarias ENC"

    def __str__(self):
        return f"tipo de maniobra {self.tipo_maniobra} - hora inicio {self.hora_inicio} - hora fin {self.hora_fin}" 
    
    # **************************************************************************************************************************
class gemar_afectaciones_maniobras_portuarias_enc(models.Model):
    puerto = models.ForeignKey(nom_puerto, on_delete=models.CASCADE, verbose_name="Puerto")
    buque = models.ForeignKey(nom_embarcacion, on_delete=models.CASCADE, verbose_name="Buque",
                             related_name='afectacion_buque',limit_choices_to={'tipo_embarcacion': 'buque'})
    hora_inicio_afectacion = models.TimeField(verbose_name = "Hora de inicio")
    hora_fin_afectacion = models.TimeField(verbose_name = "Hora de fin")
    observaciones = models.TextField(max_length=250,blank=True,null=True)
    # Campo de selección múltiple para remolcadores
    
    parte_diario_enc = models.ForeignKey(
        gemar_informe_diario_enc,
        on_delete=models.CASCADE,
        related_name='afectaciones_maniobras_portuarias')
    
    class Meta:
        verbose_name = "Afectación maniobra portuaria ENC"
        verbose_name = "Afectaciones maniobras portuarias ENC"
        unique_together = ('puerto', 'buque')

    def __str__(self):
        return f"puerto {self.puerto} - hora inicio {self.hora_inicio_afectacion} - hora fin {self.hora_fin_afectacion}" 
#******************************************************************************************************************************

class gemar_carga_seca_enc(models.Model):
    UBICACION_CHOICES = (
        ('-', '-'),
        ('navegando', 'Navegando'),
        ('con_ubicacion', 'Con ubicación'),
    )

    E_OPERATIVO_CHOICES = (
        ('operando', 'Operando'),
        ('fuera_servicio', 'Fuera de servicio'),
        ('reparando', 'Reparando'),
        ('pendiente_reparacion', 'Pendiente de reparación'),
    )

    C_VENCIDO_CHOICES = (
        ('si', 'Sí'),
        ('no', 'No'),
    )
    
    unidad_basica = models.ForeignKey(nom_entidades, on_delete=models.CASCADE, verbose_name="Unidad básica")
    embarcacion = models.ForeignKey(nom_embarcacion, on_delete=models.CASCADE, verbose_name="Embarcación",
                                    related_name="carga_seca")
    ubicacion = models.CharField(max_length=15, choices=UBICACION_CHOICES,verbose_name="Ubicación")
    puerto_ubicado = models.ForeignKey(nom_puerto, on_delete=models.CASCADE, verbose_name="Puerto ubicado",blank=True,null=True)
    estado_operativo = models.CharField(max_length=25, choices=E_OPERATIVO_CHOICES,verbose_name="Estado operativo")
    fecha_vencimiento_certificado = models.DateField()
    certificado_vencido = models.CharField(max_length=2, choices=C_VENCIDO_CHOICES,verbose_name="Certificado vencido",
                                           blank=True,null=True)
    eta = models.DateTimeField()
    ets = models.DateField()
    observaciones = models.TextField(max_length=250,blank=True,null=True)
    
    parte_diario_enc = models.ForeignKey(
        gemar_informe_diario_enc,
        on_delete=models.CASCADE,
        related_name='carga_seca_enc')
    
    class Meta:
        verbose_name = "Carga seca ENC"
        verbose_name = "Cargas secas ENC"

    def __str__(self):
        return f"unidad básica {self.unidad_basica} - embarcacion {self.embarcacion}" 
#******************************************************************************************************************************
class PartePBIP(models.Model):
    
    # Opciones para campos de selección
    NIVEL_CHOICES = [
        (1, 'Nivel 1'),
        (2, 'Nivel 2'),
        (3, 'Nivel 3'),
    ]
    
    ESTADO_CHOICES = [
        ('CREADO', 'Creado'),
        ('APROBADO', 'Aprobado'),
        ('CANCELADO', 'Cancelado'),
    ]

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
    
    fecha_hora = models.DateTimeField(
        verbose_name=_('Fecha y hora'),
        help_text=_('Fecha y hora específica del evento')
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
        
####Partes Carlos  de Gemar  ####
class diario_embarcacion(models.Model):
    fecha_operacion = models.DateField(_('Fecha de operación'))
    fecha_creacion = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    puerto= models.ForeignKey(nom_puerto, on_delete=models.SET_NULL, verbose_name=_('Puerto'),blank=True,null=True)
    embarcacion=models.ForeignKey(nom_embarcacion,  on_delete=models.SET_NULL, verbose_name=_('Embarcacion'),blank=True,null=True)
    fuera_servicio= models.BooleanField(verbose_name="Campo asociado a Fuera de servicio: F/S")
    estado_tec=models.ForeignKey(nom_estado_tecnico,  on_delete=models.SET_NULL, verbose_name=_('Estado Tecnico'),blank=True,null=True)
    observaciones_tec=models.CharField(verbose_name="Campo Enriquecido con las observaciones tecnicas")
    fecha_vencimiento = models.DateField(_('Fecha de Vencimiento'))
    cert_vencido= models.BooleanField(verbose_name="Certificado Vencido")
    observaciones_cert_vencido=models.CharField(verbose_name="Campo descriptivo sobre el certificado Vencido")
    t_estimado_afect= models.TimeField(verbose_name="Tiempo estimado de afectacion")
    medida_x_afect=models.CharField(verbose_name="Campo descriptivo sobre la medida por la afectacion")
    
    class Meta:
        verbose_name = _('Registro Diario de Embarcacion')
        verbose_name_plural = _('Registros Diario de Embarcacion')
        constraints=[models.UniqueConstraint(
            fields = [
                "fecha_operacion",
                "puerto",
                "embarcacion",
            ],
            name="unique_diario_embarcacion",
        )]


# class diario_practico(models.Model):
#     fecha_operacion = models.DateField(_('Fecha de operación'))
#     fecha_creacion = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
#     puerto= models.ForeignKey(nom_puerto, on_delete=models.SET_NULL, verbose_name=_('Puerto'),blank=True,null=True)
#     embarcacion=models.ForeignKey(nom_embarcacion,  on_delete=models.SET_NULL, verbose_name=_('Embarcacion'),blank=True,null=True)
#     fuera_servicio= models.BooleanField(verbose_name="Campo asociado a Fuera de servicio: F/S")
#     estado_tec=models.ForeignKey(nom_estado_tecnico,  on_delete=models.SET_NULL, verbose_name=_('Estado Tecnico'),blank=True,null=True)
#     observaciones_tec=models.CharField(verbose_name="Campo Enriquecido con las observaciones tecnicas")
#     fecha_vencimiento = models.DateField(_('Fecha de Vencimiento'))
#     cert_vencido= models.BooleanField(verbose_name="Certificado Vencido")
#     observaciones_cert_vencido=models.CharField(verbose_name="Campo descriptivo sobre el certificado Vencido")
#     t_estimado_afect= models.TimeField(verbose_name="Tiempo estimado de afectacion")
#     medida_x_afect=models.CharField(verbose_name="Campo descriptivo sobre la medida por la afectacion")
    
#     class Meta:
#         verbose_name = _('Registro Diario de Practico')
#         verbose_name_plural = _('Registros Diario de Practico')
#         constraints=[models.UniqueConstraint(
#             fields = [
#                 "fecha_operacion",
#                 "puerto",
#                 "embarcacion",
#             ],
#             name="unique_diario_embarcacion",
#         )]


class buques_puerto(models.Model):
    TIPO_BUQUES=[
        ("buque_carga","Buque de Carga"),
        ("buque_tanque","Buque Tanque"),
        ("buque_reparando","Buque Reparando"),
    
    ]
    UBICACIONES=[
        ("navegando","Navegando"),
        ("ubicado","Con Ubicacion"),
    ]
    OPERACIONES=[
        ("I","IMPORTACION"),
        ("E","EXPORTACION"),
        ("CR","CABOTAJE RECIBIDO"),
        ("CE","CABOTAJE EXPEDIDO"),
        ("T","TRASBORDO"),
        ("A","ALIJO"),
    ]
    
    fecha_operacion = models.DateField(_('Fecha de operación'))
    fecha_creacion = models.DateTimeField(_('Fecha de creación'), auto_now_add=True)
    puerto= models.ForeignKey(nom_puerto, on_delete=models.SET_NULL, verbose_name=_('Puerto'),blank=True,null=True)
    tipo_buque= models.CharField( default="N/A",verbose_name="Tipo de Buques",choices=TIPO_BUQUES,blank=True,null=True)
    registro=models.IntegerField(verbose_name="Campo Enriquecido con el registro de la embarcacion")
    buque=models.ForeignKey(nom_embarcacion,  on_delete=models.SET_NULL, verbose_name=_('Buque'),blank=True,null=True)
    puerto_procedencia= models.ForeignKey(nom_puerto, on_delete=models.SET_NULL, verbose_name=_('Puerto Procedencia'),blank=True,null=True, related_name='puerto_procedencia_buque')
    atraque=models.ForeignKey(nom_atraque, on_delete=models.SET_NULL, verbose_name=_('Atraque'),blank=True,null=True)
    nor=models.DateTimeField(verbose_name="Fecha y hora de entrada al atraque",blank=True,null=True)
    fecha_arribo = models.DateField(_('Fecha de arribo'))
    fecha_entrada = models.DateField(_('Fecha de entrafa'))
    operacion=models.CharField(verbose_name="Campo Enriquecido con las Operaciones",choices=OPERACIONES,blank=True,null=True)
    ets=models.DateTimeField(verbose_name="Fecha y hora ETS",blank=True,null=True)
    eta=models.DateTimeField(verbose_name="Fecha y hora ETA",blank=True,null=True)
    puerto_destino= models.ForeignKey(nom_puerto, on_delete=models.SET_NULL, verbose_name=_('Puerto Destino'),blank=True,null=True, related_name='puerto_destino_buque')
    nacionalidad=models.ForeignKey(nom_pais, on_delete=models.SET_NULL, verbose_name=_('Nacionalidad'),blank=True,null=True)
    observaciones=models.CharField(verbose_name="Campo Enriquecido con las observaciones",null=True,blank=True)
    
    class Meta:
        verbose_name = _('Registro Buque de Puerto')
        verbose_name_plural = _('Registros Buques de Puerto')
        
class producto_buque(models.Model):
    TIPO_PRODUCTO=[
        ("producto","Producto"),
        ("contenedor","Contenedor"),
    ]
    ESTADOS_CONTENEDOR=[
        ("vacio","Vacio"),
        ("lleno","Lleno"),
    ]
    producto=models.ForeignKey(nom_producto, on_delete=models.SET_NULL, verbose_name=_('Producto'),blank=True,null=True)
    tipo_producto=models.CharField(verbose_name="Tipo de Producto",choices=TIPO_PRODUCTO,blank=True,null=True,max_length=20)
    tipo_embalaje = models.ForeignKey(nom_tipo_embalaje, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(nom_unidad_medida, on_delete=models.CASCADE)  
    estado=models.CharField(choices=ESTADOS_CONTENEDOR,verbose_name="Estado del Producto",max_length=20,blank=True,null=True)  
    class Meta:
        verbose_name = _('Producto de Buque')
        verbose_name_plural = _('Productos de Buque')


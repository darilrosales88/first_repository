from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

#------------aqui comienza el nomenclador nom_pais--------------------------
class nom_pais(models.Model):
    """Nomenclador de país."""
    nacionalidad = models.CharField(max_length=3, unique=True,
                                    validators=[RegexValidator(r'^[A-Z]{3}$',"Este campo sólo acepta tres letras mayúsculas",)])
    nombre_pais = models.CharField(max_length=100,unique=True,validators=[RegexValidator(r'^[A-Z]{1}[a-záíóúé ]{2,99}$',"Este campo comienza con mayúscula seguido de espacio, caracteres alfabéticos y no puede exceder los 100 caracteres.",)])

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['nombre_pais']
        unique_together = ('nacionalidad', 'nombre_pais')
    

    def __str__(self):
        return '{}'.format(self.nombre_pais)
#------------aqui termina el nomenclador nom_pais---------------------------

#------------aqui comienza el nomenclador nom_provincia---------------------------   
class nom_provincia(models.Model):
    codigo= models.CharField(verbose_name="Código", max_length=2,validators=[RegexValidator(r'^[0-9]{2}$',"Este campo sólo admite dos números.",)], unique=True)
    pais = models.ForeignKey(nom_pais, verbose_name="País",null=False, blank=False, on_delete=models.CASCADE,help_text="Escoja una opción")
    nombre_provincia = models.CharField(verbose_name="Nombre de la provincia", max_length=100,unique=True,validators=[RegexValidator(r'^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑäëöüÄËÏÜ ]{2,99}$',"Este campo comienza con mayúscula seguido de espacio, caracteres alfabéticos y no puede exceder los 100 caracteres.",)])

    class Meta:
        verbose_name = 'Provincias'
        verbose_name_plural = 'Provincias'
        ordering = ['nombre_provincia']

    def __str__(self):
        return '{}'.format(self.nombre_provincia)
#------------aqui termina el nomenclador nom_provincia---------------------------

# -----aqui comienza el nomenclador Municipio-----
class nom_municipio(models.Model):   

    nombre_municipio = models.CharField(verbose_name="Nombre del municipio", max_length=100,
                                        unique=True,validators=[RegexValidator(r'^[A-Z][\w\d\W]{2,99}$',"ESte campo acepta letras comenzalndo con mayúscula. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.",)])
    provincia = models.ForeignKey(nom_provincia, verbose_name='Provincia', null=False, blank=False,
                                  on_delete=models.CASCADE) 

    codigo = models.CharField(verbose_name="Código", max_length=4, unique=True,
                                  validators=[RegexValidator(r'[0-9]{4}$',"Este campo admite hasta cuatro dígitos.",)])
    class Meta:
        verbose_name = 'Municipios'
        verbose_name_plural = 'Municipios'
        ordering = ['nombre_municipio']

    def __str__(self):
        return '{}'.format(self.nombre_municipio)
# -----aqui termina el nomenclador Municipio-----

#------------aqui comienza el nomenclador tipo de maniobra portuaria---------------------------
class nom_tipo_maniobra_portuaria(models.Model):

    nombre_maniobra= models.CharField( max_length=100,verbose_name="Nombre de la maniobra",
                                        validators=[RegexValidator(r'^[A-Z][\w\s]{1,99}$',"Este campo comienza con mayúscula seguido de espacio, caracteres alfabéticos y no puede exceder los 100 caracteres.",)])

    t_maniobra = (
        ('entrada', 'Maniobra de entrada'),
        ('salida', 'Maniobra de salida'),
    )
    tipo_maniobra = models.CharField(verbose_name="Tipo de maniobra", max_length=7, choices=t_maniobra, default="entrada")

    class Meta:
        verbose_name = 'Tipo de maniobra portuaria'
        verbose_name_plural = 'Tipos de maniobras portuarias'
        unique_together = ('nombre_maniobra', 'tipo_maniobra')

    def __str__(self):
        return self.nombre_maniobra
#------------aqui termina el nomenclador tipo de maniobra portuaria---------------------------

# -----------------------------Aqui comienza Modelo nom_contenedor-----------------------------------------
class nom_contenedor(models.Model):
    id_contenedor = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="Id del contenedor",
        primary_key=True,
        validators=[
            RegexValidator(
                r'^[A-Z]{4}[0-9]{7}$',
                "Este campo comienza con cuatro letras mayúsculas seguidas de siete dígitos.",
            )
        ],
    )

    t_contenedor = (
        ('DC', 'Dry Container'),
        ('RC', 'Reefer Container'),
        ('GP', 'GP'),
        ('HC', 'High Cube'),
        ('OT', 'Open Top'),
        ('FR', 'Flat Rack'),
        ('RH', 'RH'),
        ('OS', 'Open Side'),
        ('TC', 'Tank Container'),
    )

    tipo_contenedor = models.CharField(
        verbose_name="Tipo de contenedor",
        max_length=25,
        choices=t_contenedor,
        default="DC",
        help_text="Escoja una opción.",
    )

    longit = (
        ('1-20', '1-20'),
        ('2-40', '2-40'),
    )

    longitud = models.CharField(
        verbose_name="Longitud",
        max_length=4,
        choices=longit,
        default="1-20",
        help_text="Escoja una opción.",
    )

    codigo_iso = models.CharField(
        max_length=4,
        verbose_name="Código ISO",
        validators=[
            RegexValidator(
                r'^[0-9]{2}[A-Z]{1}[0-9]{1}$',
                "Este campo comienza con dos números, seguidos de una letra mayúscula y un número.",
            )
        ],
    )

    def __str__(self):
        return self.id_contenedor

    class Meta:
        verbose_name = "Contenedor"
        verbose_name_plural = "Contenedores"
# -----------------------------Aqui termina Modelo nom_contenedor-----------------------------------------

#------------aqui comienza el nomenclador Cargo---------------------------
class nom_cargo(models.Model):
    nombre_cargo = models.CharField(
        max_length=20,
        verbose_name="Cargo",
        unique=True,
        validators=[
            RegexValidator(
                r'^[A-Z][\w ]{2,18}$',
                "Este campo comienza con letra mayúscula seguida de hasta 19 caracteres alfabéticos y espacios.",
            )
        ]
    )

    class Meta:
        verbose_name = 'Cargos'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.nombre_cargo

#------------aqui termina el nomenclador Cargo---------------------------

#--------------------------------aqui comienza el nomenclador Territorio----------------------------------------
class nom_territorio(models.Model):
    nombre_territorio = models.CharField(
        max_length=100, 
        unique=True, 
        validators=[
            RegexValidator(
                r'^[A-Z]{1}[a-záíóúé ]{2,99}$', 
                "Este campo comienza con mayúscula seguido de espacio, caracteres alfabéticos y no puede exceder los 100 caracteres."
            )
        ]
    )
    abreviatura = models.CharField(
        max_length=3, 
        unique=True, 
        validators=[
            RegexValidator(
                r'^[A-Z]{3}$', 
                "Este campo sólo acepta tres letras mayúsculas."
            )
        ]
    )

    class Meta:
        verbose_name = "Territorio"
        verbose_name_plural = "Territorios"
        ordering = ['nombre_territorio']
        unique_together = ('nombre_territorio', 'abreviatura')

    def __str__(self):
        return self.nombre_territorio
#--------------------------------aqui termina el nomenclador Territorio----------------------------------------

# -----------------------------Aqui comienza Modelo Puerto-----------------------------------------
class nom_puerto(models.Model):
    """Nomenclador de puertos"""
    nombre_puerto = models.CharField(max_length=100,unique=True,verbose_name="Nombre del puerto",
                                     validators=[RegexValidator(r'^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑäëöüÄËÏÜ ]{2,99}$',"Este campo comienza con mayúscula Letras seguido de estacios y letras. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.",)])
    pais = models.ForeignKey(nom_pais, on_delete=models.CASCADE, help_text="Escoja una opción.",verbose_name="País")
    provincia = models.ForeignKey(nom_provincia, on_delete=models.CASCADE,blank=True, null=True, help_text="Escoja una opción.",verbose_name="Provincia")
    servicio_portuario = models.ForeignKey(nom_territorio, on_delete=models.CASCADE,blank=True, null=True, help_text="Escoja una opción.",verbose_name="Servicio portuario")
    latitud = models.CharField(verbose_name="Latitud", max_length=50)
    longitud = models.CharField(verbose_name="Longitud", max_length=50)

    def __str__(self):
        return '{}'.format(self.nombre_puerto)

    class Meta:
        verbose_name = "Puerto"
        verbose_name_plural = "Puertos"
        unique_together = ('nombre_puerto', 'pais')

# -----------------------------Aqui termina Modelo Puerto-----------------------------------------

# -----------------------------Aqui comienza Modelo nom_terminal-----------------------------------------
class nom_terminal(models.Model):
    nombre_terminal = models.CharField(verbose_name="Nombre",max_length=100,unique=True,validators=[RegexValidator(r'^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑäëöüÄËÏÜ ]{2,99}$',"Este campo comienza con mayuscula, seguido de letras y espacios. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.",)])
    puerto = models.ForeignKey(nom_puerto, on_delete=models.CASCADE, help_text="Escoja una opción.",)
    capacidad_almacen_importacion = models.DecimalField(verbose_name="Capacidad de almacén importación",max_digits=10,decimal_places=2)
    capacidad_almacen_exportacion = models.DecimalField(verbose_name="Capacidad de almacén exportación",max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre_terminal

    class Meta:
        verbose_name = "Terminal"
        verbose_name_plural = "Terminales"
        unique_together = ('nombre_terminal', 'puerto')

# -----------------------------Aqui termina Modelo nom_terminal-----------------------------------------

# -----------------------------Aqui comienza Modelo nom_atraque-----------------------------------------
class nom_atraque(models.Model):
    """Nomenclador de atraque"""
    nombre_atraque = models.CharField(max_length=100,unique=True,verbose_name="Nombre",
    validators=[RegexValidator(r'^[A-Z][A-Za-z ]{2,99}$',"Este campo comienza con mayúscula seguido de espacio, caracteres alfabéticos y no puede exceder los 100 caracteres.",)])
    puerto = models.ForeignKey(nom_puerto,on_delete=models.CASCADE, help_text="Escoja una opción.",)
    terminal = models.ForeignKey(nom_terminal,on_delete=models.CASCADE, help_text="Escoja una opción.",)
   
    def __str__(self):
        return self.nombre_atraque

    class Meta:
        verbose_name = "Atraque"
        verbose_name_plural = "Atraques"
        unique_together = ('nombre_atraque', 'puerto', 'terminal')

# -----------------------------Aqui termina Modelo nom_atraque-----------------------------------------

#------------aqui comienza el Modelo nom_unidad_medida---------------------------
class nom_unidad_medida(models.Model):
    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medida'

    magnitud= models.CharField(max_length=50, verbose_name="Magnitud física",
                               validators=[RegexValidator(r'^[A-Záíóúé\w\s]{1,49}$',"Este campo admite letras y espacios. Tamaño mínimo 3 caracteres y tamaño máximo 50 caracteres.",)])
    unidad_medida = models.CharField(max_length=50,verbose_name="Unidad de medida",
        unique=True,validators=[RegexValidator(r'^[A-Záíóúé\w\s]{1,49}$', "Este campo admite letras y espacios. Tamaño mínimo 3 caracteres y tamaño máximo 50 caracteres.", )])
    simbolo = models.CharField( max_length=3,verbose_name="Símbolo",
        unique=True,validators=[RegexValidator(r'^[\d\w]{1,3}$', "Este campo admite caracteres alfanuméricos. Tamaño mínimo 1 y máximo 3 caracteres.", )])

    def __str__(self):
        return self.unidad_medida

#------------aqui termina el Modelo nom_unidad_medida---------------------------

# -----------------------------Aqui comienza el Modelo nom_osde_oace_organismo-----------------------------------------
class nom_osde_oace_organismo(models.Model):
    """Nomenclador de OSDE/OACE u organismo."""
    nombre = models.CharField( unique=True,verbose_name="Nombre",max_length=50,
                                        validators=[RegexValidator(r'^[A-Z][\w\d\W]{2,99}$', "Este campo comienza con mayúscula, acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.", )])
    abreviatura = models.CharField(unique=True,verbose_name="Abreviatura",max_length=20,
                                         validators=[RegexValidator(r'^[A-ZÁÉÍÓÚ]{1}[A-Za-zÁÉÍÓÚáéíóú\s]{2,19}', "Este campo comienza con mayúscula seguido de espacio o caracteres alfabéticos. Tamaño mínimo 3 caracteres y tamaño máximo 20 caracteres.", )])

    codigo_reeup = models.BigIntegerField(verbose_name="Código REEUP",blank=True,null=True, 
    validators=[RegexValidator(r'^[0-9]{5,11}$', "Este campo sólo admite números. Tamaño mínimo 5 caracteres y tamaño máximo 11 caracteres.", )])

    def __str__(self):
        #return "Abreviatura OSDE/OACE u organismo: %s " % (self.abreviatura)
        return self.abreviatura

    class Meta:
        verbose_name = "Osde/OACE/Organismo"
        verbose_name_plural = "Osde/OACE/Organismos"
        unique_together = [['nombre', 'abreviatura', 'codigo_reeup']]
       
# -----------------------------Aqui termina el Modelo nom_osde_oace_organismo-----------------------------------------

# -----------------------------Aqui comienza Modelo nom_entidades-----------------------------------------
class nom_entidades(models.Model):
    """Nomenclador de entidades."""
    nombre = models.CharField(max_length=100, unique=True,
                                        verbose_name="Nombre",validators=[RegexValidator(r'^[A-Z][A-Za-zÁÉÍÓÚáéíóú ]{2,99}', "Este campo comienza con mayúscula, acepta letras y espacios. Tamaño mínimo 2 caracteres y tamaño máximo 100 caracteres.", )])
    abreviatura = models.CharField(max_length=20, unique=True,
                                        verbose_name="Abreviatura", validators=[RegexValidator(r'^[A-ZÁÉÍÓÚ]{1}[A-Za-zÁÉÍÓÚáéíóú\s]{2,19}$', "Este campo comienza con mayúscula seguido de espacio o caracteres alfabéticos. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.", )])

    codigo_reeup = models.CharField(verbose_name="Código REEUP",blank=True,null=True,max_length=15, 
    validators=[RegexValidator(r'^[0-9]{5,11}$', "Este campo sólo admite números. Tamaño mínimo 5 caracteres y tamaño máximo 11 caracteres.", )])

    osde_oace_organismo = models.ForeignKey(nom_osde_oace_organismo, on_delete=models.CASCADE, verbose_name=" OSDE/OACE u organismo ",
                                        null=True,blank=True, help_text="Escoja una opción.")
    
    provincia = models.ForeignKey(nom_provincia, on_delete=models.CASCADE,null=True,blank=True)

    t_entidad = (
        ('importador', 'Importador'),
        ('exportador', 'Exportador'),
        ('transportista', 'Transportista'),
        ('acceso_comercial', 'Acceso comercial'),
        ('compania_naviera', 'Compañía naviera'),
        ('mitrans', 'Mitrans'),
        ('ccd', 'Centro Carga/Descarga'),   
        ('otros', 'Otros')
    )
    tipo_entidad = models.CharField(choices=t_entidad, default="DC", help_text="Escoja una opción.",
                                     verbose_name="Tipo de entidad",max_length=30)

    territorio = models.ForeignKey(nom_territorio, on_delete=models.CASCADE,null=True,blank=True)   

    def __str__(self):
        return self.nombre
        #return "Nombre entidad: %s " % (self.nombre)

    class Meta:
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"
        #unique_together = [['nombre', 'abreviatura', 'provincia','tipo_entidad']]

# -----------------------------Aqui termina Modelo nom_entidades-----------------------------------------

# -----------------------------Aqui comienza Modelo nom_destino-----------------------------------------
class nom_destino(models.Model):
    """Nomenclador de destino"""
    cliente = models.ForeignKey(nom_entidades, on_delete=models.CASCADE, help_text="Escoja una opción.",)
    destino = models.CharField(max_length=100,
                              validators=[RegexValidator(r'^[A-Z]{1}[\d\w\W ]{2,99}$',"Este campo comienza con mayúscula seguido de espacio, letras, números y caracteres especiales. Tamaño mínimo 2 caracteres y tamaño máximo 100 caracteres.",)])

    def __str__(self):
        return self.destino

    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"
        unique_together = [['cliente', 'destino']]

# -----------------------------Aqui termina Modelo nom_destino-----------------------------------------

# -----------------------------Aqui comienza Modelo nom_tipo_equipo_ferroviario-----------------------------------------
class nom_tipo_equipo_ferroviario(models.Model):
    """Nomenclador de tipo de equipo ferroviario."""

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

    tipo_equipo = models.CharField(max_length=30,choices=t_equipo, default="casilla", verbose_name="Tipo de equipo",
                             help_text="Escoja una opción.",)

    t_carga = (
        ('combustible', 'Combustible'),
        ('aceite', 'Aceite'),
        ('miel', 'Miel'),
        ('alcohol', 'Alcohol'),
        ('quimicos', 'Químicos'),
        ('contenedores', 'Contenedores'),
        ('otros', 'Otros'),
    )

    tipo_carga = models.CharField(max_length=15,choices=t_carga, verbose_name="Tipo de carga",
                             default="Combustible", help_text="Escoja una opción.",)

    t_combustible = (
        ('-', '-'),
        ('combustible_blanco', 'Combustible blanco'),
        ('combustible_negro', 'Combustible negro'),
        ('combustible_turbo', 'Combustible turbo'),
    )
    tipo_combustible = models.CharField(max_length=20,choices=t_combustible, verbose_name="Tipo de combustible",
                                    default="-", null=True,blank=True, help_text="Escoja una opción.",)
    longitud = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Longitud (ft)",)
    peso_neto_sin_carga = models.DecimalField(max_digits=10,decimal_places=2, verbose_name="Peso neto sin carga (t)",)
    peso_maximo_con_carga = models.DecimalField(max_digits=10,decimal_places=2, verbose_name="Peso máximo con carga (t)",)
    capacidad_cubica_maxima = models.DecimalField(max_digits=10,decimal_places=2, verbose_name="Capacidad cúbica máxima (ft3)",)
    descripcion = models.CharField(max_length=60, verbose_name="Descripción",)

    def __str__(self):
        #return self.t_equipo
        return f"Tipo de equipo: {self.tipo_equipo} - Longitud: {self.longitud} - Peso neto sin carga: {self.peso_neto_sin_carga} - Peso máximo con carga: {self.peso_maximo_con_carga}"

    class Meta:
        verbose_name = "Tipo de equipo ferroviario"
        verbose_name_plural = "Tipos de equipos ferroviarios"
        unique_together = ('tipo_equipo', 'tipo_carga', 'longitud', 'peso_neto_sin_carga','descripcion')

# -----------------------------Aqui termina Modelo nom_tipo_equipo_ferroviario-----------------------------------------

# -----------------------------Aqui comienza Modelo nom_embarcacion-----------------------------------------
class nom_embarcacion(models.Model):
    """Nomenclador de embarcaciones."""

    nombre_embarcacion = models.CharField(max_length=100,unique=True,
                              validators=[RegexValidator(r'^[A-Z]{1}[A-Za-z ]{3,100}$',"Este campo comienza con mayúscula seguido de letras. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.",)])

    nacionalidad = models.ForeignKey(nom_pais, on_delete=models.CASCADE, help_text="Escoja una opción.",)
    eslora = models.DecimalField(verbose_name="Eslora", max_digits=10,decimal_places=2)
    manga = models.DecimalField(verbose_name="Manga", max_digits=10,decimal_places=2)
    calado_maximo = models.DecimalField(verbose_name="Calado máximo", max_digits=10,decimal_places=2)
    desplazamiento_maximo = models.DecimalField(verbose_name="Desplazamiento máximo", max_digits=10,decimal_places=2)
    t_embarcacion = (
        ('-', '-'),
        ('buque', 'Buque'),
        ('remolcador', 'Remolcador'),
        ('patana', 'Patana'),
        ('otros', 'Otros'),
    )

    tipo_embarcacion = models.CharField(max_length=20,choices=t_embarcacion, default="-", verbose_name="Tipo de embarcación",
                                help_text="Escoja una opción.",)

    t_buque = (
        ('buque_carga_gral', 'Buque de carga general'),
        ('buque_granelero', 'Buque granelero'),
        ('buque_ro_ro', 'Buque Ro Ro'),
        ('buque_frig', 'Buque frigorífico'),
        ('buque_tanque', 'Buque tanque'),
        ('buque_gases', 'Buque de gases'),
        ('-', '-'),
    )

    tipo_buque = models.CharField(blank=True,null=True,max_length=30, choices=t_buque, default="-", verbose_name="Tipo de buque",
                            help_text="Escoja una opción.",)

    t_patana = (
        ('pat_carga_seca', 'Patana de carga seca'),
        ('pat_carga_liquida', 'Patana de carga líquida'),
        ('patana_comb', 'Patana de combustible'),
        ('patana_ro_ro', 'Patana Ro Ro'),
        ('-', '-'),
    )

    tipo_patana = models.CharField(blank=True,null=True,max_length=30, choices=t_patana, default="-", verbose_name="Tipo de patana", 
                            help_text="Escoja una opción.",)

    imo = models.CharField(blank=True,null=True,max_length=10, verbose_name="IMO",
                           unique=True)
    potencia = models.DecimalField(max_digits=10,decimal_places=2, verbose_name="Potencia",
                           blank = True, null = True)

    def __str__(self):
        return self.nombre_embarcacion

    class Meta:
        verbose_name = "Embarcación"
        verbose_name_plural = "Embarcaciones"

# -----------------------------Aqui termina Modelo nom_embarcacion-----------------------------------------

# -----------------------------Aqui comienza Modelo nom_equipo_ferroviario-----------------------------------------
class nom_equipo_ferroviario(models.Model):
    """Nomenclador de equipo feroviario."""
    tipo_equipo = models.ForeignKey(nom_tipo_equipo_ferroviario, on_delete=models.CASCADE, help_text="Escoja el tipo de equipo ferroviario.")

    #cuando se escoja el TEF y se guarde en tipo_equipo, entonces tipo_equipo_especifico sera un combo que mostrará los diferentes
    # TEF cuyo valor tipo_equipo es el mismo,por ejemplo, pueden haber diferentes locomotoras, el usuario debe especificar en la descripcion
    # del nom_tipo_equipo_ferroviario de cada locomotora las diferencias
    #tipo_equipo_especifico = models.CharField(max_length=45,blank=True,null=True, verbose_name="Tipo de equipo específico",)
    
    #Hay que agregar un nuevo campo que sea en servicio para validar si esta o no en uso este equipo.
    #y aplicar la logica correspondiente.
    
    numero_identificacion = models.CharField(max_length=10, verbose_name="Número de identificación",
                            validators=[RegexValidator(r'^[\d\w\W\s]{3,10}$',"Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 10 caracteres.",)])

    territ = (
        ('-', '-'),
        ('oriente', 'Oriente'),
        ('centro', 'Centro'),
        ('occidente', 'Occidente'),
        )

    territorio = models.CharField(max_length=10,choices=territ, default="-", verbose_name="Territorio",)

    tipo_carga = models.CharField(max_length=28, verbose_name="Tipo de carga",)

    tipo_combustible = models.CharField(max_length=20,default='-',null=True,blank=True, verbose_name="Tipo de combustible",)

    peso_maximo = models.DecimalField(max_digits=10,decimal_places=2, verbose_name="Peso máximo (t)",)

    estado_actual = models.CharField(max_length=10, default="Disponible", verbose_name="Estado", editable=True)


    def __str__(self):
        return self.numero_identificacion

    class Meta:
        verbose_name = "Equipo ferroviario"
        verbose_name_plural = "Equipos ferroviarios"
        unique_together = ('tipo_equipo', 'numero_identificacion', 'territorio')
# ----------------------------------Aqui termina Modelo nom_equipo_ferroviario-----------------------------------------

# ------------------------------------Aqui comienza Modelo nom_estado_tecnico-----------------------------------------

class nom_estado_tecnico(models.Model):
    """Nomenclador de estado técnico."""
    codigo_estado_tecnico = models.CharField( unique=True,verbose_name="Código del estado técnico",
                                        validators=[RegexValidator(r'^[A-Za-zÁÉÍÓÚáéíóú\s]{2,5}$',"Este campo acepta letras. Tamaño mínimo 2 caracteres y tamaño máximo 5 caracteres. ",)],max_length=5)
    nombre_estado_tecnico = models.CharField(verbose_name="Nombre",
                                        validators=[RegexValidator(r'^[\w\d\W ]{3,100}$',"Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.",)],max_length=100)

    def __str__(self):
        return self.nombre_estado_tecnico

    class Meta:
        verbose_name = "Estado técnico"
        verbose_name_plural = "Estados técnicos"
# ------------------------------------------Aqui termina Modelo nom_estado_tecnico-----------------------------------------

# ------------------------------------------Aqui comienza Modelo nom_producto-----------------------------------------
class nom_producto(models.Model):
    """Nomenclador de producto."""
    codigo_producto = models.CharField(validators=[RegexValidator(r'^[\w\d\W ]{3,20}$',"Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 20 caracteres.",)],
                                              max_length=20,unique=True,null=True,blank=True,verbose_name="Código del producto")
    nombre_producto = models.CharField(validators=[RegexValidator(r'^[\w\d\W ]{3,100}$', "Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.", )],
        max_length=100, unique=True, verbose_name="Nombre")

    t_producto = (
        ('-', '-'),
        ('alimento', 'Alimento'),
        ('combustible', 'Combustible'),
        ('contenedor', 'Contenedor'),
        ('otros', 'Otros'),
    )
    tipo_producto = models.CharField(max_length=20, choices=t_producto, default="-",verbose_name="Tipo de producto")

    descripcion = models.TextField(validators=[RegexValidator(r"^[A-Z][\w\d\W]{2,399}$", "Este campo comienza con mayúscula, acepta letras, números y caracteres especiales. Tamaño mínimo 2 caracteres y tamaño máximo 399 caracteres.", )],
                            verbose_name="Descripción")

    def __str__(self):
        return self.nombre_producto

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        #ejemplo de como declarar permisos creados por mí mismo
        #permissions = [
        #    ("custom_permission", "Puede hacer algo especial con MiModelo"),
        #]
# ------------------------------------------Aqui termina Modelo nom_producto-----------------------------------------

#------------aqui comienza el Modelo nom_tipo_embalaje---------------------------
class nom_tipo_embalaje(models.Model):
    class Meta:
        verbose_name = 'Tipo de embalaje'
        verbose_name_plural = 'Tipos de embalaje'

    nombre_tipo_embalaje= models.CharField(max_length=100,verbose_name="Nombre del embalaje",
                                        unique=True,validators=[RegexValidator(r'^[A-Z][\w\s]{1,99}$',"Este campo comienza con mayúscula, acepta letras minúsculas y espacios. Tamaño mínimo 2 caracteres y tamaño máximo 100 caracteres.",)])

    def __str__(self):
        return self.nombre_tipo_embalaje

#------------aquí termina el Modelo nom_tipo_embalaje---------------------------

# ------------------------------------------Aqui comienza Modelo nom_incidencia-----------------------------------------
class nom_incidencia(models.Model):
    """Nomenclador de incidencias."""
    codigo_incidencia = models.CharField(validators=[RegexValidator(r'^[\w\d\W ]{2,5}$',"Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 2 caracteres y tamaño máximo 5 caracteres.",)], 
                                max_length=20,unique=True,verbose_name="Código de incidencia")
    nombre_incidencia = models.CharField(validators=[RegexValidator(r'^[\w\d\W ]{3,100}$',"Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.",)],
        max_length=100, unique=True,verbose_name="Nombre")

    t_imputable = (
            ('-', '-'),
            ('imputables_buque', 'Imputables al buque'),
            ('imputables_puerto', 'Imputables al puerto'),
            ('imputables_receptor', 'Imputables al receptor'),
            ('imputables_otras_causas', 'Imputables a otras causas'),
            ('imputables_imp_exp', 'Imputables al importador / exportador'),
            ('imputables_aut_portuarias', 'Imputables a las autoridades portuarias'),

        )

    tipo_imputable = models.CharField(max_length=40, choices=t_imputable, default='-', help_text="Escoja una opción.",verbose_name="Tipo imputable")

    def __str__(self):
        return self.codigo_incidencia

    class Meta:
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"
# -----------------------------------------------Aqui termina Modelo nom_incidencia-----------------------------------------

#----------------------------------Aqui comienza Modelo nom_tipo_estructura_ubicacion---------------------------
class nom_tipo_estructura_ubicacion(models.Model):
    class Meta:
        verbose_name = 'Tipo de estructura de ubicación'
        verbose_name_plural = 'Tipos de estructura de ubicación'

    nombre_tipo_estructura_ubicacion= models.CharField( max_length=100, verbose_name="Ubicación",
                                        unique=True,validators=[RegexValidator(r'^[A-Z][\w\s]{1,99}$',"Este campo comienza con mayúscula. admite letras minúsculas y espacio. Tamaño mínimo 5 caracteres y tamaño máximo 11 caracteres.",)])

    def __str__(self):
        return self.nombre_tipo_estructura_ubicacion
#----------------------------Aqui termina Modelo nom_tipo_estructura_ubicacion---------------------------------------

# ----------------------------------------------Aqui comienza el Modelo nom_estructura_ubicacion-------------------------------------------
class nom_estructura_ubicacion(models.Model):    

    terminal = models.ForeignKey(nom_terminal,  null=False, blank=False,on_delete=models.CASCADE, 
                        help_text="Escoja una opción.", verbose_name="Terminal")
    tipo_estructura = models.ForeignKey(nom_tipo_estructura_ubicacion, null=False, blank=False, on_delete=models.CASCADE, 
                        help_text="Escoja una opción.", verbose_name="Tipo de estructura")
    estructura_padre = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, 
                        help_text="Escoja una opción.",verbose_name="Estructura padre")

    nombre_estructura_ubicacion = models.CharField(max_length=100, verbose_name="Nombre",
                                        unique=True,validators=[RegexValidator(r'^[A-Z][\w\d\W]{2,99}$',"Este campo comienza con mayúscula, acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.",)])

    capacidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Estructura de Ubicación'
        verbose_name_plural = 'Estructuras de Ubicación'

    def __str__(self):
        return self.nombre_estructura_ubicacion
#-----------------------------------------Aqui termina el Modelo nom_estructura_ubicacion---------------------------




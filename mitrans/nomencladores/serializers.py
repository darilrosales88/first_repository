 #1. en este archivo se implementaran todos los serializadores que se usaran en la app, primero
# se importa desde restframeuork los serializadores(serializers), luego se importan los modelos,
from rest_framework import serializers
#para trabajar con el filtrado de los serialziadores debemos hacer la siguiente importacion
from django_filters import rest_framework as filters


#2.  importamos nom_pais
from .models import nom_pais,nom_provincia,nom_municipio,nom_tipo_maniobra_portuaria,nom_contenedor,nom_cargo 
from .models import nom_territorio,nom_puerto,nom_terminal,nom_atraque,nom_unidad_medida, nom_osde_oace_organismo,nom_entidades
from .models import nom_destino,nom_tipo_equipo_ferroviario,nom_embarcacion,nom_equipo_ferroviario,nom_estado_tecnico
from .models import nom_producto,nom_tipo_embalaje,nom_incidencia,nom_tipo_estructura_ubicacion,nom_estructura_ubicacion

#para cada modelo del que deseemos realizar el filtrado debemos hacer un filtrado
#nom_pais_filter es una clase que se implementa para definir sobre qué campos quiero filtrar los registros de mi API, 
#hereda de filters.FilterSet
class nom_pais_filter(filters.FilterSet):
    nom_pais_nacionalidad = filters.CharFilter(field_name='nacionalidad',lookup_expr = 'exact') # filtrando con dos condiciones,                                                                               
                                                                                #la primera que filtre por el campo del modelo 
                                                                                #cuyo nombre sea nacionalidad, y la otra es lookup_expr = 'exact'
                                                                                #el valor del campo debe coincidir exactamente con el parametro 
                                                                                #de busqueda

    nombre_p = filters.CharFilter(method='filter_by_nombre',lookup_expr = 'icontains')#CharFilter filtra por caracteres, la primera cond
                                                                                #es un metodo , y la otra es 
                                                                                #lookup_expr = 'icontains', pregunta si el valor del campo nombre_pais                                                                               
     # coincide en parte con el parametro de busqueda                                                                          
    def filter_by_nombre(self,queryset,value):        
        #return queryset.filter(name__icontains = value) | queryset.filter(description__icontains = value) 
        return queryset.filter(nombre_pais__icontains = value)
    
    #luego de declarar las variables por las que se filtrarán en el class Meta declaramos esos campos igualándolos al valor 
    #del lookup_expr   
    class Meta:
        #declaramos el modelo al cual se le filtrará
        model:nom_pais
        #campos de los que se filtrará
        fields:{
            'nom_pais_nacionalidad':['exact'],
            'nombre_p':['icontains'],
        }


 
#3. Ahora creamos el serializador como tal
class nom_pais_serializer(serializers.ModelSerializer):

    #declarando variable para capturar el nombre del pais
    #category_name = serializers.ReadOnlyField(source = 'category.name')

    # declarando variable para capturar el tipo de precio, esta se hace diferente pues se encuentra en un choice
    #price_type_description = serializers.ReadOnlyField(source = 'get_price_type_display')

    #3.1 en la clase Meta se declara el modelo que voy a utilizar en este serializador
    class Meta:
        model = nom_pais
        #se pone a continuacion qué campos se quieren serializar del modelo, hay dos variantes
        # si uso fields = '__all__'
        # saldrian todos los campos en el serializador y los muestra en el mismo orden en que
        # aparecen en la BD,
        # si los muestro de la forma fields = ('id','nacionalidad', 'nombre_pais')
        #se muestran solo los campos llamados y en el mismo orden en que se ponen
        fields = ('id','nacionalidad', 'nombre_pais')

        filterset_class: nom_pais_filter #esto es para que se aplique al serializador de nom_pais el filtro

       # filterset_class:productFilter #esto es para que se aplique al serializador de producto el filtro

#****************-------------------------********************--------------------***************-----------------********************************

class nom_provincia_filter(filters.FilterSet):
    #nom_provincia_codigo = filters.NumberFilter(field_name='codigo',lookup_expr = 'exact')

    nombre_prov = filters.CharFilter(method='filtrado_por_nombre_provincia',lookup_expr = 'icontains')

    def filtrado_por_nombre_provincia(self,queryset,value):        
        #return queryset.filter(name__icontains = value) | queryset.filter(description__icontains = value) 
        return queryset.filter(nombre_provincia__icontains = value)
    
    class Meta:  
        model:nom_provincia    
        fields:{
            'nombre_prov':['icontains'],
        }
        
class nom_provincia_serializer(serializers.ModelSerializer):
    nombre_pais = serializers.ReadOnlyField(source = 'pais.nombre_pais')#pais.nombre_pais, aqui pais es el nombre de la variable ForeignKey
                                                                        #del modelo nom_pais y nombre_pais es un atributo de este modelo     
    class Meta:
        model = nom_provincia       
        fields = ('id','codigo', 'pais', 'nombre_pais', 'nombre_provincia')
        filterset_class: nom_provincia_filter #esto es para que se aplique al serializador el filtro
#****************-------------------------********************--------------------***************-----------------********************************
class nom_municipio_filter(filters.FilterSet):
    municipio_codigo = filters.CharFilter(field_name='codigo',lookup_expr = 'exact')

    nombre_munic = filters.CharFilter(method='filtrado_por_nombre_municipio',lookup_expr = 'icontains')

    def filtrado_por_nombre_municipio(self,queryset,value):        
        #return queryset.filter(name__icontains = value) | queryset.filter(description__icontains = value) 
        return queryset.filter(nombre_municipio__icontains = value)
    
    class Meta:
  
        model : nom_municipio    
        fields:{
            'municipio_codigo':['exact'],
            'nombre_munic':['icontains'],
        }
class nom_municipio_serializer(serializers.ModelSerializer):
    nombre_provincia= serializers.ReadOnlyField(source = 'provincia.nombre_provincia')                    
    
    class Meta:
        model = nom_municipio       
        fields = ('id','nombre_municipio', 'provincia', 'nombre_provincia', 'codigo')
        filterset_class: nom_municipio_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_tipo_maniobra_portuaria_filter(filters.FilterSet):

    nombre_y_tipo_maniobra = filters.CharFilter(method='filter_by_nomb_y_t_maniobra',lookup_expr = 'icontains')
#filtrado por nombre o tipo de maniobra
    def filter_by_nomb_y_t_maniobra(self,queryset,value):                
        return queryset.filter(nombre_maniobra__icontains = value) | queryset.filter(tipo_maniobra__icontains = value) 
        
    
    class Meta:  
        model:nom_tipo_maniobra_portuaria    
        fields:{
            'nombre_y_tipo_maniobra':['icontains'],
        }

class nom_tipo_maniobra_portuaria_serializer(serializers.ModelSerializer):
    tipo_maniobra_description = serializers.ReadOnlyField(source = 'get_tipo_maniobra_display')#para devolver el valor de un array se pone 
                                                                        #get_nombre_campo_display, en este caso el campo es tipo_maniobra    
    class Meta:
        model = nom_tipo_maniobra_portuaria       
        fields = ('id','nombre_maniobra', 'tipo_maniobra','tipo_maniobra_description')
        filterset_class: nom_tipo_maniobra_portuaria_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_contenedor_filter(filters.FilterSet):
    id_tipo_longitud = filters.CharFilter(method='filter_by_id__tipo_longitud',lookup_expr = 'icontains')

    def filter_by_id__tipo_longitud(self,queryset,value):        
        return queryset.filter(id_contenedor__icontains = value) | queryset.filter(longitud__icontains=value) | queryset.filter(tipo_contenedor__icontains=value)
   

    
    class Meta:
  
        model : nom_contenedor    
        fields:{
            'id_tipo_longitud':['icontains'],            
        }

class nom_contenedor_serializer(serializers.ModelSerializer):
    tipo_contenedor_description = serializers.ReadOnlyField(source='get_tipo_contenedor_display')

    class Meta:
        model = nom_contenedor
        fields = ('id_contenedor', 'tipo_contenedor', 'tipo_contenedor_description', 'longitud', 'codigo_iso')
        filterset_class = nom_contenedor_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_cargo_filter(filters.FilterSet):
    n_cargo = filters.CharFilter(method='filtrado_por_nombre_cargo',lookup_expr = 'icontains')

    def filtrado_por_nombre_cargo(self,queryset,value): 
        return queryset.filter(nombre_cargo__icontains = value)
    
    class Meta:
  
        model : nom_contenedor    
        fields:{
            'n_cargo':['icontains'],
        }

class nom_cargo_serializer(serializers.ModelSerializer):
 
    class Meta:
        model = nom_cargo       
        fields = ('id','nombre_cargo')
        filterset_class: nom_cargo_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_territorio_filter(filters.FilterSet):   

    nomb_territorio = filters.CharFilter(method='filtrado_por_nombre_territorio',lookup_expr = 'icontains')

    def filtrado_por_nombre_territorio(self,queryset,value):        
        #return queryset.filter(name__icontains = value) | queryset.filter(description__icontains = value) 
        return queryset.filter(nombre_territorio__icontains = value)#nombre_territorio es el campo del modelo
    
    class Meta:
  
        model : nom_territorio    
        fields:{
            'nomb_territorio':['icontains'],
        }
class nom_territorio_serializer(serializers.ModelSerializer): 
    class Meta:
        model = nom_territorio       
        fields = ('id','nombre_territorio','abreviatura')
        filterset_class: nom_territorio_filter
#****************-------------------------********************--------------------***************-----------------********************************

class nom_puerto_filter(filters.FilterSet):   

    nombre_puerto = filters.CharFilter(method='filter_by_nombre_puerto',lookup_expr = 'icontains')

    #filtrado por nombre,codigo y descripcion del producto
    def filter_by_nombre_puerto(self,queryset,value):        
        return queryset.filter(nombre_puerto__icontains = value) | queryset.filter(pais_name__icontains = value)  
    
    
    class Meta:
  
        model : nom_puerto    
        fields:{
            'nomb_puerto':['icontains'],
        }
class nom_puerto_serializer(serializers.ModelSerializer):
    nombre_pais = serializers.ReadOnlyField(source = 'pais.nombre_pais')
    nombre_provincia = serializers.ReadOnlyField(source = 'provincia.nombre_provincia')
    servicio_portuario_name = serializers.ReadOnlyField(source = 'servicio_portuario.nombre_territorio')    
    class Meta:
        model = nom_puerto       
        fields = ('id','nombre_puerto','pais','nombre_pais', 'provincia','nombre_provincia', 'servicio_portuario','servicio_portuario_name','latitud','longitud')
        filterset_class = nom_puerto_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_terminal_filter(filters.FilterSet):
    puerto_nombre_terminal = filters.CharFilter(method='filtrado_por_nombre_terminal_puerto',lookup_expr = 'icontains')

    def filtrado_por_nombre_terminal_puerto(self,queryset,value):        
        return queryset.filter(nombre_terminal__icontains = value) | queryset.filter(puerto_name__icontains = value) 
        #return queryset.filter(nombre_terminal__icontains = value)
    
    class Meta:
  
        model : nom_terminal   
        fields:{
            'puerto_nombre_terminal':['icontains'],
        }
class nom_terminal_serializer(serializers.ModelSerializer):
    puerto_name = serializers.ReadOnlyField(source = 'puerto.nombre_puerto')
   
    class Meta:
        model = nom_terminal       
        fields = ('id','nombre_terminal','puerto','puerto_name','capacidad_almacen_importacion', 'capacidad_almacen_exportacion')
        filterset_class: nom_terminal_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_atraque_filter(filters.FilterSet):
    nombre_atraque = filters.CharFilter(method='filtrado_por_nombre_atraque',lookup_expr = 'icontains')

    def filtrado_por_nombre_atraque(self,queryset,value):        
        #return queryset.filter(name__icontains = value) | queryset.filter(description__icontains = value) 
        return queryset.filter(nombre_atraque__icontains = value)
    
    class Meta:
  
        model : nom_atraque   
        fields:{
            'nombre_atraque':['icontains'],
        }
class nom_atraque_serializer(serializers.ModelSerializer):
    puerto_name = serializers.ReadOnlyField(source = 'puerto.nombre_puerto')
    terminal_name = serializers.ReadOnlyField(source = 'terminal.nombre_terminal')
   
    class Meta:
        model = nom_atraque       
        fields = ('id','nombre_atraque','puerto','puerto_name','terminal', 'terminal_name')
        filterset_class: nom_atraque_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_unidad_medida_filter(filters.FilterSet):
    magnitud_um_simbolo= filters.CharFilter(method='filtrado_por_um_magnitud_simbolo',lookup_expr = 'exact')

    

    def filtrado_por_um_magnitud_simbolo(self,queryset,value):        
        return queryset.filter(magnitud__icontains = value) | queryset.filter(simbolo__icontains = value) | queryset.filter(unidad_medida__icontains = value)
        #return queryset.filter(magnitud__icontains = value)
    
    class Meta:
  
        model : nom_contenedor    
        fields:{            
            'magnitud_um_simbolo':['icontains'],            
        }

class nom_unidad_medida_serializer(serializers.ModelSerializer):

    class Meta:
        model = nom_unidad_medida       
        fields = ('id','magnitud','unidad_medida','simbolo')
        filterset_class: nom_unidad_medida_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_osde_oace_organismo_filter(filters.FilterSet):
   # cod_reeup = filters.NumberFilter(field_name='codigo_reeup',lookup_expr = 'exact')
    nombre = filters.CharFilter(method='filtrado_por_nombre',lookup_expr = 'icontains')

    def filtrado_por_nombre(self,queryset,value):        
        #return queryset.filter(name__icontains = value) | queryset.filter(description__icontains = value) 
        return queryset.filter(nombre__icontains = value)
    
    class Meta:
  
        model : nom_osde_oace_organismo    
        fields:{
           # 'cod_reeup':['exact'],
            'nombre':['icontains'],
        }
class nom_osde_oace_organismo_serializer(serializers.ModelSerializer):

    class Meta:
        model = nom_osde_oace_organismo       
        fields = ('id','nombre','abreviatura','codigo_reeup')
        filterset_class = nom_osde_oace_organismo_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_entidades_filter(filters.FilterSet):    
    nombre_abrev_osde = filters.CharFilter(method='filtrado_por_nombre_abrev_org',lookup_expr = 'icontains') 
    def filtrado_por_nombre_abrev_org(self,queryset,value):        
        return queryset.filter(nombre__icontains = value) | queryset.filter(abreviatura__icontains = value) | queryset.filter(osde_oace_organismo__icontains = value)
        
    
    class Meta:
  
        model : nom_entidades    
        fields:{            
            'nombre_abrev_osde':['icontains'],
        }

class nom_entidades_serializer(serializers.ModelSerializer):
    o_o_o_name = serializers.ReadOnlyField(source='osde_oace_organismo.nombre')
    provincia_name = serializers.ReadOnlyField(source='provincia.nombre_provincia')
    territorio_name = serializers.ReadOnlyField(source='territorio.nombre_territorio')
    tipo_entidad_name = serializers.ReadOnlyField(source='get_tipo_entidad_display')

    class Meta:
        model = nom_entidades
        fields = ('id', 'nombre', 'abreviatura', 'osde_oace_organismo','codigo_reeup', 'o_o_o_name', 'provincia', 'provincia_name', 
        'tipo_entidad', 'tipo_entidad_name','territorio','territorio_name',)
        extra_kwargs = {
            'osde_oace_organismo': {'allow_null': True},
            'territorio': {'allow_null': True},
            'entidad': {'allow_null': True},
        }
#****************-------------------------********************--------------------***************-----------------********************************
class nom_destino_filter(filters.FilterSet):
    cliente_destino = filters.CharFilter(method='filter_by_cliente_destino',lookup_expr = 'icontains') 

    def filter_by_cliente_destino(self,queryset,value):
           return queryset.filter(cliente__icontains = value) | queryset.filter(destino__icontains = value)
    
    class Meta:
  
        model : nom_destino   
        fields:{
            'cliente_destino':['icontains'],
        }

class nom_destino_serializer(serializers.ModelSerializer):
    cliente_name= serializers.ReadOnlyField(source = 'cliente.nombre') 
       
    
    class Meta:
        model = nom_destino       
        fields = ('id','cliente', 'cliente_name', 'destino')
        filterset_class: nom_destino_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_tipo_equipo_ferroviario_filter(filters.FilterSet):
    busqueda_tipo_equipo__tipo_carga = filters.CharFilter(method='filter_by_tipo_descrip_combustible_equipo',lookup_expr = 'icontains') 

    #filtrado por tipo de equipo, descripcion y tipo de combustible
    def filter_by_tipo_descrip_combustible_equipo(self,queryset,value):        
        #aqui se filtra por encontrar una subcadena en los campos tipo_equipo y tipo_carga
        return queryset.filter(tipo_equipo__icontains = value) | queryset.filter(tipo_carga__icontains=value)
    
    class Meta:
  
        model : nom_tipo_equipo_ferroviario    
        fields:{
            'busqueda_tipo_equipo__tipo_carga':['icontains'],        
        }

class nom_tipo_equipo_ferroviario_serializer(serializers.ModelSerializer):
    tipo_equipo_name = serializers.ReadOnlyField(source = 'get_tipo_equipo_display')
    tipo_carga_name = serializers.ReadOnlyField(source = 'get_tipo_carga_display')
    tipo_combustible_name = serializers.ReadOnlyField(source = 'get_tipo_combustible_display') 
     
    class Meta:
        model = nom_tipo_equipo_ferroviario       
        fields = ('id','tipo_equipo','tipo_equipo_name', 'tipo_carga', 'tipo_carga_name', 'tipo_combustible', 'tipo_combustible_name','longitud',
        'peso_neto_sin_carga','peso_maximo_con_carga','capacidad_cubica_maxima','descripcion')
        filterset_class: nom_tipo_equipo_ferroviario_filter 

#****************-------------------------********************--------------------***************-----------------********************************
class nom_embarcacion_filter(filters.FilterSet):
    nombre_tipo_nacionalidad = filters.CharFilter(method='filtrado_por_nombre_tipo_nacionalidad',lookup_expr = 'icontains') 
    

    def filtrado_por_nombre_tipo_nacionalidad(self,queryset,value):        
        return queryset.filter(nombre_embarcacion__icontains = value) | queryset.filter(nacionalidad_name__icontains = value) | queryset.filter(tipo_embarcacion_name__icontains = value)
        
    
    class Meta:
  
        model : nom_embarcacion    
        fields:{
            'nombre_tipo_nacionalidad':['icontains'],        
        }



class nom_embarcacion_serializer(serializers.ModelSerializer):
    nacionalidad_name = serializers.ReadOnlyField(source='nacionalidad.nombre_pais')
    tipo_embarcacion_name = serializers.ReadOnlyField(source='get_tipo_embarcacion_display')
    tipo_buque_name = serializers.ReadOnlyField(source='get_tipo_buque_display')
    tipo_patana_name = serializers.ReadOnlyField(source='get_tipo_patana_display')

    class Meta:
        model = nom_embarcacion
        fields = (
            'id', 'nombre_embarcacion', 'nacionalidad', 'nacionalidad_name',
            'eslora', 'manga', 'calado_maximo', 'desplazamiento_maximo',
            'tipo_embarcacion', 'tipo_embarcacion_name', 'tipo_buque',
            'tipo_buque_name', 'tipo_patana', 'tipo_patana_name', 'imo', 'potencia'
        )
        extra_kwargs = {
            'tipo_buque': {'allow_null': True},
            'tipo_patana': {'allow_null': True},
            'imo': {'allow_null': True},
            'potencia': {'allow_null': True},
        }
#****************-------------------------********************--------------------***************-----------------********************************
class nom_equipo_ferroviario_filter(filters.FilterSet):    
    id_tipo_equipo_territorio = filters.CharFilter(method='filtrado_por_id_tipo_equipo_territorio',lookup_expr = 'iexact')

    def filtrado_por_id_tipo_equipo_territorio(self,queryset,value):        
        return queryset.filter(tipo_equipo_name__icontains = value) | queryset.filter(numero_identificacion__icontains = value) | queryset.filter(territorio_name__icontains = value) 
    #     return queryset.filter(tipo_equipo__icontains = value)
    
    class Meta:
  
        model : nom_equipo_ferroviario    
        fields:{
            'id_tipo_equipo_territorio':['icontains'],
        }

class nom_equipo_ferroviario_serializer(serializers.ModelSerializer):
    #aqui se captura el texto de la seleccion del tipo de equipo y no el valor 
    tipo_equipo_name = serializers.ReadOnlyField(source='tipo_equipo.get_tipo_equipo_display')
    territorio_name = serializers.ReadOnlyField(source = 'get_territorio_display') 
    tipo_combustible_name=serializers.ReadOnlyField(source='tipo_equipo.get_tipo_combustible_display')
       
    
    class Meta:
        model = nom_equipo_ferroviario       
        fields = ('id','tipo_equipo','tipo_equipo_name','estado_actual', 'numero_identificacion','territorio','territorio_name','tipo_carga','tipo_combustible','tipo_combustible_name','peso_maximo')
        filterset_class: nom_equipo_ferroviario_filter 

#****************-------------------------********************--------------------***************-----------------********************************
class nom_estado_tecnico_filter(filters.FilterSet):
    codigo_estado = filters.NumberFilter(field_name='codigo_estado',lookup_expr = 'exact')
    estado_tecnico = filters.CharFilter(method='filtrado_por_nombre_estado_tecnico',lookup_expr = 'icontains')

    def filtrado_por_nombre_estado_tecnico(self,queryset,value):        
        #return queryset.filter(name__icontains = value) | queryset.filter(description__icontains = value) 
        return queryset.filter(nombre_estado_tecnico__icontains = value) | queryset.filter(codigo_estado_tecnico = value)
    
    class Meta:
  
        model : nom_estado_tecnico    
        fields:{
            'codigo_estado':['exact'],
            'estado_tecnico':['icontains'],
        }

class nom_estado_tecnico_serializer(serializers.ModelSerializer):
  
    class Meta:
        model = nom_estado_tecnico       
        fields = ('codigo_estado_tecnico','nombre_estado_tecnico')
        filterset_class: nom_estado_tecnico_filter 
#****************-------------------------********************--------------------***************-----------------********************************
class nom_producto_filter(filters.FilterSet):
    nombre_tipo_codigo_producto = filters.CharFilter(method='filter_by_nombre_tipo_codigo_producto',lookup_expr = 'icontains')

    #filtrado por nombre,codigo y descripcion del producto
    def filter_by_nombre_tipo_codigo_producto(self,queryset,value):        
        return queryset.filter(nombre_producto__icontains = value) | queryset.filter(tipo_producto__icontains = value) | queryset.filter(codigo_producto__exact = value) 
    
    class Meta:
  
        model : nom_producto    
        fields:{
            'nombre_tipo_codigo_producto':['icontains'],
        }

class nom_producto_serializer(serializers.ModelSerializer):
    tipo_producto_name = serializers.ReadOnlyField(source = 'get_tipo_producto_display')     
  
    class Meta:
        model = nom_producto       
        fields = ('id', 'codigo_producto','nombre_producto','tipo_producto','tipo_producto_name','descripcion')
        filterset_class = nom_producto_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_tipo_embalaje_filter(filters.FilterSet):    
    nombre_tipo_embalaje = filters.CharFilter(method='filtrado_por_nombre_tipo_embalaje',lookup_expr = 'icontains')

    #filtrado nombre del embalaje
    def filtrado_por_nombre_tipo_embalaje(self,queryset,value):        
        return queryset.filter(nombre_tipo_embalaje__icontains = value) 
    
    class Meta:
  
        model : nom_tipo_embalaje    
        fields:{
            'nombre_tipo_embalaje':['icontains'],
        }
        

class nom_tipo_embalaje_serializer(serializers.ModelSerializer):  
  
    class Meta:
        model = nom_tipo_embalaje       
        fields = ('id', 'nombre_tipo_embalaje')
        filterset_class = nom_tipo_embalaje_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_incidencia_filter(filters.FilterSet):
    nombre_codigo = filters.CharFilter(method='filtrado_por_nombre_codigo',lookup_expr = 'icontains')  

    def filtrado_por_nombre_codigo(self,queryset,value):        
        return queryset.filter(codigo_incidencia__icontains = value) | queryset.filter(nombre_incidencia__icontains = value)  
 
      
    
    class Meta:
  
        model : nom_contenedor    
        fields:{
            'nombre_codigo':['icontains'],
        }

class nom_incidencia_serializer(serializers.ModelSerializer):
    tipo_imputable_name = serializers.ReadOnlyField(source = 'get_tipo_imputable_display') 
  
    class Meta:
        model = nom_incidencia       
        fields = ('id', 'codigo_incidencia','nombre_incidencia','tipo_imputable','tipo_imputable_name')
        filterset_class: nom_incidencia_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_tipo_estructura_ubicacion_filter(filters.FilterSet):
    nombre_tipo_estructura_ubicacion = filters.CharFilter(field_name='nombre_tipo_estructura_ubicacion',lookup_expr = 'icontains')
    
    class Meta:
  
        model : nom_tipo_estructura_ubicacion    
        fields:{
            'nombre_tipo_estructura_ubicacion':['icontains'],
        }

class nom_tipo_estructura_ubicacion_serializer(serializers.ModelSerializer):    
    class Meta:
        model = nom_tipo_estructura_ubicacion       
        fields = ('id', 'nombre_tipo_estructura_ubicacion')
        filterset_class: nom_tipo_estructura_ubicacion_filter
#****************-------------------------********************--------------------***************-----------------********************************
class nom_estructura_ubicacion_filter(filters.FilterSet):
    nombre_estructura = filters.CharFilter(field_name='nombre_estructura_ubicacion', lookup_expr='icontains')

    class Meta:
        model = nom_estructura_ubicacion
        fields = ['nombre_estructura_ubicacion']


class nom_estructura_ubicacion_serializer(serializers.ModelSerializer):
    terminal_name = serializers.ReadOnlyField(source='terminal.nombre_terminal')
    tipo_estructura_name = serializers.ReadOnlyField(source='tipo_estructura.nombre_tipo_estructura_ubicacion')
    estructura_padre_name = serializers.ReadOnlyField(source='estructura_padre.nombre_estructura_ubicacion')

    class Meta:
        model = nom_estructura_ubicacion
        fields = (
            'id',
            'nombre_estructura_ubicacion',
            'terminal',
            'terminal_name',
            'tipo_estructura',
            'tipo_estructura_name',
            'estructura_padre',
            'estructura_padre_name',
            'capacidad'
        )
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "nomencladores_nom_cargo" (
	"id"	integer NOT NULL,
	"nombre_cargo"	varchar(20) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_contenedor" (
	"id_contenedor"	varchar(11) NOT NULL,
	"tipo_contenedor"	varchar(25) NOT NULL,
	"longitud"	varchar(4) NOT NULL,
	"codigo_iso"	varchar(4) NOT NULL,
	PRIMARY KEY("id_contenedor")
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_estado_tecnico" (
	"id"	integer NOT NULL,
	"codigo_estado_tecnico"	varchar(5) NOT NULL UNIQUE,
	"nombre_estado_tecnico"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_incidencia" (
	"id"	integer NOT NULL,
	"codigo_incidencia"	varchar(20) NOT NULL UNIQUE,
	"nombre_incidencia"	varchar(100) NOT NULL UNIQUE,
	"tipo_imputable"	varchar(40) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_producto" (
	"id"	integer NOT NULL,
	"codigo_producto"	varchar(20) UNIQUE,
	"nombre_producto"	varchar(100) NOT NULL UNIQUE,
	"tipo_producto"	varchar(20) NOT NULL,
	"descripcion"	text NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_tipo_embalaje" (
	"id"	integer NOT NULL,
	"nombre_tipo_embalaje"	varchar(100) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_tipo_estructura_ubicacion" (
	"id"	integer NOT NULL,
	"nombre_tipo_estructura_ubicacion"	varchar(100) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_unidad_medida" (
	"id"	integer NOT NULL,
	"magnitud"	varchar(50) NOT NULL,
	"unidad_medida"	varchar(50) NOT NULL UNIQUE,
	"simbolo"	varchar(3) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_destino" (
	"id"	integer NOT NULL,
	"destino"	varchar(100) NOT NULL,
	"cliente_id"	bigint NOT NULL,
	FOREIGN KEY("cliente_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_osde_oace_organismo" (
	"id"	integer NOT NULL,
	"nombre"	varchar(50) NOT NULL UNIQUE,
	"abreviatura"	varchar(20) NOT NULL UNIQUE,
	"codigo_reeup"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_pais" (
	"id"	integer NOT NULL,
	"nacionalidad"	varchar(3) NOT NULL UNIQUE,
	"nombre_pais"	varchar(100) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_provincia" (
	"id"	integer NOT NULL,
	"codigo"	varchar(2) NOT NULL UNIQUE,
	"nombre_provincia"	varchar(100) NOT NULL UNIQUE,
	"pais_id"	bigint NOT NULL,
	FOREIGN KEY("pais_id") REFERENCES "nomencladores_nom_pais"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_municipio" (
	"id"	integer NOT NULL,
	"nombre_municipio"	varchar(100) NOT NULL UNIQUE,
	"codigo"	varchar(4) NOT NULL UNIQUE,
	"provincia_id"	bigint NOT NULL,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_puerto" (
	"id"	integer NOT NULL,
	"nombre_puerto"	varchar(100) NOT NULL UNIQUE,
	"latitud"	varchar(50) NOT NULL,
	"longitud"	varchar(50) NOT NULL,
	"pais_id"	bigint NOT NULL,
	"provincia_id"	bigint,
	"servicio_portuario_id"	bigint,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("servicio_portuario_id") REFERENCES "nomencladores_nom_territorio"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("pais_id") REFERENCES "nomencladores_nom_pais"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_terminal" (
	"id"	integer NOT NULL,
	"nombre_terminal"	varchar(100) NOT NULL UNIQUE,
	"capacidad_almacen_importacion"	decimal NOT NULL,
	"capacidad_almacen_exportacion"	decimal NOT NULL,
	"puerto_id"	bigint NOT NULL,
	FOREIGN KEY("puerto_id") REFERENCES "nomencladores_nom_puerto"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_atraque" (
	"id"	integer NOT NULL,
	"nombre_atraque"	varchar(100) NOT NULL UNIQUE,
	"puerto_id"	bigint NOT NULL,
	"terminal_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("puerto_id") REFERENCES "nomencladores_nom_puerto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("terminal_id") REFERENCES "nomencladores_nom_terminal"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_territorio" (
	"id"	integer NOT NULL,
	"nombre_territorio"	varchar(100) NOT NULL UNIQUE,
	"abreviatura"	varchar(3) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_tipo_equipo_ferroviario" (
	"id"	integer NOT NULL,
	"tipo_equipo"	varchar(30) NOT NULL,
	"tipo_carga"	varchar(15) NOT NULL,
	"tipo_combustible"	varchar(20),
	"longitud"	decimal NOT NULL,
	"peso_neto_sin_carga"	decimal NOT NULL,
	"peso_maximo_con_carga"	decimal NOT NULL,
	"capacidad_cubica_maxima"	decimal NOT NULL,
	"descripcion"	varchar(60) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_estructura_ubicacion" (
	"id"	integer NOT NULL,
	"nombre_estructura_ubicacion"	varchar(100) NOT NULL UNIQUE,
	"capacidad"	decimal NOT NULL,
	"estructura_padre_id"	bigint,
	"terminal_id"	bigint NOT NULL,
	"tipo_estructura_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("terminal_id") REFERENCES "nomencladores_nom_terminal"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("estructura_padre_id") REFERENCES "nomencladores_nom_estructura_ubicacion"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_estructura_id") REFERENCES "nomencladores_nom_tipo_estructura_ubicacion"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_tipo_maniobra_portuaria" (
	"id"	integer NOT NULL,
	"nombre_maniobra"	varchar(100) NOT NULL,
	"tipo_maniobra"	varchar(7) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_embarcacion" (
	"id"	integer NOT NULL,
	"nombre_embarcacion"	varchar(100) NOT NULL UNIQUE,
	"eslora"	decimal NOT NULL,
	"manga"	decimal NOT NULL,
	"calado_maximo"	decimal NOT NULL,
	"desplazamiento_maximo"	decimal NOT NULL,
	"tipo_embarcacion"	varchar(20) NOT NULL,
	"tipo_buque"	varchar(30),
	"imo"	varchar(10) UNIQUE,
	"potencia"	decimal,
	"nacionalidad_id"	bigint NOT NULL,
	"tipo_patana"	varchar(30),
	FOREIGN KEY("nacionalidad_id") REFERENCES "nomencladores_nom_pais"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_entidades" (
	"id"	integer NOT NULL,
	"nombre"	varchar(100) NOT NULL UNIQUE,
	"abreviatura"	varchar(20) NOT NULL UNIQUE,
	"tipo_entidad"	varchar(30) NOT NULL,
	"osde_oace_organismo_id"	bigint,
	"provincia_id"	bigint,
	"territorio_id"	bigint,
	"codigo_reeup"	varchar(15),
	FOREIGN KEY("territorio_id") REFERENCES "nomencladores_nom_territorio"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("osde_oace_organismo_id") REFERENCES "nomencladores_nom_osde_oace_organismo"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_equipo_ferroviario" (
	"id"	integer NOT NULL,
	"numero_identificacion"	varchar(10) NOT NULL,
	"territorio"	varchar(10) NOT NULL,
	"tipo_carga"	varchar(28) NOT NULL,
	"tipo_combustible"	varchar(20),
	"peso_maximo"	decimal NOT NULL,
	"tipo_equipo_id"	bigint NOT NULL,
	"estado_actual"	varchar(10) NOT NULL,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "nomencladores_nom_cargo" ("id","nombre_cargo") VALUES (1,'Esp en alimentos');
INSERT INTO "nomencladores_nom_cargo" ("id","nombre_cargo") VALUES (2,'Técnico');
INSERT INTO "nomencladores_nom_cargo" ("id","nombre_cargo") VALUES (3,'Especialista');
INSERT INTO "nomencladores_nom_contenedor" ("id_contenedor","tipo_contenedor","longitud","codigo_iso") VALUES ('KJMN9999999','HC','1-20','23P0');
INSERT INTO "nomencladores_nom_contenedor" ("id_contenedor","tipo_contenedor","longitud","codigo_iso") VALUES ('KJMN0000000','RC','1-20','23P0');
INSERT INTO "nomencladores_nom_contenedor" ("id_contenedor","tipo_contenedor","longitud","codigo_iso") VALUES ('KJMN9999898','DC','1-20','23P8');
INSERT INTO "nomencladores_nom_estado_tecnico" ("id","codigo_estado_tecnico","nombre_estado_tecnico") VALUES (1,'sadf','sfdg');
INSERT INTO "nomencladores_nom_incidencia" ("id","codigo_incidencia","nombre_incidencia","tipo_imputable") VALUES (1,'43','Incidencia Un0','imputables_puerto');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (1,'CHI0012','Chícharo','alimento','Minsa');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (3,'SAD534','AAdera','alimento','Asdafgfdh');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (4,'CF33241','cafe','alimento','SERRANO');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (5,'CHF','Cafe','alimento','SERRANO');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (6,'MTD01','mortadella','alimento','ESTA VERDE');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (7,'SUKO012','Zuko','alimento','Echale mas agua');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (8,'PST01','Pasta espaguethi','alimento','ROCIO');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (9,'VELA01','Velas apagones','alimento','Velas para el apagon');
INSERT INTO "nomencladores_nom_producto" ("id","codigo_producto","nombre_producto","tipo_producto","descripcion") VALUES (17,'fqqwfqfq','feffer','otros','Grgr');
INSERT INTO "nomencladores_nom_tipo_embalaje" ("id","nombre_tipo_embalaje") VALUES (1,'Nylon');
INSERT INTO "nomencladores_nom_tipo_embalaje" ("id","nombre_tipo_embalaje") VALUES (3,'RAPEL');
INSERT INTO "nomencladores_nom_tipo_embalaje" ("id","nombre_tipo_embalaje") VALUES (4,'Paqueticos');
INSERT INTO "nomencladores_nom_tipo_estructura_ubicacion" ("id","nombre_tipo_estructura_ubicacion") VALUES (1,'Tipo de estructura Uno');
INSERT INTO "nomencladores_nom_unidad_medida" ("id","magnitud","unidad_medida","simbolo") VALUES (1,'Física','centímetro','cm');
INSERT INTO "nomencladores_nom_unidad_medida" ("id","magnitud","unidad_medida","simbolo") VALUES (2,'metro','metro','m');
INSERT INTO "nomencladores_nom_unidad_medida" ("id","magnitud","unidad_medida","simbolo") VALUES (3,'volumen','Litros','L');
INSERT INTO "nomencladores_nom_destino" ("id","destino","cliente_id") VALUES (1,'Aquel lugar',1);
INSERT INTO "nomencladores_nom_destino" ("id","destino","cliente_id") VALUES (3,'Aquel lugar1',1);
INSERT INTO "nomencladores_nom_osde_oace_organismo" ("id","nombre","abreviatura","codigo_reeup") VALUES (1,'Ministerio de Comercio Interior','MINCIN',9932984832);
INSERT INTO "nomencladores_nom_pais" ("id","nacionalidad","nombre_pais") VALUES (1,'CUB','Cuba');
INSERT INTO "nomencladores_nom_pais" ("id","nacionalidad","nombre_pais") VALUES (2,'ITA','Italiano');
INSERT INTO "nomencladores_nom_provincia" ("id","codigo","nombre_provincia","pais_id") VALUES (1,'01','La Habana',1);
INSERT INTO "nomencladores_nom_puerto" ("id","nombre_puerto","latitud","longitud","pais_id","provincia_id","servicio_portuario_id") VALUES (1,'Puerto Unos','23','23',1,1,2);
INSERT INTO "nomencladores_nom_puerto" ("id","nombre_puerto","latitud","longitud","pais_id","provincia_id","servicio_portuario_id") VALUES (3,'Puerto dos','1212','11',1,1,2);
INSERT INTO "nomencladores_nom_terminal" ("id","nombre_terminal","capacidad_almacen_importacion","capacidad_almacen_exportacion","puerto_id") VALUES (1,'Terminal unica',224.65,331.7,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (1,'Atraque Uno',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (3,'Asadert',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (4,'Claria',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (5,'LUNA',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (6,'Mjaaa',3,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (7,'DLAD',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (8,'ADAD',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (9,'AQWE',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (10,'QDAS',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (11,'FAS',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (12,'FAF',3,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (13,'FQQQ',3,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (14,'ASFQ',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (15,'ADQVC',3,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (16,'DQDD',3,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (17,'GGG',1,1);
INSERT INTO "nomencladores_nom_atraque" ("id","nombre_atraque","puerto_id","terminal_id") VALUES (18,'HHRHG',1,1);
INSERT INTO "nomencladores_nom_territorio" ("id","nombre_territorio","abreviatura") VALUES (1,'Asana','ASA');
INSERT INTO "nomencladores_nom_territorio" ("id","nombre_territorio","abreviatura") VALUES (2,'Eser','MAS');
INSERT INTO "nomencladores_nom_tipo_equipo_ferroviario" ("id","tipo_equipo","tipo_carga","tipo_combustible","longitud","peso_neto_sin_carga","peso_maximo_con_carga","capacidad_cubica_maxima","descripcion") VALUES (3,'locomotora','combustible','combustible_negro',12,2,2,12,'Mala');
INSERT INTO "nomencladores_nom_tipo_equipo_ferroviario" ("id","tipo_equipo","tipo_carga","tipo_combustible","longitud","peso_neto_sin_carga","peso_maximo_con_carga","capacidad_cubica_maxima","descripcion") VALUES (4,'locomotora','combustible','combustible_negro',12333,111,11233,123144,'La turbo');
INSERT INTO "nomencladores_nom_tipo_equipo_ferroviario" ("id","tipo_equipo","tipo_carga","tipo_combustible","longitud","peso_neto_sin_carga","peso_maximo_con_carga","capacidad_cubica_maxima","descripcion") VALUES (5,'locomotora','combustible','combustible_negro',100,10000,100000,10000,'La mole');
INSERT INTO "nomencladores_nom_tipo_equipo_ferroviario" ("id","tipo_equipo","tipo_carga","tipo_combustible","longitud","peso_neto_sin_carga","peso_maximo_con_carga","capacidad_cubica_maxima","descripcion") VALUES (6,'planc_plat','contenedores','combustible_blanco',122,1234,1234,12,'adsf');
INSERT INTO "nomencladores_nom_estructura_ubicacion" ("id","nombre_estructura_ubicacion","capacidad","estructura_padre_id","terminal_id","tipo_estructura_id") VALUES (1,'Manani',13,NULL,1,1);
INSERT INTO "nomencladores_nom_estructura_ubicacion" ("id","nombre_estructura_ubicacion","capacidad","estructura_padre_id","terminal_id","tipo_estructura_id") VALUES (2,'Majs',43,1,1,1);
INSERT INTO "nomencladores_nom_tipo_maniobra_portuaria" ("id","nombre_maniobra","tipo_maniobra") VALUES (1,'Maniobra uno','entrada');
INSERT INTO "nomencladores_nom_embarcacion" ("id","nombre_embarcacion","eslora","manga","calado_maximo","desplazamiento_maximo","tipo_embarcacion","tipo_buque","imo","potencia","nacionalidad_id","tipo_patana") VALUES (16,'Asada',34,43,43,34,'remolcador','-','-',347,1,'-');
INSERT INTO "nomencladores_nom_embarcacion" ("id","nombre_embarcacion","eslora","manga","calado_maximo","desplazamiento_maximo","tipo_embarcacion","tipo_buque","imo","potencia","nacionalidad_id","tipo_patana") VALUES (17,'Qwrt',7,57,76,6,'buque','buque_granelero','QWE1234567',NULL,1,'-');
INSERT INTO "nomencladores_nom_embarcacion" ("id","nombre_embarcacion","eslora","manga","calado_maximo","desplazamiento_maximo","tipo_embarcacion","tipo_buque","imo","potencia","nacionalidad_id","tipo_patana") VALUES (19,'Aaaaaa',0.03,0.03,0.03,0.03,'remolcador',NULL,NULL,987,1,NULL);
INSERT INTO "nomencladores_nom_embarcacion" ("id","nombre_embarcacion","eslora","manga","calado_maximo","desplazamiento_maximo","tipo_embarcacion","tipo_buque","imo","potencia","nacionalidad_id","tipo_patana") VALUES (20,'Asadert',12,12,12,12,'otros',NULL,NULL,NULL,1,NULL);
INSERT INTO "nomencladores_nom_embarcacion" ("id","nombre_embarcacion","eslora","manga","calado_maximo","desplazamiento_maximo","tipo_embarcacion","tipo_buque","imo","potencia","nacionalidad_id","tipo_patana") VALUES (21,'Asadeeww',43,43,34,34,'buque','buque_frig','ASD1234567',NULL,1,NULL);
INSERT INTO "nomencladores_nom_embarcacion" ("id","nombre_embarcacion","eslora","manga","calado_maximo","desplazamiento_maximo","tipo_embarcacion","tipo_buque","imo","potencia","nacionalidad_id","tipo_patana") VALUES (22,'Gasfdf',546,7587,67,678,'remolcador',NULL,NULL,890,1,NULL);
INSERT INTO "nomencladores_nom_embarcacion" ("id","nombre_embarcacion","eslora","manga","calado_maximo","desplazamiento_maximo","tipo_embarcacion","tipo_buque","imo","potencia","nacionalidad_id","tipo_patana") VALUES (23,'Cgdhfgh',5,45,45,456,'buque','buque_granelero','ASD1234569',NULL,1,NULL);
INSERT INTO "nomencladores_nom_embarcacion" ("id","nombre_embarcacion","eslora","manga","calado_maximo","desplazamiento_maximo","tipo_embarcacion","tipo_buque","imo","potencia","nacionalidad_id","tipo_patana") VALUES (24,'Asdfsdfg',346,456,456,45,'remolcador',NULL,NULL,339.9,1,NULL);
INSERT INTO "nomencladores_nom_entidades" ("id","nombre","abreviatura","tipo_entidad","osde_oace_organismo_id","provincia_id","territorio_id","codigo_reeup") VALUES (1,'Cuba Ron SA','CRSA','importador',1,1,2,'23455');
INSERT INTO "nomencladores_nom_entidades" ("id","nombre","abreviatura","tipo_entidad","osde_oace_organismo_id","provincia_id","territorio_id","codigo_reeup") VALUES (6,'Acceso comercial uno','ACuno','acceso_comercial',1,1,2,'1212121');
INSERT INTO "nomencladores_nom_entidades" ("id","nombre","abreviatura","tipo_entidad","osde_oace_organismo_id","provincia_id","territorio_id","codigo_reeup") VALUES (7,'CCD Uno','CCDU','ccd',1,1,2,'1212121245');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (2,'LOCO0073','oriente','Combustible','Combustible negro',11233,4,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (4,'LOCOMB001','oriente','Combustible','Combustible negro',2,3,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (11,'AAAAFFFF','centro','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (12,'ADqq11','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (14,'ADSFF','oriente','contenedor','-combust_blanco',1233,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (15,'ARRQQQ','centro','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (16,'AQWE','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (17,'HASFF','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
CREATE INDEX IF NOT EXISTS "nomencladores_nom_destino_cliente_id_78ad5f6a" ON "nomencladores_nom_destino" (
	"cliente_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_osde_oace_organismo_nombre_abreviatura_codigo_reeup_87d4ad5c_uniq" ON "nomencladores_nom_osde_oace_organismo" (
	"nombre",
	"abreviatura",
	"codigo_reeup"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_pais_nacionalidad_nombre_pais_fe8c0aa4_uniq" ON "nomencladores_nom_pais" (
	"nacionalidad",
	"nombre_pais"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_provincia_pais_id_635e11c5" ON "nomencladores_nom_provincia" (
	"pais_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_municipio_provincia_id_eaf73857" ON "nomencladores_nom_municipio" (
	"provincia_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_puerto_nombre_puerto_pais_id_4cd5109b_uniq" ON "nomencladores_nom_puerto" (
	"nombre_puerto",
	"pais_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_puerto_pais_id_0608bb9d" ON "nomencladores_nom_puerto" (
	"pais_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_puerto_provincia_id_dbbd3ef8" ON "nomencladores_nom_puerto" (
	"provincia_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_terminal_nombre_terminal_puerto_id_f5a8bc86_uniq" ON "nomencladores_nom_terminal" (
	"nombre_terminal",
	"puerto_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_terminal_puerto_id_5fe50006" ON "nomencladores_nom_terminal" (
	"puerto_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_atraque_puerto_id_fdf7bedd" ON "nomencladores_nom_atraque" (
	"puerto_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_atraque_terminal_id_b428b683" ON "nomencladores_nom_atraque" (
	"terminal_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_territorio_nombre_territorio_abreviatura_b812f7e1_uniq" ON "nomencladores_nom_territorio" (
	"nombre_territorio",
	"abreviatura"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_puerto_servicio_portuario_id_a9496608" ON "nomencladores_nom_puerto" (
	"servicio_portuario_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_tipo_equipo_ferroviario_tipo_equipo_tipo_carga_longitud_peso_neto_sin_carga_descripcion_844feb6b_uniq" ON "nomencladores_nom_tipo_equipo_ferroviario" (
	"tipo_equipo",
	"tipo_carga",
	"longitud",
	"peso_neto_sin_carga",
	"descripcion"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_estructura_ubicacion_estructura_padre_id_829e8faa" ON "nomencladores_nom_estructura_ubicacion" (
	"estructura_padre_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_estructura_ubicacion_terminal_id_1c15d859" ON "nomencladores_nom_estructura_ubicacion" (
	"terminal_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_estructura_ubicacion_tipo_estructura_id_8700d3d6" ON "nomencladores_nom_estructura_ubicacion" (
	"tipo_estructura_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_tipo_maniobra_portuaria_nombre_maniobra_tipo_maniobra_2c3df87f_uniq" ON "nomencladores_nom_tipo_maniobra_portuaria" (
	"nombre_maniobra",
	"tipo_maniobra"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_atraque_nombre_atraque_puerto_id_terminal_id_06da1e6e_uniq" ON "nomencladores_nom_atraque" (
	"nombre_atraque",
	"puerto_id",
	"terminal_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_destino_cliente_id_destino_6cfe7661_uniq" ON "nomencladores_nom_destino" (
	"cliente_id",
	"destino"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_embarcacion_nacionalidad_id_d2b9ccc2" ON "nomencladores_nom_embarcacion" (
	"nacionalidad_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_entidades_osde_oace_organismo_id_3bd090b0" ON "nomencladores_nom_entidades" (
	"osde_oace_organismo_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_entidades_provincia_id_92710e17" ON "nomencladores_nom_entidades" (
	"provincia_id"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_entidades_territorio_id_eabd4474" ON "nomencladores_nom_entidades" (
	"territorio_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_equipo_ferroviario_tipo_equipo_id_numero_identificacion_territorio_94bcad4a_uniq" ON "nomencladores_nom_equipo_ferroviario" (
	"tipo_equipo_id",
	"numero_identificacion",
	"territorio"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_equipo_ferroviario_tipo_equipo_id_1a10f23d" ON "nomencladores_nom_equipo_ferroviario" (
	"tipo_equipo_id"
);
COMMIT;

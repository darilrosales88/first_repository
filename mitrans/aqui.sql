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
	FOREIGN KEY("puerto_id") REFERENCES "nomencladores_nom_puerto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("terminal_id") REFERENCES "nomencladores_nom_terminal"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
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
	FOREIGN KEY("tipo_estructura_id") REFERENCES "nomencladores_nom_tipo_estructura_ubicacion"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("terminal_id") REFERENCES "nomencladores_nom_terminal"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("estructura_padre_id") REFERENCES "nomencladores_nom_estructura_ubicacion"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "nomencladores_nom_tipo_maniobra_portuaria" (
	"id"	integer NOT NULL,
	"nombre_maniobra"	varchar(100) NOT NULL,
	"tipo_maniobra"	varchar(7) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Administracion_customuser_groups" (
	"id"	integer NOT NULL,
	"customuser_id"	bigint NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("customuser_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "Administracion_customuser_user_permissions" (
	"id"	integer NOT NULL,
	"customuser_id"	bigint NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("customuser_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
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
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("nacionalidad_id") REFERENCES "nomencladores_nom_pais"("id") DEFERRABLE INITIALLY DEFERRED
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
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("osde_oace_organismo_id") REFERENCES "nomencladores_nom_osde_oace_organismo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("territorio_id") REFERENCES "nomencladores_nom_territorio"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "Administracion_customuser" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"first_name"	varchar(150) NOT NULL,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"cargo_id"	bigint,
	"entidad_id"	bigint,
	"role"	varchar(20) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("cargo_id") REFERENCES "nomencladores_nom_cargo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("entidad_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_producto_ufc" (
	"id"	integer NOT NULL,
	"cantidad"	integer NOT NULL,
	"estado"	varchar(20),
	"contiene"	varchar(20),
	"producto_id"	bigint NOT NULL,
	"tipo_embalaje_id"	bigint NOT NULL,
	"unidad_medida_id"	bigint NOT NULL,
	"tipo_equipo_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("unidad_medida_id") REFERENCES "nomencladores_nom_unidad_medida"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_embalaje_id") REFERENCES "nomencladores_nom_tipo_embalaje"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "nomencladores_nom_producto"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_vagon_cargado_descargado_registros_vagones" (
	"id"	integer NOT NULL,
	"vagon_cargado_descargado_id"	bigint NOT NULL,
	"registro_vagones_cargados_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("registro_vagones_cargados_id") REFERENCES "ufc_registro_vagones_cargados"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagon_cargado_descargado_id") REFERENCES "ufc_vagon_cargado_descargado"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_vagones_productos_producto" (
	"id"	integer NOT NULL,
	"vagones_productos_id"	bigint NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagones_productos_id") REFERENCES "ufc_vagones_productos"("id") DEFERRABLE INITIALLY DEFERRED
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
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_en_trenes_equipo_vagon" (
	"id"	integer NOT NULL,
	"en_trenes_id"	bigint NOT NULL,
	"nom_equipo_ferroviario_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("nom_equipo_ferroviario_id") REFERENCES "nomencladores_nom_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("en_trenes_id") REFERENCES "ufc_en_trenes"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ufc_informe_operativo" (
	"id"	integer NOT NULL,
	"fecha_operacion"	datetime NOT NULL UNIQUE,
	"fecha_actual"	datetime NOT NULL UNIQUE,
	"plan_mensual_total"	integer NOT NULL,
	"plan_diario_total_vagones_cargados"	integer NOT NULL,
	"real_total_vagones_cargados"	integer NOT NULL,
	"total_vagones_situados"	integer NOT NULL,
	"plan_total_acumulado_actual"	integer NOT NULL,
	"real_total_acumulado_actual"	integer NOT NULL,
	"estado_parte"	varchar(14) NOT NULL,
	"aprobado_por_id"	bigint,
	"creado_por_id"	bigint,
	"provincia_id"	bigint,
	"entidad_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("aprobado_por_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("creado_por_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("entidad_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_vagon_cargado_descargado" (
	"id"	integer NOT NULL,
	"tipo_origen"	varchar(50) NOT NULL,
	"origen"	varchar(40) NOT NULL,
	"estado"	varchar(50) NOT NULL,
	"operacion"	varchar(50) NOT NULL,
	"plan_diario_carga_descarga"	integer NOT NULL,
	"real_carga_descarga"	integer NOT NULL,
	"tipo_destino"	varchar(50) NOT NULL,
	"destino"	varchar(40) NOT NULL,
	"causas_incumplimiento"	text NOT NULL,
	"tipo_equipo_ferroviario_id"	bigint NOT NULL,
	"fecha"	datetime NOT NULL,
	"informe_operativo_id"	bigint,
	"producto_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("producto_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_operativo_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_ferroviario_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_vagones_productos" (
	"id"	integer NOT NULL,
	"tipo_origen"	varchar(50) NOT NULL,
	"origen"	varchar(40) NOT NULL,
	"tipo_producto"	varchar(20),
	"tipo_combustible"	varchar(20),
	"plan_mensual"	integer NOT NULL,
	"plan_dia"	integer NOT NULL,
	"vagones_situados"	integer NOT NULL,
	"vagones_cargados"	integer NOT NULL,
	"plan_aseguramiento_proximos_dias"	integer NOT NULL,
	"observaciones"	text,
	"plan_anual"	integer NOT NULL,
	"plan_acumulado_dia_anterior"	integer NOT NULL,
	"real_acumulado_dia_anterior"	integer NOT NULL,
	"tipo_equipo_ferroviario_id"	bigint,
	"fecha"	datetime NOT NULL,
	"plan_acumulado_actual"	integer NOT NULL,
	"plan_acumulado_anual"	integer NOT NULL,
	"real_acumulado_actual"	integer NOT NULL,
	"real_acumulado_anual"	integer NOT NULL,
	"informe_operativo_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("informe_operativo_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_ferroviario_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_arrastres" (
	"id"	integer NOT NULL,
	"tipo_origen"	varchar(50) NOT NULL,
	"origen"	varchar(40) NOT NULL,
	"estado"	varchar(200),
	"cantidad_vagones"	varchar(10) NOT NULL,
	"tipo_destino"	varchar(50) NOT NULL,
	"destino"	varchar(40) NOT NULL,
	"fecha"	datetime NOT NULL,
	"informe_operativo_id"	bigint,
	"tipo_equipo_id"	bigint,
	"observaciones"	text,
	"operacion"	varchar(200),
	"producto_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_operativo_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_por_situar" (
	"id"	integer NOT NULL,
	"tipo_origen"	varchar(100) NOT NULL,
	"origen"	varchar(200) NOT NULL,
	"estado"	varchar(200) NOT NULL,
	"operacion"	varchar(200) NOT NULL,
	"por_situar"	varchar(10) NOT NULL,
	"observaciones"	text,
	"fecha"	datetime NOT NULL,
	"informe_operativo_id"	bigint,
	"tipo_equipo_id"	bigint,
	"producto_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("informe_operativo_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_situado_carga_descarga" (
	"id"	integer NOT NULL,
	"tipo_origen"	varchar(100),
	"origen"	varchar(200) NOT NULL,
	"estado"	varchar(200),
	"operacion"	varchar(200),
	"situados"	varchar(10) NOT NULL,
	"pendiente_proximo_dia"	varchar(10) NOT NULL,
	"observaciones"	text,
	"fecha"	datetime NOT NULL,
	"informe_operativo_id"	bigint,
	"tipo_equipo_id"	bigint,
	"producto_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("informe_operativo_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_vagones_dias" (
	"id"	integer NOT NULL,
	"cant_dias"	smallint unsigned NOT NULL CHECK("cant_dias" >= 0),
	"equipo_ferroviario_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("equipo_ferroviario_id") REFERENCES "nomencladores_nom_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_arrastres_equipo_vagon" (
	"id"	integer NOT NULL,
	"arrastres_id"	bigint NOT NULL,
	"vagones_dias_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("arrastres_id") REFERENCES "ufc_arrastres"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagones_dias_id") REFERENCES "ufc_vagones_dias"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_por_situar_equipo_vagon" (
	"id"	integer NOT NULL,
	"por_situar_id"	bigint NOT NULL,
	"vagones_dias_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("vagones_dias_id") REFERENCES "ufc_vagones_dias"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("por_situar_id") REFERENCES "ufc_por_situar"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_situado_carga_descarga_equipo_vagon" (
	"id"	integer NOT NULL,
	"situado_carga_descarga_id"	bigint NOT NULL,
	"vagones_dias_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("situado_carga_descarga_id") REFERENCES "ufc_situado_carga_descarga"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagones_dias_id") REFERENCES "ufc_vagones_dias"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_registro_vagones_cargados" (
	"id"	integer NOT NULL,
	"fecha_despacho"	date,
	"tipo_origen"	varchar(50),
	"origen"	varchar(40),
	"fecha_llegada"	date,
	"observaciones"	text,
	"no_id"	varchar(50),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_rotacion_vagones" (
	"id"	integer NOT NULL,
	"en_servicio"	integer unsigned NOT NULL CHECK("en_servicio" >= 0),
	"plan_carga"	integer unsigned NOT NULL CHECK("plan_carga" >= 0),
	"real_carga"	integer unsigned NOT NULL CHECK("real_carga" >= 0),
	"plan_rotacion"	real NOT NULL,
	"real_rotacion"	real NOT NULL,
	"actualizado_el"	datetime NOT NULL,
	"tipo_equipo_ferroviario_id"	bigint NOT NULL,
	"fecha"	datetime NOT NULL,
	"informe_operativo_id"	bigint,
	CONSTRAINT "unique_train_rotation" UNIQUE("tipo_equipo_ferroviario_id","informe_operativo_id"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("tipo_equipo_ferroviario_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_operativo_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_en_trenes" (
	"id"	integer NOT NULL,
	"numero_identificacion_locomotora"	varchar(10),
	"estado"	varchar(50) NOT NULL,
	"tipo_origen"	varchar(50) NOT NULL,
	"origen"	varchar(40) NOT NULL,
	"tipo_destino"	varchar(50) NOT NULL,
	"destino"	varchar(40) NOT NULL,
	"cantidad_vagones"	integer NOT NULL,
	"observaciones"	text,
	"locomotora_id"	bigint NOT NULL,
	"tipo_equipo_id"	bigint NOT NULL,
	"fecha"	datetime NOT NULL,
	"informe_operativo_id"	bigint,
	"producto_id"	bigint,
	CONSTRAINT "unique_train_register" UNIQUE("tipo_equipo_id","estado","origen","destino"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_operativo_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("locomotora_id") REFERENCES "nomencladores_nom_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_situados_equipo_vagon" (
	"id"	integer NOT NULL,
	"ccd_situados_id"	bigint NOT NULL,
	"vagones_dias_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("ccd_situados_id") REFERENCES "ufc_ccd_situados"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagones_dias_id") REFERENCES "ufc_vagones_dias"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_por_situar_equipo_vagon" (
	"id"	integer NOT NULL,
	"ccd_por_situar_id"	bigint NOT NULL,
	"vagones_dias_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("vagones_dias_id") REFERENCES "ufc_vagones_dias"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("ccd_por_situar_id") REFERENCES "ufc_ccd_por_situar"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_en_trenes_equipo_vagon" (
	"id"	integer NOT NULL,
	"ccd_en_trenes_id"	bigint NOT NULL,
	"nom_equipo_ferroviario_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("ccd_en_trenes_id") REFERENCES "ufc_ccd_en_trenes"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("nom_equipo_ferroviario_id") REFERENCES "nomencladores_nom_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_arrastres_equipo_vagon" (
	"id"	integer NOT NULL,
	"ccd_arrastres_id"	bigint NOT NULL,
	"vagones_dias_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("ccd_arrastres_id") REFERENCES "ufc_ccd_arrastres"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagones_dias_id") REFERENCES "ufc_vagones_dias"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_vagones_cd_equipo_vagon" (
	"id"	integer NOT NULL,
	"ccd_vagones_cd_id"	bigint NOT NULL,
	"ccd_registro_vagones_cd_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("ccd_registro_vagones_cd_id") REFERENCES "ufc_ccd_registro_vagones_cd"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("ccd_vagones_cd_id") REFERENCES "ufc_ccd_vagones_cd"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_producto" (
	"id"	integer NOT NULL,
	"cantidad"	integer NOT NULL,
	"estado"	varchar(20),
	"contiene"	varchar(20),
	"tipo_embalaje_id"	bigint NOT NULL,
	"tipo_equipo_id"	bigint,
	"unidad_medida_id"	bigint NOT NULL,
	"producto_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("tipo_embalaje_id") REFERENCES "nomencladores_nom_tipo_embalaje"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "nomencladores_nom_producto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("unidad_medida_id") REFERENCES "nomencladores_nom_unidad_medida"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_por_situar" (
	"fecha_registro"	date NOT NULL,
	"id"	integer NOT NULL,
	"estado"	varchar(10) NOT NULL,
	"operacion"	varchar(10) NOT NULL,
	"cantidad_vagones"	integer,
	"causas_incumplimiento"	text,
	"tipo_equipo_id"	bigint NOT NULL,
	"producto_id"	bigint,
	"informe_ccd_id"	bigint NOT NULL,
	"acceso_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("acceso_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_ccd_id") REFERENCES "ufc_ufc_informe_ccd"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "ufc_ccd_producto"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_registro_vagones_cd" (
	"id"	integer NOT NULL,
	"no_id"	varchar(50),
	"fecha_despacho"	date,
	"tipo_origen"	varchar(50),
	"origen"	varchar(40),
	"fecha_llegada"	date,
	"incidencias"	bool NOT NULL,
	"observaciones"	text CHECK((JSON_VALID("observaciones") OR "observaciones" IS NULL)),
	"equipo_ferroviario_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("equipo_ferroviario_id") REFERENCES "nomencladores_nom_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_casillas_productos" (
	"id"	integer NOT NULL,
	"acceso_id"	bigint,
	"total_ayer"	integer NOT NULL,
	"entro_hoy"	integer NOT NULL,
	"plan_carga"	integer NOT NULL,
	"plan_descarga"	integer NOT NULL,
	"recepcion"	integer NOT NULL,
	"reexpedciones"	integer NOT NULL,
	"informe_ccd_id"	bigint NOT NULL,
	"total_general"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("acceso_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_ccd_id") REFERENCES "ufc_ufc_informe_ccd"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ufc_informe_ccd" (
	"id"	integer NOT NULL,
	"fecha_operacion"	datetime NOT NULL UNIQUE,
	"fecha_actual"	datetime NOT NULL UNIQUE,
	"comentarios"	text,
	"aprobado_por_id"	bigint,
	"creado_por_id"	bigint,
	"entidad_id"	bigint,
	"provincia_id"	bigint,
	"estado_parte"	varchar(14) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("entidad_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("creado_por_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("aprobado_por_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_arrastres" (
	"fecha_registro"	date NOT NULL,
	"id"	integer NOT NULL,
	"acceso_id"	bigint,
	"estado"	varchar(10) NOT NULL,
	"cantidad_vagones"	integer,
	"observaciones"	text,
	"tipo_equipo_id"	bigint NOT NULL,
	"producto_id"	bigint,
	"informe_ccd_id"	bigint NOT NULL,
	CONSTRAINT "unique_ccd_arrastres_register" UNIQUE("producto_id","tipo_equipo_id","acceso_id","informe_ccd_id"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("producto_id") REFERENCES "ufc_ccd_producto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("acceso_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_ccd_id") REFERENCES "ufc_ufc_informe_ccd"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_en_trenes" (
	"fecha_registro"	date NOT NULL,
	"id"	integer NOT NULL,
	"acceso_id"	bigint,
	"estado"	varchar(10) NOT NULL,
	"cantidad_vagones"	integer,
	"observaciones"	text,
	"tipo_equipo_id"	bigint NOT NULL,
	"producto_id"	bigint,
	"informe_ccd_id"	bigint NOT NULL,
	CONSTRAINT "unique_ccd_en_trenes_register" UNIQUE("producto_id","tipo_equipo_id","acceso_id","informe_ccd_id"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_ccd_id") REFERENCES "ufc_ufc_informe_ccd"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("acceso_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "ufc_ccd_producto"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_situados" (
	"fecha_registro"	date NOT NULL,
	"id"	integer NOT NULL,
	"acceso_id"	bigint,
	"estado"	varchar(10) NOT NULL,
	"operacion"	varchar(10) NOT NULL,
	"real_carga_descarga"	real,
	"causas_incumplimiento"	text,
	"tipo_equipo_id"	bigint NOT NULL,
	"producto_id"	bigint,
	"informe_ccd_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("acceso_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "ufc_ccd_producto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_ccd_id") REFERENCES "ufc_ufc_informe_ccd"("id") DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT "unique_ccd_situados_register" UNIQUE("producto_id","tipo_equipo_id","acceso_id","informe_ccd_id")
);
CREATE TABLE IF NOT EXISTS "ufc_ccd_vagones_cd" (
	"fecha_registro"	date,
	"id"	integer NOT NULL,
	"acceso_id"	bigint,
	"causa_incumplimiento"	text,
	"estado"	varchar(10) NOT NULL,
	"informe_ccd_id"	bigint,
	"producto_id"	bigint,
	"tipo_equipo_id"	bigint,
	"operacion"	varchar(15) NOT NULL,
	"real_carga_descarga"	real,
	PRIMARY KEY("id" AUTOINCREMENT),
	CONSTRAINT "unique_ccd_vagones_cd_register" UNIQUE("producto_id","tipo_equipo_id","acceso_id","informe_ccd_id"),
	FOREIGN KEY("producto_id") REFERENCES "ufc_ccd_producto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("acceso_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("informe_ccd_id") REFERENCES "ufc_ufc_informe_ccd"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "gemar_gemar_parte_hecho_extraordinario" (
	"id"	integer NOT NULL,
	"fecha_actual"	datetime NOT NULL,
	"estado_parte"	varchar(14) NOT NULL,
	"aprobado_por_id"	bigint,
	"creado_por_id"	bigint,
	"entidad_id"	bigint,
	"provincia_id"	bigint,
	"fecha_operacion"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("creado_por_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("entidad_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("aprobado_por_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "gemar_gemar_hecho_extraordinario" (
	"id"	integer NOT NULL,
	"fecha_operacion"	datetime NOT NULL UNIQUE,
	"fecha_actual"	datetime NOT NULL UNIQUE,
	"informado"	varchar(200) NOT NULL,
	"tipo_involucrado"	varchar(20) NOT NULL,
	"involucrado"	varchar(40),
	"tipo_origen"	varchar(50) NOT NULL,
	"origen"	varchar(40) NOT NULL,
	"destino"	varchar(40) NOT NULL,
	"tipo_diferencia"	varchar(20) NOT NULL,
	"cantidad_diferencia"	decimal,
	"valor_diferencia"	decimal,
	"averia"	varchar(2),
	"kg_averia"	decimal,
	"cantidad_averia"	decimal,
	"valor_averia"	decimal,
	"descripcion_hecho"	varchar(500),
	"embalaje_id"	bigint NOT NULL,
	"garante_id"	bigint,
	"incidencia_involucrada_id"	bigint NOT NULL,
	"producto_involucrado_id"	bigint NOT NULL,
	"unidad_medida_id"	bigint NOT NULL,
	"parte_hecho_extraordinario_id"	bigint,
	"kg_diferencia"	decimal,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("producto_involucrado_id") REFERENCES "nomencladores_nom_producto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("incidencia_involucrada_id") REFERENCES "nomencladores_nom_incidencia"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("unidad_medida_id") REFERENCES "nomencladores_nom_unidad_medida"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("embalaje_id") REFERENCES "nomencladores_nom_tipo_embalaje"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("garante_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("parte_hecho_extraordinario_id") REFERENCES "gemar_gemar_parte_hecho_extraordinario"("id") DEFERRABLE INITIALLY DEFERRED
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
INSERT INTO "nomencladores_nom_tipo_equipo_ferroviario" ("id","tipo_equipo","tipo_carga","tipo_combustible","longitud","peso_neto_sin_carga","peso_maximo_con_carga","capacidad_cubica_maxima","descripcion") VALUES (7,'planc_plat','otros','combustible_blanco',123,333,1111,1233,'Asdff');
INSERT INTO "nomencladores_nom_tipo_equipo_ferroviario" ("id","tipo_equipo","tipo_carga","tipo_combustible","longitud","peso_neto_sin_carga","peso_maximo_con_carga","capacidad_cubica_maxima","descripcion") VALUES (8,'casilla','otros','combustible_negro',14124,1231,12313,41412,'dadafffw');
INSERT INTO "nomencladores_nom_estructura_ubicacion" ("id","nombre_estructura_ubicacion","capacidad","estructura_padre_id","terminal_id","tipo_estructura_id") VALUES (1,'Manani',13,NULL,1,1);
INSERT INTO "nomencladores_nom_estructura_ubicacion" ("id","nombre_estructura_ubicacion","capacidad","estructura_padre_id","terminal_id","tipo_estructura_id") VALUES (2,'Majs',43,1,1,1);
INSERT INTO "nomencladores_nom_tipo_maniobra_portuaria" ("id","nombre_maniobra","tipo_maniobra") VALUES (1,'Maniobra uno','entrada');
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (1,1,1);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (2,1,2);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (3,1,3);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (4,1,4);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (5,1,5);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (6,1,6);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (7,1,7);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (8,1,8);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (9,1,9);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (10,1,10);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (11,1,11);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (12,1,12);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (13,1,13);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (14,1,14);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (15,1,15);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (16,1,16);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (17,1,17);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (18,1,18);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (19,1,19);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (20,1,20);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (21,1,21);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (22,1,22);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (23,1,23);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (24,1,24);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (25,1,25);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (26,1,26);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (27,1,27);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (28,1,28);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (29,1,29);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (30,1,30);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (31,1,31);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (32,1,32);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (33,1,33);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (34,1,34);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (35,1,35);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (36,1,36);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (37,1,37);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (38,1,38);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (39,1,39);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (40,1,40);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (41,1,41);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (42,1,42);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (43,1,43);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (44,1,44);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (45,1,45);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (46,1,46);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (47,1,47);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (48,1,48);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (49,1,49);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (50,1,50);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (51,1,51);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (52,1,52);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (53,1,53);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (54,1,54);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (55,1,55);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (56,1,56);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (57,1,57);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (58,1,58);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (59,1,59);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (60,1,60);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (61,1,61);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (62,1,62);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (63,1,63);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (64,1,64);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (65,1,65);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (66,1,66);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (67,1,67);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (68,1,68);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (69,1,69);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (70,1,70);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (71,1,71);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (72,1,72);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (73,1,73);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (74,1,74);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (75,1,75);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (76,1,76);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (77,1,77);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (78,1,78);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (79,1,79);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (80,1,80);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (81,1,81);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (82,1,82);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (83,1,83);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (84,1,84);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (85,1,85);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (86,1,86);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (87,1,87);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (88,1,88);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (89,1,89);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (90,1,90);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (91,1,91);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (92,1,92);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (93,1,93);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (94,1,94);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (95,1,95);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (96,1,96);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (97,1,97);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (98,1,98);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (99,1,99);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (100,1,100);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (101,1,101);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (102,1,102);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (103,1,103);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (104,1,104);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (105,1,105);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (106,1,106);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (107,1,107);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (108,1,108);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (109,1,109);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (110,1,110);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (111,1,111);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (112,1,112);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (113,1,113);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (114,1,114);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (115,1,115);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (116,1,116);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (117,1,117);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (118,1,118);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (119,1,119);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (120,1,120);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (121,1,121);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (122,1,122);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (123,1,123);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (124,1,124);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (125,1,125);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (126,1,126);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (127,1,127);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (128,1,128);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (129,2,20);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (130,2,32);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (131,2,36);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (132,2,40);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (133,2,44);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (134,2,48);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (135,2,52);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (136,2,56);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (137,2,60);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (138,2,64);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (139,2,68);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (140,2,72);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (141,2,76);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (142,2,80);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (143,2,84);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (144,2,88);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (145,2,92);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (146,2,96);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (147,2,100);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (148,2,104);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (149,2,108);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (150,2,112);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (151,2,116);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (152,2,120);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (153,1,129);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (154,1,130);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (155,1,131);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (156,1,132);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (157,1,133);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (158,1,134);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (159,1,135);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (160,1,136);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (161,1,137);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (162,1,138);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (163,1,139);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (164,1,140);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (165,3,29);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (166,3,30);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (167,3,31);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (168,3,32);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (169,3,33);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (170,3,34);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (171,3,35);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (172,3,36);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (173,3,37);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (174,3,38);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (175,3,39);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (176,3,40);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (177,3,41);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (178,3,42);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (179,3,43);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (180,3,44);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (181,3,45);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (182,3,46);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (183,3,47);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (184,3,48);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (185,3,49);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (186,3,50);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (187,3,51);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (188,3,52);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (189,3,53);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (190,3,54);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (191,3,55);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (192,3,56);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (193,3,57);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (194,3,58);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (195,3,59);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (196,3,60);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (197,3,61);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (198,3,62);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (199,3,63);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (200,3,64);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (201,3,65);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (202,3,66);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (203,3,67);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (204,3,68);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (205,3,69);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (206,3,70);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (207,3,71);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (208,3,72);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (209,3,73);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (210,3,74);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (211,3,75);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (212,3,76);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (213,3,77);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (214,3,78);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (215,3,79);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (216,3,80);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (217,3,81);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (218,3,82);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (219,3,83);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (220,3,84);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (221,3,85);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (222,3,86);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (223,3,87);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (224,3,88);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (225,3,89);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (226,3,90);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (227,3,91);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (228,3,92);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (229,3,93);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (230,3,94);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (231,3,95);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (232,3,96);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (233,3,97);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (234,3,98);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (235,3,99);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (236,3,100);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (237,3,101);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (238,3,102);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (239,3,103);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (240,3,104);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (241,3,105);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (242,3,106);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (243,3,107);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (244,3,108);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (245,3,109);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (246,3,110);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (247,3,111);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (248,3,112);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (249,3,113);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (250,3,114);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (251,3,115);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (252,3,116);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (253,3,117);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (254,3,118);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (255,3,119);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (256,3,120);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (257,3,145);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (258,3,146);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (259,3,147);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (260,3,148);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (261,3,149);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (262,3,150);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (263,3,151);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (264,3,152);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (265,4,129);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (266,4,130);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (267,4,131);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (268,4,132);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (269,4,133);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (270,4,134);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (271,4,135);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (272,4,136);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (273,4,137);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (274,4,138);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (275,4,139);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (276,4,140);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (277,4,141);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (278,4,142);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (279,4,143);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (280,4,144);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (281,4,153);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (282,4,154);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (283,4,155);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (284,4,156);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (285,4,157);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (286,4,158);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (287,4,159);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (288,4,160);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (289,4,161);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (290,4,162);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (291,4,163);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (292,4,164);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (293,4,165);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (294,4,166);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (295,4,167);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (296,4,168);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (297,4,169);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (298,4,170);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (299,4,171);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (300,4,172);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (301,4,173);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (302,4,174);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (303,4,175);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (304,4,176);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (305,4,177);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (306,4,178);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (307,4,179);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (308,4,180);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (309,4,192);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (310,4,193);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (311,4,194);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (312,4,195);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (313,4,196);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (314,4,185);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (315,4,186);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (316,4,187);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (317,4,188);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (318,4,189);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (319,4,190);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (320,4,191);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (321,5,32);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (322,5,36);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (323,5,40);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (324,5,44);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (325,5,48);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (326,5,52);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (327,5,56);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (328,5,60);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (329,5,64);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (330,5,68);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (331,5,72);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (332,5,76);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (333,5,80);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (334,5,84);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (335,5,88);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (336,5,92);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (337,5,96);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (338,5,100);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (339,5,104);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (340,5,108);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (341,5,112);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (342,5,116);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (343,5,120);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (344,6,192);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (345,6,160);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (346,6,164);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (347,6,132);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (348,6,196);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (349,6,168);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (350,6,136);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (351,6,172);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (352,6,140);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (353,6,176);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (354,6,144);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (355,6,188);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (356,6,148);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (357,6,180);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (358,6,152);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (359,6,156);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (360,6,184);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (361,7,200);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (362,7,230);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (363,1,141);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (364,1,142);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (365,1,143);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (366,1,144);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (367,1,145);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (368,1,146);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (369,1,147);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (370,1,148);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (371,1,149);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (372,1,150);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (373,1,151);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (374,1,152);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (375,1,153);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (376,1,154);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (377,1,155);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (378,1,156);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (379,1,157);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (380,1,158);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (381,1,159);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (382,1,160);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (383,1,161);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (384,1,162);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (385,1,163);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (386,1,164);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (387,1,165);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (388,1,166);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (389,1,167);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (390,1,168);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (391,1,169);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (392,1,170);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (393,1,171);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (394,1,172);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (395,1,173);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (396,1,174);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (397,1,175);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (398,1,176);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (399,1,177);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (400,1,178);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (401,1,179);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (402,1,180);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (403,1,181);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (404,1,182);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (405,1,183);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (406,1,184);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (407,1,185);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (408,1,186);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (409,1,187);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (410,1,188);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (411,1,189);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (412,1,190);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (413,1,191);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (414,1,192);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (415,1,193);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (416,1,194);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (417,1,195);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (418,1,196);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (419,1,197);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (420,1,198);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (421,1,199);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (422,1,200);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (423,1,201);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (424,1,202);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (425,1,203);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (426,1,204);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (427,1,205);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (428,1,206);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (429,1,207);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (430,1,208);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (431,1,209);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (432,1,210);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (433,1,211);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (434,1,212);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (435,1,213);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (436,1,214);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (437,1,215);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (438,1,216);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (439,1,217);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (440,1,218);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (441,1,219);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (442,1,220);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (443,1,221);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (444,1,222);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (445,1,223);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (446,1,224);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (447,1,225);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (448,1,226);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (449,1,227);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (450,1,228);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (451,1,229);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (452,1,230);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (453,1,231);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (454,7,229);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (455,7,255);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (456,7,288);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (457,7,289);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (458,4,256);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (459,4,257);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (460,4,258);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (461,4,259);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (462,4,260);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (463,4,261);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (464,4,262);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (465,4,263);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (466,4,264);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (467,4,265);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (468,4,266);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (469,4,267);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (470,4,268);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (471,4,269);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (472,4,270);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (473,4,271);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (474,4,276);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (475,4,277);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (476,4,278);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (477,4,279);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (478,4,280);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (479,4,281);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (480,4,282);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (481,4,283);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (482,4,284);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (483,4,285);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (484,4,286);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (485,4,287);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (486,4,290);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (487,4,240);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (488,4,241);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (489,4,242);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (490,4,243);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (491,4,244);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (492,4,245);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (493,4,246);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (494,4,247);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (495,4,248);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (496,4,249);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (497,4,250);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (498,4,251);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (499,4,252);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (500,4,253);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (501,4,254);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (502,4,255);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (503,4,197);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (504,4,198);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (505,4,231);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (506,4,200);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (507,4,199);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (508,4,145);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (509,4,146);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (510,4,147);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (511,4,148);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (512,4,149);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (513,4,150);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (514,4,151);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (515,4,152);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (516,8,129);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (517,8,130);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (518,8,131);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (519,8,132);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (520,8,133);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (521,8,134);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (522,8,135);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (523,8,136);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (524,8,137);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (525,8,138);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (526,8,139);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (527,8,140);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (528,8,141);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (529,8,142);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (530,8,143);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (531,8,144);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (532,8,145);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (533,8,146);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (534,8,147);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (535,8,148);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (536,8,149);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (537,8,150);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (538,8,151);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (539,8,152);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (540,8,153);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (541,8,154);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (542,8,155);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (543,8,156);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (544,8,157);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (545,8,158);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (546,8,159);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (547,8,160);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (548,8,161);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (549,8,162);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (550,8,163);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (551,8,164);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (552,8,165);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (553,8,166);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (554,8,167);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (555,8,168);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (556,8,169);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (557,8,170);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (558,8,171);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (559,8,172);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (560,8,173);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (561,8,174);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (562,8,175);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (563,8,176);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (564,8,177);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (565,8,178);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (566,8,179);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (567,8,180);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (568,8,181);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (569,8,182);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (570,8,183);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (571,8,184);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (572,8,185);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (573,8,186);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (574,8,187);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (575,8,188);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (576,8,189);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (577,8,190);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (578,8,191);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (579,8,192);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (580,8,193);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (581,8,194);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (582,8,195);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (583,8,196);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (584,8,197);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (585,8,198);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (586,8,199);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (587,8,200);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (588,8,229);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (589,8,230);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (590,8,231);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (591,8,232);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (592,8,233);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (593,8,234);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (594,8,235);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (595,8,236);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (596,8,237);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (597,8,238);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (598,8,239);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (599,8,240);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (600,8,241);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (601,8,242);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (602,8,243);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (603,8,244);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (604,8,245);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (605,8,246);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (606,8,247);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (607,8,248);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (608,8,249);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (609,8,250);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (610,8,251);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (611,8,252);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (612,8,253);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (613,8,254);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (614,8,255);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (615,8,256);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (616,8,257);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (617,8,258);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (618,8,259);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (619,8,260);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (620,8,261);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (621,8,262);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (622,8,263);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (623,8,264);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (624,8,265);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (625,8,266);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (626,8,267);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (627,8,268);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (628,8,269);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (629,8,270);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (630,8,271);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (631,8,272);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (632,8,273);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (633,8,274);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (634,8,275);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (635,8,276);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (636,8,277);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (637,8,278);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (638,8,279);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (639,8,280);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (640,8,281);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (641,8,282);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (642,8,283);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (643,8,284);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (644,8,285);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (645,8,286);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (646,8,287);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (647,8,288);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (648,8,289);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (649,8,290);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (650,1,256);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (651,1,257);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (652,1,258);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (653,1,259);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (654,1,260);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (655,1,261);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (656,1,262);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (657,1,263);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (658,1,264);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (659,1,265);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (660,1,266);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (661,1,267);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (662,1,268);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (663,1,269);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (664,1,270);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (665,1,271);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (666,1,272);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (667,1,273);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (668,1,274);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (669,1,275);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (670,1,276);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (671,1,277);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (672,1,278);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (673,1,279);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (674,1,280);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (675,1,281);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (676,1,282);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (677,1,283);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (678,1,284);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (679,1,285);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (680,1,286);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (681,1,287);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (682,1,288);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (683,1,289);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (684,1,290);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (685,1,232);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (686,1,233);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (687,1,234);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (688,1,235);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (689,1,236);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (690,1,237);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (691,1,238);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (692,1,239);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (693,1,240);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (694,1,241);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (695,1,242);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (696,1,243);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (697,1,244);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (698,1,245);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (699,1,246);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (700,1,247);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (701,1,248);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (702,1,249);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (703,1,250);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (704,1,251);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (705,1,252);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (706,1,253);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (707,1,254);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (708,1,255);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (709,4,275);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (710,4,32);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (711,4,36);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (712,4,40);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (713,4,44);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (714,4,48);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (715,4,52);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (716,4,56);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (717,4,60);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (718,4,64);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (719,4,68);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (720,4,72);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (721,4,76);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (722,4,80);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (723,4,84);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (724,4,88);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (725,4,92);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (726,4,96);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (727,4,100);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (728,4,104);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (729,4,108);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (730,4,112);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (731,4,116);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (732,4,120);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (733,9,291);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (734,9,292);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (735,9,293);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (736,9,294);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (737,9,295);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (738,9,296);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (739,9,297);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (740,9,298);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (741,9,299);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (742,9,300);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (743,9,301);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (744,10,301);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (745,10,294);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (746,11,296);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (747,11,295);
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_logentry','Insertar log entry');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (2,1,'change_logentry','Editar log entry');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (3,1,'delete_logentry','Eliminar log entry');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (4,1,'view_logentry','Visualizar log entry');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (5,2,'add_permission','Insertar permission');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (6,2,'change_permission','Editar permission');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (7,2,'delete_permission','Eliminar permission');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (8,2,'view_permission','Visualizar permission');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (9,3,'add_group','Insertar group');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (10,3,'change_group','Editar group');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (11,3,'delete_group','Eliminar group');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (12,3,'view_group','Visualizar group');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (13,4,'add_contenttype','Insertar content type');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (14,4,'change_contenttype','Editar content type');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (15,4,'delete_contenttype','Eliminar content type');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (16,4,'view_contenttype','Visualizar content type');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (17,5,'add_session','Insertar session');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (18,5,'change_session','Editar session');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (19,5,'delete_session','Eliminar session');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (20,5,'view_session','Visualizar session');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (21,6,'add_token','Insertar Token');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (22,6,'change_token','Editar Token');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (23,6,'delete_token','Eliminar Token');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (24,6,'view_token','Visualizar Token');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (25,7,'add_tokenproxy','Can add Token');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (26,7,'change_tokenproxy','Can change Token');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (27,7,'delete_tokenproxy','Can delete Token');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (28,7,'view_tokenproxy','Can view Token');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (29,8,'add_nom_cargo','Insertar Cargos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (30,8,'change_nom_cargo','Editar Cargos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (31,8,'delete_nom_cargo','Eliminar Cargos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (32,8,'view_nom_cargo','Visualizar Cargos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (33,9,'add_nom_contenedor','Insertar Contenedor');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (34,9,'change_nom_contenedor','Editar Contenedor');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (35,9,'delete_nom_contenedor','Eliminar Contenedor');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (36,9,'view_nom_contenedor','Visualizar Contenedor');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (37,10,'add_nom_entidades','Insertar Entidad');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (38,10,'change_nom_entidades','Editar Entidad');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (39,10,'delete_nom_entidades','Eliminar Entidad');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (40,10,'view_nom_entidades','Visualizar Entidad');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (41,11,'add_nom_estado_tecnico','Insertar Estado técnico');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (42,11,'change_nom_estado_tecnico','Editar Estado técnico');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (43,11,'delete_nom_estado_tecnico','Eliminar Estado técnico');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (44,11,'view_nom_estado_tecnico','Visualizar Estado técnico');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (45,12,'add_nom_incidencia','Insertar Incidencia');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (46,12,'change_nom_incidencia','Editar Incidencia');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (47,12,'delete_nom_incidencia','Eliminar Incidencia');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (48,12,'view_nom_incidencia','Visualizar Incidencia');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (49,13,'add_nom_producto','Insertar Producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (50,13,'change_nom_producto','Editar Producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (51,13,'delete_nom_producto','Eliminar Producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (52,13,'view_nom_producto','Visualizar Producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (53,14,'add_nom_tipo_embalaje','Insertar Tipo de embalaje');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (54,14,'change_nom_tipo_embalaje','Editar Tipo de embalaje');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (55,14,'delete_nom_tipo_embalaje','Eliminar Tipo de embalaje');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (56,14,'view_nom_tipo_embalaje','Visualizar Tipo de embalaje');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (57,15,'add_nom_tipo_estructura_ubicacion','Insertar Tipo de estructura de ubicación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (58,15,'change_nom_tipo_estructura_ubicacion','Editar Tipo de estructura de ubicación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (59,15,'delete_nom_tipo_estructura_ubicacion','Eliminar Tipo de estructura de ubicación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (60,15,'view_nom_tipo_estructura_ubicacion','Visualizar Tipo de estructura de ubicación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (61,16,'add_nom_unidad_medida','Insertar Unidad de medida');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (62,16,'change_nom_unidad_medida','Editar Unidad de medida');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (63,16,'delete_nom_unidad_medida','Eliminar Unidad de medida');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (64,16,'view_nom_unidad_medida','Visualizar Unidad de medida');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (65,17,'add_nom_destino','Insertar Destino');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (66,17,'change_nom_destino','Editar Destino');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (67,17,'delete_nom_destino','Eliminar Destino');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (68,17,'view_nom_destino','Visualizar Destino');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (69,18,'add_nom_osde_oace_organismo','Insertar Osde/OACE/Organismo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (70,18,'change_nom_osde_oace_organismo','Editar Osde/OACE/Organismo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (71,18,'delete_nom_osde_oace_organismo','Eliminar Osde/OACE/Organismo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (72,18,'view_nom_osde_oace_organismo','Visualizar Osde/OACE/Organismo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (73,19,'add_nom_pais','Insertar País');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (74,19,'change_nom_pais','Editar País');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (75,19,'delete_nom_pais','Eliminar País');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (76,19,'view_nom_pais','Visualizar País');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (77,20,'add_nom_embarcacion','Insertar Embarcación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (78,20,'change_nom_embarcacion','Editar Embarcación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (79,20,'delete_nom_embarcacion','Eliminar Embarcación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (80,20,'view_nom_embarcacion','Visualizar Embarcación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (81,21,'add_nom_provincia','Insertar Provincias');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (82,21,'change_nom_provincia','Editar Provincias');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (83,21,'delete_nom_provincia','Eliminar Provincias');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (84,21,'view_nom_provincia','Visualizar Provincias');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (85,22,'add_nom_municipio','Insertar Municipios');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (86,22,'change_nom_municipio','Editar Municipios');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (87,22,'delete_nom_municipio','Eliminar Municipios');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (88,22,'view_nom_municipio','Visualizar Municipios');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (89,23,'add_nom_puerto','Insertar Puerto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (90,23,'change_nom_puerto','Editar Puerto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (91,23,'delete_nom_puerto','Eliminar Puerto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (92,23,'view_nom_puerto','Visualizar Puerto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (93,24,'add_nom_terminal','Insertar Terminal');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (94,24,'change_nom_terminal','Editar Terminal');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (95,24,'delete_nom_terminal','Eliminar Terminal');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (96,24,'view_nom_terminal','Visualizar Terminal');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (97,25,'add_nom_atraque','Insertar Atraque');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (98,25,'change_nom_atraque','Editar Atraque');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (99,25,'delete_nom_atraque','Eliminar Atraque');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (100,25,'view_nom_atraque','Visualizar Atraque');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (101,26,'add_nom_territorio','Insertar Territorio');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (102,26,'change_nom_territorio','Editar Territorio');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (103,26,'delete_nom_territorio','Eliminar Territorio');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (104,26,'view_nom_territorio','Visualizar Territorio');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (105,27,'add_nom_tipo_equipo_ferroviario','Insertar Tipo de equipo ferroviario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (106,27,'change_nom_tipo_equipo_ferroviario','Editar Tipo de equipo ferroviario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (107,27,'delete_nom_tipo_equipo_ferroviario','Eliminar Tipo de equipo ferroviario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (108,27,'view_nom_tipo_equipo_ferroviario','Visualizar Tipo de equipo ferroviario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (109,28,'add_nom_estructura_ubicacion','Insertar Estructura de Ubicación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (110,28,'change_nom_estructura_ubicacion','Editar Estructura de Ubicación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (111,28,'delete_nom_estructura_ubicacion','Eliminar Estructura de Ubicación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (112,28,'view_nom_estructura_ubicacion','Visualizar Estructura de Ubicación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (113,29,'add_nom_tipo_maniobra_portuaria','Insertar Tipo de maniobra portuaria');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (114,29,'change_nom_tipo_maniobra_portuaria','Editar Tipo de maniobra portuaria');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (115,29,'delete_nom_tipo_maniobra_portuaria','Eliminar Tipo de maniobra portuaria');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (116,29,'view_nom_tipo_maniobra_portuaria','Visualizar Tipo de maniobra portuaria');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (117,30,'add_nom_equipo_ferroviario','Insertar Equipo ferroviario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (118,30,'change_nom_equipo_ferroviario','Editar Equipo ferroviario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (119,30,'delete_nom_equipo_ferroviario','Eliminar Equipo ferroviario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (120,30,'view_nom_equipo_ferroviario','Visualizar Equipo ferroviario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (121,31,'add_customuser','Insertar Usuario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (122,31,'change_customuser','Editar Usuario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (123,31,'delete_customuser','Eliminar Usuario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (124,31,'view_customuser','Visualizar Usuario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (125,32,'add_auditoria','Insertar auditoria');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (126,32,'change_auditoria','Editar auditoria');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (127,32,'delete_auditoria','Eliminar auditoria');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (128,32,'view_auditoria','Visualizar auditoria');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (129,33,'add_productos_vagones_cargados_descargados','Insertar Producto de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (130,33,'change_productos_vagones_cargados_descargados','Editar Producto de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (131,33,'delete_productos_vagones_cargados_descargados','Eliminar Producto de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (132,33,'view_productos_vagones_cargados_descargados','Visualizar Producto de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (133,34,'add_vagon_cargado_descargado','Insertar Vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (134,34,'change_vagon_cargado_descargado','Editar Vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (135,34,'delete_vagon_cargado_descargado','Eliminar Vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (136,34,'view_vagon_cargado_descargado','Visualizar Vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (137,35,'add_en_trenes','Insertar Tren');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (138,35,'change_en_trenes','Editar Tren');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (139,35,'delete_en_trenes','Eliminar Tren');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (140,35,'view_en_trenes','Visualizar Tren');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (141,36,'add_producto_en_vagon','Insertar Producto en vagon');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (142,36,'change_producto_en_vagon','Editar Producto en vagon');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (143,36,'delete_producto_en_vagon','Eliminar Producto en vagon');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (144,36,'view_producto_en_vagon','Visualizar Producto en vagon');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (145,37,'add_situado_carga_descarga','Insertar situado_ carga_ descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (146,37,'change_situado_carga_descarga','Editar situado_ carga_ descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (147,37,'delete_situado_carga_descarga','Eliminar situado_ carga_ descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (148,37,'view_situado_carga_descarga','Visualizar situado_ carga_ descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (149,38,'add_por_situar_carga_descarga','Insertar por_situar_carga_descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (150,38,'change_por_situar_carga_descarga','Editar por_situar_carga_descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (151,38,'delete_por_situar_carga_descarga','Eliminar por_situar_carga_descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (152,38,'view_por_situar_carga_descarga','Visualizar por_situar_carga_descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (153,39,'add_por_situar_carga_descarga','Insertar por_situar_carga_descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (154,39,'change_por_situar_carga_descarga','Editar por_situar_carga_descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (155,39,'delete_por_situar_carga_descarga','Eliminar por_situar_carga_descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (156,39,'view_por_situar_carga_descarga','Visualizar por_situar_carga_descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (157,40,'add_situado_carga_descarga','Insertar Situado ');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (158,40,'change_situado_carga_descarga','Editar Situado ');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (159,40,'delete_situado_carga_descarga','Eliminar Situado ');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (160,40,'view_situado_carga_descarga','Visualizar Situado ');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (161,41,'add_arrastrependientes','Insertar Arrastre Pendiente');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (162,41,'change_arrastrependientes','Editar Arrastre Pendiente');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (163,41,'delete_arrastrependientes','Eliminar Arrastre Pendiente');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (164,41,'view_arrastrependientes','Visualizar Arrastre Pendiente');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (165,42,'add_arrastre_pendientes','Insertar arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (166,42,'change_arrastre_pendientes','Editar arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (167,42,'delete_arrastre_pendientes','Eliminar arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (168,42,'view_arrastre_pendientes','Visualizar arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (169,43,'add_arrastres','Insertar arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (170,43,'change_arrastres','Editar arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (171,43,'delete_arrastres','Eliminar arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (172,43,'view_arrastres','Visualizar arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (173,44,'add_por_situar','Insertar Por situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (174,44,'change_por_situar','Editar Por situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (175,44,'delete_por_situar','Eliminar Por situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (176,44,'view_por_situar','Visualizar Por situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (177,45,'add_registro_vagones_cargados','Insertar Registro de vagón cargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (178,45,'change_registro_vagones_cargados','Editar Registro de vagón cargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (179,45,'delete_registro_vagones_cargados','Eliminar Registro de vagón cargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (180,45,'view_registro_vagones_cargados','Visualizar Registro de vagón cargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (181,46,'add_productos_vagones_productos','Insertar Producto de vagones y productos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (182,46,'change_productos_vagones_productos','Editar Producto de vagones y productos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (183,46,'delete_productos_vagones_productos','Eliminar Producto de vagones y productos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (184,46,'view_productos_vagones_productos','Visualizar Producto de vagones y productos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (185,47,'add_vagones_productos','Insertar Vagón y producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (186,47,'change_vagones_productos','Editar Vagón y producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (187,47,'delete_vagones_productos','Eliminar Vagón y producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (188,47,'view_vagones_productos','Visualizar Vagón y producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (189,48,'add_producto_ufc','Insertar Producto UFC');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (190,48,'change_producto_ufc','Editar Producto UFC');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (191,48,'delete_producto_ufc','Eliminar Producto UFC');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (192,48,'view_producto_ufc','Visualizar Producto UFC');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (193,49,'add_rotacion_vagones','Insertar Registro de rotación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (194,49,'change_rotacion_vagones','Editar Registro de rotación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (195,49,'delete_rotacion_vagones','Eliminar Registro de rotación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (196,49,'view_rotacion_vagones','Visualizar Registro de rotación');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (197,50,'add_ufc_informe_operativo','Insertar Parte informe operativo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (198,50,'change_ufc_informe_operativo','Editar Parte informe operativo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (199,50,'delete_ufc_informe_operativo','Eliminar Parte informe operativo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (200,50,'view_ufc_informe_operativo','Visualizar Parte informe operativo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (201,51,'add_historialvagonporsituar','Insertar Historial de vagón por situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (202,51,'change_historialvagonporsituar','Editar Historial de vagón por situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (203,51,'delete_historialvagonporsituar','Eliminar Historial de vagón por situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (204,51,'view_historialvagonporsituar','Visualizar Historial de vagón por situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (205,52,'add_historialvagonesproductos','Insertar Historial de vagón-producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (206,52,'change_historialvagonesproductos','Editar Historial de vagón-producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (207,52,'delete_historialvagonesproductos','Eliminar Historial de vagón-producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (208,52,'view_historialvagonesproductos','Visualizar Historial de vagón-producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (209,53,'add_historialvagoncargadodescargado','Insertar Historial de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (210,53,'change_historialvagoncargadodescargado','Editar Historial de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (211,53,'delete_historialvagoncargadodescargado','Eliminar Historial de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (212,53,'view_historialvagoncargadodescargado','Visualizar Historial de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (213,54,'add_historialsituadocargadescarga','Insertar Historial de situado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (214,54,'change_historialsituadocargadescarga','Editar Historial de situado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (215,54,'delete_historialsituadocargadescarga','Eliminar Historial de situado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (216,54,'view_historialsituadocargadescarga','Visualizar Historial de situado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (217,55,'add_historialrotacionvagones','Insertar Historial de rotación de vagones');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (218,55,'change_historialrotacionvagones','Editar Historial de rotación de vagones');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (219,55,'delete_historialrotacionvagones','Eliminar Historial de rotación de vagones');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (220,55,'view_historialrotacionvagones','Visualizar Historial de rotación de vagones');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (221,56,'add_historialentrenes','Insertar Historial de tren');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (222,56,'change_historialentrenes','Editar Historial de tren');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (223,56,'delete_historialentrenes','Eliminar Historial de tren');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (224,56,'view_historialentrenes','Visualizar Historial de tren');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (225,57,'add_historialarrastres','Insertar Historial de arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (226,57,'change_historialarrastres','Editar Historial de arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (227,57,'delete_historialarrastres','Eliminar Historial de arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (228,57,'view_historialarrastres','Visualizar Historial de arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (229,50,'puede_rechazar_informe','Puede rechazar informes operativos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (230,50,'puede_aprobar_informe','Puede aprobar informes operativos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (231,50,'puede_cambiar_a_listo','Puede cambiar el estado del informe a listo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (232,58,'add_vagones_dias','Insertar vagones_dias');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (233,58,'change_vagones_dias','Editar vagones_dias');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (234,58,'delete_vagones_dias','Eliminar vagones_dias');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (235,58,'view_vagones_dias','Visualizar vagones_dias');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (236,59,'add_vagones_por_situar_situados_pendientes','Insertar Vagón asociado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (237,59,'change_vagones_por_situar_situados_pendientes','Editar Vagón asociado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (238,59,'delete_vagones_por_situar_situados_pendientes','Eliminar Vagón asociado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (239,59,'view_vagones_por_situar_situados_pendientes','Visualizar Vagón asociado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (240,60,'add_ccd_vagones_cargados_descargados','Insertar ccd_vagones_cargados_descargados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (241,60,'change_ccd_vagones_cargados_descargados','Editar ccd_vagones_cargados_descargados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (242,60,'delete_ccd_vagones_cargados_descargados','Eliminar ccd_vagones_cargados_descargados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (243,60,'view_ccd_vagones_cargados_descargados','Visualizar ccd_vagones_cargados_descargados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (244,61,'add_producto_ccd','Insertar Producto CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (245,61,'change_producto_ccd','Editar Producto CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (246,61,'delete_producto_ccd','Eliminar Producto CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (247,61,'view_producto_ccd','Visualizar Producto CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (248,62,'add_ccd_situados','Insertar CCD Equipos Situados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (249,62,'change_ccd_situados','Editar CCD Equipos Situados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (250,62,'delete_ccd_situados','Eliminar CCD Equipos Situados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (251,62,'view_ccd_situados','Visualizar CCD Equipos Situados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (252,63,'add_ufc_informe_ccd','Insertar Parte CCD por Producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (253,63,'change_ufc_informe_ccd','Editar Parte CCD por Producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (254,63,'delete_ufc_informe_ccd','Eliminar Parte CCD por Producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (255,63,'view_ufc_informe_ccd','Visualizar Parte CCD por Producto');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (256,64,'add_ccd_arrastres','Insertar CCD Equipos Pendientes al Arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (257,64,'change_ccd_arrastres','Editar CCD Equipos Pendientes al Arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (258,64,'delete_ccd_arrastres','Eliminar CCD Equipos Pendientes al Arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (259,64,'view_ccd_arrastres','Visualizar CCD Equipos Pendientes al Arrastre');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (260,65,'add_ccd_por_situar','Insertar CCD Equipos Por Situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (261,65,'change_ccd_por_situar','Editar CCD Equipos Por Situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (262,65,'delete_ccd_por_situar','Eliminar CCD Equipos Por Situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (263,65,'view_ccd_por_situar','Visualizar CCD Equipos Por Situar');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (264,66,'add_casillas_ccd_productos','Insertar casillas_ccd_productos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (265,66,'change_casillas_ccd_productos','Editar casillas_ccd_productos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (266,66,'delete_casillas_ccd_productos','Eliminar casillas_ccd_productos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (267,66,'view_casillas_ccd_productos','Visualizar casillas_ccd_productos');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (268,67,'add_ccd_en_trenes','Insertar CCD Equipos En Trenes');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (269,67,'change_ccd_en_trenes','Editar CCD Equipos En Trenes');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (270,67,'delete_ccd_en_trenes','Eliminar CCD Equipos En Trenes');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (271,67,'view_ccd_en_trenes','Visualizar CCD Equipos En Trenes');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (272,68,'add_ccd_registro_vagones_cd','Insertar Registro de vagón cargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (273,68,'change_ccd_registro_vagones_cd','Editar Registro de vagón cargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (274,68,'delete_ccd_registro_vagones_cd','Eliminar Registro de vagón cargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (275,68,'view_ccd_registro_vagones_cd','Visualizar Registro de vagón cargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (276,60,'add_ccd_vagones_cd','Insertar CCD Vagones Cargados/Descargados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (277,60,'change_ccd_vagones_cd','Editar CCD Vagones Cargados/Descargados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (278,60,'delete_ccd_vagones_cd','Eliminar CCD Vagones Cargados/Descargados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (279,60,'view_ccd_vagones_cd','Visualizar CCD Vagones Cargados/Descargados');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (280,61,'add_ccd_producto','Insertar Producto CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (281,61,'change_ccd_producto','Editar Producto CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (282,61,'delete_ccd_producto','Eliminar Producto CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (283,61,'view_ccd_producto','Visualizar Producto CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (284,66,'add_ccd_casillas_productos','Insertar CCD Casillas por Centro Carga/Descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (285,66,'change_ccd_casillas_productos','Editar CCD Casillas por Centro Carga/Descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (286,66,'delete_ccd_casillas_productos','Eliminar CCD Casillas por Centro Carga/Descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (287,66,'view_ccd_casillas_productos','Visualizar CCD Casillas por Centro Carga/Descarga');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (288,63,'puede_rechazar_informe','Puede rechazar informes CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (289,63,'puede_aprobar_informe','Puede aprobar informes CCD');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (290,63,'puede_cambiar_a_listo','Puede cambiar el estado del informe CCD a listo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (291,69,'add_gemar_parte_hecho_extraordinario','Insertar Parte de hecho extraordinario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (292,69,'change_gemar_parte_hecho_extraordinario','Editar Parte de hecho extraordinario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (293,69,'delete_gemar_parte_hecho_extraordinario','Eliminar Parte de hecho extraordinario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (294,69,'view_gemar_parte_hecho_extraordinario','Visualizar Parte de hecho extraordinario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (295,69,'gemar_puede_rechazar_informe','Puede rechazar hechos extraordinarios');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (296,69,'gemar_puede_aprobar_informe','Puede aprobar hechos extraordinarios');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (297,69,'gemar_puede_cambiar_a_listo','Puede cambiar el estado del informe a listo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (298,70,'add_gemar_hecho_extraordinario','Insertar Hecho extraordinario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (299,70,'change_gemar_hecho_extraordinario','Editar Hecho extraordinario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (300,70,'delete_gemar_hecho_extraordinario','Eliminar Hecho extraordinario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (301,70,'view_gemar_hecho_extraordinario','Visualizar Hecho extraordinario');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (302,69,'gemar_puede_cambiar_informe_a_listo','Puede cambiar el estado del informe de hechos extraordinarios a listo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (303,71,'add_gemar_parte_programacion_maniobras','Insertar Parte de programación de maniobras');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (304,71,'change_gemar_parte_programacion_maniobras','Editar Parte de programación de maniobras');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (305,71,'delete_gemar_parte_programacion_maniobras','Eliminar Parte de programación de maniobras');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (306,71,'view_gemar_parte_programacion_maniobras','Visualizar Parte de programación de maniobras');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (307,71,'gemar_puede_rechazar_informe_programacion_maniobra','Puede rechazar partes de programación de maniobra');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (308,71,'gemar_puede_aprobar_informe_programacion_maniobra','Puede aprobar partes de programación de maniobra');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (309,71,'gemar_puede_cambiar__informe_programacion_maniobra_a_listo','Puede cambiar el estado del informe de programación de maniobra a listo');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (310,72,'add_gemar_programacion_maniobras','Insertar Programación de maniobras');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (311,72,'change_gemar_programacion_maniobras','Editar Programación de maniobras');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (312,72,'delete_gemar_programacion_maniobras','Eliminar Programación de maniobras');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (313,72,'view_gemar_programacion_maniobras','Visualizar Programación de maniobras');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (314,72,'gemar_puede_rechazar_informe_programacion_maniobra','Puede rechazar partes de programación de maniobra');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (315,72,'gemar_puede_aprobar_informe_programacion_maniobra','Puede aprobar partes de programación de maniobra');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (316,72,'gemar_puede_cambiar__informe_programacion_maniobra_a_listo','Puede cambiar el estado del informe de programación de maniobra a listo');
INSERT INTO "auth_group" ("id","name") VALUES (1,'Admin');
INSERT INTO "auth_group" ("id","name") VALUES (2,'Consultor');
INSERT INTO "auth_group" ("id","name") VALUES (3,'AdminNomencladores');
INSERT INTO "auth_group" ("id","name") VALUES (4,'OperadorUFC');
INSERT INTO "auth_group" ("id","name") VALUES (5,'VisualizadorNomencladores');
INSERT INTO "auth_group" ("id","name") VALUES (6,'VisualizadorUFC');
INSERT INTO "auth_group" ("id","name") VALUES (7,'RevisorUFC');
INSERT INTO "auth_group" ("id","name") VALUES (8,'AdminUFC');
INSERT INTO "auth_group" ("id","name") VALUES (9,'AdminGEMAR');
INSERT INTO "auth_group" ("id","name") VALUES (10,'VisualizadorGEMAR');
INSERT INTO "auth_group" ("id","name") VALUES (11,'RevisorGEMAR');
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (1,1,1);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (2,2,2);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (7,1,3);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (8,1,4);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (11,4,3);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (12,4,4);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (13,1,2);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (14,1,7);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (15,5,7);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (16,6,1);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (17,6,2);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (18,6,3);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (19,6,4);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (20,6,5);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (21,6,6);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (22,6,7);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (24,9,4);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (25,9,6);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (26,10,7);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (27,9,5);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (28,11,5);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (29,11,6);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (30,11,7);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (31,12,7);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (32,13,4);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (33,1,8);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (34,1,9);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (35,1,11);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (9,6,1);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (10,6,2);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (11,6,3);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (12,6,4);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (13,6,5);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (14,6,6);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (15,6,7);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (16,6,8);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (17,6,9);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (18,6,10);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (19,6,11);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (20,6,12);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (21,6,13);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (22,6,14);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (23,6,15);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (24,6,16);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (25,6,17);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (26,6,18);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (27,6,19);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (28,6,20);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (29,6,21);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (30,6,22);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (31,6,23);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (32,6,24);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (33,6,25);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (34,6,26);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (35,6,27);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (36,6,28);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (37,6,29);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (38,6,30);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (39,6,31);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (40,6,32);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (41,6,33);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (42,6,34);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (43,6,35);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (44,6,36);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (45,6,37);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (46,6,38);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (47,6,39);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (48,6,40);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (49,6,41);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (50,6,42);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (51,6,43);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (52,6,44);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (53,6,45);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (54,6,46);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (55,6,47);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (56,6,48);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (57,6,49);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (58,6,50);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (59,6,51);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (60,6,52);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (61,6,53);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (62,6,54);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (63,6,55);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (64,6,56);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (65,6,57);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (66,6,58);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (67,6,59);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (68,6,60);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (69,6,61);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (70,6,62);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (71,6,63);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (72,6,64);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (73,6,65);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (74,6,66);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (75,6,67);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (76,6,68);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (77,6,69);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (78,6,70);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (79,6,71);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (80,6,72);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (81,6,73);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (82,6,74);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (83,6,75);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (84,6,76);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (85,6,77);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (86,6,78);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (87,6,79);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (88,6,80);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (89,6,81);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (90,6,82);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (91,6,83);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (92,6,84);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (93,6,85);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (94,6,86);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (95,6,87);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (96,6,88);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (97,6,89);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (98,6,90);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (99,6,91);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (100,6,92);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (101,6,93);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (102,6,94);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (103,6,95);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (104,6,96);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (105,6,97);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (106,6,98);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (107,6,99);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (108,6,100);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (109,6,101);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (110,6,102);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (111,6,103);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (112,6,104);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (113,6,105);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (114,6,106);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (115,6,107);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (116,6,108);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (117,6,109);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (118,6,110);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (119,6,111);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (120,6,112);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (121,6,113);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (122,6,114);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (123,6,115);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (124,6,116);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (125,6,117);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (126,6,118);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (127,6,119);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (128,6,120);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (129,6,121);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (130,6,122);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (131,6,123);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (132,6,124);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (133,6,125);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (134,6,126);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (135,6,127);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (136,6,128);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (137,6,129);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (138,6,130);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (139,6,131);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (140,6,132);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (141,6,133);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (142,6,134);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (143,6,135);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (144,6,136);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (145,6,137);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (146,6,138);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (147,6,139);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (148,6,140);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (149,6,141);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (150,6,142);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (151,6,143);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (152,6,144);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (153,6,145);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (154,6,146);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (155,6,147);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (156,6,148);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (157,6,149);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (158,6,150);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (159,6,151);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (160,6,152);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (161,6,153);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (162,6,154);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (163,6,155);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (164,6,156);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (165,6,157);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (166,6,158);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (167,6,159);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (168,6,160);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (169,6,161);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (170,6,162);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (171,6,163);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (172,6,164);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (173,6,165);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (174,6,166);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (175,6,167);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (176,6,168);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (177,6,169);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (178,6,170);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (179,6,171);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (180,6,172);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (181,6,173);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (182,6,174);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (183,6,175);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (184,6,176);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (185,6,177);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (186,6,178);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (187,6,179);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (188,6,180);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (189,6,181);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (190,6,182);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (191,6,183);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (192,6,184);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (193,6,185);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (194,6,186);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (195,6,187);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (196,6,188);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (197,6,189);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (198,6,190);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (199,6,191);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (200,6,192);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (201,6,193);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (202,6,194);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (203,6,195);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (204,6,196);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (205,6,197);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (206,6,198);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (207,6,199);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (208,6,200);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (209,6,201);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (210,6,202);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (211,6,203);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (212,6,204);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (213,6,205);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (214,6,206);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (215,6,207);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (216,6,208);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (217,6,209);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (218,6,210);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (219,6,211);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (220,6,212);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (221,6,213);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (222,6,214);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (223,6,215);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (224,6,216);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (225,6,217);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (226,6,218);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (227,6,219);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (228,6,220);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (229,6,221);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (230,6,222);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (231,6,223);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (232,6,224);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (233,6,225);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (234,6,226);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (235,6,227);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (236,6,228);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (237,6,229);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (238,6,230);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (239,6,231);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (240,6,232);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (241,6,233);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (242,6,234);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (243,6,235);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (244,6,236);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (245,6,237);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (246,6,238);
INSERT INTO "Administracion_customuser_user_permissions" ("id","customuser_id","permission_id") VALUES (247,6,239);
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
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (1,'pbkdf2_sha256$870000$ouawk2HDXoMOyC27gzEzP7$85u6pXiLq0gcS52ALx9C3apwkjrLkC8ckLeQIu1h44w=','2025-07-31 14:40:48.612203',1,'admin','Administrador','Primero','admin@desoft.cu',1,1,'2025-02-24 18:55:23',1,1,'ufc');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (2,'pbkdf2_sha256$870000$w1qQtbjR1E9CkncsWJs36g$OVi4keqRQX8ZyfCCNo+u621k7s28n6PqAZvtbxS2nhc=','2025-02-24 22:37:15.603477',0,'alain','Alain','Dellon Mask','alain@desoft.cu',0,1,'2025-02-24 19:13:22.712464',2,1,'operador');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (3,'pbkdf2_sha256$870000$r2ZPhSKJlCRftnvX0M68rA$AYmqaupSq7OUChmVVLIvvKS0snuj2HIiu6aZGPbpkUE=','2025-03-13 13:41:50.584033',0,'carlos','Carlos','Gonza','carlosr301101@gmail.com',0,1,'2025-03-11 13:18:54.449569',2,7,'ufc');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (4,'pbkdf2_sha256$870000$VUDkbzd2NRkZWFZ8ebGu7D$8de8M+Qf4oJHhhuO6qz1OyCAGrhKQ4BpX6Bti3xJbGY=','2025-04-27 02:13:37.774451',0,'juanito','juanito','GLEZ','juanito@gmail.com',0,1,'2025-03-11 13:23:18',1,7,'operador');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (5,'pbkdf2_sha256$870000$VgyLjwWWlSiFiBa0qOeRsL$DTWfUsK06e2AkWL7ysnmTjA8GvXOHfyx996+5+N+f50=',NULL,0,'adsdad','Csda','Asdad','asdad@fasffa.com',0,1,'2025-05-16 10:40:34.456057',3,1,'ufc');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (6,'pbkdf2_sha256$870000$hDTs6R1xTOP0wQWhBq9yBS$0CAIM0LnWhB9NV920sYjJgi1DwFfLgiSrzLYMLt18Fc=','2025-06-03 13:22:53.277479',0,'pseudo','Carlos','González Alejo','trikiruski@gmail.com',0,1,'2025-05-20 10:00:43',1,7,'admin');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (7,'pbkdf2_sha256$870000$oOUXdb6bF5xooKmTJk2xNW$BA8FW4qRV4DBaj6BnUrf8uXSh+wpqD7XcHHsolpy1EM=','2025-06-01 01:45:17.963016',0,'pepe','Pepe','Antonio','pepe@gmail.com',0,1,'2025-06-01 01:39:16.137508',2,7,'operador');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (9,'pbkdf2_sha256$870000$xycj6Qs9h8Fi1OYjHlPKQy$DHtOdabk9WLzN/2RO70rOfpDU+R2o6oet5UO1S9tDlU=','2025-07-21 15:15:45.098448',0,'solrac','Solrac','Solrac','solrac@gmail.com',0,1,'2025-07-19 23:37:01',2,1,'operador');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (10,'pbkdf2_sha256$870000$xiImwaEeCsIZWR7Ar1wMST$8DUBVL1m0JS86Z6FxmDbRDAw+a/La6RM3yPA2jJcPE0=','2025-07-20 19:58:18.472018',0,'revisor','Revisor','Revisor','revisor@gmail.com',0,1,'2025-07-20 00:22:42.067949',1,7,'operador');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (11,'pbkdf2_sha256$870000$hfvYLYek1IaygvEYxzEw0E$SwPRb3YljBvHXuSp5SIS8iIGc+oVAmfWiTo1uHgI0BI=',NULL,0,'test','Test','Test','test@gmail.com',0,1,'2025-07-21 22:09:00.483752',2,7,'operador');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (12,'pbkdf2_sha256$870000$si2jf71JbQtbWzQ1jmktit$5zS460VYD3me1KYLiNA6D5zD979l8VJH5kXOtX2YpA8=','2025-07-23 00:55:02.076278',0,'revisorSQL','Revisorsql','Revisorsql','revisorsql@gmail.com',0,1,'2025-07-23 00:52:58',2,6,'ufc');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (13,'pbkdf2_sha256$870000$Sp5rtl5QvsH4FbhI6yHTZ6$0CdV7ZvBs1MukhpIKl2JwHBpeGsIAmkdCwrCR+VAHeg=','2025-07-23 00:58:49.384043',0,'operadorSQL','Operadorsql','Operador','operadorsql@gmail.com',0,1,'2025-07-23 00:57:59.027946',2,7,'ufc');
INSERT INTO "ufc_producto_ufc" ("id","cantidad","estado","contiene","producto_id","tipo_embalaje_id","unidad_medida_id","tipo_equipo_id") VALUES (1,100,'lleno','alimentos',4,1,3,NULL);
INSERT INTO "ufc_producto_ufc" ("id","cantidad","estado","contiene","producto_id","tipo_embalaje_id","unidad_medida_id","tipo_equipo_id") VALUES (2,12,'lleno','alimentos',8,3,3,NULL);
INSERT INTO "ufc_producto_ufc" ("id","cantidad","estado","contiene","producto_id","tipo_embalaje_id","unidad_medida_id","tipo_equipo_id") VALUES (3,20,'lleno','alimentos',6,3,2,NULL);
INSERT INTO "ufc_producto_ufc" ("id","cantidad","estado","contiene","producto_id","tipo_embalaje_id","unidad_medida_id","tipo_equipo_id") VALUES (4,10,'lleno','alimentos',1,3,3,NULL);
INSERT INTO "ufc_producto_ufc" ("id","cantidad","estado","contiene","producto_id","tipo_embalaje_id","unidad_medida_id","tipo_equipo_id") VALUES (5,134,'lleno','alimentos',1,4,3,6);
INSERT INTO "ufc_vagon_cargado_descargado_registros_vagones" ("id","vagon_cargado_descargado_id","registro_vagones_cargados_id") VALUES (90,41,90);
INSERT INTO "ufc_vagones_productos_producto" ("id","vagones_productos_id","producto_ufc_id") VALUES (39,8,3);
INSERT INTO "ufc_vagones_productos_producto" ("id","vagones_productos_id","producto_ufc_id") VALUES (40,8,4);
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (2,'LOCO0073','oriente','Combustible','Combustible negro',11233,4,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (4,'LOCOMB001','oriente','Combustible','Combustible negro',2,3,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (11,'AAAAFFFF','centro','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (12,'ADqq11','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (15,'ARRQQQ','centro','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (16,'AQWE','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (17,'HASFF','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (18,'HAV1','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (19,'HAV2','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (20,'HAV3','occidente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (21,'STG1','oriente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (22,'STG2','oriente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (23,'STG3','oriente','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (24,'CAV1','centro','Contenedores','Combustible blanco',1234,6,'Asignado al estado Pendiente a Arrastre');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (25,'CAV2','centro','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (26,'CAV3','centro','Contenedores','Combustible blanco',1234,6,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (27,'VCL1','centro','Otros','-',12444,8,'Disponible');
INSERT INTO "nomencladores_nom_equipo_ferroviario" ("id","numero_identificacion","territorio","tipo_carga","tipo_combustible","peso_maximo","tipo_equipo_id","estado_actual") VALUES (28,'VCL2','centro','Contenedor','Combustible blanco',1234,8,'Disponible');
INSERT INTO "ufc_ufc_informe_operativo" ("id","fecha_operacion","fecha_actual","plan_mensual_total","plan_diario_total_vagones_cargados","real_total_vagones_cargados","total_vagones_situados","plan_total_acumulado_actual","real_total_acumulado_actual","estado_parte","aprobado_por_id","creado_por_id","provincia_id","entidad_id") VALUES (73,'2025-06-27 00:40:54.126614','2025-06-27 00:40:54.126638',0,0,0,0,0,0,'Creado',NULL,1,1,1);
INSERT INTO "ufc_ufc_informe_operativo" ("id","fecha_operacion","fecha_actual","plan_mensual_total","plan_diario_total_vagones_cargados","real_total_vagones_cargados","total_vagones_situados","plan_total_acumulado_actual","real_total_acumulado_actual","estado_parte","aprobado_por_id","creado_por_id","provincia_id","entidad_id") VALUES (74,'2025-06-28 19:51:02.329393','2025-07-20 20:03:48.344891',0,0,0,0,0,0,'Rechazado',10,1,1,1);
INSERT INTO "ufc_ufc_informe_operativo" ("id","fecha_operacion","fecha_actual","plan_mensual_total","plan_diario_total_vagones_cargados","real_total_vagones_cargados","total_vagones_situados","plan_total_acumulado_actual","real_total_acumulado_actual","estado_parte","aprobado_por_id","creado_por_id","provincia_id","entidad_id") VALUES (76,'2025-07-03 09:09:22.421191','2025-07-03 09:34:17.733061',0,0,0,0,0,0,'Aprobado',1,1,1,1);
INSERT INTO "ufc_ufc_informe_operativo" ("id","fecha_operacion","fecha_actual","plan_mensual_total","plan_diario_total_vagones_cargados","real_total_vagones_cargados","total_vagones_situados","plan_total_acumulado_actual","real_total_acumulado_actual","estado_parte","aprobado_por_id","creado_por_id","provincia_id","entidad_id") VALUES (78,'2025-07-18 11:07:52.259224','2025-07-28 17:26:36.352521',0,12,1,0,0,0,'Rechazado',1,1,1,1);
INSERT INTO "ufc_ufc_informe_operativo" ("id","fecha_operacion","fecha_actual","plan_mensual_total","plan_diario_total_vagones_cargados","real_total_vagones_cargados","total_vagones_situados","plan_total_acumulado_actual","real_total_acumulado_actual","estado_parte","aprobado_por_id","creado_por_id","provincia_id","entidad_id") VALUES (98,'2025-07-20 19:09:50.272120','2025-07-20 20:02:59.924234',0,0,0,0,0,0,'Aprobado',10,9,1,1);
INSERT INTO "ufc_ufc_informe_operativo" ("id","fecha_operacion","fecha_actual","plan_mensual_total","plan_diario_total_vagones_cargados","real_total_vagones_cargados","total_vagones_situados","plan_total_acumulado_actual","real_total_acumulado_actual","estado_parte","aprobado_por_id","creado_por_id","provincia_id","entidad_id") VALUES (99,'2025-07-21 15:15:57.951065','2025-07-21 15:15:57.951084',0,0,0,0,0,0,'Creado',NULL,9,1,1);
INSERT INTO "ufc_ufc_informe_operativo" ("id","fecha_operacion","fecha_actual","plan_mensual_total","plan_diario_total_vagones_cargados","real_total_vagones_cargados","total_vagones_situados","plan_total_acumulado_actual","real_total_acumulado_actual","estado_parte","aprobado_por_id","creado_por_id","provincia_id","entidad_id") VALUES (101,'2025-07-23 16:59:34.387221','2025-07-23 16:59:34.387244',0,0,0,0,0,0,'Creado',NULL,1,1,1);
INSERT INTO "ufc_vagon_cargado_descargado" ("id","tipo_origen","origen","estado","operacion","plan_diario_carga_descarga","real_carga_descarga","tipo_destino","destino","causas_incumplimiento","tipo_equipo_ferroviario_id","fecha","informe_operativo_id","producto_id") VALUES (41,'puerto','Puerto Unos','vacio','carga',12,1,'puerto','Puerto dos','asdad',6,'2025-07-18 16:23:03.061136',78,5);
INSERT INTO "ufc_vagones_productos" ("id","tipo_origen","origen","tipo_producto","tipo_combustible","plan_mensual","plan_dia","vagones_situados","vagones_cargados","plan_aseguramiento_proximos_dias","observaciones","plan_anual","plan_acumulado_dia_anterior","real_acumulado_dia_anterior","tipo_equipo_ferroviario_id","fecha","plan_acumulado_actual","plan_acumulado_anual","real_acumulado_actual","real_acumulado_anual","informe_operativo_id") VALUES (8,'ac_ccd','Cuba Ron SA','producto','',12,132,3,2,2,'asdadwd',0,0,0,NULL,'2025-05-28 23:27:56.086735',132,13158,2,236,NULL);
INSERT INTO "ufc_arrastres" ("id","tipo_origen","origen","estado","cantidad_vagones","tipo_destino","destino","fecha","informe_operativo_id","tipo_equipo_id","observaciones","operacion","producto_id") VALUES (15,'puerto','Puerto Unos','cargado','1','ac_ccd','Acceso comercial uno','2025-07-21 16:13:36.680739',99,6,'QEQTGQT','descarga',5);
INSERT INTO "ufc_por_situar" ("id","tipo_origen","origen","estado","operacion","por_situar","observaciones","fecha","informe_operativo_id","tipo_equipo_id","producto_id") VALUES (38,'puerto','Puerto Unos','cargado','descarga','1','asdada','2025-06-27 00:41:40.691020',73,6,NULL);
INSERT INTO "ufc_por_situar" ("id","tipo_origen","origen","estado","operacion","por_situar","observaciones","fecha","informe_operativo_id","tipo_equipo_id","producto_id") VALUES (39,'puerto','Puerto dos','vacio','carga','1','adsdafaf','2025-06-28 19:56:06.849724',74,6,5);
INSERT INTO "ufc_por_situar" ("id","tipo_origen","origen","estado","operacion","por_situar","observaciones","fecha","informe_operativo_id","tipo_equipo_id","producto_id") VALUES (40,'puerto','Puerto Unos','cargado','descarga','1','','2025-07-03 09:16:43.247220',76,6,5);
INSERT INTO "ufc_por_situar" ("id","tipo_origen","origen","estado","operacion","por_situar","observaciones","fecha","informe_operativo_id","tipo_equipo_id","producto_id") VALUES (43,'puerto','Puerto Unos','cargado','descarga','1','cacsaca','2025-07-20 19:58:04.525520',98,6,5);
INSERT INTO "ufc_situado_carga_descarga" ("id","tipo_origen","origen","estado","operacion","situados","pendiente_proximo_dia","observaciones","fecha","informe_operativo_id","tipo_equipo_id","producto_id") VALUES (14,'ac_ccd','Cuba Ron SA','cargado','carga','1','10','adsda','2025-05-22 13:52:38.534583',NULL,6,NULL);
INSERT INTO "ufc_situado_carga_descarga" ("id","tipo_origen","origen","estado","operacion","situados","pendiente_proximo_dia","observaciones","fecha","informe_operativo_id","tipo_equipo_id","producto_id") VALUES (15,'puerto','Puerto Unos','cargado','descarga','1','12','adsda','2025-05-25 18:18:18.913036',NULL,6,NULL);
INSERT INTO "ufc_situado_carga_descarga" ("id","tipo_origen","origen","estado","operacion","situados","pendiente_proximo_dia","observaciones","fecha","informe_operativo_id","tipo_equipo_id","producto_id") VALUES (16,'ac_ccd','Acceso comercial uno','vacio','carga','1','123','adsda','2025-05-25 18:25:50.915492',NULL,6,NULL);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (94,2,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (95,1,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (96,1,25);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (97,1,26);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (100,1,26);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (101,1,23);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (102,12,26);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (103,12,22);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (104,123,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (105,1,28);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (106,1,28);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (107,1,27);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (108,1,26);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (109,1,26);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (110,1,27);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (111,1,27);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (112,1,26);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (113,1,26);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (114,1,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (115,1,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (116,1,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (117,1,21);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (118,1,21);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (119,1,22);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (120,1,22);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (121,1,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (122,1,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (123,1,24);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (124,120,26);
INSERT INTO "ufc_vagones_dias" ("id","cant_dias","equipo_ferroviario_id") VALUES (125,140,28);
INSERT INTO "ufc_arrastres_equipo_vagon" ("id","arrastres_id","vagones_dias_id") VALUES (22,15,123);
INSERT INTO "ufc_por_situar_equipo_vagon" ("id","por_situar_id","vagones_dias_id") VALUES (52,38,95);
INSERT INTO "ufc_por_situar_equipo_vagon" ("id","por_situar_id","vagones_dias_id") VALUES (53,39,96);
INSERT INTO "ufc_por_situar_equipo_vagon" ("id","por_situar_id","vagones_dias_id") VALUES (54,40,97);
INSERT INTO "ufc_por_situar_equipo_vagon" ("id","por_situar_id","vagones_dias_id") VALUES (57,43,114);
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (62,'2025-05-20','ac_ccd','Cuba Ron SA','2025-05-20','asdafafafaf','HASFF');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (63,'2025-05-21','ac_ccd','CCD Uno','2025-05-21','dadada','AAAAFFFF');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (67,'2025-05-22','ac_ccd','Cuba Ron SA','2025-05-22','daasdad','ARRQQQ');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (68,'2025-05-22','ac_ccd','Cuba Ron SA','2025-05-22','DSADASD','AQWE');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (69,'2025-05-22','ac_ccd','Cuba Ron SA','2025-05-22','SDADA','ADSFF');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (71,'2025-05-22','ac_ccd','Acceso comercial uno','2025-05-22','ASDASDA','ADqq11');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (72,'2025-05-26','ac_ccd','Cuba Ron SA','2025-05-26','dasdad','ADqq11');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (78,'2025-05-29','ac_ccd','Cuba Ron SA','2025-05-29','asda','ARRQQQ');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (79,'2025-05-29','ac_ccd','CCD Uno','2025-05-29','asdadad','HASFF');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (81,'2025-05-30','ac_ccd','Cuba Ron SA','2025-05-30','sadad','HASFF');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (82,'2025-05-30','ac_ccd','Cuba Ron SA','2025-05-30','awsdaaw','HAV2');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (83,'2025-06-01','ac_ccd','Acceso comercial uno','2025-06-01','adadad','STG1');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (84,'2025-06-01','ac_ccd','CCD Uno','2025-06-01','asdadwdd','STG3');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (85,'2025-06-03','ac_ccd','Cuba Ron SA','2025-06-03','dadasd','AQWE');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (86,'2025-06-11','ac_ccd','Cuba Ron SA','2025-06-11','asdad','STG1');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (90,'2025-07-18','ac_ccd','Cuba Ron SA','2025-07-18','adsada','CAV2');
INSERT INTO "ufc_registro_vagones_cargados" ("id","fecha_despacho","tipo_origen","origen","fecha_llegada","observaciones","no_id") VALUES (91,'2025-07-23','ac_ccd','Cuba Ron SA','2025-07-23','aDAD','CAV2');
INSERT INTO "ufc_ccd_vagones_cd_equipo_vagon" ("id","ccd_vagones_cd_id","ccd_registro_vagones_cd_id") VALUES (5,1,6);
INSERT INTO "ufc_ccd_producto" ("id","cantidad","estado","contiene","tipo_embalaje_id","tipo_equipo_id","unidad_medida_id","producto_id") VALUES (2,1233,'lleno','alimentos',3,6,3,1);
INSERT INTO "ufc_ccd_producto" ("id","cantidad","estado","contiene","tipo_embalaje_id","tipo_equipo_id","unidad_medida_id","producto_id") VALUES (3,333,'lleno','alimentos',3,6,3,1);
INSERT INTO "ufc_ccd_producto" ("id","cantidad","estado","contiene","tipo_embalaje_id","tipo_equipo_id","unidad_medida_id","producto_id") VALUES (4,30,'lleno','alimentos',3,6,3,1);
INSERT INTO "ufc_ccd_producto" ("id","cantidad","estado","contiene","tipo_embalaje_id","tipo_equipo_id","unidad_medida_id","producto_id") VALUES (7,12,'lleno','alimentos',3,3,1,1);
INSERT INTO "ufc_ccd_producto" ("id","cantidad","estado","contiene","tipo_embalaje_id","tipo_equipo_id","unidad_medida_id","producto_id") VALUES (8,1111,'lleno','alimentos',3,6,3,1);
INSERT INTO "ufc_ccd_producto" ("id","cantidad","estado","contiene","tipo_embalaje_id","tipo_equipo_id","unidad_medida_id","producto_id") VALUES (10,202,'lleno','alimentos',3,6,3,1);
INSERT INTO "ufc_ccd_registro_vagones_cd" ("id","no_id","fecha_despacho","tipo_origen","origen","fecha_llegada","incidencias","observaciones","equipo_ferroviario_id") VALUES (1,'CAV3','2025-07-10','municipio','Acceso 1','2025-07-10',1,'{"faltante": "No hay faltante"}',26);
INSERT INTO "ufc_ccd_registro_vagones_cd" ("id","no_id","fecha_despacho","tipo_origen","origen","fecha_llegada","incidencias","observaciones","equipo_ferroviario_id") VALUES (2,NULL,NULL,NULL,NULL,NULL,1,NULL,26);
INSERT INTO "ufc_ccd_registro_vagones_cd" ("id","no_id","fecha_despacho","tipo_origen","origen","fecha_llegada","incidencias","observaciones","equipo_ferroviario_id") VALUES (3,NULL,'2020-10-01','municipio','CCD uno','2019-11-01',1,'"adsafafasf"',25);
INSERT INTO "ufc_ccd_registro_vagones_cd" ("id","no_id","fecha_despacho","tipo_origen","origen","fecha_llegada","incidencias","observaciones","equipo_ferroviario_id") VALUES (4,'41414','2020-10-01','municipio','CCD uno','2019-11-01',1,'"adsafafasf"',25);
INSERT INTO "ufc_ccd_registro_vagones_cd" ("id","no_id","fecha_despacho","tipo_origen","origen","fecha_llegada","incidencias","observaciones","equipo_ferroviario_id") VALUES (5,'414','2020-10-01','municipio','CCD uno','2019-11-01',1,'{"faltante": 120, "peso_destino": 12000}',25);
INSERT INTO "ufc_ccd_registro_vagones_cd" ("id","no_id","fecha_despacho","tipo_origen","origen","fecha_llegada","incidencias","observaciones","equipo_ferroviario_id") VALUES (6,'CABV222','2025-07-22','municipio','ACC','2025-07-22',1,'{"faltante": 120}',26);
INSERT INTO "ufc_ccd_casillas_productos" ("id","acceso_id","total_ayer","entro_hoy","plan_carga","plan_descarga","recepcion","reexpedciones","informe_ccd_id","total_general") VALUES (2,1,12,15,5,3,2,1,1,27);
INSERT INTO "ufc_ccd_casillas_productos" ("id","acceso_id","total_ayer","entro_hoy","plan_carga","plan_descarga","recepcion","reexpedciones","informe_ccd_id","total_general") VALUES (3,1,0,10,0,10,0,0,1,10);
INSERT INTO "ufc_ufc_informe_ccd" ("id","fecha_operacion","fecha_actual","comentarios","aprobado_por_id","creado_por_id","entidad_id","provincia_id","estado_parte") VALUES (1,'2025-07-22 01:09:32.046391','2025-07-22 01:09:52.462692','Este parte es PRIMERO',NULL,9,1,1,'creado');
INSERT INTO "ufc_ccd_vagones_cd" ("fecha_registro","id","acceso_id","causa_incumplimiento","estado","informe_ccd_id","producto_id","tipo_equipo_id","operacion","real_carga_descarga") VALUES ('2025-07-22',1,1,'adada','cargado',1,2,8,'descarga',12.0);
INSERT INTO "gemar_gemar_parte_hecho_extraordinario" ("id","fecha_actual","estado_parte","aprobado_por_id","creado_por_id","entidad_id","provincia_id","fecha_operacion") VALUES (14,'2025-07-30 11:17:24.860485','Creado',NULL,1,1,1,'2025-07-30 00:00:00');
INSERT INTO "gemar_gemar_parte_hecho_extraordinario" ("id","fecha_actual","estado_parte","aprobado_por_id","creado_por_id","entidad_id","provincia_id","fecha_operacion") VALUES (15,'2025-07-31 16:59:42.505895','Aprobado',1,1,1,1,'2025-07-31 00:00:00');
INSERT INTO "gemar_gemar_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","informado","tipo_involucrado","involucrado","tipo_origen","origen","destino","tipo_diferencia","cantidad_diferencia","valor_diferencia","averia","kg_averia","cantidad_averia","valor_averia","descripcion_hecho","embalaje_id","garante_id","incidencia_involucrada_id","producto_involucrado_id","unidad_medida_id","parte_hecho_extraordinario_id","kg_diferencia") VALUES (6,'2025-07-30 12:13:03.460657','2025-07-30 12:13:03.460683','Informado del dia 24','puerto','Puerto Unos','puerto','Puerto Unos','Aquel lugar','sobrante',NULL,NULL,'no',NULL,NULL,NULL,'qwerty',4,1,1,3,3,14,NULL);
INSERT INTO "gemar_gemar_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","informado","tipo_involucrado","involucrado","tipo_origen","origen","destino","tipo_diferencia","cantidad_diferencia","valor_diferencia","averia","kg_averia","cantidad_averia","valor_averia","descripcion_hecho","embalaje_id","garante_id","incidencia_involucrada_id","producto_involucrado_id","unidad_medida_id","parte_hecho_extraordinario_id","kg_diferencia") VALUES (7,'2025-07-31 15:18:46.849422','2025-07-31 15:18:46.849451','we32','puerto','Puerto Unos','entidad','Acceso comercial uno','Jatibonico','sobrante',0.05,233.98,'no',NULL,NULL,NULL,'wer',3,1,1,5,2,15,34.23);
INSERT INTO "gemar_gemar_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","informado","tipo_involucrado","involucrado","tipo_origen","origen","destino","tipo_diferencia","cantidad_diferencia","valor_diferencia","averia","kg_averia","cantidad_averia","valor_averia","descripcion_hecho","embalaje_id","garante_id","incidencia_involucrada_id","producto_involucrado_id","unidad_medida_id","parte_hecho_extraordinario_id","kg_diferencia") VALUES (8,'2025-07-31 15:44:31.820908','2025-07-31 15:44:31.820939','weQW','puerto','Puerto Unos','entidad','Acceso comercial uno','Jatibonico','sobrante',NULL,NULL,'no',NULL,NULL,NULL,'QWERQWR',3,6,1,1,3,15,3.43534534);
INSERT INTO "gemar_gemar_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","informado","tipo_involucrado","involucrado","tipo_origen","origen","destino","tipo_diferencia","cantidad_diferencia","valor_diferencia","averia","kg_averia","cantidad_averia","valor_averia","descripcion_hecho","embalaje_id","garante_id","incidencia_involucrada_id","producto_involucrado_id","unidad_medida_id","parte_hecho_extraordinario_id","kg_diferencia") VALUES (9,'2025-07-31 16:12:23.836826','2025-07-31 16:32:04.041868','Mala talla','entidad','Acceso comercial uno','entidad','Cuba Ron SA','Jatibonico','sobrante',43,65.98,'si',23.34,11100,76,'Unos datos',3,6,1,5,2,15,33114.34);
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
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "Administracion_customuser_groups_customuser_id_group_id_5e19dcb9_uniq" ON "Administracion_customuser_groups" (
	"customuser_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "Administracion_customuser_groups_customuser_id_eb3c3f33" ON "Administracion_customuser_groups" (
	"customuser_id"
);
CREATE INDEX IF NOT EXISTS "Administracion_customuser_groups_group_id_9e3b03cc" ON "Administracion_customuser_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "Administracion_customuser_user_permissions_customuser_id_permission_id_e9cccd3f_uniq" ON "Administracion_customuser_user_permissions" (
	"customuser_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "Administracion_customuser_user_permissions_customuser_id_0693f36f" ON "Administracion_customuser_user_permissions" (
	"customuser_id"
);
CREATE INDEX IF NOT EXISTS "Administracion_customuser_user_permissions_permission_id_519c4aa1" ON "Administracion_customuser_user_permissions" (
	"permission_id"
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
CREATE INDEX IF NOT EXISTS "Administracion_customuser_cargo_id_5a2dcb16" ON "Administracion_customuser" (
	"cargo_id"
);
CREATE INDEX IF NOT EXISTS "Administracion_customuser_entidad_id_93ab5786" ON "Administracion_customuser" (
	"entidad_id"
);
CREATE INDEX IF NOT EXISTS "ufc_producto_ufc_producto_id_abb0af13" ON "ufc_producto_ufc" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_producto_ufc_tipo_embalaje_id_592fae07" ON "ufc_producto_ufc" (
	"tipo_embalaje_id"
);
CREATE INDEX IF NOT EXISTS "ufc_producto_ufc_unidad_medida_id_65b30885" ON "ufc_producto_ufc" (
	"unidad_medida_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_registros_vagones_vagon_cargado_descargado_id_registro_vagones_cargados_id_124792b4_uniq" ON "ufc_vagon_cargado_descargado_registros_vagones" (
	"vagon_cargado_descargado_id",
	"registro_vagones_cargados_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_registros_vagones_vagon_cargado_descargado_id_0ee51755" ON "ufc_vagon_cargado_descargado_registros_vagones" (
	"vagon_cargado_descargado_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_registros_vagones_registro_vagones_cargados_id_704f3f2f" ON "ufc_vagon_cargado_descargado_registros_vagones" (
	"registro_vagones_cargados_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_vagones_productos_producto_vagones_productos_id_producto_ufc_id_436a30e2_uniq" ON "ufc_vagones_productos_producto" (
	"vagones_productos_id",
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagones_productos_producto_vagones_productos_id_98260b87" ON "ufc_vagones_productos_producto" (
	"vagones_productos_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagones_productos_producto_producto_ufc_id_d9ca2331" ON "ufc_vagones_productos_producto" (
	"producto_ufc_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "nomencladores_nom_equipo_ferroviario_tipo_equipo_id_numero_identificacion_territorio_94bcad4a_uniq" ON "nomencladores_nom_equipo_ferroviario" (
	"tipo_equipo_id",
	"numero_identificacion",
	"territorio"
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_equipo_ferroviario_tipo_equipo_id_1a10f23d" ON "nomencladores_nom_equipo_ferroviario" (
	"tipo_equipo_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_en_trenes_equipo_vagon_en_trenes_id_nom_equipo_ferroviario_id_1947c747_uniq" ON "ufc_en_trenes_equipo_vagon" (
	"en_trenes_id",
	"nom_equipo_ferroviario_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_equipo_vagon_en_trenes_id_baad43ad" ON "ufc_en_trenes_equipo_vagon" (
	"en_trenes_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_equipo_vagon_nom_equipo_ferroviario_id_0deb6446" ON "ufc_en_trenes_equipo_vagon" (
	"nom_equipo_ferroviario_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_tipo_equipo_ferroviario_id_8b575d8e" ON "ufc_vagon_cargado_descargado" (
	"tipo_equipo_ferroviario_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagones_productos_tipo_equipo_ferroviario_id_797fe5e9" ON "ufc_vagones_productos" (
	"tipo_equipo_ferroviario_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ufc_informe_operativo_aprobado_por_id_a9e9246b" ON "ufc_ufc_informe_operativo" (
	"aprobado_por_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ufc_informe_operativo_creado_por_id_d6dba88e" ON "ufc_ufc_informe_operativo" (
	"creado_por_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ufc_informe_operativo_provincia_id_b09ac5e8" ON "ufc_ufc_informe_operativo" (
	"provincia_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_informe_operativo_id_5df0478d" ON "ufc_vagon_cargado_descargado" (
	"informe_operativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagones_productos_informe_operativo_id_1054fb49" ON "ufc_vagones_productos" (
	"informe_operativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_informe_operativo_id_3c1a46f0" ON "ufc_arrastres" (
	"informe_operativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_tipo_equipo_id_fbc87f5c" ON "ufc_arrastres" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_informe_operativo_id_5529b300" ON "ufc_por_situar" (
	"informe_operativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_tipo_equipo_id_c0c16380" ON "ufc_por_situar" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_informe_operativo_id_99d87790" ON "ufc_situado_carga_descarga" (
	"informe_operativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_tipo_equipo_id_e6b486ce" ON "ufc_situado_carga_descarga" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagones_dias_equipo_ferroviario_id_9c509e4f" ON "ufc_vagones_dias" (
	"equipo_ferroviario_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_arrastres_equipo_vagon_arrastres_id_vagones_dias_id_43a8fd87_uniq" ON "ufc_arrastres_equipo_vagon" (
	"arrastres_id",
	"vagones_dias_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_equipo_vagon_arrastres_id_d7a4b67b" ON "ufc_arrastres_equipo_vagon" (
	"arrastres_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_equipo_vagon_vagones_dias_id_7b0f0ca2" ON "ufc_arrastres_equipo_vagon" (
	"vagones_dias_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_por_situar_equipo_vagon_por_situar_id_vagones_dias_id_10076d76_uniq" ON "ufc_por_situar_equipo_vagon" (
	"por_situar_id",
	"vagones_dias_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_equipo_vagon_por_situar_id_ad31a9ce" ON "ufc_por_situar_equipo_vagon" (
	"por_situar_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_equipo_vagon_vagones_dias_id_d4c1a972" ON "ufc_por_situar_equipo_vagon" (
	"vagones_dias_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_equipo_vagon_situado_carga_descarga_id_vagones_dias_id_2ec228c6_uniq" ON "ufc_situado_carga_descarga_equipo_vagon" (
	"situado_carga_descarga_id",
	"vagones_dias_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_equipo_vagon_situado_carga_descarga_id_15324db2" ON "ufc_situado_carga_descarga_equipo_vagon" (
	"situado_carga_descarga_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_equipo_vagon_vagones_dias_id_09fb5a83" ON "ufc_situado_carga_descarga_equipo_vagon" (
	"vagones_dias_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ufc_informe_operativo_entidad_id_d3af35fd" ON "ufc_ufc_informe_operativo" (
	"entidad_id"
);
CREATE INDEX IF NOT EXISTS "ufc_rotacion_vagones_tipo_equipo_ferroviario_id_d4b425ca" ON "ufc_rotacion_vagones" (
	"tipo_equipo_ferroviario_id"
);
CREATE INDEX IF NOT EXISTS "ufc_rotacion_vagones_informe_operativo_id_a15eb94b" ON "ufc_rotacion_vagones" (
	"informe_operativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_locomotora_id_c87f1198" ON "ufc_en_trenes" (
	"locomotora_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_tipo_equipo_id_6ee3bd99" ON "ufc_en_trenes" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_informe_operativo_id_045a2892" ON "ufc_en_trenes" (
	"informe_operativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_producto_ufc_tipo_equipo_id_ee4c21fc" ON "ufc_producto_ufc" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_producto_id_1f2030a3" ON "ufc_arrastres" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_producto_id_b4bd6b1d" ON "ufc_en_trenes" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_producto_id_93024405" ON "ufc_por_situar" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_producto_id_0e4391cc" ON "ufc_situado_carga_descarga" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_producto_id_ca0aec1a" ON "ufc_vagon_cargado_descargado" (
	"producto_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_ccd_situados_equipo_vagon_ccd_situados_id_vagones_dias_id_98819c13_uniq" ON "ufc_ccd_situados_equipo_vagon" (
	"ccd_situados_id",
	"vagones_dias_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_situados_equipo_vagon_ccd_situados_id_82da7376" ON "ufc_ccd_situados_equipo_vagon" (
	"ccd_situados_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_situados_equipo_vagon_vagones_dias_id_8d1c5039" ON "ufc_ccd_situados_equipo_vagon" (
	"vagones_dias_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_ccd_por_situar_equipo_vagon_ccd_por_situar_id_vagones_dias_id_305a51e6_uniq" ON "ufc_ccd_por_situar_equipo_vagon" (
	"ccd_por_situar_id",
	"vagones_dias_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_por_situar_equipo_vagon_ccd_por_situar_id_8a73b653" ON "ufc_ccd_por_situar_equipo_vagon" (
	"ccd_por_situar_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_por_situar_equipo_vagon_vagones_dias_id_8bcfa11c" ON "ufc_ccd_por_situar_equipo_vagon" (
	"vagones_dias_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_ccd_en_trenes_equipo_vagon_ccd_en_trenes_id_nom_equipo_ferroviario_id_5e05b01b_uniq" ON "ufc_ccd_en_trenes_equipo_vagon" (
	"ccd_en_trenes_id",
	"nom_equipo_ferroviario_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_en_trenes_equipo_vagon_ccd_en_trenes_id_de464055" ON "ufc_ccd_en_trenes_equipo_vagon" (
	"ccd_en_trenes_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_en_trenes_equipo_vagon_nom_equipo_ferroviario_id_aedc6bd8" ON "ufc_ccd_en_trenes_equipo_vagon" (
	"nom_equipo_ferroviario_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_ccd_arrastres_equipo_vagon_ccd_arrastres_id_vagones_dias_id_24155f05_uniq" ON "ufc_ccd_arrastres_equipo_vagon" (
	"ccd_arrastres_id",
	"vagones_dias_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_arrastres_equipo_vagon_ccd_arrastres_id_782501a6" ON "ufc_ccd_arrastres_equipo_vagon" (
	"ccd_arrastres_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_arrastres_equipo_vagon_vagones_dias_id_e455f41d" ON "ufc_ccd_arrastres_equipo_vagon" (
	"vagones_dias_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_ccd_vagones_cd_equipo_vagon_ccd_vagones_cd_id_ccd_registro_vagones_cd_id_f2ce5546_uniq" ON "ufc_ccd_vagones_cd_equipo_vagon" (
	"ccd_vagones_cd_id",
	"ccd_registro_vagones_cd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_vagones_cd_equipo_vagon_ccd_vagones_cd_id_e2594346" ON "ufc_ccd_vagones_cd_equipo_vagon" (
	"ccd_vagones_cd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_vagones_cd_equipo_vagon_ccd_registro_vagones_cd_id_349c3e91" ON "ufc_ccd_vagones_cd_equipo_vagon" (
	"ccd_registro_vagones_cd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_producto_tipo_embalaje_id_00dbac5a" ON "ufc_ccd_producto" (
	"tipo_embalaje_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_producto_tipo_equipo_id_8e1ec9d8" ON "ufc_ccd_producto" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_producto_unidad_medida_id_9bd18eff" ON "ufc_ccd_producto" (
	"unidad_medida_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_producto_producto_id_6b8f109b" ON "ufc_ccd_producto" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_por_situar_tipo_equipo_id_5b2c3206" ON "ufc_ccd_por_situar" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_por_situar_producto_id_62935c6a" ON "ufc_ccd_por_situar" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_por_situar_informe_ccd_id_6832ea56" ON "ufc_ccd_por_situar" (
	"informe_ccd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_por_situar_acceso_id_f3d1578b" ON "ufc_ccd_por_situar" (
	"acceso_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_registro_vagones_cd_equipo_ferroviario_id_617ddba9" ON "ufc_ccd_registro_vagones_cd" (
	"equipo_ferroviario_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_casillas_productos_acceso_id_3393bedb" ON "ufc_ccd_casillas_productos" (
	"acceso_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_casillas_productos_informe_ccd_id_517621b7" ON "ufc_ccd_casillas_productos" (
	"informe_ccd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ufc_informe_ccd_aprobado_por_id_4843a7ee" ON "ufc_ufc_informe_ccd" (
	"aprobado_por_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ufc_informe_ccd_creado_por_id_fb7fae6b" ON "ufc_ufc_informe_ccd" (
	"creado_por_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ufc_informe_ccd_entidad_id_4e5afda4" ON "ufc_ufc_informe_ccd" (
	"entidad_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ufc_informe_ccd_provincia_id_7b75d891" ON "ufc_ufc_informe_ccd" (
	"provincia_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_arrastres_acceso_id_edd6da54" ON "ufc_ccd_arrastres" (
	"acceso_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_arrastres_tipo_equipo_id_d6ced233" ON "ufc_ccd_arrastres" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_arrastres_producto_id_4e81207a" ON "ufc_ccd_arrastres" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_arrastres_informe_ccd_id_f45502f8" ON "ufc_ccd_arrastres" (
	"informe_ccd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_en_trenes_acceso_id_f05c9fe5" ON "ufc_ccd_en_trenes" (
	"acceso_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_en_trenes_tipo_equipo_id_c4fa5827" ON "ufc_ccd_en_trenes" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_en_trenes_producto_id_f42f7a73" ON "ufc_ccd_en_trenes" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_en_trenes_informe_ccd_id_8cfbb0fd" ON "ufc_ccd_en_trenes" (
	"informe_ccd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_situados_acceso_id_4d375c8b" ON "ufc_ccd_situados" (
	"acceso_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_situados_tipo_equipo_id_7034546b" ON "ufc_ccd_situados" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_situados_producto_id_0c7f0bbe" ON "ufc_ccd_situados" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_situados_informe_ccd_id_39f8a44c" ON "ufc_ccd_situados" (
	"informe_ccd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_vagones_cd_acceso_id_fbac4c78" ON "ufc_ccd_vagones_cd" (
	"acceso_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_vagones_cd_informe_ccd_id_e7dac725" ON "ufc_ccd_vagones_cd" (
	"informe_ccd_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_vagones_cd_producto_id_5d2161ac" ON "ufc_ccd_vagones_cd" (
	"producto_id"
);
CREATE INDEX IF NOT EXISTS "ufc_ccd_vagones_cd_tipo_equipo_id_177a98bd" ON "ufc_ccd_vagones_cd" (
	"tipo_equipo_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_parte_hecho_extraordinario_aprobado_por_id_33d4fc5d" ON "gemar_gemar_parte_hecho_extraordinario" (
	"aprobado_por_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_parte_hecho_extraordinario_creado_por_id_65a0cc9a" ON "gemar_gemar_parte_hecho_extraordinario" (
	"creado_por_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_parte_hecho_extraordinario_entidad_id_55294c68" ON "gemar_gemar_parte_hecho_extraordinario" (
	"entidad_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_parte_hecho_extraordinario_provincia_id_8e099d67" ON "gemar_gemar_parte_hecho_extraordinario" (
	"provincia_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "gemar_gemar_hecho_extraordinario_garante_id_producto_involucrado_id_origen_destino_tipo_diferencia_descripcion_hecho_c231abde_uniq" ON "gemar_gemar_hecho_extraordinario" (
	"garante_id",
	"producto_involucrado_id",
	"origen",
	"destino",
	"tipo_diferencia",
	"descripcion_hecho"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_hecho_extraordinario_embalaje_id_e60ede15" ON "gemar_gemar_hecho_extraordinario" (
	"embalaje_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_hecho_extraordinario_garante_id_ec95c702" ON "gemar_gemar_hecho_extraordinario" (
	"garante_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_hecho_extraordinario_incidencia_involucrada_id_296492a4" ON "gemar_gemar_hecho_extraordinario" (
	"incidencia_involucrada_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_hecho_extraordinario_producto_involucrado_id_8e9e81a1" ON "gemar_gemar_hecho_extraordinario" (
	"producto_involucrado_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_hecho_extraordinario_unidad_medida_id_e4b8dd6d" ON "gemar_gemar_hecho_extraordinario" (
	"unidad_medida_id"
);
CREATE INDEX IF NOT EXISTS "gemar_gemar_hecho_extraordinario_parte_hecho_extraordinario_id_f4a28e36" ON "gemar_gemar_hecho_extraordinario" (
	"parte_hecho_extraordinario_id"
);
COMMIT;

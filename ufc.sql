BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "nomencladores_nom_municipio" (
	"id"	integer NOT NULL,
	"nombre_municipio"	varchar(100) NOT NULL UNIQUE,
	"codigo"	varchar(4) NOT NULL UNIQUE,
	"provincia_id"	bigint NOT NULL,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_ufc_informe_operativo" (
	"id"	integer NOT NULL,
	"fecha_operacion"	datetime NOT NULL,
	"fecha_actual"	datetime NOT NULL,
	"plan_mensual_total"	integer NOT NULL,
	"plan_diario_total_vagones_cargados"	integer NOT NULL,
	"real_total_vagones_cargados"	integer NOT NULL,
	"total_vagones_situados"	integer NOT NULL,
	"plan_total_acumulado_actual"	integer NOT NULL,
	"real_total_acumulado_actual"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_producto_ufc" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
	"cantidad"	integer NOT NULL,
	"estado"	varchar(20),
	"contiene"	varchar(20),
	"producto_id"	bigint NOT NULL,
	"tipo_embalaje_id"	bigint NOT NULL,
	"unidad_medida_id"	bigint NOT NULL,
	FOREIGN KEY("tipo_embalaje_id") REFERENCES "nomencladores_nom_tipo_embalaje"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_id") REFERENCES "nomencladores_nom_producto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("unidad_medida_id") REFERENCES "nomencladores_nom_unidad_medida"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_producto_ufc_historico" (
	"id"	integer NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_por_situar" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
	"tipo_origen"	varchar(100) NOT NULL,
	"origen"	varchar(200) NOT NULL,
	"tipo_equipo"	varchar(200) NOT NULL,
	"estado"	varchar(200) NOT NULL,
	"operacion"	varchar(200) NOT NULL,
	"por_situar"	varchar(10) NOT NULL,
	"observaciones"	text,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_por_situar_historico" (
	"id"	integer NOT NULL,
	"por_situar_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("por_situar_id") REFERENCES "ufc_por_situar"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_por_situar_producto" (
	"id"	integer NOT NULL,
	"por_situar_id"	bigint NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("por_situar_id") REFERENCES "ufc_por_situar"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_en_trenes" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
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
	FOREIGN KEY("tipo_equipo_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("locomotora_id") REFERENCES "nomencladores_nom_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_en_trenes_equipo_vagon" (
	"id"	integer NOT NULL,
	"en_trenes_id"	bigint NOT NULL,
	"nom_equipo_ferroviario_id"	bigint NOT NULL,
	FOREIGN KEY("en_trenes_id") REFERENCES "ufc_en_trenes"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("nom_equipo_ferroviario_id") REFERENCES "nomencladores_nom_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_en_trenes_historico" (
	"id"	integer NOT NULL,
	"en_trenes_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("en_trenes_id") REFERENCES "ufc_en_trenes"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_en_trenes_producto" (
	"id"	integer NOT NULL,
	"en_trenes_id"	bigint NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	FOREIGN KEY("en_trenes_id") REFERENCES "ufc_en_trenes"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_arrastres" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
	"tipo_origen"	varchar(50) NOT NULL,
	"origen"	varchar(40) NOT NULL,
	"tipo_equipo"	varchar(200),
	"estado"	varchar(200),
	"cantidad_vagones"	varchar(10) NOT NULL,
	"tipo_destino"	varchar(50) NOT NULL,
	"destino"	varchar(40) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_arrastres_historico" (
	"id"	integer NOT NULL,
	"arrastres_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("arrastres_id") REFERENCES "ufc_arrastres"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_arrastres_producto" (
	"id"	integer NOT NULL,
	"arrastres_id"	bigint NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	FOREIGN KEY("arrastres_id") REFERENCES "ufc_arrastres"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_registro_vagones_cargados" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
	"no_id"	varchar(50) UNIQUE,
	"fecha_despacho"	date,
	"tipo_origen"	varchar(50),
	"origen"	varchar(40),
	"fecha_llegada"	date,
	"observaciones"	text,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_registro_vagones_cargados_historico" (
	"id"	integer NOT NULL,
	"registro_vagones_cargados_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("registro_vagones_cargados_id") REFERENCES "ufc_registro_vagones_cargados"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_rotacion_vagones" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
	"en_servicio"	integer unsigned NOT NULL CHECK("en_servicio" >= 0),
	"plan_carga"	integer unsigned NOT NULL CHECK("plan_carga" >= 0),
	"real_carga"	integer unsigned NOT NULL CHECK("real_carga" >= 0),
	"plan_rotacion"	integer unsigned NOT NULL CHECK("plan_rotacion" >= 0),
	"real_rotacion"	integer unsigned NOT NULL CHECK("real_rotacion" >= 0),
	"creado_el"	datetime NOT NULL,
	"actualizado_el"	datetime NOT NULL,
	"tipo_equipo_ferroviario_id"	bigint NOT NULL,
	FOREIGN KEY("tipo_equipo_ferroviario_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_rotacion_vagones_historico" (
	"id"	integer NOT NULL,
	"rotacion_vagones_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("rotacion_vagones_id") REFERENCES "ufc_rotacion_vagones"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_situado_carga_descarga" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
	"tipo_origen"	varchar(100),
	"origen"	varchar(200) NOT NULL,
	"tipo_equipo"	varchar(200),
	"estado"	varchar(200),
	"operacion"	varchar(200),
	"situados"	varchar(10) NOT NULL,
	"pendiente_proximo_dia"	varchar(10) NOT NULL,
	"observaciones"	text,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_situado_carga_descarga_historico" (
	"id"	integer NOT NULL,
	"situado_carga_descarga_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("situado_carga_descarga_id") REFERENCES "ufc_situado_carga_descarga"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_situado_carga_descarga_producto" (
	"id"	integer NOT NULL,
	"situado_carga_descarga_id"	bigint NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	FOREIGN KEY("situado_carga_descarga_id") REFERENCES "ufc_situado_carga_descarga"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_historicooperativo" (
	"id"	integer NOT NULL,
	"contenido"	text NOT NULL CHECK((JSON_VALID("contenido") OR "contenido" IS NULL)),
	"fecha_registro"	datetime NOT NULL,
	"informe_id"	bigint NOT NULL,
	FOREIGN KEY("informe_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagon_cargado_descargado" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
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
	FOREIGN KEY("tipo_equipo_ferroviario_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagon_cargado_descargado_historico" (
	"id"	integer NOT NULL,
	"vagon_cargado_descargado_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("vagon_cargado_descargado_id") REFERENCES "ufc_vagon_cargado_descargado"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagon_cargado_descargado_producto" (
	"id"	integer NOT NULL,
	"vagon_cargado_descargado_id"	bigint NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagon_cargado_descargado_id") REFERENCES "ufc_vagon_cargado_descargado"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagon_cargado_descargado_registros_vagones" (
	"id"	integer NOT NULL,
	"vagon_cargado_descargado_id"	bigint NOT NULL,
	"registro_vagones_cargados_id"	bigint NOT NULL,
	FOREIGN KEY("vagon_cargado_descargado_id") REFERENCES "ufc_vagon_cargado_descargado"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("registro_vagones_cargados_id") REFERENCES "ufc_registro_vagones_cargados"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagones_productos" (
	"id"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
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
	FOREIGN KEY("tipo_equipo_ferroviario_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagones_productos_historico" (
	"id"	integer NOT NULL,
	"vagones_productos_id"	bigint NOT NULL,
	"historicooperativo_id"	bigint NOT NULL,
	FOREIGN KEY("historicooperativo_id") REFERENCES "ufc_historicooperativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagones_productos_id") REFERENCES "ufc_vagones_productos"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagones_productos_producto" (
	"id"	integer NOT NULL,
	"vagones_productos_id"	bigint NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	FOREIGN KEY("vagones_productos_id") REFERENCES "ufc_vagones_productos"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE INDEX IF NOT EXISTS "nomencladores_nom_municipio_provincia_id_eaf73857" ON "nomencladores_nom_municipio" (
	"provincia_id"
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
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_producto_ufc_historico_producto_ufc_id_historicooperativo_id_4bb38f51_uniq" ON "ufc_producto_ufc_historico" (
	"producto_ufc_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_producto_ufc_historico_producto_ufc_id_667ff1d1" ON "ufc_producto_ufc_historico" (
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_producto_ufc_historico_historicooperativo_id_0afdf9fa" ON "ufc_producto_ufc_historico" (
	"historicooperativo_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_por_situar_historico_por_situar_id_historicooperativo_id_0b823ba4_uniq" ON "ufc_por_situar_historico" (
	"por_situar_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_historico_por_situar_id_be36bf0c" ON "ufc_por_situar_historico" (
	"por_situar_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_historico_historicooperativo_id_41d4c0d2" ON "ufc_por_situar_historico" (
	"historicooperativo_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_por_situar_producto_por_situar_id_producto_ufc_id_fdbbc3cf_uniq" ON "ufc_por_situar_producto" (
	"por_situar_id",
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_producto_por_situar_id_3ab27078" ON "ufc_por_situar_producto" (
	"por_situar_id"
);
CREATE INDEX IF NOT EXISTS "ufc_por_situar_producto_producto_ufc_id_fd1c17e7" ON "ufc_por_situar_producto" (
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_locomotora_id_c87f1198" ON "ufc_en_trenes" (
	"locomotora_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_tipo_equipo_id_6ee3bd99" ON "ufc_en_trenes" (
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
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_en_trenes_historico_en_trenes_id_historicooperativo_id_ba9d6839_uniq" ON "ufc_en_trenes_historico" (
	"en_trenes_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_historico_en_trenes_id_a2feef33" ON "ufc_en_trenes_historico" (
	"en_trenes_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_historico_historicooperativo_id_456af0ba" ON "ufc_en_trenes_historico" (
	"historicooperativo_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_en_trenes_producto_en_trenes_id_producto_ufc_id_03c1f152_uniq" ON "ufc_en_trenes_producto" (
	"en_trenes_id",
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_producto_en_trenes_id_81a6f66d" ON "ufc_en_trenes_producto" (
	"en_trenes_id"
);
CREATE INDEX IF NOT EXISTS "ufc_en_trenes_producto_producto_ufc_id_57072a5c" ON "ufc_en_trenes_producto" (
	"producto_ufc_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_arrastres_historico_arrastres_id_historicooperativo_id_5270aeec_uniq" ON "ufc_arrastres_historico" (
	"arrastres_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_historico_arrastres_id_e69cadc1" ON "ufc_arrastres_historico" (
	"arrastres_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_historico_historicooperativo_id_8e49c4c7" ON "ufc_arrastres_historico" (
	"historicooperativo_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_arrastres_producto_arrastres_id_producto_ufc_id_e5af6304_uniq" ON "ufc_arrastres_producto" (
	"arrastres_id",
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_producto_arrastres_id_905607fb" ON "ufc_arrastres_producto" (
	"arrastres_id"
);
CREATE INDEX IF NOT EXISTS "ufc_arrastres_producto_producto_ufc_id_79f6acae" ON "ufc_arrastres_producto" (
	"producto_ufc_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_registro_vagones_cargados_historico_registro_vagones_cargados_id_historicooperativo_id_215981fb_uniq" ON "ufc_registro_vagones_cargados_historico" (
	"registro_vagones_cargados_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_registro_vagones_cargados_historico_registro_vagones_cargados_id_11938e48" ON "ufc_registro_vagones_cargados_historico" (
	"registro_vagones_cargados_id"
);
CREATE INDEX IF NOT EXISTS "ufc_registro_vagones_cargados_historico_historicooperativo_id_1a964469" ON "ufc_registro_vagones_cargados_historico" (
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_rotacion_vagones_tipo_equipo_ferroviario_id_d4b425ca" ON "ufc_rotacion_vagones" (
	"tipo_equipo_ferroviario_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_rotacion_vagones_historico_rotacion_vagones_id_historicooperativo_id_31a7cc95_uniq" ON "ufc_rotacion_vagones_historico" (
	"rotacion_vagones_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_rotacion_vagones_historico_rotacion_vagones_id_37faf0ce" ON "ufc_rotacion_vagones_historico" (
	"rotacion_vagones_id"
);
CREATE INDEX IF NOT EXISTS "ufc_rotacion_vagones_historico_historicooperativo_id_7c06e15c" ON "ufc_rotacion_vagones_historico" (
	"historicooperativo_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_historico_situado_carga_descarga_id_historicooperativo_id_ded36fb4_uniq" ON "ufc_situado_carga_descarga_historico" (
	"situado_carga_descarga_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_historico_situado_carga_descarga_id_f9ad9b17" ON "ufc_situado_carga_descarga_historico" (
	"situado_carga_descarga_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_historico_historicooperativo_id_3c066f35" ON "ufc_situado_carga_descarga_historico" (
	"historicooperativo_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_producto_situado_carga_descarga_id_producto_ufc_id_ace797fe_uniq" ON "ufc_situado_carga_descarga_producto" (
	"situado_carga_descarga_id",
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_producto_situado_carga_descarga_id_c173d946" ON "ufc_situado_carga_descarga_producto" (
	"situado_carga_descarga_id"
);
CREATE INDEX IF NOT EXISTS "ufc_situado_carga_descarga_producto_producto_ufc_id_20a21b50" ON "ufc_situado_carga_descarga_producto" (
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_historicooperativo_informe_id_aac81e53" ON "ufc_historicooperativo" (
	"informe_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_tipo_equipo_ferroviario_id_8b575d8e" ON "ufc_vagon_cargado_descargado" (
	"tipo_equipo_ferroviario_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_historico_vagon_cargado_descargado_id_historicooperativo_id_c7ceaabf_uniq" ON "ufc_vagon_cargado_descargado_historico" (
	"vagon_cargado_descargado_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_historico_vagon_cargado_descargado_id_83ee34b5" ON "ufc_vagon_cargado_descargado_historico" (
	"vagon_cargado_descargado_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_historico_historicooperativo_id_b60cbabe" ON "ufc_vagon_cargado_descargado_historico" (
	"historicooperativo_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_producto_vagon_cargado_descargado_id_producto_ufc_id_c999567a_uniq" ON "ufc_vagon_cargado_descargado_producto" (
	"vagon_cargado_descargado_id",
	"producto_ufc_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_producto_vagon_cargado_descargado_id_7822c7ff" ON "ufc_vagon_cargado_descargado_producto" (
	"vagon_cargado_descargado_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_producto_producto_ufc_id_5869718f" ON "ufc_vagon_cargado_descargado_producto" (
	"producto_ufc_id"
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
CREATE INDEX IF NOT EXISTS "ufc_vagones_productos_tipo_equipo_ferroviario_id_797fe5e9" ON "ufc_vagones_productos" (
	"tipo_equipo_ferroviario_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ufc_vagones_productos_historico_vagones_productos_id_historicooperativo_id_eddd765f_uniq" ON "ufc_vagones_productos_historico" (
	"vagones_productos_id",
	"historicooperativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagones_productos_historico_vagones_productos_id_0ac2675b" ON "ufc_vagones_productos_historico" (
	"vagones_productos_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagones_productos_historico_historicooperativo_id_9a64e766" ON "ufc_vagones_productos_historico" (
	"historicooperativo_id"
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
COMMIT;

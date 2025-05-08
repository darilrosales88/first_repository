BEGIN TRANSACTION;
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
	"informe_operativo_id"	bigint,
	"tipo_equipo_ferroviario_id"	bigint NOT NULL,
	FOREIGN KEY("informe_operativo_id") REFERENCES "ufc_ufc_informe_operativo"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tipo_equipo_ferroviario_id") REFERENCES "nomencladores_nom_tipo_equipo_ferroviario"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagon_cargado_descargado_producto" (
	"id"	integer NOT NULL,
	"vagon_cargado_descargado_id"	bigint NOT NULL,
	"producto_ufc_id"	bigint NOT NULL,
	FOREIGN KEY("vagon_cargado_descargado_id") REFERENCES "ufc_vagon_cargado_descargado"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_ufc_id") REFERENCES "ufc_producto_ufc"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ufc_vagon_cargado_descargado_registros_vagones" (
	"id"	integer NOT NULL,
	"vagon_cargado_descargado_id"	bigint NOT NULL,
	"registro_vagones_cargados_id"	bigint NOT NULL,
	FOREIGN KEY("registro_vagones_cargados_id") REFERENCES "ufc_registro_vagones_cargados"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vagon_cargado_descargado_id") REFERENCES "ufc_vagon_cargado_descargado"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_informe_operativo_id_5df0478d" ON "ufc_vagon_cargado_descargado" (
	"informe_operativo_id"
);
CREATE INDEX IF NOT EXISTS "ufc_vagon_cargado_descargado_tipo_equipo_ferroviario_id_8b575d8e" ON "ufc_vagon_cargado_descargado" (
	"tipo_equipo_ferroviario_id"
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
COMMIT;

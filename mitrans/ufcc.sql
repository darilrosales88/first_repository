BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "gemar_gemar_parte_hecho_extraordinario" (
	"id"	integer NOT NULL,
	"fecha_operacion"	datetime NOT NULL,
	"fecha_actual"	datetime NOT NULL,
	"estado_parte"	varchar(14) NOT NULL,
	"aprobado_por_id"	bigint,
	"creado_por_id"	bigint,
	"entidad_id"	bigint,
	"provincia_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("aprobado_por_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("creado_por_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("entidad_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("provincia_id") REFERENCES "nomencladores_nom_provincia"("id") DEFERRABLE INITIALLY DEFERRED
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
	"kg_diferencia"	decimal,
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
	FOREIGN KEY("incidencia_involucrada_id") REFERENCES "nomencladores_nom_incidencia"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("embalaje_id") REFERENCES "nomencladores_nom_tipo_embalaje"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("unidad_medida_id") REFERENCES "nomencladores_nom_unidad_medida"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("producto_involucrado_id") REFERENCES "nomencladores_nom_producto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("parte_hecho_extraordinario_id") REFERENCES "gemar_gemar_parte_hecho_extraordinario"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("garante_id") REFERENCES "nomencladores_nom_entidades"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "gemar_gemar_parte_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","estado_parte","aprobado_por_id","creado_por_id","entidad_id","provincia_id") VALUES (14,'2025-07-30 00:00:00','2025-07-30 11:17:24.860485','Creado',1,1,1,1);
INSERT INTO "gemar_gemar_parte_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","estado_parte","aprobado_por_id","creado_por_id","entidad_id","provincia_id") VALUES (15,'2025-07-31 00:00:00','2025-07-31 16:59:42.505895','Aprobado',1,1,1,1);
INSERT INTO "gemar_gemar_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","informado","tipo_involucrado","involucrado","tipo_origen","origen","destino","tipo_diferencia","kg_diferencia","cantidad_diferencia","valor_diferencia","averia","kg_averia","cantidad_averia","valor_averia","descripcion_hecho","embalaje_id","garante_id","incidencia_involucrada_id","producto_involucrado_id","unidad_medida_id","parte_hecho_extraordinario_id") VALUES (6,'2025-07-30 12:13:03.460657','2025-07-30 12:13:03.460683','Informado del dia 24','puerto','Puerto Unos','puerto','Puerto Unos','Aquel lugar','sobrante',NULL,NULL,NULL,'no',NULL,NULL,NULL,'qwerty',4,1,1,3,3,14);
INSERT INTO "gemar_gemar_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","informado","tipo_involucrado","involucrado","tipo_origen","origen","destino","tipo_diferencia","kg_diferencia","cantidad_diferencia","valor_diferencia","averia","kg_averia","cantidad_averia","valor_averia","descripcion_hecho","embalaje_id","garante_id","incidencia_involucrada_id","producto_involucrado_id","unidad_medida_id","parte_hecho_extraordinario_id") VALUES (7,'2025-07-31 15:18:46.849422','2025-07-31 15:18:46.849451','we32','puerto','Puerto Unos','entidad','Acceso comercial uno','Jatibonico','sobrante',34.23,0.05,233.98,'no',NULL,NULL,NULL,'wer',3,1,1,5,2,15);
INSERT INTO "gemar_gemar_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","informado","tipo_involucrado","involucrado","tipo_origen","origen","destino","tipo_diferencia","kg_diferencia","cantidad_diferencia","valor_diferencia","averia","kg_averia","cantidad_averia","valor_averia","descripcion_hecho","embalaje_id","garante_id","incidencia_involucrada_id","producto_involucrado_id","unidad_medida_id","parte_hecho_extraordinario_id") VALUES (8,'2025-07-31 15:44:31.820908','2025-07-31 15:44:31.820939','weQW','puerto','Puerto Unos','entidad','Acceso comercial uno','Jatibonico','sobrante',3.43534534,NULL,NULL,'no',NULL,NULL,NULL,'QWERQWR',3,6,1,1,3,15);
INSERT INTO "gemar_gemar_hecho_extraordinario" ("id","fecha_operacion","fecha_actual","informado","tipo_involucrado","involucrado","tipo_origen","origen","destino","tipo_diferencia","kg_diferencia","cantidad_diferencia","valor_diferencia","averia","kg_averia","cantidad_averia","valor_averia","descripcion_hecho","embalaje_id","garante_id","incidencia_involucrada_id","producto_involucrado_id","unidad_medida_id","parte_hecho_extraordinario_id") VALUES (9,'2025-07-31 16:12:23.836826','2025-07-31 16:32:04.041868','Mala talla','entidad','Acceso comercial uno','entidad','Cuba Ron SA','Jatibonico','sobrante',33114.34,43,65.98,'si',23.34,11100,76,'Unos datos',3,6,1,5,2,15);
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

BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
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
	FOREIGN KEY("customuser_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "Administracion_customuser_user_permissions" (
	"id"	integer NOT NULL,
	"customuser_id"	bigint NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("customuser_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	bigint NOT NULL,
	"action_time"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "authtoken_token" (
	"key"	varchar(40) NOT NULL,
	"created"	datetime NOT NULL,
	"user_id"	bigint NOT NULL UNIQUE,
	PRIMARY KEY("key"),
	FOREIGN KEY("user_id") REFERENCES "Administracion_customuser"("id") DEFERRABLE INITIALLY DEFERRED
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
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (2,'auth','permission');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (3,'auth','group');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (4,'contenttypes','contenttype');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (5,'sessions','session');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (6,'authtoken','token');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (7,'authtoken','tokenproxy');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (8,'nomencladores','nom_cargo');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (9,'nomencladores','nom_contenedor');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (10,'nomencladores','nom_entidades');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (11,'nomencladores','nom_estado_tecnico');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (12,'nomencladores','nom_incidencia');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (13,'nomencladores','nom_producto');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (14,'nomencladores','nom_tipo_embalaje');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (15,'nomencladores','nom_tipo_estructura_ubicacion');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (16,'nomencladores','nom_unidad_medida');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (17,'nomencladores','nom_destino');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (18,'nomencladores','nom_osde_oace_organismo');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (19,'nomencladores','nom_pais');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (20,'nomencladores','nom_embarcacion');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (21,'nomencladores','nom_provincia');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (22,'nomencladores','nom_municipio');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (23,'nomencladores','nom_puerto');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (24,'nomencladores','nom_terminal');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (25,'nomencladores','nom_atraque');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (26,'nomencladores','nom_territorio');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (27,'nomencladores','nom_tipo_equipo_ferroviario');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (28,'nomencladores','nom_estructura_ubicacion');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (29,'nomencladores','nom_tipo_maniobra_portuaria');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (30,'nomencladores','nom_equipo_ferroviario');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (31,'Administracion','customuser');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (32,'Administracion','auditoria');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (33,'ufc','productos_vagones_cargados_descargados');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (34,'ufc','vagon_cargado_descargado');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (35,'ufc','en_trenes');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (36,'ufc','producto_en_vagon');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (37,'nomencladores','situado_carga_descarga');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (38,'nomencladores','por_situar_carga_descarga');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (39,'ufc','por_situar_carga_descarga');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (40,'ufc','situado_carga_descarga');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (41,'ufc','arrastrependientes');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (42,'ufc','arrastre_pendientes');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (43,'ufc','arrastres');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (44,'ufc','por_situar');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (45,'ufc','registro_vagones_cargados');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (46,'ufc','productos_vagones_productos');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (47,'ufc','vagones_productos');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (48,'ufc','producto_ufc');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (49,'ufc','rotacion_vagones');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (50,'ufc','ufc_informe_operativo');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (51,'ufc','historialvagoncargadodescargado');
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
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (361,4,200);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (362,4,197);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (363,4,198);
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (364,4,199);
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
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (201,51,'add_historialvagoncargadodescargado','Insertar Historial de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (202,51,'change_historialvagoncargadodescargado','Editar Historial de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (203,51,'delete_historialvagoncargadodescargado','Eliminar Historial de vagón cargado/descargado');
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (204,51,'view_historialvagoncargadodescargado','Visualizar Historial de vagón cargado/descargado');
INSERT INTO "auth_group" ("id","name") VALUES (1,'Admin');
INSERT INTO "auth_group" ("id","name") VALUES (2,'Consultor');
INSERT INTO "auth_group" ("id","name") VALUES (3,'AdminNomencladores');
INSERT INTO "auth_group" ("id","name") VALUES (4,'AdminUFC');
INSERT INTO "auth_group" ("id","name") VALUES (5,'VisualizadorNomencladores');
INSERT INTO "auth_group" ("id","name") VALUES (6,'VisualizadorUFC');
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (1,1,1);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (2,2,2);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (7,1,3);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (8,1,4);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (9,1,5);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (10,1,6);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (11,4,3);
INSERT INTO "Administracion_customuser_groups" ("id","customuser_id","group_id") VALUES (12,4,4);
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (1,'1','Admin',1,'[{"added": {}}]',3,1,'2025-02-24 19:04:26.143069');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (2,'2','Consultor',1,'[{"added": {}}]',3,1,'2025-02-24 19:04:54.704922');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (3,'1','admin - ',2,'[{"changed": {"fields": ["Groups"]}}]',31,1,'2025-02-24 19:05:17.063373');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (4,'1','admin - Administrador Primero',2,'[{"changed": {"fields": ["Last login"]}}]',31,1,'2025-02-24 21:14:29.087454');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (5,'1','admin - Administrador Primero',2,'[{"changed": {"fields": ["User permissions"]}}]',31,1,'2025-02-24 21:56:23.103459');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (6,'1','admin - Administrador Primero',2,'[]',31,1,'2025-02-24 22:29:43.398539');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (7,'1','admin - Administrador Primero',2,'[{"changed": {"fields": ["User permissions"]}}]',31,1,'2025-02-24 22:30:40.997248');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (8,'2','alain - Alain Dellon Mask',2,'[{"changed": {"fields": ["password"]}}]',31,1,'2025-02-24 22:36:50.800890');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (9,'1','Ansakjdf',1,'[{"added": {}}]',26,1,'2025-02-25 21:57:01.689997');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (10,'1','Puerto Uno',1,'[{"added": {}}]',23,1,'2025-02-25 22:40:34.590777');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (11,'1','Terminal unica',1,'[{"added": {}}]',24,1,'2025-02-25 22:41:18.828000');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (12,'1','Una descrip',1,'[{"added": {}}]',27,1,'2025-02-25 23:08:55.906657');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (13,'1','Tipo de estructura Uno',1,'[{"added": {}}]',15,1,'2025-02-25 23:29:53.514815');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (14,'1','Chícharo',1,'[{"added": {}}]',13,1,'2025-02-25 23:45:03.338559');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (15,'1','tipo de producto Producto - Chícharo',1,'[{"added": {}}]',33,1,'2025-03-09 02:37:05.995686');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (16,'1','Vagón 1 - Vacío',1,'[{"added": {}}]',34,1,'2025-03-09 02:39:10.134338');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (17,'1','Admin',2,'[{"changed": {"fields": ["Permissions"]}}]',3,1,'2025-03-11 05:25:58.767829');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (18,'3','Tipo de equipo: locomotora - Longitud: 12.00 - Peso neto sin carga: 2.00 - Peso máximo con carga: 2.00',2,'[]',27,1,'2025-03-11 05:29:34.321048');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (19,'11','Vagón 11 - Cargado',1,'[{"added": {}}]',34,1,'2025-03-11 05:33:00.886596');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (20,'1','En trenes 1 - Cargado',1,'[{"added": {}}]',35,1,'2025-03-11 05:34:20.260558');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (21,'4','Tipo de equipo: locomotora - Longitud: 12333 - Peso neto sin carga: 111 - Peso máximo con carga: 11233',1,'[{"added": {}}]',27,1,'2025-03-11 05:42:12.814801');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (22,'2','En trenes 2 - Cargado',1,'[{"added": {}}]',35,1,'2025-03-11 05:42:44.857638');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (23,'3','En trenes 3 - Cargado',1,'[{"added": {}}]',35,1,'2025-03-11 05:44:56.026026');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (24,'4','En trenes 4 - Cargado',1,'[{"added": {}}]',35,1,'2025-03-11 05:54:19.652280');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (25,'3','carlos - Carlos Gonza',1,'[{"added": {}}]',31,1,'2025-03-11 13:18:55.176497');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (26,'1','admin - Administrador Primero',2,'[{"changed": {"fields": ["Rol que desempe\u00f1a"]}}]',31,1,'2025-03-11 13:20:54.651914');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (27,'4','juanito - juanito GLEZ',1,'[{"added": {}}]',31,1,'2025-03-11 13:23:20.083793');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (28,'5','Cafe',1,'[{"added": {}}]',13,1,'2025-03-13 00:53:22.515275');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (29,'6','tipo de producto Producto - Cafe',1,'[{"added": {}}]',33,1,'2025-03-13 00:53:39.074234');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (30,'5','En trenes 5 - Vacío',1,'[{"added": {}}]',35,1,'2025-03-13 00:54:11.090379');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (31,'5','En trenes 5 - Cargado',2,'[{"changed": {"fields": ["Estado"]}}]',35,1,'2025-03-13 00:54:18.844522');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (32,'1','tipo de producto Lleno - Chícharo',1,'[{"added": {}}]',36,1,'2025-03-17 04:16:25.241223');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (33,'1','En trenes 1 -11244124- Cargado',1,'[{"added": {}}]',35,1,'2025-03-17 04:17:03.101680');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (34,'6','mortadella',1,'[{"added": {}}]',13,1,'2025-03-17 14:18:59.951134');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (35,'3','RAPEL',1,'[{"added": {}}]',14,1,'2025-03-17 14:19:06.082466');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (36,'2','metro',1,'[{"added": {}}]',16,1,'2025-03-17 14:19:42.865747');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (37,'2','tipo de producto Lleno - mortadella',1,'[{"added": {}}]',36,1,'2025-03-17 14:19:53.996044');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (38,'7','Zuko',1,'[{"added": {}}]',13,1,'2025-03-17 14:20:44.902292');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (39,'4','Paqueticos',1,'[{"added": {}}]',14,1,'2025-03-17 14:20:55.725027');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (40,'3','Litros',1,'[{"added": {}}]',16,1,'2025-03-17 14:21:16.926027');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (41,'3','tipo de producto Lleno - Zuko',1,'[{"added": {}}]',36,1,'2025-03-17 14:21:25.166441');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (42,'5','Tipo de equipo: locomotora - Longitud: 100 - Peso neto sin carga: 10000 - Peso máximo con carga: 100000',1,'[{"added": {}}]',27,1,'2025-03-17 14:22:14.765854');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (43,'6','MOLE321',1,'[{"added": {}}]',30,1,'2025-03-17 14:23:10.993588');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (44,'3','En trenes 3 -MOLE321- Cargado',1,'[{"added": {}}]',35,1,'2025-03-17 14:24:58.451832');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (45,'3','En trenes 3 -MOLE321- Cargado',3,'',35,1,'2025-03-17 14:25:08.846452');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (46,'2','En trenes 2 -11244124- Cargado',3,'',35,1,'2025-03-17 14:25:20.053334');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (47,'1','En trenes 1 -MOLE321- Cargado',1,'[{"added": {}}]',35,1,'2025-03-17 16:40:07.297627');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (48,'1','por_situar_carga_descarga object (1)',1,'[{"added": {}}]',39,1,'2025-03-31 13:26:18.478702');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (49,'1','Situado_Carga_Descarga object (1)',1,'[{"added": {}}]',40,1,'2025-03-31 13:32:00.445374');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (50,'1','Arrastre Pendiente1 - Puerto1',1,'[{"added": {}}]',43,1,'2025-04-05 05:02:57.758665');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (51,'5','Situado_Carga_Descarga object (5)',3,'',40,1,'2025-04-10 00:27:18.298647');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (52,'5','por_situar_carga_descarga object (5)',3,'',39,1,'2025-04-10 00:27:28.876811');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (53,'1','por_situar object (1)',1,'[{"added": {}}]',44,1,'2025-04-10 03:40:05.880453');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (54,'32','por_situar object (32)',3,'',44,1,'2025-04-10 04:20:13.961905');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (55,'31','por_situar object (31)',3,'',44,1,'2025-04-10 04:20:18.159325');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (56,'30','por_situar object (30)',3,'',44,1,'2025-04-10 04:20:21.852324');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (57,'29','por_situar object (29)',3,'',44,1,'2025-04-10 04:20:27.493964');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (58,'10','por_situar object (10)',3,'',44,1,'2025-04-10 04:20:50.833182');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (59,'28','por_situar object (28)',3,'',44,1,'2025-04-10 04:21:07.524716');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (60,'27','por_situar object (27)',3,'',44,1,'2025-04-10 04:21:07.524763');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (61,'26','por_situar object (26)',3,'',44,1,'2025-04-10 04:21:07.524791');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (62,'25','por_situar object (25)',3,'',44,1,'2025-04-10 04:21:07.524817');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (63,'24','por_situar object (24)',3,'',44,1,'2025-04-10 04:21:07.524842');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (64,'23','por_situar object (23)',3,'',44,1,'2025-04-10 04:21:07.524866');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (65,'22','por_situar object (22)',3,'',44,1,'2025-04-10 04:21:07.524891');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (66,'21','por_situar object (21)',3,'',44,1,'2025-04-10 04:21:07.524916');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (67,'20','por_situar object (20)',3,'',44,1,'2025-04-10 04:21:07.524939');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (68,'19','por_situar object (19)',3,'',44,1,'2025-04-10 04:21:07.524962');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (69,'18','por_situar object (18)',3,'',44,1,'2025-04-10 04:21:07.524985');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (70,'17','por_situar object (17)',3,'',44,1,'2025-04-10 04:21:07.525008');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (71,'16','por_situar object (16)',3,'',44,1,'2025-04-10 04:21:07.525031');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (72,'15','por_situar object (15)',3,'',44,1,'2025-04-10 04:21:07.525054');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (73,'14','por_situar object (14)',3,'',44,1,'2025-04-10 04:21:16.852708');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (74,'13','por_situar object (13)',3,'',44,1,'2025-04-10 04:21:16.852773');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (75,'12','por_situar object (12)',3,'',44,1,'2025-04-10 04:21:16.852801');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (76,'11','por_situar object (11)',3,'',44,1,'2025-04-10 04:21:16.852827');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (77,'9','por_situar object (9)',3,'',44,1,'2025-04-10 04:21:16.852851');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (78,'8','por_situar object (8)',3,'',44,1,'2025-04-10 04:21:16.852875');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (79,'7','por_situar object (7)',3,'',44,1,'2025-04-10 04:21:16.852899');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (80,'23','tipo de producto Alimentos - cafe',3,'',36,1,'2025-04-20 04:39:00.684644');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (81,'21','tipo de producto Productos Varios - AAdera',3,'',36,1,'2025-04-20 04:40:55.539913');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (82,'19','tipo de producto Alimentos - Zuko',3,'',36,1,'2025-04-20 04:40:59.181325');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (83,'18','tipo de producto Productos Varios - AAdera',3,'',36,1,'2025-04-20 04:41:02.804597');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (84,'16','tipo de producto Alimentos - Chícharo',3,'',36,1,'2025-04-20 04:41:06.976755');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (85,'15','tipo de producto Alimentos - Zuko',3,'',36,1,'2025-04-20 04:48:07.926173');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (86,'13','tipo de producto Productos Varios - Velas apagones',3,'',36,1,'2025-04-20 04:48:14.154659');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (87,'24','tipo de producto Alimentos - mortadella',1,'[{"added": {}}]',36,1,'2025-04-20 04:48:52.170690');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (88,'7','Zuko',2,'[{"changed": {"fields": ["Tipo de producto"]}}]',13,1,'2025-04-20 05:00:02.878738');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (89,'6','mortadella',2,'[]',13,1,'2025-04-20 05:00:07.593868');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (90,'9','Velas apagones',2,'[]',13,1,'2025-04-20 05:00:11.839369');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (91,'1','Chícharo',2,'[{"changed": {"fields": ["Tipo de producto"]}}]',13,1,'2025-04-20 05:00:18.054325');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (92,'1','Chícharo',2,'[]',13,1,'2025-04-20 05:00:21.751203');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (93,'3','AAdera',2,'[]',13,1,'2025-04-20 05:00:25.421826');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (94,'4','cafe',2,'[]',13,1,'2025-04-20 05:00:28.368938');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (95,'5','Cafe',2,'[]',13,1,'2025-04-20 05:00:31.529343');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (96,'7','Zuko',2,'[]',13,1,'2025-04-20 05:00:34.145856');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (97,'7','Zuko',2,'[]',13,1,'2025-04-20 05:00:37.549035');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (98,'8','Pasta espaguethi',2,'[]',13,1,'2025-04-20 05:00:39.712448');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (99,'9','Velas apagones',2,'[]',13,1,'2025-04-20 05:00:41.580297');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (100,'3','tipo de producto Alimentos - Zuko',2,'[{"changed": {"fields": ["Estado", "Contiene"]}}]',36,1,'2025-04-20 05:00:58.297860');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (101,'2','tipo de producto Productos Varios - mortadella',2,'[{"changed": {"fields": ["Estado", "Contiene"]}}]',36,1,'2025-04-20 05:01:05.374610');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (102,'25','tipo de producto Alimentos - feffer',1,'[{"added": {}}]',36,1,'2025-04-20 05:01:19.564628');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (103,'1','tipo de producto Alimentos - Chícharo',2,'[{"changed": {"fields": ["Estado", "Contiene"]}}]',36,1,'2025-04-20 05:01:51.766113');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (104,'2','tipo de producto Alimentos - mortadella',2,'[{"changed": {"fields": ["Contiene"]}}]',36,1,'2025-04-20 05:01:57.415170');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (105,'9','Velas apagones',2,'[{"changed": {"fields": ["Tipo de producto"]}}]',13,1,'2025-04-20 05:04:11.193781');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (106,'3','AdminNomencladores',1,'[{"added": {}}]',3,1,'2025-04-20 22:39:22.004419');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (107,'4','AdminUFC',1,'[{"added": {}}]',3,1,'2025-04-20 22:39:57.017170');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (108,'1','admin - Administrador Primero',2,'[{"changed": {"fields": ["Groups"]}}]',31,1,'2025-04-20 22:40:16.039416');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (109,'1','cafe - Paqueticos',1,'[{"added": {}}]',48,1,'2025-04-25 23:01:47.579453');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (110,'2','Zuko - Nylon',1,'[{"added": {}}]',48,1,'2025-04-25 23:02:13.028570');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (111,'1','cafe - Nylon',1,'[{"added": {}}]',48,1,'2025-04-26 22:07:50.582036');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (112,'2','Pasta espaguethi - RAPEL',1,'[{"added": {}}]',48,1,'2025-04-26 22:08:13.422496');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (113,'3','mortadella - RAPEL',1,'[{"added": {}}]',48,1,'2025-04-26 22:08:34.516618');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (114,'4','AdminUFC',2,'[{"changed": {"fields": ["Permissions"]}}]',3,1,'2025-04-27 01:01:48.941236');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (115,'1','admin - Administrador Primero',2,'[{"changed": {"fields": ["password"]}}]',31,1,'2025-04-27 01:03:15.685050');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (116,'5','VisualizadorNomencladores',1,'[{"added": {}}]',3,1,'2025-04-27 01:04:34.144406');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (117,'6','VisualizadorUFC',1,'[{"added": {}}]',3,1,'2025-04-27 01:05:37.490356');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (118,'1','admin - Administrador Primero',2,'[{"changed": {"fields": ["Groups"]}}]',31,1,'2025-04-27 01:05:56.497154');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (119,'4','juanito - juanito GLEZ',2,'[{"changed": {"fields": ["password"]}}]',31,1,'2025-04-27 01:08:13.392205');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (120,'4','juanito - juanito GLEZ',2,'[{"changed": {"fields": ["Groups"]}}]',31,1,'2025-04-27 01:08:24.207727');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (121,'4','AdminUFC',2,'[{"changed": {"fields": ["Permissions"]}}]',3,1,'2025-05-02 22:11:45.602747');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (122,'1','Fecha de operación 2025-05-02 22:11:54.335768+00:00 - fecha actual: 2025-05-02 22:11:54.335793+00:00',1,'[{"added": {}}]',50,1,'2025-05-02 22:11:54.337678');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (123,'1','Fecha de operación 2025-05-02 22:11:54.335768+00:00 - fecha actual: 2025-05-02 22:11:54.335793+00:00',3,'',50,1,'2025-05-02 22:12:05.421159');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (124,'2','Fecha de operación 2025-05-04 21:56:41.281369+00:00 - fecha actual: 2025-05-04 21:56:41.281425+00:00',3,'',50,1,'2025-05-04 22:00:50.386488');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (125,'2','Vagón 2 - Vacío',3,'',34,1,'2025-05-05 18:02:01.525206');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (126,'4','Fecha de operación 2025-05-05 14:28:09.665733+00:00 - fecha actual: 2025-05-05 14:28:09.665808+00:00',3,'',50,1,'2025-05-05 18:04:50.683906');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (127,'3','Fecha de operación 2025-05-04 22:40:09.270643+00:00 - fecha actual: 2025-05-04 22:40:09.270666+00:00',3,'',50,1,'2025-05-05 18:04:50.683987');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (128,'6','Fecha de operación 2025-05-06 01:09:31.988667+00:00 - fecha actual: 2025-05-06 01:09:31.988724+00:00',3,'',50,1,'2025-05-06 01:12:52.885014');
INSERT INTO "django_admin_log" ("id","object_id","object_repr","action_flag","change_message","content_type_id","user_id","action_time") VALUES (129,'5','Fecha de operación 2025-05-05 18:49:36.254914+00:00 - fecha actual: 2025-05-05 18:49:36.254937+00:00',3,'',50,1,'2025-05-06 01:12:52.885119');
INSERT INTO "authtoken_token" ("key","created","user_id") VALUES ('99ff5c146534b742f430c2d9f745bdbbfba79b56','2025-03-13 13:41:50.577974',3);
INSERT INTO "authtoken_token" ("key","created","user_id") VALUES ('dfb3e9eb2f8992510d0075d4669b3e7851a5a620','2025-04-27 02:11:32.259112',1);
INSERT INTO "authtoken_token" ("key","created","user_id") VALUES ('3a523bae4ff891fbb6dfe3eff67124397ad34827','2025-04-27 02:13:37.766690',4);
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (1,'pbkdf2_sha256$870000$ouawk2HDXoMOyC27gzEzP7$85u6pXiLq0gcS52ALx9C3apwkjrLkC8ckLeQIu1h44w=','2025-05-06 20:36:16.086679',1,'admin','Administrador','Primero','admin@desoft.cu',1,1,'2025-02-24 18:55:23',1,1,'admin');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (2,'pbkdf2_sha256$870000$w1qQtbjR1E9CkncsWJs36g$OVi4keqRQX8ZyfCCNo+u621k7s28n6PqAZvtbxS2nhc=','2025-02-24 22:37:15.603477',0,'alain','Alain','Dellon Mask','alain@desoft.cu',0,1,'2025-02-24 19:13:22.712464',2,1,'operador');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (3,'pbkdf2_sha256$870000$r2ZPhSKJlCRftnvX0M68rA$AYmqaupSq7OUChmVVLIvvKS0snuj2HIiu6aZGPbpkUE=','2025-03-13 13:41:50.584033',0,'carlos','Carlos','Gonza','carlosr301101@gmail.com',0,1,'2025-03-11 13:18:54.449569',2,7,'ufc');
INSERT INTO "Administracion_customuser" ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","cargo_id","entidad_id","role") VALUES (4,'pbkdf2_sha256$870000$VUDkbzd2NRkZWFZ8ebGu7D$8de8M+Qf4oJHhhuO6qz1OyCAGrhKQ4BpX6Bti3xJbGY=','2025-04-27 02:13:37.774451',0,'juanito','juanito','GLEZ','juanito@gmail.com',0,1,'2025-03-11 13:23:18',1,7,'operador');
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
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
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "Administracion_customuser_cargo_id_5a2dcb16" ON "Administracion_customuser" (
	"cargo_id"
);
CREATE INDEX IF NOT EXISTS "Administracion_customuser_entidad_id_93ab5786" ON "Administracion_customuser" (
	"entidad_id"
);
COMMIT;

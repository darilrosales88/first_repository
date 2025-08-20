BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
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
COMMIT;

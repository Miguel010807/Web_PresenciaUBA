CREATE TABLE "usuarios" (
	"id_usuario"	INTEGER NOT NULL UNIQUE,
	"nombre"	TEXT NOT NULL,
	"apellido"	TEXT NOT NULL,
	"dni"	VARCHAR(15) NOT NULL,
	"rol"	TEXT NOT NULL,
	"curso"	TEXT NOT NULL,
	"estado"	TEXT NOT NULL DEFAULT Activo,
	"correo"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_usuario" AUTOINCREMENT)
);

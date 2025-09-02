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

CREATE TABLE "materias" (
	"id_materia"	INTEGER NOT NULL UNIQUE,
	"nombre_materia"	TEXT NOT NULL,
	"aula"	VARCHAR(3) NOT NULL,
	"qr_materia"	TEXT NOT NULL UNIQUE,
	"id_usuario"	INTEGER NOT NULL,
	"horario"	TEXT NOT NULL,
	FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id_usuario"),
	PRIMARY KEY("id_materia" AUTOINCREMENT)
);

CREATE TABLE "sesiones" (
	"id_sesion"	INTEGER NOT NULL UNIQUE,
	"id_usuario"	INTEGER NOT NULL,
	"fecha_y_hora_inicial"	TEXT NOT NULL,
	"fecha_y_hora_final"	TEXT,
	"ip_dispositivo"	INTEGER,
	"ssid validado"	TEXT DEFAULT 'UBA-WiFi',
	FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id_usuario"),
	PRIMARY KEY("id_sesion" AUTOINCREMENT)
);
CREATE TABLE "presenciaGeneral" (
	"id_presencia_general"	INTEGER,
	"id_usuario"	INTEGER NOT NULL,
	"fecha"	TEXT NOT NULL,
	"hora_entrada"	TEXT NOT NULL,
	"hora_salida"	TEXT,
	"validacion_wifi"	INTEGER NOT NULL CHECK("validacion_wifi" IN (0, 1)),
	PRIMARY KEY("id_presencia_general" AUTOINCREMENT),
	FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id_usuario")
);

CREATE TABLE "asistenciaMateria" (
	"id_asistencia_materia"	INTEGER NOT NULL,
	"id_usuario"	INTEGER NOT NULL,
	"id_materia"	INTEGER NOT NULL,
	"fecha"	TEXT NOT NULL,
	"hora_registro"	TEXT NOT NULL,
	"qr_validado"	INTEGER NOT NULL CHECK(qr_svalidado IN (0,1)),
	FOREIGN KEY("id_usuario") REFERENCES "usuarios"("id_usuario"),
	FOREIGN KEY("id_materia") REFERENCES "materia"("id_materia"),
	PRIMARY KEY("id_asistencia_materia" AUTOINCREMENT)
);




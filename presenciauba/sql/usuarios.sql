-- Tabla Usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20),  -- opcional
    correo_institucional VARCHAR(150) UNIQUE NOT NULL,
    contraseña TEXT UNIQUE NOT NULL,
    rol ENUM('estudiante', 'docente', 'preceptor', 'admin') NOT NULL,
    carrera_curso VARCHAR(100),
    estado ENUM('activo', 'inactivo') DEFAULT 'activo'
);

INSERT INTO usuarios (correo_institucional, constraseña, nombre, apellido, rol)
VALUES ('tgomez@etec.uba.ar', 'thiago1234', "Thiago David", "Gomez Ovelar", 'estudiante'), --Thiago
       ('mdiaz@etec.uba.ar', 'miguel1234', 'Miguel Angel', 'Díaz', 'estudiante'), --Miguel
       ('pdellatorre@etec.uba.ar','priscila1234','Priscila Antonella','Della Torre', 'estudiante'), --Priscila
       ('fgvalerianoclaros@etec.uba.ar','gabriel1234','Fabian Gabriel','Valeriano Claro', 'estudiante'), --Gabriel
       ('jcari@etec.uba.ar','joel1234','Joel Agustin','Cari', 'estudiante'), --Joel
       ('bcamachouscamayta@etec@etec.uba.ar','briseida1234','Briseida Eva', 'Camacho Uscamayta', 'estudiante'), --Briseida
       ('luavia@etec.uba.ar','luciano1234','Luciano Uriel','Savia', 'estudiante'), --Lucho S
       ('lucianoalcaraz@etec.uba.ar','luciano123','Luciano','Alcaraz', 'estudiante'), --Lucho A
       ('baguirrepinaya@etec.uba.ar','brigit123','Brigit lisette','Aguirre Pinaya', 'estudiante'), --Brigit
       ('lslopez@etec.uba.ar','luana1234','Luana Sofia','Lopez', 'estudiante'), --Luana
       ('kdiaz@etec.uba.ar','karen1234','Karen Johana','Diaz', 'estudiante'), --Karen
       ('leonardoojeda@etec.uba.ar','leonardo1234','Leonardo','Ojeda', 'estudiante'), --Leonardo
       ('jbmendozacabrera@etec.uba.ar','julieta1234','Julieta Belen','Mendoza Cabrera', 'estudiante'), --Julieta
       ('acporcoflores@etec.uba.ar','ana123','Ana Cristina','Porco Flores', 'estudiante'), --Ana
       ('sperezramirez@etec.uba.ar','sol1234','Sol','Perez Ramirez', 'estudiante'), --Sol
       ('bumoyanocaruso@etec.uba.ar','bautista1234','Baustista Uriel','Mayono Caruso', 'estudiante'), --Bauti
    --Docentes   
       ('fvillace@etec.uba.ar', 'federico1234', 'Federico', 'Villace', 'docente'), --Fede
       ('tmayorga@etec.uba.ar','tomas1234','Tomas','Mayorga', 'docente'); --Tomas
       
       
contraseña TEXT UNIQUE NOT NULL,

-- Tabla Materias / Cursos
CREATE TABLE materias (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_materia VARCHAR(150) NOT NULL,
    aula VARCHAR(50) NOT NULL,
    qr_code VARCHAR(255) UNIQUE NOT NULL, -- hash único
    docente_responsable INT NOT NULL,
    horario VARCHAR(255),
    FOREIGN KEY (docente_responsable) REFERENCES usuarios(id_usuario)
);

-- Tabla Sesiones / Autenticaciones
CREATE TABLE sesiones (
    id_sesion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME,
    ip_dispositivo VARCHAR(45), -- IPv4 o IPv6
    ssid_validado VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla Asistencia General (entrada a la ETEC)
CREATE TABLE asistencia_general (
    id_asistencia_general INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME,
    validacion_wifi BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla Asistencia por Materia
CREATE TABLE asistencia_materia (
    id_asistencia_materia INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_materia INT NOT NULL,
    fecha DATE NOT NULL,
    hora_registro TIME NOT NULL,
    qr_validado BOOLEAN DEFAULT FALSE,
    dispositivo VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_materia) REFERENCES materias(id_materia)
);

-- Tabla Historial de Incidencias
CREATE TABLE incidencias (
    id_incidencia INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_incidencia VARCHAR(255) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

INSERT INTO usuarios (correo_institucional, constraseña, nombre, apellido)
VALUES ('mdiaz@etec.uba.ar', '12345678', 'Mario', 'Díaz');

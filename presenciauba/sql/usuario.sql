-- Tabla Usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20),  -- opcional
    correo_institucional VARCHAR(150) UNIQUE NOT NULL,
    rol ENUM('estudiante', 'docente', 'preceptor', 'admin') NOT NULL,
    carrera_curso VARCHAR(100),
    estado ENUM('activo', 'inactivo') DEFAULT 'activo'
);

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

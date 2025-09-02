from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20))
    correo_institucional = db.Column(db.String(150), unique=True, nullable=False)
    rol = db.Column(db.Enum("estudiante", "docente", "preceptor", "admin"), nullable=False)
    carrera_curso = db.Column(db.String(100))
    estado = db.Column(db.Enum("activo", "inactivo"), default="activo")

class Materia(db.Model):
    __tablename__ = "materias"
    id_materia = db.Column(db.Integer, primary_key=True)
    nombre_materia = db.Column(db.String(150), nullable=False)
    aula = db.Column(db.String(50), nullable=False)
    qr_code = db.Column(db.String(255), unique=True, nullable=False)
    docente_responsable = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    horario = db.Column(db.String(255))

class Sesion(db.Model):
    __tablename__ = "sesiones"
    id_sesion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_hora_inicio = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_hora_fin = db.Column(db.DateTime)
    ip_dispositivo = db.Column(db.String(45))
    ssid_validado = db.Column(db.String(100), nullable=False)

class AsistenciaGeneral(db.Model):
    __tablename__ = "asistencia_general"
    id_asistencia_general = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow().date(), nullable=False)
    hora_entrada = db.Column(db.Time, default=datetime.utcnow().time(), nullable=False)
    hora_salida = db.Column(db.Time)
    validacion_wifi = db.Column(db.Boolean, default=False)

class AsistenciaMateria(db.Model):
    __tablename__ = "asistencia_materia"
    id_asistencia_materia = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey("materias.id_materia"), nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow().date(), nullable=False)
    hora_registro = db.Column(db.Time, default=datetime.utcnow().time(), nullable=False)
    qr_validado = db.Column(db.Boolean, default=False)
    dispositivo = db.Column(db.String(50))

class Incidencia(db.Model):
    __tablename__ = "incidencias"
    id_incidencia = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"), nullable=False)
    tipo_incidencia = db.Column(db.String(255), nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

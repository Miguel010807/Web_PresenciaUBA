from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # Inicializa SQLAlchemy (ORM)

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), default="estudiante")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol
        }

# Modelo de Asistencia
class Asistencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    qr_code = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación: un usuario tiene muchas asistencias
    user = db.relationship("User", backref="asistencias")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "qr_code": self.qr_code,
            "fecha": self.fecha.isoformat()
        }

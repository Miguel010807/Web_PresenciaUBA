from flask import Flask, request, jsonify
from flask_cors import CORS #sirve para que el backend (Flask en este caso) permita peticiones desde un dominio diferente al suyo.
from models import db, User, Asistencia
from config import Config

app = Flask(__name__)
app.config.from_object(Config)  # Carga configuración desde config.py
CORS(app)  # Permite peticiones desde el frontend (React)

db.init_app(app)  # Inicializa la conexión a la base de datos


@app.route("/")
def index():
    # Ruta de prueba para ver si la API funciona
    return jsonify({"message": "Presencia UBA API funcionando 🚀"})


# Endpoint para login
@app.route("/login", methods=["POST"])
def login():
    data = request.json  # Recibe los datos en JSON
    correo = data.get("correo")
    password = data.get("password")

    # Busca un usuario con ese correo y contraseña
    user = User.query.filter_by(correo=correo, password=password).first()
    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Devuelve los datos del usuario
    return jsonify({"message": "Login exitoso", "user": user.to_dict()})


# Endpoint para registrar asistencia con QR
@app.route("/asistencia", methods=["POST"])
def registrar_asistencia():
    data = request.json
    user_id = data.get("user_id")
    qr_code = data.get("qr_code")

    # Busca al usuario en la base de datos
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Crea la asistencia
    asistencia = Asistencia(user_id=user.id, qr_code=qr_code)
    db.session.add(asistencia)
    db.session.commit()

    return jsonify({"message": "Asistencia registrada", "asistencia": asistencia.to_dict()})


# Endpoint para obtener asistencias de un usuario
@app.route("/asistencias/<int:user_id>", methods=["GET"])
def obtener_asistencias(user_id):
    asistencias = Asistencia.query.filter_by(user_id=user_id).all()
    return jsonify([a.to_dict() for a in asistencias])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)  # Ejecuta el servidor en modo debug

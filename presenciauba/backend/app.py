from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# -----------------------------
# ⚠️ CÓDIGO ORIGINAL (MYSQL)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://10.9.120.5:8080/PresenciaUBA'
# -----------------------------

# ✅ AHORA USAMOS SQLITE LOCAL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///presenciauba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# -----------------------------
# ⚠️ MODELO PARA USUARIOS (antes la tabla venía de MySQL)
# -----------------------------
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20))
    correo_institucional = db.Column(db.String(150), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), nullable=False)  # ('estudiante', 'docente', etc.)


@app.route("/")
def index():
    return jsonify({"message": "Presencia UBA API funcionando con SQLite"})


# Endpoint para login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")
    password = data.get("password")

    # -----------------------------
    # ⚠️ CONSULTA DIRECTA MYSQL (comentada)
    # query = "SELECT * FROM usuarios WHERE correo_institucional=%s AND contraseña=%s LIMIT 1"
    # result = db.session.execute(query, (correo, password)).fetchone()
    # -----------------------------

    # ✅ CONSULTA ORM SQLITE
    usuario = Usuario.query.filter_by(
        correo_institucional=correo,
        contraseña=password
    ).first()

    if not usuario:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Devuelve los datos del usuario como diccionario
    usuarios = {
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "correo_institucional": usuario.correo_institucional,
        "rol": usuario.rol
    }
    return jsonify({"message": "Login exitoso", "usuarios": usuarios})


if __name__ == "__main__":
    # ✅ Esto crea la DB si no existe
    with app.app_context():
        db.create_all()
    app.run(debug=True)
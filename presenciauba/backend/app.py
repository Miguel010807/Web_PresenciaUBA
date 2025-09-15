from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# Configuración de MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://10.9.120.5:8080/PresenciaUBA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/")
def index():
    return jsonify({"message": "Presencia UBA API funcionando"})


# Endpoint para login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")
    password = data.get("password")

    # Consulta directa a MySQL
    query = "SELECT * FROM usuarios WHERE correo_institucional=%s AND password=%s LIMIT 1"
    result = db.session.execute(query, (correo, password)).fetchone()

    if not result:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Devuelve los datos del usuario como diccionario
    user = dict(result.items())
    return jsonify({"message": "Login exitoso", "user": user})


# Endpoint para registrar asistencia con QR
@app.route("/asistencia", methods=["POST"])
def registrar_asistencia():
    data = request.json
    user_id = data.get("user_id")
    qr_code = data.get("qr_code")

    # Verifica que el usuario exista
    query_user = "SELECT * FROM usuarios WHERE id_usuario=%s"
    result_user = db.session.execute(query_user, (user_id,)).fetchone()
    if not result_user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Inserta la asistencia
    query_insert = "INSERT INTO asistencias (user_id, qr_code) VALUES (%s, %s)"
    db.session.execute(query_insert, (user_id, qr_code))
    db.session.commit()

    return jsonify({"message": "Asistencia registrada"})


# Endpoint para obtener asistencias de un usuario
@app.route("/asistencias/<int:user_id>", methods=["GET"])
def obtener_asistencias(user_id):
    query = "SELECT * FROM asistencias WHERE user_id=%s"
    results = db.session.execute(query, (user_id,)).fetchall()

    asistencias = [dict(row.items()) for row in results]
    return jsonify(asistencias)


if __name__ == "__main__":
    app.run(debug=True)

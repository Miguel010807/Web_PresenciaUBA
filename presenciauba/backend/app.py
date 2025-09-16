from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
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



if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de la conexión a MySQL desde el .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

# Función para obtener conexión
def get_connection():
    return pymysql.connect(**DB_CONFIG)

# Variable global para modo mantenimiento
MANTENIMIENTO = False

# --- RUTA LOGIN ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")
    password = data.get("password")

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = """
                SELECT correo_institucional, password
                FROM usuarios
                WHERE correo_institucional=%s AND password=%s
                LIMIT 1
            """
            cursor.execute(sql, (correo, password))
            user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "Credenciales inválidas"}), 401

        return jsonify({
            "message": "Login exitoso",
            "user": {
                "correo": user[0],
                "password": user[1]
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- RUTA MANTENIMIENTO ---
@app.route("/mantenimiento", methods=["POST"])
def toggle_mantenimiento():
    global MANTENIMIENTO
    MANTENIMIENTO = not MANTENIMIENTO
    estado = "en mantenimiento" if MANTENIMIENTO else "disponible"
    return jsonify({"message": f"El sistema está {estado}"}), 200


# --- FUNCIÓN DE CONTROL DE MANTENIMIENTO ---
def check_mantenimiento():
    if MANTENIMIENTO:
        return jsonify({"message": "El sistema está en mantenimiento. Intente más tarde."}), 503
    return None


# --- RUTA PARA ACTUALIZAR USUARIO ---
@app.route("/usuarios/<int:id_usuario>", methods=["PUT"])
def actualizar_usuario(id_usuario):
    mantenimiento_response = check_mantenimiento()
    if mantenimiento_response:
        return mantenimiento_response

    data = request.json
    nuevo_numero = data.get("numero")

    if not nuevo_numero:
        return jsonify({"error": "Falta el número de celular"}), 400

    try:
        db = get_connection()
        with db.cursor() as cursor:
            cursor.execute("SELECT numero FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            numero_celular = cursor.fetchone()

            if not numero_celular:
                return jsonify({"error": "Usuario no encontrado"}), 404

            cursor.execute("UPDATE usuarios SET numero = %s WHERE id_usuario = %s", (nuevo_numero, id_usuario))
            db.commit()

        db.close()
        return jsonify({"message": "Cambio exitoso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- EJECUCIÓN ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

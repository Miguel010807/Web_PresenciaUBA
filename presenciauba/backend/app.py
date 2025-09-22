from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de la conexión a MySQL
DB_CONFIG = {
    "host": "10.9.120.5",
    "user": "presencia",
    "password": "presencia1234",
    "database": "PresenciaUBA",
    "port": 3306
    ,  # Cambiar a 8080 si tu MySQL realmente escucha ahí
}

# Función para obtener conexión
def get_connection():
    return pymysql.connect(**DB_CONFIG)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")
    password = data.get("password")

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = """
                SELECT id_usuario, nombre, apellido, rol, estado
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
            "user": user
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/usuarios", methods=["GET", "POST"])
def get_usuarios():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "SELECT id_usuario, nombre, apellido, correo_institucional, rol, estado FROM usuarios"
            cursor.execute(sql)
            usuarios = cursor.fetchall()
        conn.close()

        return jsonify({
            "message": "Lista de usuarios",
            "usuarios": usuarios
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

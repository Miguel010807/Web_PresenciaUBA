from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de la conexión a MySQL

DB_CONFIG = {
    "host": "10.9.120.5",
    "user": "presencia", #<-- este es el Usuario para entrar al PHP
    "password": "presencia1234", #<-- este es el Password para entrar al PHP
    "database": "PresenciaUBA",
    "port": 3306
    ,  
}

# Función para obtener conexión
def get_connection():
    return pymysql.connect(**DB_CONFIG)


@app.route("/login", methods=["POST"]) #Funciona en postman
def login():
    data = request.json
    correo = data.get("correo")
    password = data.get("password")

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = """
            SELECT id_usuario, nombre, apellido, correo_institucional
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
        "id": user[0],
        "nombre": user[1],
        "apellido": user[2],
        "correo": user[3]
        }})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/usuarios", methods=["GET"]) #Funciona en postman
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
    app.run(host="0.0.0.0", port=5000, debug=True)


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


#Validacion de Login
@app.route("/login", methods=["POST"]) #Funciona en postman
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
        }})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Muestra los usuarios
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

#Cambiar datos(en este caso, el numero)
@app.route("/usuarios/<int:id_usuario>", methods=["PUT"]) #hay que probarlo en postman
def actualizar_usuario(id_usuario):
    data = request.json
    nuevo_celular = data.get("celular")

    if not nuevo_celular:
        return jsonify({"error": "Falta el número de celular"}), 400

    try:
        # Ver si el usuario existe y qué celular tiene
        cursor.execute("SELECT celular FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if not usuario["celular"] or usuario["celular"].strip() == "":#Este es en el caso que no tenga celular registrado(NULL)
            cursor.execute("UPDATE usuarios SET celular = %s WHERE id = %s", (nuevo_celular, id_usuario))
            db.commit()
            return jsonify({"message": "Celular agregado correctamente"}), 200
        else:                                                                #Este es en el caso que si tenga celular registrado(1132859054)
            cursor.execute("UPDATE usuarios SET celular = %s WHERE id = %s", (nuevo_celular, id_usuario))
            db.commit()
            return jsonify({"message": "Celular actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

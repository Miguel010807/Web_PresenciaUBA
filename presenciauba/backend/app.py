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
# @app.route("/usuarios", methods=["GET"]) #Funciona en postman
# def get_usuarios():
#     try:
#         conn = get_connection()
#         with conn.cursor() as cursor:
#             sql = "SELECT id_usuario, nombre, apellido, correo_institucional, rol, estado FROM usuarios"
#             cursor.execute(sql)  
#             usuarios = cursor.fetchall()
#         conn.close()

#         return jsonify({
#             "message": "Lista de usuarios",
#             "usuarios": usuarios
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# @app.route('/resource/<int:resource_id>', methods=['PUT'])
# def update_resource(resource_id):
#     # ... (code to handle the PUT request)
#     return f"Resource {resource_id} updated successfully."

#Cambiar datos(en este caso, el numero)
@app.route("/usuarios/<int:id_usuario>", methods=["PUT"]) #hay que probarlo en postman
def actualizar_usuario(id_usuario):
    # return f"Resource {id_usuario} updated successfully."

    data = request.json
    nuevo_numero = data.get("numero")

    print(nuevo_numero)
    if not nuevo_numero:
        return jsonify({"error": "Falta el número de celular"}), 400

    try:
        db=get_connection()
        cursor = db.cursor
        # Ver si el usuario existe y qué celular tiene
        cursor.execute("SELECT numero FROM usuarios WHERE id = %s", (str(id_usuario,)))
        numero_celular = cursor.fetchone()
        print(usuario)
        if not numero_celular:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        cursor.execute(f"UPDATE usuarios SET numero = {nuevo_numero} WHERE id={id_usuario}")
        return jsonify({"message":"Cambio exitoso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



####hay que hacer una parte que cuando nosotros editemos algo aparesca en la pantalla "En mantenimiento"

# Variable global para controlar el estado de mantenimiento
MANTENIMIENTO = False  # Si es True, el sistema está en mantenimiento

@app.route("/mantenimiento", methods=["POST"])
def toggle_mantenimiento():
    global MANTENIMIENTO
    MANTENIMIENTO = not MANTENIMIENTO  # Cambia el estado
    return jsonify({"message": f"El sistema está {'en mantenimiento' if MANTENIMIENTO else 'disponible'}"}), 200

# Función que se ejecuta para cada ruta de actualización o cambios
def check_mantenimiento():
    if MANTENIMIENTO:
        return jsonify({"message": "El sistema está en mantenimiento. Intente más tarde."}), 503
    return None  # No hay problemas si no está en mantenimiento

# Modificar la ruta de actualización de usuario para aplicar el mantenimiento
@app.route("/usuarios/<int:id_usuario>", methods=["PUT"]) 
def actualizar_usuario(id_usuario):
    mantenimiento_response = check_mantenimiento()
    if mantenimiento_response:
        return mantenimiento_response  # Si está en mantenimiento, retorna el mensaje

    data = request.json
    nuevo_numero = data.get("numero")

    if not nuevo_numero:
        return jsonify({"error": "Falta el número de celular"}), 400

    try:
        db = get_connection()
        cursor = db.cursor()

        cursor.execute("SELECT numero FROM usuarios WHERE id = %s", (str(id_usuario,)))
        numero_celular = cursor.fetchone()

        if not numero_celular:
            return jsonify({"error": "Usuario no encontrado"}), 404

        cursor.execute(f"UPDATE usuarios SET numero = {nuevo_numero} WHERE id={id_usuario}")
        return jsonify({"message": "Cambio exitoso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

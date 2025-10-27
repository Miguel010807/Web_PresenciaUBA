from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import datetime
import qrcode          # Para generar el código QR
import io              # Para manejar datos en memoria (usado en el buffer de la imagen)
import base64          # Para convertir la imagen QR a base64


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de la conexión a MySQL
DB_CONFIG = {
    "host": "10.9.120.5",
    "user": "presencia", # <--- Usuario para entrar a la base
    "password": "presencia1234", # <--- Contraseña para entrar a la base
    "database": "PresenciaUBA",
    "port": 3306,
}

# Función para obtener conexión a la base de datos
def get_connection():
    return pymysql.connect(**DB_CONFIG)

# Validación de Login (Endpoint POST)
@app.route("/login", methods=["POST"]) 
def login():
    data = request.json
    correo = data.get("correo")
    password = data.get("password")

    try:
        # Conexión a la base de datos
        conn = get_connection()
        with conn.cursor() as cursor:
            # Se consulta el correo y la contraseña, y también el rol
            sql = """
                SELECT id_usuario, nombre, apellido, correo_institucional, password, rol
                FROM usuarios
                WHERE correo_institucional=%s AND password=%s
                LIMIT 1
            """
            cursor.execute(sql, (correo, password))
            user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "Credenciales inválidas"}), 401

        # Responder con los datos del usuario, incluyendo el rol
        return jsonify({
            "message": "Login exitoso",
            "user": {
                "id_usuario": user[0],
                "nombre": user[1],
                "apellido": user[2],
                "correo_institucional": user[3],
                "password": user[4],
                "rol": user[5]  # Aquí se devuelve el rol (Estudiante/Docente)
            }
        })
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
        
        if not numero_celular:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        cursor.execute(f"UPDATE usuarios SET numero = {nuevo_numero} WHERE id={id_usuario}")
        return jsonify({"message":"Cambio exitoso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/asistencia", methods=["POST"])
def registrar_asistencia():
    try:
        db=get_connection()
        data = request.get_json()
        id_estudiante = data["id_estudiante"]
        id_clase = data["id_clase"]
        hora = datetime.now().strftime("%H:%M:%S")

        cursor = db.cursor()
        cursor.execute("""
            UPDATE asistencia_materia
            SET estado = 'Presente', hora_ingreso = %s
            WHERE id_estudiante = %s AND id_clase = %s
        """, (hora, id_estudiante, id_clase))
        db.commit()

        return jsonify({"mensaje": "Asistencia registrada con éxito"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generar_qr", methods=["POST"])
def generar_qr():
    data = request.get_json()
    numero_aula = data["numero_aula"]
    curso = data["curso"]
    materia = data["materia"]
    fecha = data["fecha"]

    # Contenido del QR
    contenido = f"Aula: {numero_aula}, Curso: {curso}, Materia: {materia}, Fecha: {fecha}"

    # Generar QR como imagen base64
    qr_img = qrcode.make(contenido)
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Guardar en MySQL
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO registro_qr (numero_aula, curso, materia, fecha, qr_contenido)
        VALUES (%s, %s, %s, %s, %s)
    """, (numero_aula, curso, materia, fecha, contenido))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "QR generado exitosamente",
        "qr_image": qr_base64
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




####hay que hacer una parte que cuando nosotros editemos algo aparesca en la pantalla "En mantenimiento"

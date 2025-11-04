from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import jwt
import os
import qrcode # Para generar el código QR 
import io # Para manejar datos en memoria (usado en el buffer de la imagen) 
import base64

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de la conexión a MySQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

# Configuración JWT
JWT_SECRET = os.getenv("JWT_SECRET", "mi_secreto_superseguro")
app.config["SECRET_KEY"] = JWT_SECRET   # Usar misma clave en todo el backend
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600  # 1 hora


# ------------------ LOGIN ------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")
    password = data.get("password")

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = """
                SELECT id_usuario, nombre, apellido, correo_institucional, password, rol
                FROM usuarios
                WHERE correo_institucional=%s
                LIMIT 1
            """
            cursor.execute(sql, (correo,))
            user = cursor.fetchone()
        conn.close()

        # Si no existe el usuario
        if not user:
            return jsonify({"error": "Credenciales inválidas"}), 401

        password_bd = user[4]

        # ✅ Compatibilidad: si la contraseña aún no está hasheada (texto plano)
        if password_bd == password:
            pass  # login permitido

        # ✅ Si está hasheada, usar check_password_hash
        elif check_password_hash(password_bd, password):
            pass  # login permitido

        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

        # Generar el JWT
        payload = {
            "id_usuario": user[0],
            "rol": user[5],
            "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "user": {
                "id_usuario": user[0],
                "nombre": user[1],
                "apellido": user[2],
                "correo_institucional": user[3],
                "rol": user[5]
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ------------------ MIDDLEWARE JWT ------------------
def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token faltante"}), 401

        try:
            data = jwt.decode(
                token,
                app.config["SECRET_KEY"],   # Ahora usa la misma clave
                algorithms=[JWT_ALGORITHM]
            )
            usuario_id = data["id_usuario"]

        except Exception as e:
            print("Error JWT:", e)
            return jsonify({"message": "Token inválido"}), 401

        return f(usuario_id, *args, **kwargs)

    return decorador


# ------------------ CAMBIAR CONTRASEÑA ------------------
@app.route("/cambiar_contrasena", methods=["POST"])
@token_requerido
def cambiar_contrasena(usuario_id):
    db = get_connection()
    data = request.get_json()
    actual = data.get("actual")
    nueva = data.get("nueva")

    if not actual or not nueva:
        return jsonify({"message": "Faltan datos"}), 400

    cursor = db.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()

    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    password_bd = usuario[0]

    # si la contraseña está hasheada o no
    if password_bd == actual or check_password_hash(password_bd, actual):
        nueva_hash = generate_password_hash(nueva)
        cursor.execute(
            "UPDATE usuarios SET password = %s WHERE id_usuario = %s",
            (nueva_hash, usuario_id)
        )
        db.commit()
        return jsonify({"message": "Contraseña actualizada correctamente"}), 200
    else:
        return jsonify({"message": "Contraseña actual incorrecta"}), 400



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


# @app.route("/asistencia", methods=["POST"])
# def registrar_asistencia():
#     try:
#         db=get_connection()
#         data = request.get_json()
#         id_estudiante = data["id_estudiante"]
#         id_clase = data["id_clase"]
#         hora = datetime.now().strftime("%H:%M:%S")

#         cursor = db.cursor()
#         cursor.execute("""
#             UPDATE asistencia_materia
#             SET estado = 'Presente', hora_ingreso = %s
#             WHERE id_estudiante = %s AND id_clase = %s
#         """, (hora, id_estudiante, id_clase))
#         db.commit()

#         return jsonify({"mensaje": "Asistencia registrada con éxito"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

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

@app.route("/registrar_asistencia", methods=["POST"])
def registrar_asistencia():
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    qr_data = data.get("qr_data")
    fecha = datetime.now().date()
    hora = datetime.now().strftime("%H:%M:%S")

    cursor = db.cursor()

    # Supongamos que en el QR viene el id_materia
    try:
        db=get_connection()
        cursor.execute("""
            INSERT INTO asistencia_materia (id_usuario, id_materia, fecha, hora_registro, qr_validado, dispositivo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, qr_data, fecha, hora, 1, "Navegador Web"))
        db.commit()
        return jsonify({"message": "Asistencia registrada correctamente"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        ssl_context=("certs/cert.crt", "certs/cert.key")
    )

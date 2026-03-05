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
import uuid
from flask import g


# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

 
    # Configuración de CORS
CORS(
        app, 
        # Añadimos la IP de la red por si el navegador la usa
        resources={r"/*": {"origins": [
            "https://localhost:5173", 
            "https://127.0.0.1:5173",
            "https://192.168.0.110:5173" 
        ]}},
        allow_headers=["Content-Type", "Authorization"], 
        supports_credentials=True, 
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

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

        #  Compatibilidad: si la contraseña aún no está hasheada (texto plano)
        if password_bd == password:
            pass  # login permitido

        # Si está hasheada, usar check_password_hash
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
                app.config["SECRET_KEY"],
                algorithms=[JWT_ALGORITHM]
            )

            g.usuario_id = data["id_usuario"]

        except Exception as e:
            print("Error JWT:", e)
            return jsonify({"message": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorador

# ------------------ CAMBIAR CONTRASEÑA ------------------
@app.route("/cambiar_contrasena", methods=["POST"])
@token_requerido
def cambiar_contrasena():
    usuario_id = g.usuario_id

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

#--------------------CAMBIAR NUMERO--------------------------
@app.route("/cambiar_numero", methods=["PUT"])
@token_requerido
def cambiar_numero():
    usuario_id = g.usuario_id
    try:
        data = request.get_json()
        numero_actual = data.get("numero_actual")
        numero_nuevo = data.get("numero_nuevo")

        if not numero_actual or not numero_nuevo:
            return jsonify({"message": "Faltan datos"}), 400

        db = get_connection()
        cursor = db.cursor()

        # Buscar número actual en base
        cursor.execute(
            "SELECT numero FROM usuarios WHERE id_usuario = %s",
            (usuario_id,)
        )
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        numero_bd = usuario[0]

        if numero_bd != numero_actual:
            return jsonify({"message": "Número actual incorrecto"}), 400

        # Actualizar número
        cursor.execute(
            "UPDATE usuarios SET numero = %s WHERE id_usuario = %s",
            (numero_nuevo, usuario_id)
        )

        db.commit()
        cursor.close()
        db.close()

        return jsonify({"message": "Número actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": "Error interno"}), 500


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


#--------------------------GENERAR QR------------------------------------
@app.route("/generar_qr", methods=["POST"])
@token_requerido
def generar_qr():
    try:
        data = request.get_json()

        numero_aula = data["numero_aula"]
        curso = data["curso"]
        materia = data["materia"]
        fecha = data["fecha"]

        id_clase = str(uuid.uuid4())

        db = get_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO registro_qr (id, numero_aula, curso, materia, fecha, fecha_creacion)
            VALUES ( %s, %s, %s, %s, %s, %s)
        """, (id_clase, numero_aula, curso, materia, fecha, datetime.now()))

        db.commit()

        url_qr = f"http://10.56.13.31:5000/registrar_asistencia?id={id_clase}"

        qr_img = qrcode.make(url_qr)
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return jsonify({"qr": qr_base64, "id": id_clase})

    except Exception as e:
        print("Error interno:", e)
        return jsonify({"error": "Error interno"}), 500

#-------------------REGISTRAR ASISTENCIA(RUTAS PARAMETRIZADAS)------------------------
@app.route("/asistencias/clases/<int:id_clase>/estudiantes/<int:usuario_id>", methods=["POST"])
@token_requerido
def registrar_asistencia(id_clase, usuario_id):
    try:
        fecha = datetime.now().date()
        hora = datetime.now().strftime("%H:%M:%S")

        db = get_connection()
        cursor = db.cursor()

        cursor.execute("""
            SELECT id_materia FROM clases WHERE id = %s
        """, (id_clase,))
        clase = cursor.fetchone()

        if not clase:
            return jsonify({"error": "Clase no encontrada"}), 404

        id_materia = clase[0]

        # Verificar asistencia existente
        cursor.execute("""
            SELECT id_asistencia_materia 
            FROM asistencia_materia
            WHERE id_usuario = %s 
            AND id_materia = %s 
            AND fecha = %s
        """, (usuario_id, id_materia, fecha))

        existente = cursor.fetchone()

        if existente:
            cursor.execute("""
                UPDATE asistencia_materia
                SET qr_validado = 1,
                    hora_registro = %s,
                    dispositivo = %s
                WHERE id_usuario = %s 
                AND id_materia = %s 
                AND fecha = %s
            """, (hora, "Navegador Web", usuario_id, id_materia, fecha))
        else:
            cursor.execute("""
                INSERT INTO asistencia_materia
                (id_usuario, id_materia, fecha, hora_registro, qr_validado, dispositivo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (usuario_id, id_materia, fecha, hora, 1, "Navegador Web"))

        db.commit()
        cursor.close()
        db.close()

        return jsonify({"message": "Asistencia registrada correctamente"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Error interno"}), 500

@app.route("/mi_asistencia", methods=["GET"])
@token_requerido
def mi_asistencia(usuario_id):
    try:
        db = get_connection()
        cursor = db.cursor()

        cursor.execute("""
            SELECT m.nombre, a.fecha, a.hora_registro, a.qr_validado
            FROM asistencia_materia a
            JOIN materias m ON a.id_materia = m.id_materia
            WHERE a.id_usuario = %s
            ORDER BY a.fecha DESC
        """, (usuario_id,))

        resultados = cursor.fetchall()

        asistencias = []

        for fila in resultados:
            asistencias.append({
                "materia": fila[0],
                "fecha": str(fila[1]),
                "hora": fila[2],
                "estado": "Presente" if fila[3] == 1 else "Ausente"
            })

        cursor.close()
        db.close()

        return jsonify({
            "total": len(asistencias),
            "asistencias": asistencias
        }), 200

    except Exception as e:
        print("Error en mi_asistencia:", e)
        return jsonify({"error": "Error interno"}), 500




if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
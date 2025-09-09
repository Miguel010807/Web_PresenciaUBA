from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configuración de conexión MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tu_password",
    database="presencia_uba"  # tu base de datos
    port=8080
)

cursor = db.cursor(dictionary=True)  # dictionary=True => resultados como diccionarios


@app.route("/api/usuario", methods=["POST"])
def usuario():
    sql = """
        INSERT INTO usuarios (nombre, apellido, dni, correo_institucional, rol, curso)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = ("Miguel Angel", "Diaz", "48117823", "mdiaz@etec.uba.ar", "estudiante", "5B")

    try:
        cursor.execute(sql, values)
        db.commit()
        return jsonify({
            "message": "Usuario insertado con éxito",
            "id_usuario": cursor.lastrowid
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="10.9.120.5", port=8080, debug=True)
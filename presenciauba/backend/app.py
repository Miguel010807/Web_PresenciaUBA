from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Usuario, Materia, AsistenciaGeneral, AsistenciaMateria, Incidencia
from config import Config
import jwt, datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# -------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")

    if not correo.endswith("@etec.uba.ar"):
        return jsonify({"error": "Correo inválido"}), 401

    usuario = Usuario.query.filter_by(correo_institucional=correo).first()
    if not usuario:
        return jsonify({"error": "Usuario no registrado"}), 404

    token = jwt.encode(
        {"user_id": usuario.id_usuario, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)},
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token": token, "usuario": {"id": usuario.id_usuario, "nombre": usuario.nombre}})

# -------- ASISTENCIA GENERAL ----------
@app.route("/asistencia/general", methods=["POST"])
def asistencia_general():
    data = request.json
    user_id = data.get("usuario_id")

    asistencia = AsistenciaGeneral(id_usuario=user_id)
    db.session.add(asistencia)
    db.session.commit()

    return jsonify({"msg": "Asistencia general registrada"})

# -------- ASISTENCIA POR MATERIA ----------
@app.route("/asistencia/materia", methods=["POST"])
def asistencia_materia():
    data = request.json
    user_id = data.get("usuario_id")
    materia_id = data.get("materia_id")

    asistencia = AsistenciaMateria(id_usuario=user_id, id_materia=materia_id, qr_validado=True)
    db.session.add(asistencia)
    db.session.commit()

    return jsonify({"msg": "Asistencia en materia registrada"})

# -------- LISTAR ASISTENCIAS ----------
@app.route("/asistencias/<int:user_id>", methods=["GET"])
def listar_asistencias(user_id):
    generales = AsistenciaGeneral.query.filter_by(id_usuario=user_id).all()
    materias = AsistenciaMateria.query.filter_by(id_usuario=user_id).all()

    result = {
        "general": [{"fecha": g.fecha.isoformat(), "hora_entrada": str(g.hora_entrada)} for g in generales],
        "materias": [{"materia": m.id_materia, "fecha": m.fecha.isoformat(), "hora": str(m.hora_registro)} for m in materias]
    }
    return jsonify(result)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

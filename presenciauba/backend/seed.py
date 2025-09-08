from app import app, db
from models import Usuario, Materia

with app.app_context():
    db.drop_all()
    db.create_all()

    u1 = Usuario(nombre="Thiago", apellido="Gomez", correo_institucional="tgomez@etec.uba.ar", rol="estudiante")
    u2 = Usuario(nombre="Gabriel", apellido="Valeriano", correo_institucional="mdiaz@etec.uba.ar", rol="estudiante")
    u3 = Usuario(nombre="Miguel", apellido="Díaz", correo_institucional="sperezramirez@etec.uba.ar", rol="estudiante")

    m1 = Materia(nombre_materia="Matemática", aula="101", qr_code="qr-mate-123", docente_responsable=1, horario="08:00-09:30")
    m2 = Materia(nombre_materia="Historia", aula="102", qr_code="qr-hist-456", docente_responsable=1, horario="10:00-11:30")

    db.session.add_all([u1, u2, u3, m1, m2])
    db.session.commit()

    print("Datos cargados correctamente")

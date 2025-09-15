from app import app, db
from models import User

# Script para crear usuarios de prueba
with app.app_context():
    db.create_all()

    if not User.query.first():
        usuarios = [
            User(nombre="Thiago Gomez", correo="tgomez@etec.uba.ar", password="1234", rol="estudiante"),
            User(nombre="Miguel Diaz", correo="mdiaz@etec.uba.ar", password="abcd", rol="docente"),
        ]
        db.session.add_all(usuarios)
        db.session.commit()
        print("Usuarios iniciales cargados ")
    else:
        print("Ya existen usuarios, no se cargó nada.")

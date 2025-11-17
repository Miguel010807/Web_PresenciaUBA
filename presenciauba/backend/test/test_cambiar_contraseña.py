import jwt
from app import JWT_SECRET, JWT_ALGORITHM


def test_cambiar_contrasena_ok(client):

    # Creamos token válido
    token = jwt.encode({"id_usuario": 1}, JWT_SECRET, algorithm=JWT_ALGORITHM)

    resp = client.post(
        "/cambiar_contrasena",
        json={"actual": "miguel1234", "nueva": "admin12345"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 200
    assert resp.json["message"] == "Contraseña actualizada correctamente"


def test_cambiar_contrasena_incorrecta(client):

    token = jwt.encode({"id_usuario": 1}, JWT_SECRET, algorithm=JWT_ALGORITHM)

    resp = client.post(
        "/cambiar_contrasena",
        json={"actual": "ArturoVidal", "nueva": "admin12345"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 400
    assert resp.json["message"] == "Contraseña actual incorrecta"



#<----- funciona solo que tengo que usarlo con datos mockeados
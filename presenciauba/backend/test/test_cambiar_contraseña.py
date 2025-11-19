import jwt
from app import JWT_SECRET, JWT_ALGORITHM


def generar_token(id_usuario):
    return jwt.encode({"id_usuario": id_usuario}, JWT_SECRET, algorithm=JWT_ALGORITHM)


def test_cambiar_contrasena_ok(client, mock_db):
    token = generar_token(1)
    mock_cursor = mock_db.cursor.return_value

    # la contraseña almacenada coincide
    mock_cursor.fetchone.return_value = ("1234",)

    resp = client.post("/cambiar_contrasena",
        json={"actual": "1234", "nueva": "abcd"},
        headers={"Authorization": f"Bearer {token}"}
    )
 
    assert resp.status_code == 200
    assert resp.json["message"] == "Contraseña actualizada correctamente"


def test_cambiar_contrasena_incorrecta(client, mock_db):
    token = generar_token(1)
    mock_cursor = mock_db.cursor.return_value

    # guardada y actual NO coinciden
    mock_cursor.fetchone.return_value = ("1234",)

    resp = client.post("/cambiar_contrasena",
        json={"actual": "9999", "nueva": "abcd"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert resp.status_code == 400

#<----- funciona solo que tengo que usarlo con datos mockeados
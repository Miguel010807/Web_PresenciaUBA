import jwt
from datetime import datetime, timedelta
from unittest.mock import MagicMock

JWT_SECRET = "mi_secreto_superseguro"
JWT_ALGORITHM = "HS256"


def generar_token(id_usuario): #<--- genera un token
    payload = {
        "id_usuario": id_usuario, #<--- usuario para el token
        "exp": datetime.utcnow() + timedelta(minutes=10) #<--- el tiempo en el que vence el token
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def test_registrar_asistencia_ok(client, mocker):
    token = generar_token(id_usuario=1) #<--- genera un usuario autentico(alumno)

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Orden de llamadas fetchone():
    # 1️⃣ SELECT id_materia FROM clases
    # 2️⃣ SELECT asistencia existente
    mock_cursor.fetchone.side_effect = [
        (10,),     # id_materia
        None       # no existe asistencia previa
    ]

    mocker.patch("app.get_connection", return_value=mock_conn)

    # -------------------------
    # 3. Request simulada
    # -------------------------
    response = client.post(
        "/registrar_asistencia?id=UUID_TEST",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    assert response.json["message"] == "Asistencia registrada correctamente"

    # INSERT ejecutado
    mock_cursor.execute.assert_called()
    mock_conn.commit.assert_called_once()
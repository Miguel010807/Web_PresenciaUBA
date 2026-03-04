import pytest
from unittest.mock import patch, MagicMock
import jwt
from datetime import datetime, timedelta


@pytest.fixture
def token_valido():
    return jwt.encode(
        {
            "id_usuario": 1,
            "rol": "alumno",
            "exp": datetime.utcnow() + timedelta(minutes=5)
        },
        "mi_secreto_superseguro",
        algorithm="HS256"
    )


# 🧪 TEST: número correcto
@patch("app.get_connection")
def test_cambiar_numero_correcto(mock_get_connection, client, token_valido):

    # 🔹 Crear conexión falsa
    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor

    # 🔹 Simulamos que el número actual en BD es 1122334455
    mock_cursor.fetchone.return_value = ("1122334455",)

    response = client.put(
        "/cambiar_numero",
        json={
            "numero_actual": "1122334455",
            "numero_nuevo": "1199988877"
        },
        headers={"Authorization": f"Bearer {token_valido}"}
    )

    assert response.status_code == 200
    assert response.json["message"] == "Número actualizado correctamente"

    # 🔍 Verificar que se llamó al UPDATE
    mock_cursor.execute.assert_any_call(
        "UPDATE usuarios SET numero = %s WHERE id_usuario = %s",
        ("1199988877", 1)
    )

    # 🔍 Verificar commit
    mock_db.commit.assert_called_once()

@patch("app.get_connection")

def test_cambiar_numero_incorrecto(mock_get_connection, client, token_valido):

    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor

    # 🔹 En BD el número es diferente
    mock_cursor.fetchone.return_value = ("1122334455",)

    response = client.put(
        "/cambiar_numero",
        json={
            "numero_actual": "0000000000",  # incorrecto
            "numero_nuevo": "1199988877"
        },
        headers={"Authorization": f"Bearer {token_valido}"}
    )

    assert response.status_code == 400
    assert response.json["message"] == "Número actual incorrecto"

    # 🔍 Verificar que NO se hizo commit
    mock_db.commit.assert_not_called()
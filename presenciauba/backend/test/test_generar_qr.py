import base64
from unittest.mock import MagicMock

def test_generar_qr_ok(client, mocker):
    # --- Mock DB ---
    mock_conn = MagicMock() #<---- db
    mock_cursor = MagicMock() #<---- cursor = db.cursor()
    mock_conn.cursor.return_value = mock_cursor

    mocker.patch("app.get_connection", return_value=mock_conn) #<---- db = get_connection()

    payload = {
        "numero_aula": "101",
        "curso": "5to 1ra",
        "materia": "Matemática",
        "fecha": "2025-11-26"
    }
    response = client.post("/generar_qr", json=payload)
    assert response.status_code == 200 

    data = response.json

    # Debe venir un ID
    assert "id" in data
    assert isinstance(data["id"], str)

    # Debe venir un QR en base64
    assert "qr" in data
    qr = data["qr"]

    # Verifica que sea base64 válido
    try:
        base64.b64decode(qr)
    except Exception:
        assert False, "El QR no es un base64 válido"

    # Verifica que se haya llamado el INSERT
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()



def test_generar_qr_db_error(client, mocker):
    # Simula que get_connection explota
    mocker.patch("app.get_connection", side_effect=Exception("DB error"))

    payload = {
        "numero_aula": "101",
        "curso": "5",
        "materia": "Matemática",
        "fecha": "2025-11-26"
    }

    response = client.post("/generar_qr", json=payload)

    # Debe devolver error interno
    assert response.status_code == 500
    assert response.json == {"error": "Error interno"}
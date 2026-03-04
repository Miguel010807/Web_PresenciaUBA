import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


@patch("app.get_connection")
def test_registrar_asistencia_insert(mock_get_connection, client, token_valido):
    """
    Caso 1:
    - La clase existe
    - No hay asistencia previa
    - Debe hacer INSERT
    """

    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor

    # 🔹 Primera consulta: SELECT id_materia FROM clases
    # 🔹 Segunda consulta: SELECT asistencia existente
    mock_cursor.fetchone.side_effect = [
        (1,),      # Clase encontrada
        None       # No existe asistencia previa
    ]

    response = client.post(
        "/asistencias/clases/1/estudiantes/5",
        headers={"Authorization": f"Bearer {token_valido}"}
    )

    assert response.status_code == 200
    assert b"Asistencia registrada correctamente" in response.data

    # Verificar que se hizo INSERT
    assert mock_cursor.execute.call_count >= 3
    mock_db.commit.assert_called_once()


@patch("app.get_connection")
def test_registrar_asistencia_update(mock_get_connection, client, token_valido):
    """
    Caso 2:
    - La clase existe
    - Ya hay asistencia previa
    - Debe hacer UPDATE
    """

    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor

    # 🔹 Primera consulta: Clase encontrada
    # 🔹 Segunda consulta: Asistencia existente
    mock_cursor.fetchone.side_effect = [
        (1,),     # Clase encontrada
        (10,)     # Asistencia ya existente
    ]

    response = client.post(
        "/asistencias/clases/1/estudiantes/5",
        headers={"Authorization": f"Bearer {token_valido}"}
    )

    assert response.status_code == 200
    mock_db.commit.assert_called_once()
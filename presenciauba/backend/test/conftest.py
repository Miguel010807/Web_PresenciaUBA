import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app import app


# ----------------------------
# CONFIGURACIÓN GENERAL TEST
# ----------------------------
@pytest.fixture(scope="session")
def client():
    """
    Cliente de pruebas para Flask.
    """
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "mi_secreto_superseguro"

    with app.test_client() as client:
        yield client


# ----------------------------
# TOKEN JWT VÁLIDO
# ----------------------------
@pytest.fixture
def token_valido():
    """
    Genera un token JWT válido para pruebas.
    """
    payload = {
        "id_usuario": 5,
        "rol": "estudiante",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return token


# ----------------------------
# MOCK BASE DE DATOS GLOBAL
# ----------------------------
@pytest.fixture
def mock_db():
    """
    Mockea completamente la conexión a la base de datos.
    Evita tocar MySQL real.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch("app.get_connection", return_value=mock_conn):
        yield mock_conn
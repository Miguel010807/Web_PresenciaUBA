import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    """
    Cliente de pruebas para Flask.
    """
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db():
    """
    Mockea get_connection() y pymysql.connect.
    Crea una conexión y cursor falsos totalmente funcionales.
    """
    # Creamos objetos falsos
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # El cursor del mock debe devolver el mock_cursor
    mock_conn.cursor.return_value = mock_cursor

    # Para endpoints con get_connection()
    with patch("app.get_connection", return_value=mock_conn):
        # Para endpoints que usan pymysql.connect directamente
        with patch("pymysql.connect", return_value=mock_conn):
            yield mock_conn

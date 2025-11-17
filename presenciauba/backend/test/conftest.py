import pytest
import pymysql
from unittest.mock import patch
from app import app, get_connection


@pytest.fixture
def client():
    """
    Crea un cliente de prueba para pytest.
    Además pone el backend en modo TESTING.
"""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db():
    """
    Mockea la conexión MySQL para evitar usar la base real.
    Reemplaza get_connection() por un objeto falso.
"""
    with patch("app.get_connection") as mock_conn:
        # objeto conexión falso
        mock_connection = patch("pymysql.connect").start()

        mock_conn.return_value = mock_connection
        yield mock_connection

        patch.stopall()

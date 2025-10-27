import pytest
from app import app  # importa tu Flask app principal

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

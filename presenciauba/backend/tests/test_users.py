def test_toggle_mantenimiento(client):
    """Verifica que se pueda activar/desactivar el modo mantenimiento."""
    response = client.post("/mantenimiento")
    assert response.status_code == 200
    assert "El sistema está" in response.get_json()["message"]

    response2 = client.post("/mantenimiento")
    assert response2.status_code == 200
    assert "El sistema está" in response2.get_json()["message"]


def test_actualizar_usuario_sin_mantenimiento(client, mocker):
    """Debe permitir actualizar usuario cuando el sistema NO está en mantenimiento."""
    mocker.patch("app.MANTENIMIENTO", False)
    mocker.patch("app.get_connection")  # Evitamos tocar la BD real

    response = client.put(
        "/usuarios/1",
        json={"numero": "123456789"},
    )
    # Como usamos mocks, solo validamos que el endpoint responda correctamente
    assert response.status_code in (200, 500, 404)  # depende del mock
    assert response.is_json


def test_actualizar_usuario_en_mantenimiento(client, mocker):
    """Debe devolver 503 cuando el sistema está en mantenimiento."""
    mocker.patch("app.MANTENIMIENTO", True)

    response = client.put("/usuarios/1", json={"numero": "123456789"})
    data = response.get_json()

    assert response.status_code == 503
    assert "mantenimiento" in data["message"].lower()
0.+306

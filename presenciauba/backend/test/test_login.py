def test_login_ok(client):

    resp = client.post("/login", json={
        "correo": "mdiaz@etec.uba.ar",
        "password": "miguel1234"  # <---- Como estoy usando datos reales, esto lo voy a tener que mover
    })                            # a menos que lo mockee

    assert resp.status_code == 200
    assert resp.json["message"] == "Login exitoso"

def test_login_incorecto(client):
    resp = client.post("/login", json={
        "correo": "error@etec.uba.ar",
        "password": "error1"

    })

    assert resp.status_code == 401
    assert resp.json["error"] == "Credenciales inválidas"
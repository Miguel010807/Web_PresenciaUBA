def test_generar_qr(client, mock_db):
    data = {
        "numero_aula": "305",
        "curso": "5B",
        "materia": "Programación",
        "fecha": "2025-11-20"
    }

    resp = client.post("/generar_qr", json=data)

    assert resp.status_code == 200
    assert "qr_image" in resp.json
    assert resp.json["message"] == "QR generado exitosamente"
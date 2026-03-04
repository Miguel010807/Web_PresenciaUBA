##def test_mi_asistencia(client, token_valido):
##    response = client.get(
##        "/mi_asistencia",
##        headers={"Authorization": f"Bearer {token_valido}"}
##    )
##
##    assert response.status_code in [200, 404] ##
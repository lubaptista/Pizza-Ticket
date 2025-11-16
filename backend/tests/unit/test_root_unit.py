def test_route_not_found(client):
    resp = client.get("/rota_inexistente")
    assert resp.status_code == 404

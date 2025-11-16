def test_listar_itens(client):
    resp = client.get("/itens/")
    assert resp.status_code == 200
    assert isinstance(resp.json, list)

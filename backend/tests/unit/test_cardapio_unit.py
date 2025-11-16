def test_listar_cardapio(client):
    resp = client.get("/cardapio/")
    assert resp.status_code == 200
    assert isinstance(resp.json, list)

def test_criar_pedido_dados_invalidos(client):
    resp = client.post("/pedidos/criar", json={})
    assert resp.status_code == 400

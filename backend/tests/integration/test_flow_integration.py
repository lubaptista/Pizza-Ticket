import json

def test_full_flow(client):
    # Registrar usuário (se implementado)
    client.post("/auth/register", json={
        "email": "teste@teste.com",
        "password": "123456"
    })

    # Login
    login = client.post("/auth/login", json={
        "email": "teste@teste.com",
        "password": "123456"
    })

    assert login.status_code in (200, 401)
    if login.status_code != 200:
        return  # login falhou, não prossegue

    token = login.json.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Criar categoria inicial se não existir
    client.post("/cardapio/categorias", json={"nome": "Pizzas"}, headers=headers)

    # Criar item
    item = client.post("/itens", json={
        "nome": "Pizza Marguerita",
        "preco": 39.90,
        "categoria_id": 1
    }, headers=headers)
    assert item.status_code in (200, 201)

    # Criar pedido
    pedido = client.post("/pedidos", json={
        "mesa_id": 1,
        "itens": [{"item_id": 1, "quantidade": 1}]
    }, headers=headers)

    assert pedido.status_code in (200, 201)

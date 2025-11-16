def test_pedido_status_changes(client, app):
    # Criar mesa no banco antes
    from models import db, Mesa

    with app.app_context():
        mesa = Mesa(label="Mesa Teste")
        db.session.add(mesa)
        db.session.commit()
        mesa_id = mesa.id

    # Criar pedido básico
    resp = client.post("/pedidos/criar", json={
        "mesa": mesa_id,
        "itens": []
    })
    assert resp.status_code == 201

    pedido_id = resp.json.get("id")

    # Atualiza status do pedido
    r = client.patch(f"/pedidos/{pedido_id}/status", json={"status": "preparando"})
    assert r.status_code == 200

    r2 = client.patch(f"/pedidos/{pedido_id}/status", json={"status": "finalizado"})
    assert r2.status_code == 200

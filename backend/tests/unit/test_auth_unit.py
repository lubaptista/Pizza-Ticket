def test_login_invalid_credentials(client):
    resp = client.post("/auth/login", json={
        "email": "naoexiste@teste.com",
        "password": "123456"
    })
    assert resp.status_code == 401

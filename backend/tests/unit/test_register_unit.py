def test_register_missing_fields(client):
    resp = client.post("/auth/register", json={})
    assert resp.status_code == 400
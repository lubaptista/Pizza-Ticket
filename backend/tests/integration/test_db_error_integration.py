from models import db

def test_db_failure_simulation(app, client, monkeypatch):
    # Simula exceção forçada no banco
    def fail(*a, **k):
        raise Exception("Simulated DB failure")

    monkeypatch.setattr(db.session, "execute", fail)

    resp = client.get("/pedidos/")
    assert resp.status_code in (500, 503)

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app
from models import db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True

    # IMPORTANTE:
    # - Em SQLite local → cria DB temporário em memória
    # - Em Docker/Postgres → usa DATABASE_URL já injetada
    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

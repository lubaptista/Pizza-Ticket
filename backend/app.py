from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes.auth import auth_bp
from routes.pedidos import pedidos_bp
from routes.cardapio import cardapio_bp
from routes.itens import itens_bp
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa banco e JWT
    db.init_app(app)
    jwt = JWTManager(app)

    # CORS – híbrido (Docker usa localhost)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(pedidos_bp, url_prefix="/pedidos")
    app.register_blueprint(cardapio_bp, url_prefix="/cardapio")
    app.register_blueprint(itens_bp)

    return app


# Executar localmente (não usado no Docker)
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=5000)

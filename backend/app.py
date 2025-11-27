# backend/app.py
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db
from .routes.auth import auth_bp
from .routes.pedidos import pedidos_bp
from .routes.cardapio import cardapio_bp
from .routes.itens import itens_bp

def create_app(testing=False):
    app = Flask(__name__)
    
    # 1. Configuração Dinâmica do Banco de Dados
    # Usa a variável de ambiente (setada no docker-compose) ou SQLite como fallback
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        # Padrão para desenvolvimento local com SQLite
        database_url = 'sqlite:///instance/database.db' 

    # Configurações do App
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta")
    
    db.init_app(app)
    JWTManager(app)
    
    # Configuração do CORS (Mantenha o seu código, ajustado para ser dinâmico no ambiente de teste)
    CORS(app, origins="*", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])

    # Registro de Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth") 
    app.register_blueprint(pedidos_bp, url_prefix="/pedidos")
    app.register_blueprint(cardapio_bp, url_prefix="/cardapio")
    app.register_blueprint(itens_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Apenas cria o DB se for SQLite ou se for o primeiro boot do Postgres
        db.create_all()
    # Use 0.0.0.0 para que o container exponha a porta corretamente
    app.run(host="0.0.0.0", debug=True, port=5000)
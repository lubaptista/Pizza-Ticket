from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes.auth import auth_bp
from routes.pedidos import pedidos_bp
from routes.cardapio import cardapio_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "sua_chave_secreta"

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Rota de login/logout, geração de JWT:
app.register_blueprint(auth_bp, url_prefix="/auth") 
# Rota para abrir pedido, listar, atualizar status:
app.register_blueprint(pedidos_bp, url_prefix="/pedidos")
# Rota paar realizar CRUD de categorias e itens:
app.register_blueprint(cardapio_bp, url_prefix="/cardapio")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

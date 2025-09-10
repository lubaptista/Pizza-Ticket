from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'garcom' ou 'cozinha' ou 'admin'

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey("mesa.id"), nullable=False)
    status = db.Column(db.String(20), default="aberto")  # aberto, preparando, finalizado
    
    itens = db.relationship('PedidoItem', backref='pedido', lazy=True)

class PedidoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantidade = db.Column(db.Integer, default=1)
    item = db.relationship('Item', backref='pedido_itens')
    status = db.Column(db.String(20), default="aberto")

class Mesa(db.Model):
    __tablename__ = "mesa"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)
    ocupada = db.Column(db.Boolean, default=False)

    pedidos = db.relationship("Pedido", backref="mesa", lazy=True)
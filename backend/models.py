from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=True)  # pode ser null p/ compatibilidade
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, garcom, cozinha, user


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

    # ⚠️ ATENÇÃO: SQLite não aplica default antes de persistir
    # por isso precisamos do __init__
    ocupada = db.Column(db.Boolean, default=False, nullable=False)

    pedidos = db.relationship("Pedido", backref="mesa", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Garante que o valor default seja aplicado ao objeto Python
        if self.ocupada is None:
            self.ocupada = False

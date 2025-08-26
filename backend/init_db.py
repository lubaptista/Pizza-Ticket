from werkzeug.security import generate_password_hash
from app import app
from models import db, Usuario, Categoria, Item, Pedido, PedidoItem

def init_db():
    with app.app_context():
        # Apaga e recria o banco
        db.drop_all()
        db.create_all()

        # Usuários iniciais
        usuarios = [
            Usuario(nome="Administrador", email="admin@pizzaria.com", password=generate_password_hash("123456"), role="admin"),
            Usuario(nome="Garçom", email="garcom@pizzaria.com", password=generate_password_hash("123456"), role="garcom"),
            Usuario(nome="Cozinha", email="cozinha@pizzaria.com", password=generate_password_hash("123456"), role="cozinha"),
        ]
        db.session.add_all(usuarios)

        # Categorias
        categorias = [
            Categoria(nome="Pizzas"),
            Categoria(nome="Bebidas"),
        ]
        db.session.add_all(categorias)
        db.session.commit()

        # Itens (já vinculados às categorias)
        itens = [
            Item(nome="Pizza Mussarela", preco=40.0, categoria_id=categorias[0].id),
            Item(nome="Pizza Calabresa", preco=45.0, categoria_id=categorias[0].id),
            Item(nome="Refrigerante Lata", preco=6.0, categoria_id=categorias[1].id),
            Item(nome="Cerveja Long Neck", preco=9.0, categoria_id=categorias[1].id),
        ]
        db.session.add_all(itens)
        db.session.commit()

        print("✅ Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db()

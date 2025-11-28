import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario, Item, Pedido, Mesa, Categoria
from app import app


@pytest.fixture
def client():
    """Fixture para criar um cliente de teste"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            from models import db
            db.create_all()
        yield client


# ======================================================
# 1) USUÁRIO – 2 TESTES
# ======================================================

def test_usuario_creation(client):
    """Testa a criação de um usuário"""
    with app.app_context():
        from models import db
        usuario = Usuario(
            nome="Teste",
            email="teste@teste.com",
            password=generate_password_hash("senha123"),
            role="garcom"
        )
        db.session.add(usuario)
        db.session.commit()
        
        assert usuario.id is not None
        assert usuario.email == "teste@teste.com"
        assert usuario.role == "garcom"


def test_password_hashing(client):
    """Testa hashing de senha"""
    senha = "senha123"
    senha_hash = generate_password_hash(senha)

    assert senha_hash != senha
    assert check_password_hash(senha_hash, senha)
    assert not check_password_hash(senha_hash, "errada")


# ======================================================
# 2) ITEM – 2 TESTES
# ======================================================

def test_item_creation(client):
    """Testa criação de item"""
    with app.app_context():
        from models import db
        categoria = Categoria(nome="Pizza")
        db.session.add(categoria)
        db.session.commit()
        
        item = Item(nome="Pizza Calabresa", preco=42.0, categoria_id=categoria.id)
        db.session.add(item)
        db.session.commit()
        
        assert item.id is not None
        assert item.preco == 42.0
        assert item.categoria_id == categoria.id


def test_item_price_validation(client):
    """Testa se o preço do item é válido"""
    with app.app_context():
        from models import db
        categoria = Categoria(nome="Bebidas")
        db.session.add(categoria)
        db.session.commit()
        
        item = Item(nome="Suco", preco=7.0, categoria_id=categoria.id)
        db.session.add(item)
        db.session.commit()
        
        assert item.preco > 0


# ======================================================
# 3) MESA – 1 TESTE
# ======================================================

def test_mesa_creation(client):
    """Testa criação de mesa"""
    with app.app_context():
        from models import db
        mesa = Mesa(label="Mesa 1", ocupada=False)
        db.session.add(mesa)
        db.session.commit()
        
        assert mesa.id is not None
        assert mesa.label == "Mesa 1"
        assert mesa.ocupada is False


# ======================================================
# 4) PEDIDO – 2 TESTES
# ======================================================

def test_pedido_creation(client):
    """Testa criação de pedido"""
    with app.app_context():
        from models import db
        mesa = Mesa(label="Mesa 3", ocupada=True)
        db.session.add(mesa)
        db.session.commit()
        
        pedido = Pedido(mesa_id=mesa.id, status="aberto")
        db.session.add(pedido)
        db.session.commit()
        
        assert pedido.id is not None
        assert pedido.status == "aberto"


def test_pedido_status_update(client):
    """Testa atualização do status do pedido"""
    with app.app_context():
        from models import db
        mesa = Mesa(label="Mesa 4", ocupada=True)
        db.session.add(mesa)
        db.session.commit()
        
        pedido = Pedido(mesa_id=mesa.id, status="aberto")
        db.session.add(pedido)
        db.session.commit()
        
        pedido.status = "pronto"
        db.session.commit()
        
        assert pedido.status == "pronto"

import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario, Item, Pedido, Mesa, PedidoItem, Categoria
from app import app
import json


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


class TestUsuarioModel:
    """Testes unitários para o modelo Usuario"""
    
    def test_usuario_creation(self, client):
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
            assert usuario.nome == "Teste"
            assert usuario.email == "teste@teste.com"
            assert usuario.role == "garcom"
    
    def test_password_hashing(self, client):
        """Testa se a senha é hasheada corretamente"""
        senha_original = "senha123"
        senha_hash = generate_password_hash(senha_original)
        
        assert senha_hash != senha_original
        assert check_password_hash(senha_hash, senha_original)
        assert not check_password_hash(senha_hash, "senhaerrada")


class TestItemModel:
    """Testes unitários para o modelo Item"""
    
    def test_item_creation(self, client):
        """Testa a criação de um item"""
        with app.app_context():
            from models import db
            categoria = Categoria(nome="Pizza")
            db.session.add(categoria)
            db.session.commit()
            
            item = Item(
                nome="Pizza Calabresa",
                preco=45.0,
                categoria_id=categoria.id
            )
            db.session.add(item)
            db.session.commit()
            
            assert item.id is not None
            assert item.nome == "Pizza Calabresa"
            assert item.preco == 45.0
            assert item.categoria_id == categoria.id
    
    def test_item_price_validation(self, client):
        """Testa se o preço do item é válido"""
        with app.app_context():
            from models import db
            categoria = Categoria(nome="Bebidas")
            db.session.add(categoria)
            db.session.commit()
            
            item = Item(nome="Refrigerante", preco=6.0, categoria_id=categoria.id)
            db.session.add(item)
            db.session.commit()
            
            assert item.preco > 0


class TestMesaModel:
    """Testes unitários para o modelo Mesa"""
    
    def test_mesa_creation(self, client):
        """Testa a criação de uma mesa"""
        with app.app_context():
            from models import db
            mesa = Mesa(label="Mesa 1", ocupada=False)
            db.session.add(mesa)
            db.session.commit()
            
            assert mesa.id is not None
            assert mesa.label == "Mesa 1"
            assert mesa.ocupada == False
    
    def test_mesa_status_toggle(self, client):
        """Testa a alteração do status da mesa"""
        with app.app_context():
            from models import db
            mesa = Mesa(label="Mesa 2", ocupada=False)
            db.session.add(mesa)
            db.session.commit()
            
            mesa.ocupada = True
            db.session.commit()
            
            assert mesa.ocupada == True


class TestPedidoModel:
    """Testes unitários para o modelo Pedido"""
    
    def test_pedido_creation(self, client):
        """Testa a criação de um pedido"""
        with app.app_context():
            from models import db
            mesa = Mesa(label="Mesa 3", ocupada=True)
            db.session.add(mesa)
            db.session.commit()
            
            pedido = Pedido(mesa_id=mesa.id, status="aberto")
            db.session.add(pedido)
            db.session.commit()
            
            assert pedido.id is not None
            assert pedido.mesa_id == mesa.id
            assert pedido.status == "aberto"
    
    def test_pedido_status_update(self, client):
        """Testa a atualização do status do pedido"""
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
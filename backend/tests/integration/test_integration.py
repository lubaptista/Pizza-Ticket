import pytest
import json
from werkzeug.security import generate_password_hash
from models import Usuario, Item, Pedido, Mesa, Categoria, PedidoItem
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
            
            # Cria dados iniciais.
            categoria = Categoria(nome="Pizza")
            db.session.add(categoria)
            db.session.commit()
            
            item = Item(nome="Pizza Mussarela", preco=40.0, categoria_id=categoria.id)
            db.session.add(item)
            
            mesa = Mesa(label="Mesa 1", ocupada=False)
            db.session.add(mesa)
            
            usuario = Usuario(
                nome="Garçom Teste",
                email="garcom@teste.com",
                password=generate_password_hash("123456"),
                role="garcom"
            )
            db.session.add(usuario)
            db.session.commit()
            
        yield client


# ==========================================
# 1) TESTE DE INTEGRAÇÃO — AUTH
# ==========================================

def test_auth_login_success(client):
    """Testa login bem-sucedido"""
    response = client.post('/auth/login', 
        json={
            'email': 'garcom@teste.com',
            'password': '123456'
        })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['role'] == 'garcom'


# ==========================================
# 2) TESTE DE INTEGRAÇÃO — PEDIDOS
# ==========================================

def test_pedido_criar_pedido(client):
    """Testa criação de um pedido completo"""
    with app.app_context():
        mesa = Mesa.query.first()
        item = Item.query.first()
    
    response = client.post('/pedidos/criar',
        json={
            'mesa': mesa.id,
            'itens': [{'id': item.id, 'quantidade': 2}]
        })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'aberto'
    assert len(data['itens']) == 1


# ==========================================
# 3) TESTE DE INTEGRAÇÃO — MESAS
# ==========================================

def test_mesas_listar(client):
    """Testa listagem de mesas"""
    response = client.get('/pedidos/mesas')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0
    assert 'label' in data[0]
    assert 'ocupada' in data[0]

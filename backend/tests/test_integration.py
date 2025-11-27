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
            
            # Cria dados iniciais para os testes
            categoria = Categoria(nome="Pizza")
            db.session.add(categoria)
            db.session.commit()
            
            item1 = Item(nome="Pizza Mussarela", preco=40.0, categoria_id=categoria.id)
            item2 = Item(nome="Pizza Calabresa", preco=45.0, categoria_id=categoria.id)
            db.session.add_all([item1, item2])
            db.session.commit()
            
            mesa1 = Mesa(label="Mesa 1", ocupada=False)
            mesa2 = Mesa(label="Mesa 2", ocupada=False)
            db.session.add_all([mesa1, mesa2])
            db.session.commit()
            
            usuario = Usuario(
                nome="Garçom Teste",
                email="garcom@teste.com",
                password=generate_password_hash("123456"),
                role="garcom"
            )
            db.session.add(usuario)
            db.session.commit()
            
        yield client


class TestAuthIntegration:
    """Testes de integração para autenticação"""
    
    def test_login_success(self, client):
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
    
    def test_login_invalid_credentials(self, client):
        """Testa login com credenciais inválidas"""
        response = client.post('/auth/login',
            json={
                'email': 'garcom@teste.com',
                'password': 'senhaerrada'
            })
        
        assert response.status_code == 401
    
    def test_register_new_user(self, client):
        """Testa registro de novo usuário"""
        response = client.post('/auth/register',
            json={
                'email': 'novo@teste.com',
                'password': 'senha123'
            })
        
        assert response.status_code == 201


class TestPedidoIntegration:
    """Testes de integração para pedidos"""
    
    def test_criar_pedido_completo(self, client):
        """Testa criação de um pedido completo"""
        with app.app_context():
            from models import db
            mesas = Mesa.query.all()
            itens = Item.query.all()
            
            mesa_id = mesas[0].id
            item_id = itens[0].id
        
        response = client.post('/pedidos/criar',
            json={
                'mesa': mesa_id,
                'itens': [
                    {'id': item_id, 'quantidade': 2}
                ]
            })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'aberto'
        assert len(data['itens']) == 1
    
    def test_listar_pedidos_abertos(self, client):
        """Testa listagem de pedidos abertos"""
        # Primeiro cria um pedido
        with app.app_context():
            from models import db
            mesa = Mesa.query.first()
            item = Item.query.first()
            
            pedido = Pedido(mesa_id=mesa.id, status="aberto")
            db.session.add(pedido)
            db.session.commit()
            
            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                item_id=item.id,
                quantidade=1,
                status="aberto"
            )
            db.session.add(pedido_item)
            db.session.commit()
        
        response = client.get('/pedidos/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0
        assert data[0]['status'] == 'aberto'
    
    def test_atualizar_status_pedido(self, client):
        """Testa atualização do status de um pedido"""
        with app.app_context():
            from models import db
            mesa = Mesa.query.first()
            
            pedido = Pedido(mesa_id=mesa.id, status="aberto")
            db.session.add(pedido)
            db.session.commit()
            
            pedido_id = pedido.id
        
        response = client.patch(f'/pedidos/{pedido_id}/status',
            json={'status': 'pronto'})
        
        assert response.status_code == 200
        
        with app.app_context():
            from models import db
            pedido = Pedido.query.get(pedido_id)
            assert pedido.status == 'pronto'


class TestMesaIntegration:
    """Testes de integração para mesas"""
    
    def test_listar_mesas(self, client):
        """Testa listagem de mesas"""
        response = client.get('/pedidos/mesas')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) > 0
        assert 'label' in data[0]
        assert 'ocupada' in data[0]
    
    def test_alterar_status_mesa(self, client):
        """Testa alteração do status de uma mesa"""
        with app.app_context():
            from models import db
            mesa = Mesa.query.first()
            mesa_id = mesa.id
        
        response = client.put(f'/pedidos/mesa/{mesa_id}/status',
            json={'ocupada': True})
        
        assert response.status_code == 200
        
        with app.app_context():
            from models import db
            mesa = Mesa.query.get(mesa_id)
            assert mesa.ocupada == True
    
    def test_remover_pedidos_mesa(self, client):
        """Testa remoção de todos os pedidos de uma mesa"""
        with app.app_context():
            from models import db
            mesa = Mesa.query.first()
            item = Item.query.first()
            
            pedido = Pedido(mesa_id=mesa.id, status="aberto")
            db.session.add(pedido)
            db.session.commit()
            
            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                item_id=item.id,
                quantidade=1
            )
            db.session.add(pedido_item)
            db.session.commit()
            
            mesa_id = mesa.id
        
        response = client.delete(f'/pedidos/mesa/{mesa_id}/todos')
        
        assert response.status_code == 200
        
        with app.app_context():
            from models import db
            pedidos = Pedido.query.filter_by(mesa_id=mesa_id).all()
            assert len(pedidos) == 0
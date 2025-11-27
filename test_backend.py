# test_backend.py
import pytest
import os
import json
from backend.app import create_app # Importa a função create_app do seu módulo backend/app.py
from backend.models import db, Pedido, PedidoItem, Mesa, Item, Categoria # Importa o db e os Models
from backend.utils import valida_mesa_id, calcula_valor_total_pedido, formata_data_para_exibicao, verifica_status_valido
from datetime import datetime

# Fixture para configurar o cliente de teste do Flask
@pytest.fixture
def client():
    # Garante que o app use o DB PostgreSQL no container
    os.environ['DATABASE_URL'] = 'postgresql://user:password@db:5432/pizza_ticket_test'
    app = create_app(testing=True)
    
    with app.app_context():
        # Limpar e recriar o esquema do banco de dados antes de cada suite de testes
        db.drop_all()
        db.create_all() 
        
        # Insere dados iniciais necessários para testes de integração (categoria)
        categoria1 = Categoria(id=1, nome="Pizzas")
        categoria2 = Categoria(id=2, nome="Bebidas")
        db.session.add_all([categoria1, categoria2])

        # Teste criar mesa e cadastrar item
        mesa1 = Mesa(label="Mesa 1")
        item1 = Item(nome="Pizza Calabresa", preco=45.0, categoria_id=1)
        item2 = Item(nome="Refrigerante", preco=6.0, categoria_id=2)
        db.session.add_all([mesa1, item1, item2])
        db.session.commit()
        
        # O Pedido é a sua ComandaModel
        class ComandaModel:
            def __init__(self, mesa, pedido, status="aberto"):
                self.mesa = mesa
                self.pedido = pedido
                self.status = status
        
        yield app.test_client()

# =================================================================
# UNIT TESTS (MÍNIMO 7 REQUERIDO)
# =================================================================

# 1. Teste de Validação de Mesa (da utils.py)
def test_validacao_mesa_positiva_unidade_1():
    assert valida_mesa_id(15) == True
    
# 2. Teste de Validação de Mesa Negativa (da utils.py)
def test_validacao_mesa_negativa_unidade_2():
    assert valida_mesa_id(-1) == False

# 3. Teste de Cálculo de Preço Simples (da utils.py)
def test_calcula_preco_simples_unidade_3():
    itens = [{'preco': 10.0, 'quantidade': 2}]
    assert calcula_valor_total_pedido(itens) == 20.0

# 4. Teste de Cálculo de Preço com Múltiplos Itens (da utils.py)
def test_calcula_preco_multiplos_itens_unidade_4():
    itens = [{'preco': 45.0, 'quantidade': 1}, {'preco': 6.0, 'quantidade': 3}]
    assert calcula_valor_total_pedido(itens) == 63.0

# 5. Teste de Formatação de Data (da utils.py)
def test_formatacao_data_unidade_5():
    data_mock = datetime(2025, 12, 10, 15, 30, 0)
    assert formata_data_para_exibicao(data_mock) == "10/12/2025 15:30:00"

# 6. Teste de Verificação de Status Válido (da utils.py)
def test_verifica_status_valido_unidade_6():
    assert verifica_status_valido("preparando") == True
    
# 7. Teste de Verificação de Status Inválido (da utils.py)
def test_verifica_status_invalido_unidade_7():
    assert verifica_status_valido("entregue") == False

# =================================================================
# INTEGRATION TESTS (MÍNIMO 3 REQUERIDO)
# =================================================================

# 1. Teste de Criação de Pedido (Rota POST)
def test_criar_pedido_integracao_1(client):
    # IDs de Item criados na fixture: 1 (Pizza) e 2 (Refrigerante)
    data = {
        'mesa': 1,
        'itens': [
            {'id': 1, 'quantidade': 2},
            {'id': 2, 'quantidade': 1}
        ]
    }
    response = client.post('/pedidos/criar', json=data)
    
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data['mesa'] == 'Mesa 1'
    
    # Verifica a persistência no DB
    # CORRIGIDO: Substituindo Pedido.query.get() por db.session.get()
    pedido_db = db.session.get(Pedido, response_data['id'])
    assert pedido_db is not None
    assert len(pedido_db.itens) == 2 # 2 PedidoItems criados

# 2. Teste de Listagem de Pedidos Abertos (Rota GET)
def test_lista_pedidos_abertos_integracao_2(client):
    # Cria um pedido antes de listar
    client.post('/pedidos/criar', json={
        'mesa': 1, 
        'itens': [{'id': 1, 'quantidade': 1}]
    })

    # Verifica a rota GET /pedidos (lista abertos)
    response = client.get('/pedidos/')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert len(response_data) == 1 # Deve haver 1 pedido
    assert response_data[0]['status'] == 'aberto'

# 3. Teste de Atualização de Status de Pedido (Rota PATCH)
def test_atualiza_status_pedido_integracao_3(client):
    # 1. Cria um pedido
    response_cria = client.post('/pedidos/criar', json={
        'mesa': 1, 
        'itens': [{'id': 1, 'quantidade': 1}]
    })
    pedido_id = json.loads(response_cria.data)['id']

    # 2. Atualiza o status
    response_patch = client.patch(f'/pedidos/{pedido_id}/status', json={'status': 'preparando'})
    assert response_patch.status_code == 200
    
    # 3. Verifica a alteração no DB
    # CORRIGIDO: Substituindo Pedido.query.get() por db.session.get()
    pedido_db = db.session.get(Pedido, pedido_id)
    assert pedido_db.status == 'preparando'
from flask import Blueprint, request, jsonify
from ..models import db, Pedido, PedidoItem, Item, Mesa
from sqlalchemy import select, delete # NOVO: Importa 'select' e 'delete' para consultas 2.0

pedidos_bp = Blueprint("pedidos", __name__)

# ============================
# ROTAS DO GARÇOM
# ============================

# Listar mesas e se estão ocupadas
@pedidos_bp.route("/mesas", methods=["GET"])
def listar_mesas():
    # ALTERADO: De Mesa.query.all() para sintaxe 2.0
    mesas = db.session.scalars(select(Mesa)).all()
    
    # ALTERADO: De Pedido.query.filter_by().all() para sintaxe 2.0
    stmt_pedidos = select(Pedido).filter_by(status="aberto")
    pedidos_abertos = db.session.scalars(stmt_pedidos).all()
    
    ocupadas = {p.mesa_id for p in pedidos_abertos}

    result = []
    for mesa in mesas:
        result.append({
            "id": mesa.id,
            "label": mesa.label,
            "ocupada": mesa.ocupada
        })
    return jsonify(result)

@pedidos_bp.route("/mesa/<int:mesa_id>/status", methods=["PUT"])
def alterar_status_mesa(mesa_id):
    try:
        data = request.get_json()
        ocupada = data.get('ocupada')

        # ALTERADO: De Mesa.query.get_or_404(mesa_id) para db.session.get() e tratamento manual de 404
        mesa = db.session.get(Mesa, mesa_id)
        if mesa is None:
            return jsonify({'error': 'Mesa não encontrada'}), 404
            
        mesa.ocupada = bool(ocupada)
        db.session.commit()

        return jsonify({'message': 'Status da mesa atualizado', 'ocupada': mesa.ocupada}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Criar pedido
@pedidos_bp.route("/criar", methods=["POST"])
def criar_pedido():
    data = request.json
    mesa_id = data.get("mesa")
    itens_ids = data.get("itens")  # lista de ids de Item

    if not mesa_id or not itens_ids:
        return jsonify({"error": "Mesa ou itens não informados"}), 400

    # Cria pedido
    pedido = Pedido(mesa_id=mesa_id, status="aberto")
    db.session.add(pedido)
    db.session.commit()  # gera o ID do pedido

    # Cria itens do pedido
    for item_data in itens_ids:
        item_id = item_data.get("id")
        quantidade = item_data.get("quantidade", 1)
        
        # ALTERADO: De Item.query.get(item_id) para db.session.get()
        item = db.session.get(Item, item_id)
        
        if item:
            pi = PedidoItem(pedido_id=pedido.id, item_id=item.id, quantidade=quantidade, status="aberto")
            db.session.add(pi)

    db.session.commit()

    return jsonify({
        "id": pedido.id,
        "mesa": pedido.mesa.label,
        "itens": [{"id": i.item_id, "quantidade": i.quantidade} for i in pedido.itens],
        "status": pedido.status
    }), 201

# Remover todos os pedidos de uma mesa
@pedidos_bp.route("/mesa/<int:mesa_id>/todos", methods=["DELETE"])
def remover_pedidos_mesa(mesa_id):
    try:
        # Busca todos os pedidos da mesa
        # ALTERADO: De Pedido.query.filter_by().all() para sintaxe 2.0
        stmt_pedidos = select(Pedido).filter_by(mesa_id=mesa_id)
        pedidos_da_mesa = db.session.scalars(stmt_pedidos).all()
        
        if not pedidos_da_mesa:
            return jsonify({"message": "Nenhum pedido encontrado para esta mesa"}), 404

        # Remove todos os itens de cada pedido e o pedido
        for pedido in pedidos_da_mesa:
            # ALTERADO: De PedidoItem.query.filter_by(pedido_id=pedido.id).delete() para sintaxe 2.0
            db.session.execute(delete(PedidoItem).where(PedidoItem.pedido_id == pedido.id))
            db.session.delete(pedido) 

        db.session.commit()
        return jsonify({"message": f"Todos os pedidos da mesa {mesa_id} foram removidos"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# ============================
# ROTAS DA COZINHA
# ============================

# Listar todos os pedidos abertos
@pedidos_bp.route("/", methods=["GET"])
def listar_pedidos():
    # ALTERADO: De Pedido.query.filter_by().all() para sintaxe 2.0
    stmt = select(Pedido).filter_by(status="aberto")
    pedidos = db.session.scalars(stmt).all()
    
    result = []

    for pedido in pedidos:
        itens = []
        for pi in pedido.itens:
            itens.append({
                "id": pi.id,
                "nome": pi.item.nome,
                "quantidade": pi.quantidade,
                "status": pi.status
            })
        result.append({
            "id": pedido.id,
            "mesa": pedido.mesa.label,
            "status": pedido.status,
            "itens": itens
        })
    return jsonify(result)

@pedidos_bp.route("/todos", methods=["GET"])
def listar_todos_pedidos():
    # ALTERADO: De Pedido.query.all() para sintaxe 2.0
    pedidos = db.session.scalars(select(Pedido)).all() 
    
    result = []

    for pedido in pedidos:
        itens = []
        for pi in pedido.itens:
            itens.append({
                "id": pi.id,
                "nome": pi.item.nome,
                "quantidade": pi.quantidade,
                "preco": pi.item.preco,
                "status": pi.status
            })
        result.append({
            "id": pedido.id,
            "mesa": pedido.mesa.label,
            "status": pedido.status,
            "itens": itens
        })
    return jsonify(result)

# Atualizar status de um item
@pedidos_bp.route("/item/<int:item_id>/status", methods=["PATCH"])
def atualizar_status_item(item_id):
    data = request.json
    status = data.get("status")
    if not status:
        return jsonify({"error": "Status não informado"}), 400

    # ALTERADO: De PedidoItem.query.get(item_id) para db.session.get()
    pi = db.session.get(PedidoItem, item_id)
    
    if not pi:
        return jsonify({"error": "Item não encontrado"}), 404

    pi.status = status
    db.session.commit()
    return jsonify({"ok": True})

# Atualizar status de um pedido inteiro
@pedidos_bp.route("/<int:pedido_id>/status", methods=["PATCH"])
def atualizar_status_pedido(pedido_id):
    data = request.json
    status = data.get("status")
    if not status:
        return jsonify({"error": "Status não informado"}), 400

    # ALTERADO: De Pedido.query.get(pedido_id) para db.session.get()
    pedido = db.session.get(Pedido, pedido_id)
    
    if not pedido:
        return jsonify({"error": "Pedido não encontrado"}), 404

    pedido.status = status
    db.session.commit()
    return jsonify({"ok": True})
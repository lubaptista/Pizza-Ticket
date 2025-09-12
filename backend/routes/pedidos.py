from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt
# from extensions import db, socketio
# from models import Pedido, PedidoItem, Item, Table, OrderStatus, OrderStatusLog
from models import db, Pedido, PedidoItem, Item, Mesa

pedidos_bp = Blueprint("pedidos", __name__)

# ============================
# ROTAS DO GARÇOM
# ============================

# Listar mesas e se estão ocupadas
@pedidos_bp.route("/mesas", methods=["GET"])
def listar_mesas():
    mesas = Mesa.query.all()
    pedidos_abertos = Pedido.query.filter_by(status="aberto").all()
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

        mesa = Mesa.query.get_or_404(mesa_id)
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
        item = Item.query.get(item_id)
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
        pedidos_da_mesa = Pedido.query.filter_by(mesa_id=mesa_id).all()
        if not pedidos_da_mesa:
            return jsonify({"message": "Nenhum pedido encontrado para esta mesa"}), 404

        # Remove todos os itens de cada pedido
        for pedido in pedidos_da_mesa:
            PedidoItem.query.filter_by(pedido_id=pedido.id).delete()
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
    pedidos = Pedido.query.filter_by(status="aberto").all()
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
    pedidos = Pedido.query.all()  # Remove o filtro para buscar todos os pedidos
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

    pi = PedidoItem.query.get(item_id)
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

    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return jsonify({"error": "Pedido não encontrado"}), 404

    pedido.status = status
    db.session.commit()
    return jsonify({"ok": True})    

# orders_bp = Blueprint('pedidos', __name__, url_prefix='/api/pedidos')

# @orders_bp.post('')
# @jwt_required()
# def create_order():
#     identity = get_jwt()
#     waiter_id = identity['sub']['id'] if 'sub' in identity else identity['id']
#     table_id = request.json.get('table_id')
#     order = Pedido(table_id=table_id, waiter_id=waiter_id)
#     db.session.add(order)
#     db.session.commit()
#     socketio.emit('orders:created', {"order_id": order.id})
#     return {"id": order.id, "status": order.status.value}

# @orders_bp.get('')
# @jwt_required() 
# def list_orders():
#     status = request.args.get('status')
#     q = Pedido.query
#     if status:
#         q = q.filter(Pedido.status == status)
#     orders = q.order_by(Pedido.created_at.desc()).all()
#     return [{
#         "id": o.id,
#         "table": o.table.label,
#         "status": o.status.value,
#         "items": [{
#             "id": i.id,
#             "name": i.menu_item.name,
#             "qty": i.qty,
#             "status": i.status.value
#         } for i in o.items]
#     } for o in orders]

# @orders_bp.post('/<int:order_id>/items')
# @jwt_required()
# def add_item(order_id):
#     data = request.get_json()
#     item = Item.query.get_or_404(data['menu_item_id'])
#     oi = PedidoItem(order_id=order_id, menu_item_id=item.id, qty=data.get('qty',1), note=data.get('note'))
#     db.session.add(oi)
#     db.session.commit()
#     socketio.emit('orders:updated', {"order_id": order_id})
#     return {"id": oi.id}

# @orders_bp.put('/<int:order_id>/status')
# @jwt_required()
# def update_order_status(order_id):
#     to_status = request.json.get('to_status')
#     order = Pedido.query.get_or_404(order_id)
#     log = OrderStatusLog(order_id=order.id, from_status=order.status.value, to_status=to_status)
#     order.status = to_status
#     db.session.add(log)
#     db.session.commit()
#     socketio.emit('orders:updated', {"order_id": order.id, "to": to_status})
#     return {"ok": True}

# @orders_bp.put('/<int:order_id>/items/<int:item_id>/status')
# @jwt_required()
# def update_order_item_status(order_id, item_id):
#     to_status = request.json.get('to_status')
#     oi = PedidoItem.query.filter_by(order_id=order_id, id=item_id).first_or_404()
#     oi.status = to_status
#     db.session.commit()
#     socketio.emit('orders:updated', {"order_id": order_id})
#     return {"ok": True}
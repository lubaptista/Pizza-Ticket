from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt
# from extensions import db, socketio
# from models import Pedido, PedidoItem, Item, Table, OrderStatus, OrderStatusLog

pedidos_bp = Blueprint("pedidos", __name__)

pedidos_mock = []

@pedidos_bp.route("/", methods=["GET"])
def listar_pedidos():
    return jsonify(pedidos_mock)

@pedidos_bp.route("/", methods=["POST"])
def criar_pedido():
    pedido = request.json
    pedidos_mock.append(pedido)
    return jsonify(pedido), 201


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
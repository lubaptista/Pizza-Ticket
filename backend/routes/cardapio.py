from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required
# from extensions import db
# from models import Categoria

cardapio_bp = Blueprint("cardapio", __name__)

itens_mock = [{"id": 1, "nome": "Pizza Mussarela", "preco": 40.0, "categoria": "Pizza"}]

@cardapio_bp.route("/", methods=["GET"])
def listar_itens():
    return jsonify(itens_mock)


# cardapio_bp = Blueprint('cardapio', __name__, url_prefix='/api/cardapio')

# @cardapio_bp.get('')
# def list_cardapio():
#     cats = Categoria.query.filter_by(is_active=True).all()
#     return [{"id": c.id, "name": c.name} for c in cats]

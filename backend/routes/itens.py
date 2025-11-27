# routes/itens.py
from flask import Blueprint, jsonify
from ..models import Item

itens_bp = Blueprint("itens", __name__, url_prefix="/itens")

@itens_bp.route("/", methods=["GET"])
def listar_itens():
    itens = Item.query.all()
    return jsonify([{
        "id": item.id,
        "nome": item.nome,
        "preco": item.preco
    } for item in itens])

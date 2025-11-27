from flask import Blueprint, request, jsonify
from ..models import Usuario, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
import os

auth_bp = Blueprint("auth", __name__)

# Rota para Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = Usuario.query.filter_by(email=data.get("email")).first()

    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Credenciais inválidas"}), 401
    
    access_token = create_access_token(identity={"id": user.id, "role": user.role})
    
    return jsonify({"access_token": access_token, "role": user.role}), 200

# Rota para registrar usuário comum:
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    # Checa se usuário já existe
    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Usuário já existe"}), 400

    new_user = Usuario(
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role="user"  # 🔹 Padrão sempre será 'user'
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso"}), 201

# Rota para criar usuário (somente admin)
@auth_bp.route("/create-user", methods=["POST"])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()

    if current_user["role"] != "admin":
        return jsonify({"error": "Apenas admins podem criar usuários"}), 403

    data = request.get_json()

    if not data.get("email") or not data.get("password") or not data.get("role"):
        return jsonify({"error": "Email, senha e role são obrigatórios"}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Usuário já existe"}), 400

    new_user = Usuario(
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role=data["role"]  # 🔹 Admin define o perfil
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"Usuário {data['email']} criado com role {data['role']}"}), 201
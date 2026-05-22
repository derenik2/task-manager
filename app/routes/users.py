from flask import Blueprint, jsonify, request
from ..services import user_service

users_bp = Blueprint("users", __name__)


@users_bp.get("/")
def list_users():
    users = user_service.get_all_users()
    return jsonify([u.to_dict() for u in users])


@users_bp.post("/")
def create_user():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    if not username or not email:
        return jsonify({"error": "username and email are required"}), 400
    user = user_service.create_user(username, email)
    return jsonify(user.to_dict()), 201


@users_bp.get("/<int:user_id>")
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(user.to_dict())


@users_bp.delete("/<int:user_id>")
def delete_user(user_id: int):
    if not user_service.delete_user(user_id):
        return jsonify({"error": "not found"}), 404
    return "", 204

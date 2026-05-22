from flask import Blueprint, jsonify, request
from ..services import task_service

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.get("/user/<int:owner_id>")
def list_tasks(owner_id: int):
    tasks = task_service.get_tasks_for_user(owner_id)
    return jsonify([t.to_dict() for t in tasks])


@tasks_bp.post("/")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    owner_id = data.get("owner_id")
    if not title or owner_id is None:
        return jsonify({"error": "title and owner_id are required"}), 400
    task = task_service.create_task(title, owner_id)
    return jsonify(task.to_dict()), 201


@tasks_bp.patch("/<int:task_id>/toggle")
def toggle_task(task_id: int):
    task = task_service.toggle_task(task_id)
    if task is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(task.to_dict())


@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id: int):
    if not task_service.delete_task(task_id):
        return jsonify({"error": "not found"}), 404
    return "", 204

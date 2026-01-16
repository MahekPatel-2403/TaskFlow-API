from flask import Blueprint, request, jsonify, g
from app.services.task_service import create_task, get_tasks_paginated
from app.utils.auth_middleware import login_required
from app.utils.errors import error_response

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/tasks", methods=["POST"])
@login_required
def create():
    data = request.get_json()
    if not data:
        return error_response("Invalid JSON", 400)

    task, error = create_task(data, g.user_id)

    if error:
        return error_response(error, 400)

    return jsonify(task), 201


@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    tasks = get_tasks_paginated(page, limit)

    return jsonify({
        "page": page,
        "limit": limit,
        "tasks": tasks
    }), 200

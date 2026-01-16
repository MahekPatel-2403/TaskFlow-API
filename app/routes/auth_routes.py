from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, authenticate_user
from app.utils.errors import error_response
from app.utils.jwt_utils import generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods = ["POST"])
def register():
    data = request.get_json()
    if not data:
        return error_response("Invalid JSON", 400)
    
    user, error = create_user(data)
    if error:
        return error_response(error, 400)
    
    return jsonify({
        "id" : user["id"],
        "username" : user["username"]
    }), 201

@auth_bp.route("/auth/login", methods = ["POST"])
def login():
    data = request.get_json()
    if not data:
        return error_response("Invalid JSON", 400)
    
    user = authenticate_user(
        data.get("username"),
        data.get("password")
    )

    if not user:
        return error_response("Invalid credentials", 401)
    
    token = generate_token(user["id"])
    return jsonify({
        "token" : token,
        "message" : "Login Successful"
        }),200


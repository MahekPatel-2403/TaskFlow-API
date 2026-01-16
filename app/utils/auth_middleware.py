from flask import request, g
import jwt
import os
from app.utils.errors import error_response

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        return None

def login_required(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return error_response("Token missing", 401)

        if not auth_header.startswith("Bearer "):
            return error_response("Invalid token format", 401)

        token = auth_header.split(" ")[1]

        payload = verify_token(token)

        if not payload:
            return error_response("Invalid Token", 401)

        g.user_id = payload.get("user_id")   

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

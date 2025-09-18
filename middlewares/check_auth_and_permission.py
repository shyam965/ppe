from flask import request, jsonify
from functools import wraps
from utils.jwt_utils import verify_access_token


def check_auth_and_permission(required_role=[]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token_header = request.headers.get("Authorization")
            if not token_header:
                return jsonify({"error": "Token is missing"}), 400

            try:
                token = token_header.split("Bearer ")[1].strip()
            except IndexError:
                return jsonify({"error": "Token is missing"}), 401

            error, payload = verify_access_token(token)
            if error:
                return jsonify({"error": str(error)}), 401

            if required_role and payload.get("role") not in required_role:
                return jsonify({"error": "You are not authorized to access this resource"}), 403

            request.user = payload
            return func(*args, **kwargs)

        return wrapper
    return decorator

from flask import Blueprint, request, jsonify
from configs_and_constants.db import db
from utils.jwt_utils import generate_access_token, generate_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users", __name__)
users_collection = db["users"]


@users_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    role = data.get("role", "user")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)

    user = {
        "name": name,
        "phone": phone,
        "email": email,
        "password": hashed_pw,
        "role": role,
    }
    result = users_collection.insert_one(user)

    return jsonify({"message": "User registered", "id": str(result.inserted_id)}), 201


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = users_collection.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    user_data = {
        "id": str(user["_id"]),
        "email": user["email"],
        "role": user.get("role", "user"),
        "name": user.get("name"),
        "phone": user.get("phone"),
    }

    access_token = generate_access_token(user_data)
    refresh_token = generate_refresh_token(user_data)

    return (
        jsonify(
            {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_data,
            }
        ),
        200,
    )

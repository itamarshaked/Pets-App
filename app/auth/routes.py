from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    existing_user = User.query.filter_by(
        username=data["username"]
    ).first()

    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    user = User(
    username=data["username"],
    role=data.get("role", "user")
)
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(
        username=data["username"]
    ).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.username)

    return jsonify({"access_token": access_token})

@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    username = get_jwt_identity()

    current_user = User.query.filter_by(
        username=username
    ).first()

    if current_user.role != "admin":
        return jsonify({
            "error": "Admin access required"
        }), 403

    users = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
        for user in users
    ])
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Pet, User

from app.extensions import db
from app.models import Pet

pets_bp = Blueprint("pets", __name__)


@pets_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@pets_bp.route("/pets", methods=["POST"])
@jwt_required()
def create_pet():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    data = request.json

    pet = Pet(
        name=data["name"],
        species=data["species"],
        age=data["age"],
        owner_id=user.id
    )

    db.session.add(pet)
    db.session.commit()

    return jsonify(pet.to_dict())


@pets_bp.route("/pets", methods=["GET"])
@jwt_required()
def get_pets():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    pets = Pet.query.filter_by(owner_id=user.id).all()

    return jsonify([pet.to_dict() for pet in pets])

@pets_bp.route("/pets/<int:pet_id>", methods=["GET"])
def get_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return jsonify(pet.to_dict())


@pets_bp.route("/pets/<int:pet_id>", methods=["PUT"])
def update_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    data = request.json

    pet.name = data["name"]
    pet.species = data["species"]
    pet.age = data["age"]

    db.session.commit()

    return jsonify(pet.to_dict())


@pets_bp.route("/pets/<int:pet_id>", methods=["DELETE"])
@jwt_required()
def delete_pet(pet_id):
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    if user.role != "admin":
        return jsonify({"error": "Admin access required"}), 403

    pet = Pet.query.get_or_404(pet_id)

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"message": "Pet deleted successfully"})
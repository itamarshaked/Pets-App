from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models import Pet

pets_bp = Blueprint("pets", __name__)


@pets_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@pets_bp.route("/pets", methods=["POST"])
def create_pet():
    data = request.json

    pet = Pet(
        name=data["name"],
        species=data["species"],
        age=data["age"]
    )

    db.session.add(pet)
    db.session.commit()

    return jsonify(pet.to_dict())


@pets_bp.route("/pets", methods=["GET"])
def get_pets():
    pets = Pet.query.all()

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
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"message": "Pet deleted successfully"})
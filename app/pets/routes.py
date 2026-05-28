from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from app.extensions import db
from app.models import Pet, User
from app.schemas import PetSchema


pets_bp = Blueprint(
    "pets",
    __name__,
    url_prefix="/pets",
    description="Pets operations"
)


@pets_bp.route("/", methods=["GET"])
@jwt_required()
@pets_bp.response(200, PetSchema(many=True))
def get_pets():
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    pets = Pet.query.filter_by(owner_id=user.id).all()

    return pets


@pets_bp.route("/", methods=["POST"])
@jwt_required()
@pets_bp.arguments(PetSchema)
@pets_bp.response(200, PetSchema)
def create_pet(data):
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    pet = Pet(
        name=data["name"],
        species=data["species"],
        age=data["age"],
        owner_id=user.id
    )

    db.session.add(pet)
    db.session.commit()

    return pet


@pets_bp.route("/<int:pet_id>", methods=["GET"])
@jwt_required()
@pets_bp.response(200, PetSchema)
def get_pet(pet_id):
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    pet = Pet.query.filter_by(
        id=pet_id,
        owner_id=user.id
    ).first_or_404()

    return pet


@pets_bp.route("/<int:pet_id>", methods=["PUT"])
@jwt_required()
@pets_bp.arguments(PetSchema)
@pets_bp.response(200, PetSchema)
def update_pet(data, pet_id):
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()

    pet = Pet.query.filter_by(
        id=pet_id,
        owner_id=user.id
    ).first_or_404()

    pet.name = data["name"]
    pet.species = data["species"]
    pet.age = data["age"]

    db.session.commit()

    return pet


@pets_bp.route("/<int:pet_id>", methods=["DELETE"])
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
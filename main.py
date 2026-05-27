from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Pet
from models import Base
from schemas import PetCreate, PetResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/pets", response_model=PetResponse)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    db_pet = Pet(
        name=pet.name,
        species=pet.species,
        age=pet.age
    )

    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)

    return db_pet


@app.get("/pets", response_model=list[PetResponse])
def get_pets(db: Session = Depends(get_db)):
    return db.query(Pet).all()

@app.get("/pets/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    return pet


@app.put("/pets/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, updated_pet: PetCreate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet.name = updated_pet.name
    pet.species = updated_pet.species
    pet.age = updated_pet.age

    db.commit()
    db.refresh(pet)

    return pet


@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    db.delete(pet)
    db.commit()

    return {"message": "Pet deleted successfully"}
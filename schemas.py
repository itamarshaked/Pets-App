from pydantic import BaseModel

class PetCreate(BaseModel):
    name: str
    species: str
    age: int

class PetResponse(PetCreate):
    id: int

    class Config:
        orm_mode = True
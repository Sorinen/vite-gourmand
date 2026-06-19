from pydantic import BaseModel


class TypePlatBase(BaseModel):
    libelle: str


class TypePlatCreate(TypePlatBase):
    pass


class TypePlat(TypePlatBase):
    id: int

    class Config:
        from_attributes = True
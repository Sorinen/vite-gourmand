from pydantic import BaseModel


class PlatBase(BaseModel):
    nom: str
    photo: str
    type_plat_id: int


class PlatCreate(PlatBase):
    pass


class Plat(PlatBase):
    id: int

    class Config:
        from_attributes = True

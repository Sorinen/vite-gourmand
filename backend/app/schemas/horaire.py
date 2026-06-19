from pydantic import BaseModel


class HoraireBase(BaseModel):
    libelle: str


class HoraireCreate(HoraireBase ):
    pass


class Horaire(HoraireBase):
    id: int

    class Config:
        from_attributes = True
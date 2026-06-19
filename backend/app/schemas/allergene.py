from pydantic import BaseModel


class AllergeneBase(BaseModel):
    libelle: str


class AllergeneCreate(AllergeneBase):
    pass


class Allergene(AllergeneBase):
    id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel


class RegimeBase(BaseModel):
    libelle: str


class RegimeCreate(RegimeBase):
    pass


class Regime(RegimeBase):
    id: int

    class Config:
        from_attributes = True
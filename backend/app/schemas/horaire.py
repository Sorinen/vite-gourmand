from pydantic import BaseModel
from typing import Optional
from datetime import time

class HoraireBase(BaseModel):
    jour: str
    heure_ouverture: Optional[time] = None
    heure_fermeture: Optional[time] = None
    ferme: bool = False

class HoraireCreate(HoraireBase):
    pass

class Horaire(HoraireBase):
    id: int
    class Config:
        from_attributes = True
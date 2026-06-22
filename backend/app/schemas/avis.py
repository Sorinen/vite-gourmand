from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AvisBase(BaseModel):
    note: int
    commentaire: Optional[str] = None
    statut: str


class AvisCreate(AvisBase):
    commande_id: int
    utilisateur_id: int


class Avis(AvisBase):
    id: int
    commande_id: int
    utilisateur_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
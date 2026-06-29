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
    menu_id: Optional[int] = None

class Avis(AvisBase):
    id: int
    commande_id: int
    utilisateur_id: int
    menu_id: Optional[int] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True
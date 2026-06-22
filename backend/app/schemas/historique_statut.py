from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HistoriqueStatutBase(BaseModel):
    statut: str


class HistoriqueStatutCreate(HistoriqueStatutBase):
    commande_id: int
    modifie_par: int


class HistoriqueStatut(HistoriqueStatutBase):
    id: int
    commande_id: int
    modifie_par: int
    date_changement: Optional[datetime] = None

    class Config:
        from_attributes = True
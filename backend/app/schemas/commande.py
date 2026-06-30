from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time

class CommandeBase(BaseModel):
    date_prestation: date
    heure_livraison: time
    adresse_livraison: str
    nombre_personnes: int
    prix_menu: float
    prix_livraison: float
    prix_total: float
    statut: str
    motif_annulation: Optional[str] = None
    mode_contact: Optional[str] = None
    pret_materiel: bool
    utilisateur_id: int
    menu_id: int

class CommandeCreate(CommandeBase):
    pass

class CommandeUpdate(BaseModel):
    date_prestation: Optional[date] = None
    heure_livraison: Optional[time] = None
    adresse_livraison: Optional[str] = None
    nombre_personnes: Optional[int] = None
    prix_menu: Optional[float] = None
    prix_livraison: Optional[float] = None
    prix_total: Optional[float] = None
    pret_materiel: Optional[bool] = None

class Commande(CommandeBase):
    id: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

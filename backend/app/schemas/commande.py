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

class Commande(CommandeBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
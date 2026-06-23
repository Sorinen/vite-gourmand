from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UtilisateurBase(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    telephone: Optional[str] = None
    adresse_postale: Optional[str] = None
    role_id: int

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str

class Utilisateur(UtilisateurBase):
    id: int
    actif: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.utilisateur import Utilisateur, UtilisateurCreate
from app.crud import utilisateur as utilisateur_crud

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])

@router.get("/", response_model=list[Utilisateur])
def read_utilisateurs(db: Session = Depends(get_db)):
    return utilisateur_crud.get_utilisateurs(db)

@router.post("/", response_model=Utilisateur)
def create_utilisateur(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    existing = utilisateur_crud.get_utilisateur_by_email(db, utilisateur.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    return utilisateur_crud.create_utilisateur(db, utilisateur)
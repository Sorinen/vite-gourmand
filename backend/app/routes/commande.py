from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.commande import Commande, CommandeCreate
from app.crud import commande as commande_crud
from app.utils.dependencies import get_current_user
from app.models.utilisateur import Utilisateur

router = APIRouter(prefix="/commandes", tags=["commandes"])

@router.get("/", response_model=list[Commande])
def read_commandes(db: Session = Depends(get_db)):
    return commande_crud.get_commandes(db)

@router.post("/", response_model=Commande)
def create_commande(
    commande: CommandeCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    return commande_crud.create_commande(db, commande)
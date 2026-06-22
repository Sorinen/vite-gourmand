from fastapi import APIRouter ,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.historique_statut import HistoriqueStatut, HistoriqueStatutCreate
from app.crud import historique_statut as historique_statut_crud

router = APIRouter(prefix="/historique-statuts", tags=["historique-statuts "])

@router.get("/", response_model=list[HistoriqueStatut])
def read_historique_statuts(db: Session = Depends(get_db)):
    return historique_statut_crud.get_historique_statuts(db)

@router.post("/", response_model=HistoriqueStatut)
def create_historique_statut(historique_statut: HistoriqueStatutCreate, db: Session = Depends(get_db)):
    return historique_statut_crud.create_historique_statut(db, historique_statut)

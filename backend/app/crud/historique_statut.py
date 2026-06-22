from sqlalchemy.orm import Session
from app.models.historique_statut import HistoriqueStatut as HistoriqueStatutModel
from app.schemas.historique_statut import HistoriqueStatutCreate

def get_historique_statuts(db: Session):
    return db.query(HistoriqueStatutModel).all()

def get_historique_statut(db: Session, historique_statut_id: int):
    return db.query(HistoriqueStatutModel).filter(HistoriqueStatutModel.id == historique_statut_id).first()

def create_historique_statut(db: Session, historique_statut: HistoriqueStatutCreate):
    db_historique_statut = HistoriqueStatutModel(
        statut=historique_statut.statut,
        commande_id=historique_statut.commande_id,
        modifie_par=historique_statut.modifie_par
    )
    db.add(db_historique_statut)
    db.commit()
    db.refresh(db_historique_statut)
    return db_historique_statut
    
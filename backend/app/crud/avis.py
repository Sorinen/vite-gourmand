from sqlalchemy.orm import Session
from app.models.avis import Avis
from app.schemas.avis import AvisCreate

def get_all_avis(db: Session):
    return db.query(Avis).all()

def get_avis_by_id(db: Session, avis_id: int):
    return db.query(Avis).filter(Avis.id == avis_id).first()

def create_avis(db: Session, avis_data: AvisCreate):
    nouvel_avis = Avis(
        note=avis_data.note,
        commentaire=avis_data.commentaire,
        statut=avis_data.statut,
        commande_id=avis_data.commande_id,
        utilisateur_id=avis_data.utilisateur_id,
        menu_id=avis_data.menu_id
    )
    db.add(nouvel_avis)
    db.commit()
    db.refresh(nouvel_avis)
    return nouvel_avis

def delete_avis(db: Session, avis_id: int):
    avis = get_avis_by_id(db, avis_id)
    if not avis:
        return None
    db.delete(avis)
    db.commit()
    return avis
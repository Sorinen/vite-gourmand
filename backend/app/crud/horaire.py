from sqlalchemy.orm import Session
from app.models.horaire import Horaire
from app.schemas.horaire import HoraireCreate


def get_horaire(db: Session):
    return db.query(Horaire).all()


def get_horaire_by_id(db: Session, horaire_id: int):
    return db.query(Horaire).filter(Horaire.id == horaire_id).first()


def create_horaire(db: Session, horaire: HoraireCreate):
    db_horaire = Horaire(libelle=horaire.libelle)
    db.add(db_horaire)
    db.commit()
    db.refresh(db_horaire)
    return db_horaire
from sqlalchemy.orm import Session
from app.models.allergene import Allergene
from app.schemas.allergene import AllergeneCreate


def get_allergenes(db: Session):
    return db.query(Allergene).all()

def get_allergene(db: Session, allergene_id: int):
    return db.query(Allergene).filter(Allergene.id == allergene_id).first()

def create_allergene(db: Session, allergene: AllergeneCreate):
    db_allergene = Allergene(libelle=allergene.libelle)
    db.add(db_allergene)
    db.commit()
    db.refresh(db_allergene)
    return db_allergene
    
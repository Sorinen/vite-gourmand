from sqlalchemy.orm import Session
from app.models.plat import Plat
from app.schemas.plat import PlatCreate


def get_plats(db: Session):
    return db.query(Plat).all()

def get_plat(db: Session, plat_id: int):
    return db.query(Plat).filter(Plat.id == plat_id).first()

def create_plat(db: Session, plat: PlatCreate):
    db_plat = Plat(**plat.dict())
    db.add(db_plat)
    db.commit()
    db.refresh(db_plat)
    return db_plat
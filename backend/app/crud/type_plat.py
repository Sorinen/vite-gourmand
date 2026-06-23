from sqlalchemy.orm import Session
from app.models.type_plat import TypePlat
from app.schemas.type_plat import TypePlatCreate


def get_type_plats(db: Session):
    return db.query(TypePlat).all()


def get_type_plat(db: Session, type_plat_id: int):
    return db.query(TypePlat).filter(TypePlat.id == type_plat_id).first()


def create_type_plat(db: Session, type_plat: TypePlatCreate):
    db_type_plat = TypePlat(libelle=type_plat.libelle)
    db.add(db_type_plat)
    db.commit()
    db.refresh(db_type_plat)
    return db_type_plat
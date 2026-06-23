from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate


def get_roles(db: Session):
    return db.query(Role).all()


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def create_role(db: Session, role: RoleCreate):
    db_role = Role(libelle=role.libelle)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role
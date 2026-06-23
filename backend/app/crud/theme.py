from sqlalchemy.orm import Session
from app.models.theme import Theme
from app.schemas.theme import ThemeCreate


def get_themes(db: Session):
    return db.query(Theme).all()


def get_theme(db: Session, theme_id: int):
    return db.query(Theme).filter(Theme.id == theme_id).first()


def create_theme(db: Session, theme: ThemeCreate):
    db_theme = Theme(libelle=theme.libelle)
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme
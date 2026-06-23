from sqlalchemy.orm import Session
from app.models.regime import Regime
from app.schemas.regime import RegimeCreate


def get_regimes(db: Session):
    return db.query(Regime).all()


def get_regime(db: Session, regime_id: int):
    return db.query(Regime).filter(Regime.id == regime_id).first()


def create_regime(db: Session, regime: RegimeCreate):
    db_regime = Regime(libelle=regime.libelle)
    db.add(db_regime)
    db.commit()
    db.refresh(db_regime)
    return db_regime
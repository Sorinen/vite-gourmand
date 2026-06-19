from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.regime import Regime, RegimeCreate
from app.crud import regime as regime_crud

router = APIRouter(prefix="/regimes", tags=["regimes"])


@router.get("/", response_model=list[Regime])
def read_regimes(db: Session = Depends(get_db)):
    return regime_crud.get_regimes(db)


@router.post("/", response_model=Regime)
def create_regime(regime: RegimeCreate, db: Session = Depends(get_db)):
    return regime_crud.create_regime(db, regime)
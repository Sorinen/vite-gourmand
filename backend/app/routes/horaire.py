from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.horaire import Horaire, HoraireCreate
from app.crud import horaire as horaire_crud
from app.utils.dependencies import require_role

router = APIRouter(prefix="/horaire", tags=["horaire"])


@router.get("/", response_model=list[Horaire])
def read_horaire(db: Session = Depends(get_db)):
    return horaire_crud.get_horaire(db)


@router.post("/", response_model=Horaire)
def create_horaire(
    horaire: HoraireCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur", "employé"))
):
    return horaire_crud.create_horaire(db, horaire)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.allergene import Allergene, AllergeneCreate
from app.crud import allergene as allergene_crud
from app.utils.dependencies import require_role

router = APIRouter(prefix="/allergenes", tags=["allergenes"])


@router.get("/", response_model=list[Allergene])
def read_allergenes(db: Session = Depends(get_db)):
    return allergene_crud.get_allergenes(db)


@router.post("/", response_model=Allergene)
def create_allergene(
    allergene: AllergeneCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur", "employé"))
):
    return allergene_crud.create_allergene(db, allergene)
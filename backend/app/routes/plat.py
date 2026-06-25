from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.plat import Plat, PlatCreate
from app.crud import plat as plat_crud
from app.utils.dependencies import require_role

router = APIRouter(prefix="/plat", tags=["plat"])

@router.get("/", response_model=list[Plat])
def read_plats(db: Session = Depends(get_db)):
    return plat_crud.get_plats(db)

@router.get("/{plat_id}", response_model=Plat)
def read_plat(plat_id: int, db: Session = Depends(get_db)):
    plat = plat_crud.get_plat(db, plat_id)

    if plat is None:
        raise HTTPException(
            status_code=404,
            detail="Plat non trouvé"
        )
    return plat

@router.post("/", response_model=Plat)
def create_plat(
    plat: PlatCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur", "employé"))
):
    return plat_crud.create_plat(db, plat)
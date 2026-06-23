from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.type_plat import TypePlat, TypePlatCreate
from app.crud import type_plat as type_plat_crud
from app.utils.dependencies import require_role

router = APIRouter(prefix="/type_plats", tags=["type_plats"])

@router.get("/", response_model=list[TypePlat])
def read_type_plats(db: Session = Depends(get_db)):
    return type_plat_crud.get_type_plats(db)

@router.post("/", response_model=TypePlat)
def create_type_plat(
    type_plat: TypePlatCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur", "employé"))
):
    return type_plat_crud.create_type_plat(db, type_plat)
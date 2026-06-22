from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.avis import Avis, AvisCreate
from app.crud.avis import (
    get_all_avis,
    get_avis_by_id,
    create_avis,
    delete_avis,
)

router = APIRouter(
    prefix="/avis",
    tags=["Avis"]
)


@router.get("/", response_model=list[Avis])
def read_all_avis(db: Session = Depends(get_db)):
    return get_all_avis(db)


@router.get("/{avis_id}", response_model=Avis)
def read_avis(avis_id: int, db: Session = Depends(get_db)):
    avis = get_avis_by_id(db, avis_id)

    if not avis:
        raise HTTPException(
            status_code=404,
            detail="Avis introuvable"
        )

    return avis


@router.post("/", response_model=Avis, status_code=201)
def create_new_avis(
    avis: AvisCreate,
    db: Session = Depends(get_db)
):
    return create_avis(db, avis)


@router.delete("/{avis_id}")
def remove_avis(
    avis_id: int,
    db: Session = Depends(get_db)
):
    avis = delete_avis(db, avis_id)

    if not avis:
        raise HTTPException(
            status_code=404,
            detail="Avis introuvable"
        )

    return {
        "message": "Avis supprimé avec succès"
    }
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.theme import Theme, ThemeCreate
from app.crud import theme as theme_crud
from app.utils.dependencies import require_role

router = APIRouter(prefix="/themes", tags=["themes"])

@router.get("/", response_model=list[Theme])
def read_themes(db: Session = Depends(get_db)):
    return theme_crud.get_themes(db)

@router.post("/", response_model=Theme)
def create_theme(
    theme: ThemeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur", "employé"))
):
    return theme_crud.create_theme(db, theme)
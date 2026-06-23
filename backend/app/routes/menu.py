from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.menu import Menu, MenuCreate
from app.crud import menu as menu_crud
from app.utils.dependencies import require_role

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/", response_model=list[Menu])
def read_menus(db: Session = Depends(get_db)):
    return menu_crud.get_menus(db)

@router.post("/", response_model=Menu)
def create_menu(
    menu: MenuCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur", "employé"))
):
    return menu_crud.create_menu(db, menu)
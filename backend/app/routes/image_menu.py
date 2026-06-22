from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.image_menu import ImageMenu, ImageMenuCreate
from app.crud import image_menu as image_menu_crud

router = APIRouter(prefix="/image_menu", tags=["image_menu"])


@router.get("/", response_model=list[ImageMenu])
def read_image_menus(db: Session = Depends(get_db)):
    return image_menu_crud.get_image_menus(db)


@router.post("/", response_model=ImageMenu)
def create_image_menu(image_menu: ImageMenuCreate, db: Session = Depends(get_db)):
    return image_menu_crud.create_image_menu(db, image_menu)
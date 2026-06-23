from sqlalchemy.orm import Session
from app.models.image_menu import ImageMenu
from app.schemas.image_menu import ImageMenuCreate


def get_image_menus(db: Session):
    return db.query(ImageMenu).all()


def get_image_menu_by_id(db: Session, image_menu_id: int):
    return db.query(ImageMenu).filter(ImageMenu.id == image_menu_id).first()


def create_image_menu(db: Session, image_menu: ImageMenuCreate):
    db_image_menu = ImageMenu(**image_menu.dict())
    db.add(db_image_menu)
    db.commit()
    db.refresh(db_image_menu)
    return db_image_menu
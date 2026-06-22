from sqlalchemy import Column, Integer, String , Boolean ,ForeignKey
from app.database import Base


class ImageMenu(Base):
    __tablename__ = "image_menu"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    ordre = Column(Integer, nullable=False)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
    
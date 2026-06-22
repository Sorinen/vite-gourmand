from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class MenuPlat(Base):
    __tablename__ = "menu_plat"

    menu_id = Column(Integer, ForeignKey("menu.id"), primary_key=True)
    plat_id = Column(Integer, ForeignKey("plat.id"), primary_key=True)
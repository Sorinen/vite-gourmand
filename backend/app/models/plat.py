from sqlalchemy import Column, Integer, String , Boolean ,ForeignKey
from app.database import Base


class Plat(Base):
    __tablename__ = "plat"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    photo = Column(String, nullable=False)
    type_plat_id = Column(Integer, ForeignKey("type_plat.id"), nullable=False)

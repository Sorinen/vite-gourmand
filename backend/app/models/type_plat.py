from sqlalchemy import Column, Integer, String
from app.database import Base


class TypePlat(Base):
    __tablename__ = "type_plat"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String, nullable=False)
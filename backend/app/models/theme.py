from sqlalchemy import Column, Integer, String
from app.database import Base


class Theme(Base):
    __tablename__ = "theme"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String, nullable=False)
from sqlalchemy import Column, Integer, String
from app.database import Base


class Horaire(Base):
    __tablename__ = "horaire"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String, nullable=False)
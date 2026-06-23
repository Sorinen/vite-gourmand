from sqlalchemy import Column, Integer, String
from app.database import Base


class Allergene(Base):
    __tablename__ = "allergene"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String, nullable=False)
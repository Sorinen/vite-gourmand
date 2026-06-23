from sqlalchemy import Column, Integer, String
from app.database import Base


class Regime(Base):
    __tablename__ = "regime"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String, nullable=False)
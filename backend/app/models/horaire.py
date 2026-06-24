from sqlalchemy import Column, Integer, String, Boolean, Time
from app.database import Base

class Horaire(Base):
    __tablename__ = "horaire"
    id = Column(Integer, primary_key=True, index=True)
    jour = Column(String, nullable=False)
    heure_ouverture = Column(Time, nullable=True)
    heure_fermeture = Column(Time, nullable=True)
    ferme = Column(Boolean, default=False)
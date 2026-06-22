from sqlalchemy import Column, Integer, String , Boolean ,ForeignKey,Numeric
from app.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    description = Column(String, nullable=False)
    nombre_personnes_min = Column(Integer, nullable=False)
    prix_base = Column(Numeric(10, 2), nullable=False)
    conditions = Column(String, nullable=False)
    stock_disponible = Column(Integer, nullable=False)
    actif = Column(Boolean, nullable=False)
    theme_id = Column(Integer, ForeignKey("theme.id"), nullable=False)
    regime_id = Column(Integer, ForeignKey("regime.id"), nullable=False)
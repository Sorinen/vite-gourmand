from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import Base
from datetime import datetime, timezone

class Avis(Base):
    __tablename__ = "avis"
    id = Column(Integer, primary_key=True, index=True)
    note = Column(Integer, nullable=False)
    commentaire = Column(String, nullable=True)
    statut = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    commande_id = Column(Integer, ForeignKey("commande.id"), nullable=False)
    utilisateur_id = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=True)
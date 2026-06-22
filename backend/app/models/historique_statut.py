from sqlalchemy import Column, Integer, String,DateTime ,ForeignKey
from app.database import Base
from datetime import datetime, timezone



class HistoriqueStatut(Base):
    __tablename__ = "historique_statut"

    id = Column(Integer, primary_key=True, index=True)
    statut = Column(String, nullable=False)  
    date_changement = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    commande_id = Column(Integer, ForeignKey("commande.id"), nullable=False)  
    modifie_par = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
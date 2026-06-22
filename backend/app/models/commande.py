from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Date, Time, DateTime
from datetime import datetime, timezone
from app.database import Base

class Commande(Base):
    __tablename__ = "commande"

    id = Column(Integer, primary_key=True, index=True)
    date_prestation = Column(Date, nullable=False)
    heure_livraison = Column(Time, nullable=False)
    adresse_livraison = Column(String, nullable=False)
    nombre_personnes = Column(Integer, nullable=False)
    prix_menu = Column(Numeric(10, 2), nullable=False)
    prix_livraison = Column(Numeric(10, 2), nullable=False)
    prix_total = Column(Numeric(10, 2), nullable=False)
    statut = Column(String, nullable=False)
    motif_annulation = Column(String, nullable=True)
    mode_contact = Column(String, nullable=True)
    pret_materiel = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    utilisateur_id = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
from sqlalchemy.orm import Session
from app.models.commande import Commande
from app.schemas.commande import CommandeCreate

def get_commandes(db: Session):
    return db.query(Commande).all()

def get_commande(db: Session, commande_id: int):
    return db.query(Commande).filter(Commande.id == commande_id).first()

def get_commande_by_utilisateur_id(db: Session, utilisateur_id: int):
    return db.query(Commande).filter(Commande.utilisateur_id == utilisateur_id).first()


def create_commande(db: Session, commande: CommandeCreate):
    db_commande = Commande(
        date_prestation=commande.date_prestation,
        heure_livraison=commande.heure_livraison,
        adresse_livraison=commande.adresse_livraison,
        nombre_personnes=commande.nombre_personnes,
        prix_menu=commande.prix_menu,
        prix_livraison=commande.prix_livraison,
        prix_total=commande.prix_total,
        statut=commande.statut,
        motif_annulation=commande.motif_annulation,
        mode_contact=commande.mode_contact,
        pret_materiel=commande.pret_materiel,
        utilisateur_id=commande.utilisateur_id,
        menu_id=commande.menu_id
    )
    db.add(db_commande)
    db.commit()
    db.refresh(db_commande)
    return db_commande  

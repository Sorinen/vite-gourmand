from sqlalchemy.orm import Session
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate
from app.utils.securite import hash_password

def get_utilisateurs(db: Session):
    return db.query(Utilisateur).all()

def get_utilisateur(db: Session, utilisateur_id: int):
    return db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()

def get_utilisateur_by_email(db: Session, email: str):
    return db.query(Utilisateur).filter(Utilisateur.email == email).first()

def create_utilisateur(db: Session, utilisateur: UtilisateurCreate):
    hashed = hash_password(utilisateur.mot_de_passe)
    db_utilisateur = Utilisateur(
        email=utilisateur.email,
        mot_de_passe=hashed,
        nom=utilisateur.nom,
        prenom=utilisateur.prenom,
        telephone=utilisateur.telephone,
        adresse_postale=utilisateur.adresse_postale,
        role_id=utilisateur.role_id
    )
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur
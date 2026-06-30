import secrets
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.utilisateur import get_utilisateur_by_email
from app.utils.securite import verify_password, hash_password
from app.utils.jwt import create_access_token
from app.utils.mail import mail_reinitialisation_mdp

router = APIRouter(prefix="/auth", tags=["auth"])

class DemandeReinitialisation(BaseModel):
    email: str

class ConfirmationReinitialisation(BaseModel):
    token: str
    nouveau_mot_de_passe: str

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_utilisateur_by_email(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    if not verify_password(form_data.password, user.mot_de_passe):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    token = create_access_token(data={"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/mot-de-passe-oublie")
def demander_reinitialisation(data: DemandeReinitialisation, db: Session = Depends(get_db)):
    user = get_utilisateur_by_email(db, data.email)
    if not user:
        return {"message": "Si cet email existe, un lien de réinitialisation a été envoyé."}

    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    db.commit()

    mail_reinitialisation_mdp(user.email, user.prenom, token)

    return {"message": "Si cet email existe, un lien de réinitialisation a été envoyé."}

@router.post("/reinitialiser-mot-de-passe")
def reinitialiser_mot_de_passe(data: ConfirmationReinitialisation, db: Session = Depends(get_db)):
    from app.models.utilisateur import Utilisateur

    user = db.query(Utilisateur).filter(Utilisateur.reset_token == data.token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Lien invalide ou expiré")

    if not user.reset_token_expiration or user.reset_token_expiration < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Lien expiré, veuillez refaire une demande")

    user.mot_de_passe = hash_password(data.nouveau_mot_de_passe)
    user.reset_token = None
    user.reset_token_expiration = None
    db.commit()

    return {"message": "Mot de passe réinitialisé avec succès"}

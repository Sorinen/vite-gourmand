from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.utilisateur import Utilisateur, UtilisateurCreate, UtilisateurUpdate
from app.crud import utilisateur as utilisateur_crud
from app.utils.mail import mail_bienvenue, mail_employe_cree
from app.utils.dependencies import require_role, get_current_user
from app.utils.securite import hash_password
from app.models.utilisateur import Utilisateur as UtilisateurModel

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])

class EmployeCreate(BaseModel):
    email: str
    mot_de_passe: str
    nom: str
    prenom: str

class ToggleActif(BaseModel):
    actif: bool

@router.get("/", response_model=list[Utilisateur])
def read_utilisateurs(db: Session = Depends(get_db)):
    return utilisateur_crud.get_utilisateurs(db)

@router.get("/{utilisateur_id}", response_model=Utilisateur)
def read_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    utilisateur = utilisateur_crud.get_utilisateur(db, utilisateur_id)
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

@router.post("/", response_model=Utilisateur)
def create_utilisateur(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    existing = utilisateur_crud.get_utilisateur_by_email(db, utilisateur.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    nouvel_utilisateur = utilisateur_crud.create_utilisateur(db, utilisateur)
    mail_bienvenue(nouvel_utilisateur.email, nouvel_utilisateur.prenom)
    return nouvel_utilisateur

@router.post("/admin/creer-employe", response_model=Utilisateur)
def creer_employe(
    data: EmployeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur"))
):
    existing = utilisateur_crud.get_utilisateur_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    employe = UtilisateurModel(
        email=data.email,
        mot_de_passe=hash_password(data.mot_de_passe),
        nom=data.nom,
        prenom=data.prenom,
        telephone=None,
        adresse_postale=None,
        actif=True,
        role_id=2
    )
    db.add(employe)
    db.commit()
    db.refresh(employe)

    mail_employe_cree(data.email)

    return employe

@router.patch("/admin/employes/{employe_id}/actif")
def toggle_actif_employe(
    employe_id: int,
    data: ToggleActif,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur"))
):
    employe = utilisateur_crud.get_utilisateur(db, employe_id)
    if not employe:
        raise HTTPException(status_code=404, detail="Employé introuvable")
    if employe.role_id != 2:
        raise HTTPException(status_code=400, detail="Ce compte n'est pas un employé")

    employe.actif = data.actif
    db.commit()
    return {"message": f"Compte {'activé' if data.actif else 'désactivé'} avec succès"}

@router.get("/admin/employes")
def get_employes(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur"))
):
    employes = db.query(UtilisateurModel).filter(UtilisateurModel.role_id == 2).all()
    return [
        {
            "id": e.id,
            "email": e.email,
            "nom": e.nom,
            "prenom": e.prenom,
            "actif": e.actif
        }
        for e in employes
    ]

@router.patch("/{utilisateur_id}", response_model=Utilisateur)
def update_utilisateur(
    utilisateur_id: int,
    data: UtilisateurUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    from app.schemas.utilisateur import UtilisateurUpdate as UU
    utilisateur = utilisateur_crud.get_utilisateur(db, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    if utilisateur.id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(utilisateur, key, value)
    db.commit()
    db.refresh(utilisateur)
    return utilisateur

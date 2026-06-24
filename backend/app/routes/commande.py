from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.commande import Commande, CommandeCreate
from app.crud import commande as commande_crud
from app.crud.menu import get_menu
from app.utils.dependencies import get_current_user
from app.models.utilisateur import Utilisateur
from app.utils.mail import mail_confirmation_commande
from app.services.stats_service import enregistrer_commande_stats

router = APIRouter(prefix="/commandes", tags=["commandes"])


@router.get("/", response_model=list[Commande])
def read_commandes(db: Session = Depends(get_db)):
    return commande_crud.get_commandes(db)


@router.post("/", response_model=Commande)
def create_commande(
    commande: CommandeCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    menu = get_menu(db, commande.menu_id)

    if not menu:
        raise HTTPException(
            status_code=404,
            detail="Menu introuvable"
        )

    nouvelle_commande = commande_crud.create_commande(db, commande)

    background_tasks.add_task(
        enregistrer_commande_stats,
        commande_id=nouvelle_commande.id,
        menu_id=nouvelle_commande.menu_id,
        menu_titre=menu.titre,
        prix_total=float(nouvelle_commande.prix_total),
        nombre_personnes=nouvelle_commande.nombre_personnes
    )

    background_tasks.add_task(
        mail_confirmation_commande,
        current_user.email,
        current_user.prenom,
        nouvelle_commande.id
    )

    return nouvelle_commande
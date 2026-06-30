from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.commande import Commande, CommandeCreate
from app.crud import commande as commande_crud
from app.crud.menu import get_menu
from app.utils.dependencies import get_current_user, require_role
from app.models.utilisateur import Utilisateur
from app.models.historique_statut import HistoriqueStatut
from app.utils.mail import mail_confirmation_commande, mail_commande_terminee
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
        raise HTTPException(status_code=404, detail="Menu introuvable")

    nouvelle_commande = commande_crud.create_commande(db, commande)

    historique = HistoriqueStatut(
        statut=nouvelle_commande.statut,
        commande_id=nouvelle_commande.id,
        modifie_par=current_user.id
    )
    db.add(historique)
    db.commit()

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

@router.patch("/{commande_id}/statut")
def changer_statut(
    commande_id: int,
    data: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Administrateur", "employé"))
):
    commande = commande_crud.get_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    nouveau_statut = data["statut"]
    commande.statut = nouveau_statut

    if "motif_annulation" in data:
        commande.motif_annulation = data["motif_annulation"]
    if "mode_contact" in data:
        commande.mode_contact = data["mode_contact"]

    db.commit()
    db.refresh(commande)

    historique = HistoriqueStatut(
        statut=nouveau_statut,
        commande_id=commande.id,
        modifie_par=current_user.id
    )
    db.add(historique)
    db.commit()

    if nouveau_statut == "terminee":
        client = db.query(Utilisateur).filter(Utilisateur.id == commande.utilisateur_id).first()
        if client:
            background_tasks.add_task(
                mail_commande_terminee,
                client.email,
                client.prenom,
                commande.id
            )

    return commande

@router.get("/{commande_id}/historique")
def get_historique(commande_id: int, db: Session = Depends(get_db)):
    historique = db.query(HistoriqueStatut).filter(
        HistoriqueStatut.commande_id == commande_id
    ).order_by(HistoriqueStatut.date_changement).all()
    return [
        {
            "id": h.id,
            "statut": h.statut,
            "date_changement": h.date_changement
        }
        for h in historique
    ]

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.commande import Commande, CommandeCreate, CommandeUpdate
from app.crud import commande as commande_crud
from app.crud.menu import get_menu
from app.utils.dependencies import get_current_user, require_role
from app.models.utilisateur import Utilisateur
from app.models.historique_statut import HistoriqueStatut
from app.utils.mail import mail_confirmation_commande, mail_commande_terminee, mail_retour_materiel
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

    if menu.stock_disponible <= 0:
        raise HTTPException(status_code=400, detail="Ce menu n'est plus disponible (stock épuisé)")

    nouvelle_commande = commande_crud.create_commande(db, commande)

    menu.stock_disponible -= 1
    db.commit()

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

@router.put("/{commande_id}", response_model=Commande)
def update_commande(
    commande_id: int,
    data: CommandeUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    commande = commande_crud.get_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    if commande.utilisateur_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous ne pouvez modifier que vos propres commandes")

    if commande.statut != "en_attente":
        raise HTTPException(status_code=400, detail="Cette commande ne peut plus être modifiée")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(commande, key, value)

    db.commit()
    db.refresh(commande)
    return commande

@router.delete("/{commande_id}")
def annuler_commande_client(
    commande_id: int,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    commande = commande_crud.get_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    if commande.utilisateur_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous ne pouvez annuler que vos propres commandes")

    if commande.statut != "en_attente":
        raise HTTPException(status_code=400, detail="Cette commande ne peut plus être annulée")

    commande.statut = "annulee"
    db.commit()

    menu = get_menu(db, commande.menu_id)
    if menu:
        menu.stock_disponible += 1
        db.commit()

    historique = HistoriqueStatut(
        statut="annulee",
        commande_id=commande.id,
        modifie_par=current_user.id
    )
    db.add(historique)
    db.commit()

    return {"message": "Commande annulée"}

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

    ancien_statut = commande.statut
    nouveau_statut = data["statut"]
    commande.statut = nouveau_statut

    if "motif_annulation" in data:
        commande.motif_annulation = data["motif_annulation"]
    if "mode_contact" in data:
        commande.mode_contact = data["mode_contact"]

    if nouveau_statut == "annulee" and ancien_statut != "annulee":
        menu = get_menu(db, commande.menu_id)
        if menu:
            menu.stock_disponible += 1

    db.commit()
    db.refresh(commande)

    historique = HistoriqueStatut(
        statut=nouveau_statut,
        commande_id=commande.id,
        modifie_par=current_user.id
    )
    db.add(historique)
    db.commit()

    client = db.query(Utilisateur).filter(Utilisateur.id == commande.utilisateur_id).first()

    if nouveau_statut == "terminee" and client:
        background_tasks.add_task(
            mail_commande_terminee,
            client.email,
            client.prenom,
            commande.id
        )

    if nouveau_statut == "en_attente_retour_materiel" and client:
        background_tasks.add_task(
            mail_retour_materiel,
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

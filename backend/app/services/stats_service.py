from app.mongodb import collection_commandes
from datetime import datetime

async def enregistrer_commande_stats(
    commande_id: int,
    menu_id: int,
    menu_titre: str,
    prix_total: float,
    nombre_personnes: int
):
    await collection_commandes.insert_one({
        "commande_id": commande_id,
        "menu_id": menu_id,
        "menu_titre": menu_titre,
        "prix_total": prix_total,
        "nombre_personnes": nombre_personnes,
        "date": datetime.utcnow()
    })

async def get_stats_par_menu():
    pipeline = [
        {
            "$group": {
                "_id": "$menu_id",
                "menu_titre": {"$first": "$menu_titre"},
                "nombre_commandes": {"$sum": 1},
                "chiffre_affaires": {"$sum": "$prix_total"}
            }
        },
        {"$sort": {"nombre_commandes": -1}}
    ]
    cursor = collection_commandes.aggregate(pipeline)
    return await cursor.to_list(length=100)
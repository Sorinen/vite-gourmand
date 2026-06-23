def calculer_prix(
    prix_base_menu,
    nombre_personnes,
    nombre_personnes_min,
    ville,
    distance_km
):
    # Prix du menu
    prix_menu = prix_base_menu * nombre_personnes

    # Remise de 10 %
    if nombre_personnes >= nombre_personnes_min + 5:
        prix_menu *= 0.90
        
    # Prix de livraison
    if ville.lower() == "bordeaux":
        prix_livraison = 0
    else:
        prix_livraison = 5 + (distance_km * 0.59)

    # Prix total
    prix_total = prix_menu + prix_livraison
    return {
        "prix_menu": round(prix_menu, 2),
        "prix_livraison": round(prix_livraison, 2),
        "prix_total": round(prix_total, 2)
    }
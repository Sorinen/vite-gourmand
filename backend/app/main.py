from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import utilisateur, role, theme, regime, allergene, type_plat, horaire, contact, menu, plat, image_menu, commande, historique_statut, avis, auth, stats
from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vite & Gourmand API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://zotpresta.re",
        "https://api.zotpresta.re"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(role.router)
app.include_router(theme.router)
app.include_router(regime.router)
app.include_router(allergene.router)
app.include_router(type_plat.router)
app.include_router(horaire.router)
app.include_router(contact.router)
app.include_router(utilisateur.router)
app.include_router(menu.router)
app.include_router(plat.router)
app.include_router(image_menu.router)
app.include_router(commande.router)
app.include_router(historique_statut.router)
app.include_router(avis.router)
app.include_router(auth.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {"message": "API Vite & Gourmand"}
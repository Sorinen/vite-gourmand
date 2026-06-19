from fastapi import FastAPI
from app.routes import utilisateur
from app.routes import role,theme,regime,allergene,type_plat,horaire,contact

app = FastAPI(title="Vite & Gourmand API")

app.include_router(role.router)
app.include_router(theme.router)
app.include_router(regime.router)
app.include_router(allergene.router)
app.include_router(type_plat.router)
app.include_router(horaire.router)
app.include_router(contact.router)
app.include_router(utilisateur.router)

@app.get("/")
def root():
    return {"message": "API Vite & Gourmand"}

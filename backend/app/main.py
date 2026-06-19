from fastapi import FastAPI
from app.routes import role

app = FastAPI(title="Vite & Gourmand API")

app.include_router(role.router)


@app.get("/")
def root():
    return {"message": "API Vite & Gourmand"}
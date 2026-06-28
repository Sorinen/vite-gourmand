from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.contact import Contact, ContactCreate
from app.crud import contact as contact_crud

router = APIRouter(prefix="/contact", tags=["contact"])

@router.get("/", response_model=list[Contact])
def read_contacts(db: Session = Depends(get_db)):
    return contact_crud.get_contacts(db)

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return contact_crud.create_contact(db, contact)

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = contact_crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact introuvable")
    db.delete(contact)
    db.commit()
    return {"message": "Message supprimé"}
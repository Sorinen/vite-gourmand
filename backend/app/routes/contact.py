from fastapi import APIRouter, Depends
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
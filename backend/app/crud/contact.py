from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate

def get_contacts(db: Session):
    return db.query(Contact).all()

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(
        nom=contact.nom,
        email=contact.email,
        telephone=contact.telephone,
        message=contact.message
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

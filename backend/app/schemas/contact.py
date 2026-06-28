from pydantic import BaseModel
from typing import Optional

class ContactBase(BaseModel):
    nom: str
    email: str
    telephone: Optional[str] = None
    message: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    class Config:
        from_attributes = True
from pydantic import BaseModel


class ContactBase(BaseModel):
    libelle: str


class ContactCreate(ContactBase ):
    pass


class Contact(ContactBase):
    id: int

    class Config:
        from_attributes = True
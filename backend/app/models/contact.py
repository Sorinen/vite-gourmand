from sqlalchemy import Column, Integer, String
from app.database import Base


class Contact(Base):
    __tablename__ = "contact "

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String, nullable=False)
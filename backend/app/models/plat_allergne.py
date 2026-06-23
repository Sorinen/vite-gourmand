from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class PlatAllergene(Base):
    __tablename__ = "plat_allergene"

    plat_id = Column(Integer, ForeignKey("plat.id"), primary_key=True)
    allergene_id = Column(Integer, ForeignKey("allergene.id"), primary_key=True)
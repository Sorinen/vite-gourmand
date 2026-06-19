from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.role import Role, RoleCreate
from app.crud import role as role_crud

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=list[Role])
def read_roles(db: Session = Depends(get_db)):
    return role_crud.get_roles(db)


@router.post("/", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_crud.create_role(db, role)
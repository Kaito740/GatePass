from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.models import Usuario, Rol
from app.schemas.schemas import RolResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=List[RolResponse])
def listar_roles(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    return db.query(Rol).order_by(Rol.id).all()

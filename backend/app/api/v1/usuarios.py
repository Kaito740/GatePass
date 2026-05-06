from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import require_rol
from app.models.models import Usuario, Area
from app.schemas.schemas import AreaCreate, AreaResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ============================================================
# ÁREAS — solo crear, las iniciales vienen del seeder
# ============================================================

@router.post("/areas", response_model=AreaResponse, status_code=201)
def crear_area(
    datos: AreaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol("superadmin"))
):
    """Solo superadmin puede crear nuevas áreas."""
    existe = db.query(Area).filter(Area.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un área con ese nombre"
        )
    area = Area(nombre=datos.nombre)
    db.add(area)
    db.commit()
    db.refresh(area)
    return area

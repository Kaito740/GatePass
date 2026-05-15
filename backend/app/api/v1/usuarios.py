from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_rol
from app.core.roles import Rol
from app.models.models import Usuario, Area
from app.schemas.schemas import (
    UsuarioCreate, UsuarioResponse,
    AreaCreate, AreaUpdate, AreaResponse,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# USUARIOS

@router.get("", response_model=List[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return (
        db.query(Usuario)
        .options(selectinload(Usuario.rol), selectinload(Usuario.area))
        .order_by(Usuario.id)
        .all()
    )


@router.post("", response_model=UsuarioResponse, status_code=201)
def crear_usuario(
    datos: UsuarioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN)),
):
    if db.query(Usuario).filter(Usuario.dni == datos.dni).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese DNI",
        )

    if datos.telefono_wa:
        if db.query(Usuario).filter(Usuario.telefono_wa == datos.telefono_wa).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con ese teléfono",
            )

    usuario = Usuario(**datos.model_dump())
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return (
        db.query(Usuario)
        .options(selectinload(Usuario.rol), selectinload(Usuario.area))
        .filter(Usuario.id == usuario.id)
        .first()
    )


# ÁREAS

@router.get("/areas", response_model=List[AreaResponse])
def listar_areas(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    """Cualquier usuario autenticado puede ver las áreas."""
    return db.query(Area).order_by(Area.id).all()


@router.post("/areas", response_model=AreaResponse, status_code=201)
def crear_area(
    datos: AreaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
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


@router.put("/areas/{area_id}", response_model=AreaResponse)
def actualizar_area(
    area_id: int,
    datos: AreaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
):
    """Solo superadmin puede actualizar el nombre de un área."""
    area = db.query(Area).filter(Area.id == area_id).first()

    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Área no encontrada"
        )

    duplicado = db.query(Area).filter(
        Area.nombre == datos.nombre,
        Area.id != area_id
    ).first()

    if duplicado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un área con ese nombre"
        )

    area.nombre = datos.nombre
    db.commit()
    db.refresh(area)
    return area


@router.delete("/areas/{area_id}", status_code=204)
def eliminar_area(
    area_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
):
    """
    Elimina un área solo si no tiene usuarios asignados.
    Solo superadmin puede hacer esto.
    """
    area = db.query(Area).filter(Area.id == area_id).first()

    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Área no encontrada"
        )

    # Verifica que no haya usuarios en esta área
    tiene_usuarios = db.query(Usuario).filter(
        Usuario.area_id == area_id
    ).first()

    if tiene_usuarios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un área con usuarios asignados"
        )

    db.delete(area)
    db.commit()

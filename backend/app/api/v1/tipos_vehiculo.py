from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_rol
from app.core.roles import Rol
from app.models.models import Usuario, TipoVehiculo, Vehiculo
from app.schemas.schemas import TipoVehiculoCreate, TipoVehiculoUpdate, TipoVehiculoResponse

router = APIRouter(prefix="/tipos-vehiculo", tags=["Tipos de Vehículo"])


@router.get("/", response_model=List[TipoVehiculoResponse])
def listar_tipos_vehiculo(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    return db.query(TipoVehiculo).order_by(TipoVehiculo.id).all()


@router.post("/", response_model=TipoVehiculoResponse, status_code=201)
def crear_tipo_vehiculo(
    datos: TipoVehiculoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
):
    existe = db.query(TipoVehiculo).filter(TipoVehiculo.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un tipo de vehículo con ese nombre"
        )
    tipo = TipoVehiculo(nombre=datos.nombre)
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo


@router.put("/{tipo_id}", response_model=TipoVehiculoResponse)
def actualizar_tipo_vehiculo(
    tipo_id: int,
    datos: TipoVehiculoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
):
    tipo = db.query(TipoVehiculo).filter(TipoVehiculo.id == tipo_id).first()
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de vehículo no encontrado"
        )
    duplicado = db.query(TipoVehiculo).filter(
        TipoVehiculo.nombre == datos.nombre,
        TipoVehiculo.id != tipo_id
    ).first()
    if duplicado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un tipo de vehículo con ese nombre"
        )
    tipo.nombre = datos.nombre
    db.commit()
    db.refresh(tipo)
    return tipo


@router.delete("/{tipo_id}", status_code=204)
def eliminar_tipo_vehiculo(
    tipo_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
):
    tipo = db.query(TipoVehiculo).filter(TipoVehiculo.id == tipo_id).first()
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de vehículo no encontrado"
        )
    vehiculos_asociados = db.query(Vehiculo).filter(Vehiculo.tipo_id == tipo_id).count()
    if vehiculos_asociados > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"No se puede eliminar: {vehiculos_asociados} vehículo(s) están usando este tipo"
        )
    db.delete(tipo)
    db.commit()

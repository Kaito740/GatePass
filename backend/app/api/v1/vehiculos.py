from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_rol
from app.core.roles import Rol
from app.models.models import Usuario, Vehiculo, TipoVehiculo
from app.schemas.schemas import VehiculoCreate, VehiculoUpdate, VehiculoResponse

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


@router.get("/", response_model=List[VehiculoResponse])
def listar_vehiculos(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    return db.query(Vehiculo).order_by(Vehiculo.id).all()


@router.post("/", response_model=VehiculoResponse, status_code=201)
def crear_vehiculo(
    datos: VehiculoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
):
    existe = db.query(Vehiculo).filter(Vehiculo.placa == datos.placa).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un vehículo con esa placa"
        )

    tipo_valido = db.query(TipoVehiculo).filter(TipoVehiculo.id == datos.tipo_id).first()
    if not tipo_valido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tipo de vehículo especificado no existe"
        )

    vehiculo = Vehiculo(**datos.model_dump())
    db.add(vehiculo)
    db.commit()
    db.refresh(vehiculo)
    return vehiculo


@router.put("/{vehiculo_id}", response_model=VehiculoResponse)
def actualizar_vehiculo(
    vehiculo_id: int,
    datos: VehiculoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )

    if datos.placa is not None:
        duplicado = db.query(Vehiculo).filter(
            Vehiculo.placa == datos.placa,
            Vehiculo.id != vehiculo_id
        ).first()
        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro vehículo con esa placa"
            )
        vehiculo.placa = datos.placa

    if datos.tipo_id is not None:
        tipo_valido = db.query(TipoVehiculo).filter(TipoVehiculo.id == datos.tipo_id).first()
        if not tipo_valido:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El tipo de vehículo especificado no existe"
            )
        vehiculo.tipo_id = datos.tipo_id

    if datos.capacidad_pasajeros is not None:
        vehiculo.capacidad_pasajeros = datos.capacidad_pasajeros
    if datos.marca is not None:
        vehiculo.marca = datos.marca
    if datos.modelo is not None:
        vehiculo.modelo = datos.modelo
    if datos.anio is not None:
        vehiculo.anio = datos.anio
    if datos.color is not None:
        vehiculo.color = datos.color
    if datos.soat_vencimiento is not None:
        vehiculo.soat_vencimiento = datos.soat_vencimiento
    if datos.estado_actual is not None:
        vehiculo.estado_actual = datos.estado_actual
    if datos.activo is not None:
        vehiculo.activo = datos.activo

    db.commit()
    db.refresh(vehiculo)
    return vehiculo


@router.delete("/{vehiculo_id}", status_code=204)
def eliminar_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol(Rol.SUPERADMIN))
):
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )

    if vehiculo.asignaciones:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar: el vehículo tiene asignaciones registradas"
        )

    db.delete(vehiculo)
    db.commit()

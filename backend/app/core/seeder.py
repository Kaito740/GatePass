from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.models import Rol, Area, Usuario, CuentaAdmin, TipoVehiculo, Vehiculo
from app.core.security import hashear_password
import os

# ============================================================
# ROLES — fijos, sin endpoint POST
# ============================================================

ROLES = [
    {"id": 1, "nombre": "superadmin"},
    {"id": 2, "nombre": "rrhh"},
    {"id": 3, "nombre": "jefe_area"},
    {"id": 4, "nombre": "conductor"},
    {"id": 5, "nombre": "vigilante"},
]

# ============================================================
# ÁREAS INICIALES — fijas, sin endpoint POST
# ============================================================

AREAS = [
    {"id": 1, "nombre": "Administración"},
    {"id": 2, "nombre": "Recursos Humanos"},
    {"id": 3, "nombre": "Logística"},
    {"id": 4, "nombre": "Operaciones"},
    {"id": 5, "nombre": "Gerencia"},
]

# ============================================================
# SUPERADMIN — credenciales desde .env
# ============================================================

SUPERADMIN = {
    "dni"       : os.getenv("SUPERADMIN_DNI",      "00000000"),
    "nombres"   : os.getenv("SUPERADMIN_NOMBRES",  "Admin"),
    "apellidos" : os.getenv("SUPERADMIN_APELLIDOS", "Sistema"),
    "cargo"     : "Administrador del Sistema",
    "rol_id"    : 1,  # superadmin
    "area_id"   : 5,  # Gerencia
    "activo"    : True,
}

SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD", "admin1234")

# ============================================================
# TIPOS DE VEHÍCULO — fijos, sin endpoint POST
# ============================================================

TIPOS_VEHICULO = [
    {"id": 1, "nombre": "Sedan"},
    {"id": 2, "nombre": "SUV"},
    {"id": 3, "nombre": "Camioneta"},
    {"id": 4, "nombre": "Van"},
    {"id": 5, "nombre": "Bus"},
]

# ============================================================
# VEHÍCULOS INICIALES
# ============================================================

VEHICULOS = [
    {"placa": "ABC-123", "tipo_id": 1, "capacidad_pasajeros": 4,  "marca": "Toyota",   "modelo": "Corolla", "anio": 2020, "color": "Blanco", "soat_vencimiento": "2026-12-31"},
    {"placa": "DEF-456", "tipo_id": 2, "capacidad_pasajeros": 5,  "marca": "Hyundai",  "modelo": "Tucson",  "anio": 2021, "color": "Negro",  "soat_vencimiento": "2026-11-30"},
    {"placa": "GHI-789", "tipo_id": 3, "capacidad_pasajeros": 2,  "marca": "Nissan",   "modelo": "NP300",   "anio": 2022, "color": "Azul",   "soat_vencimiento": "2027-01-15"},
    {"placa": "JKL-012", "tipo_id": 4, "capacidad_pasajeros": 8,  "marca": "Mercedes", "modelo": "Sprinter","anio": 2023, "color": "Blanco", "soat_vencimiento": "2027-03-20"},
    {"placa": "MNO-345", "tipo_id": 5, "capacidad_pasajeros": 30, "marca": "Scania",   "modelo": "K310",    "anio": 2024, "color": "Rojo",   "soat_vencimiento": "2027-05-10"},
    {"placa": "PQR-678", "tipo_id": 1, "capacidad_pasajeros": 4,  "marca": "Mazda",    "modelo": "3",       "anio": 2019, "color": "Gris",   "soat_vencimiento": "2026-08-25"},
    {"placa": "STU-901", "tipo_id": 3, "capacidad_pasajeros": 2,  "marca": "Toyota",   "modelo": "Hilux",   "anio": 2023, "color": "Plata",  "soat_vencimiento": "2027-02-28"},
]


def reset_sequence(db: Session, tabla: str) -> None:
    """
    Resetea la secuencia autoincremental de una tabla al valor
    máximo actual + 1. Necesario cuando insertamos IDs manualmente.
    """
    db.execute(text(
        f"SELECT setval(pg_get_serial_sequence('{tabla}', 'id'), "
        f"COALESCE(MAX(id), 0) + 1, false) FROM {tabla}"
    ))
    db.commit()


def seed_roles(db: Session) -> None:
    for data in ROLES:
        existe = db.query(Rol).filter(Rol.id == data["id"]).first()
        if not existe:
            db.add(Rol(**data))
    db.commit()
    reset_sequence(db, "roles")


def seed_areas(db: Session) -> None:
    for data in AREAS:
        existe = db.query(Area).filter(Area.id == data["id"]).first()
        if not existe:
            db.add(Area(**data))
    db.commit()
    reset_sequence(db, "areas")


def seed_superadmin(db: Session) -> None:
    existe = db.query(Usuario).filter(
        Usuario.dni == SUPERADMIN["dni"]
    ).first()

    if not existe:
        usuario = Usuario(**SUPERADMIN)
        db.add(usuario)
        db.flush()

        cuenta = CuentaAdmin(
            usuario_id=usuario.id,
            password_hash=hashear_password(SUPERADMIN_PASSWORD)
        )
        db.add(cuenta)
        db.commit()


def seed_tipos_vehiculo(db: Session) -> None:
    for data in TIPOS_VEHICULO:
        existe = db.query(TipoVehiculo).filter(TipoVehiculo.id == data["id"]).first()
        if not existe:
            db.add(TipoVehiculo(**data))
    db.commit()
    reset_sequence(db, "tipos_vehiculo")


def seed_vehiculos(db: Session) -> None:
    for data in VEHICULOS:
        existe = db.query(Vehiculo).filter(Vehiculo.placa == data["placa"]).first()
        if not existe:
            db.add(Vehiculo(**data))
    db.commit()
    reset_sequence(db, "vehiculos")


def run_all_seeders(db: Session) -> None:
    seed_roles(db)
    seed_areas(db)
    seed_superadmin(db)
    seed_tipos_vehiculo(db)
    seed_vehiculos(db)

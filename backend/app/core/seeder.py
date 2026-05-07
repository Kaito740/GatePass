from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.models import Rol, Area, Usuario, CuentaAdmin
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


def run_all_seeders(db: Session) -> None:
    seed_roles(db)
    seed_areas(db)
    seed_superadmin(db)

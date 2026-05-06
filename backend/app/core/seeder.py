from sqlalchemy.orm import Session
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


def seed_roles(db: Session) -> None:
    for data in ROLES:
        existe = db.query(Rol).filter(Rol.id == data["id"]).first()
        if not existe:
            db.add(Rol(**data))
    db.commit()


def seed_areas(db: Session) -> None:
    for data in AREAS:
        existe = db.query(Area).filter(Area.id == data["id"]).first()
        if not existe:
            db.add(Area(**data))
    db.commit()


def seed_superadmin(db: Session) -> None:
    existe = db.query(Usuario).filter(
        Usuario.dni == SUPERADMIN["dni"]
    ).first()

    if not existe:
        # Crea el usuario superadmin
        usuario = Usuario(**SUPERADMIN)
        db.add(usuario)
        db.flush()  # genera el id sin hacer commit todavía

        # Crea su cuenta con password hasheado
        cuenta = CuentaAdmin(
            usuario_id=usuario.id,
            password_hash=hashear_password(SUPERADMIN_PASSWORD)
        )
        db.add(cuenta)
        db.commit()


def run_all_seeders(db: Session) -> None:
    seed_roles(db)       # primero roles — usuario depende de ellos
    seed_areas(db)       # luego áreas — usuario depende de ellas
    seed_superadmin(db)  # último — depende de roles y áreas

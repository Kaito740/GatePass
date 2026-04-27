from sqlalchemy.orm import Session
from app.models.models import Rol

# ============================================================
# DATOS SEMILLA — no se crean endpoints para estas tablas
# Se insertan una sola vez al arrancar la app
# ============================================================

ROLES = [
    {"id": 1, "nombre": "superadmin"},
    {"id": 2, "nombre": "rrhh"},
    {"id": 3, "nombre": "jefe_area"},
    {"id": 4, "nombre": "conductor"},
    {"id": 5, "nombre": "vigilante"},
]

def seed_roles(db: Session) -> None:
    for data in ROLES:
        existe = db.query(Rol).filter(Rol.id == data["id"]).first()
        if not existe:
            db.add(Rol(**data))
    db.commit()

def run_all_seeders(db: Session) -> None:
    seed_roles(db)

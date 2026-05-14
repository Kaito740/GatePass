from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import SessionLocal
from app.core.seeder import run_all_seeders
from app.api.v1 import auth, usuarios, tipos_vehiculo, vehiculos, roles


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        run_all_seeders(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="GatePass API",
    description="Sistema de control de pases de salida y flota vehicular",
    version="1.0.0",
    lifespan=lifespan,
)
# ROUTERS
app.include_router(auth.router,     prefix="/api/v1")
app.include_router(usuarios.router,      prefix="/api/v1")
app.include_router(tipos_vehiculo.router, prefix="/api/v1")
app.include_router(vehiculos.router,       prefix="/api/v1")
app.include_router(roles.router,           prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok", "app": "GatePass"}

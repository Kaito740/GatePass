from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import SessionLocal
from app.core.seeder import run_all_seeders


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- AL ARRANCAR ---
    db = SessionLocal()
    try:
        run_all_seeders(db)
    finally:
        db.close()

    yield  # la app corre aquí

    # --- AL APAGAR --- (opcional, para cleanup futuro)


app = FastAPI(
    title="GatePass API",
    description="Sistema de control de pases de salida y flota vehicular",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def health_check():
    return {"status": "ok", "app": "GatePass"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verificar_password, crear_token, hashear_password
from app.core.dependencies import get_current_user, require_rol
from app.models.models import Usuario, CuentaAdmin
from app.schemas.schemas import (
    LoginInput, TokenResponse,
    CuentaAdminCreate, CuentaAdminResponse,
    UsuarioResponse
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


# ============================================================
# LOGIN
# ============================================================

@router.post("/login", response_model=TokenResponse)
def login(datos: LoginInput, db: Session = Depends(get_db)):
    """
    Recibe DNI + password.
    Devuelve un JWT si las credenciales son correctas.
    """
    # 1. Busca el usuario por DNI
    usuario = db.query(Usuario).filter(
        Usuario.dni == datos.dni,
        Usuario.activo == True
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # 2. Busca su cuenta admin
    cuenta = db.query(CuentaAdmin).filter(
        CuentaAdmin.usuario_id == usuario.id
    ).first()

    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Este usuario no tiene acceso al sistema"
        )

    # 3. Verifica el password
    if not verificar_password(datos.password, cuenta.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # 4. Genera el token con el id del usuario en el payload
    token = crear_token(data={"sub": str(usuario.id)})

    return TokenResponse(access_token=token)


# ============================================================
# CREAR CUENTA ADMIN
# Solo el superadmin puede crear cuentas de acceso al sistema
# ============================================================

@router.post("/cuenta", response_model=CuentaAdminResponse, status_code=201)
def crear_cuenta(
    datos: CuentaAdminCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_rol("superadmin"))
):
    """
    Crea una cuenta de acceso al sistema para un usuario existente.
    Solo superadmin puede hacer esto.
    """
    # Verifica que el usuario exista
    usuario = db.query(Usuario).filter(
        Usuario.id == datos.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Verifica que no tenga ya una cuenta
    existe = db.query(CuentaAdmin).filter(
        CuentaAdmin.usuario_id == datos.usuario_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este usuario ya tiene una cuenta de acceso"
        )

    # Crea la cuenta con el password hasheado
    cuenta = CuentaAdmin(
        usuario_id=datos.usuario_id,
        password_hash=hashear_password(datos.password)
    )
    db.add(cuenta)
    db.commit()
    db.refresh(cuenta)

    return cuenta


# ============================================================
# PERFIL PROPIO
# Cualquier usuario autenticado puede ver su propio perfil
# ============================================================

@router.get("/me", response_model=UsuarioResponse)
def mi_perfil(usuario_actual: Usuario = Depends(get_current_user)):
    """
    Devuelve el perfil del usuario autenticado.
    No necesita parámetros — lee el token del header.
    """
    return usuario_actual

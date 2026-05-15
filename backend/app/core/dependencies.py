from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verificar_token
from app.core.roles import Rol
from app.models.models import Usuario, CuentaAdmin

# Muestra un campo simple "Bearer token" en Swagger
http_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia que extrae y valida el token JWT de cada request.
    Si el token es inválido o expiró, lanza 401 automáticamente.
    """
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # HTTPBearer ya extrae el token del header — solo tomamos el valor
    token = credentials.credentials

    payload = verificar_token(token)
    if payload is None:
        raise credenciales_invalidas

    usuario_id: int = payload.get("sub")
    if usuario_id is None:
        raise credenciales_invalidas

    cuenta = db.query(CuentaAdmin).filter(
        CuentaAdmin.usuario_id == int(usuario_id)
    ).first()

    if cuenta is None:
        raise credenciales_invalidas

    usuario = db.query(Usuario).filter(
        Usuario.id == cuenta.usuario_id,
        Usuario.activo == True
    ).first()

    if usuario is None:
        raise credenciales_invalidas

    return usuario


def require_rol(*roles_permitidos: Rol):
    """
    Dependencia que verifica si el usuario tiene el rol necesario.
    """
    def verificar(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.rol.nombre not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere rol: {', '.join(roles_permitidos)}"
            )
        return usuario
    return verificar

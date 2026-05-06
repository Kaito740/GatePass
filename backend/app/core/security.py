from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings
import uuid


# ============================================================
# HASHING DE CONTRASEÑAS — usando bcrypt directo
# ============================================================

def hashear_password(password: str) -> str:
    """Convierte un password en texto plano a un hash seguro."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verificar_password(password_plano: str, password_hash: str) -> bool:
    """Compara un password en texto plano contra su hash guardado en la DB."""
    return bcrypt.checkpw(
        password_plano.encode("utf-8"),
        password_hash.encode("utf-8")
    )


# ============================================================
# JWT — JSON Web Tokens
# ============================================================

def crear_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()

    if expires_delta:
        expira = datetime.now(timezone.utc) + expires_delta
    else:
        expira = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload.update({
        "exp": expira,
        "jti": str(uuid.uuid4())
    })

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token


def verificar_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None

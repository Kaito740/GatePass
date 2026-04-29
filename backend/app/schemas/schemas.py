from pydantic import BaseModel, field_validator
from datetime import datetime, date, time
from typing import Optional

# ROL
class RolResponse(BaseModel):
    id    : int
    nombre: str

    model_config = {"from_attributes": True}


# AREA
class AreaCreate(BaseModel):
    nombre: str

class AreaResponse(BaseModel):
    id    : int
    nombre: str

    model_config = {"from_attributes": True}


# USUARIO
class UsuarioCreate(BaseModel):
    dni        : str
    nombres    : str
    apellidos  : str
    rol_id     : int
    cargo      : Optional[str] = None
    area_id    : int
    telefono_wa: Optional[str] = None

class UsuarioUpdate(BaseModel):
    nombres    : Optional[str] = None
    apellidos  : Optional[str] = None
    cargo      : Optional[str] = None
    rol_id     : Optional[int] = None
    area_id    : Optional[int] = None
    telefono_wa: Optional[str] = None
    activo     : Optional[bool] = None

class UsuarioResponse(BaseModel):
    id         : int
    dni        : str
    nombres    : str
    apellidos  : str
    cargo      : Optional[str]
    telefono_wa: Optional[str]
    activo     : bool
    created_at : datetime
    rol        : RolResponse
    area       : AreaResponse

    model_config = {"from_attributes": True}


# USUARIO
class CuentaAdminCreate(BaseModel):
    usuario_id: int
    password  : str  # llega como texto plano, se hashea en el servicio

    @field_validator("password")
    @classmethod
    def password_minimo(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v

class CuentaAdminResponse(BaseModel):
    id        : int
    usuario_id: int

    model_config = {"from_attributes": True}


# AUTH — Login
class LoginInput(BaseModel):
    dni     : str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type  : str = "bearer"


# TIPO VEHICULO
class TipoVehiculoCreate(BaseModel):
    nombre: str

class TipoVehiculoResponse(BaseModel):
    id    : int
    nombre: str

    model_config = {"from_attributes": True}


# VEHICULO
class VehiculoCreate(BaseModel):
    placa              : str
    tipo_id            : int
    capacidad_pasajeros: int
    marca              : Optional[str] = None
    modelo             : Optional[str] = None
    anio               : Optional[int] = None
    color              : Optional[str] = None
    soat_vencimiento   : date

class VehiculoUpdate(BaseModel):
    marca              : Optional[str]  = None
    modelo             : Optional[str]  = None
    anio               : Optional[int]  = None
    color              : Optional[str]  = None
    soat_vencimiento   : Optional[date] = None
    estado_actual      : Optional[str]  = None
    activo             : Optional[bool] = None

class VehiculoResponse(BaseModel):
    id                 : int
    placa              : str
    capacidad_pasajeros: int
    marca              : Optional[str]
    modelo             : Optional[str]
    anio               : Optional[int]
    color              : Optional[str]
    soat_vencimiento   : date
    estado_actual      : str
    activo             : bool
    tipo               : TipoVehiculoResponse

    model_config = {"from_attributes": True}


# CONDUCTOR
class ConductorCreate(BaseModel):
    usuario_id          : int
    licencia_categoria  : Optional[str]  = None
    licencia_numero     : Optional[str]  = None
    licencia_vencimiento: Optional[date] = None

class ConductorUpdate(BaseModel):
    licencia_categoria  : Optional[str]  = None
    licencia_numero     : Optional[str]  = None
    licencia_vencimiento: Optional[date] = None

class ConductorResponse(BaseModel):
    id                  : int
    licencia_categoria  : Optional[str]
    licencia_numero     : Optional[str]
    licencia_vencimiento: Optional[date]
    usuario             : UsuarioResponse

    model_config = {"from_attributes": True}


# ASIGNACION TRANSPORTE
class AsignacionCreate(BaseModel):
    conductor_id: int
    vehiculo_id : int
    fecha       : date
    hora_salida : time

class AsignacionResponse(BaseModel):
    id          : int
    fecha       : date
    hora_salida : time
    is_active   : bool
    conductor   : ConductorResponse
    vehiculo    : VehiculoResponse

    model_config = {"from_attributes": True}


# TICKET SALIDA
class TicketCreate(BaseModel):
    asignacion_id: int
    destino      : str
    motivo       : str

class TicketAprobarJefe(BaseModel):
    aprobador_jefe_id: int

class TicketAprobarRRHH(BaseModel):
    aprobador_rrhh_id: int

class TicketResponse(BaseModel):
    id                : int
    destino           : str
    motivo            : str
    status            : str
    created_at        : datetime
    solicitante       : UsuarioResponse
    aprobador_jefe    : Optional[UsuarioResponse]
    aprobador_rrhh    : Optional[UsuarioResponse]
    asignacion        : AsignacionResponse

    model_config = {"from_attributes": True}


# BITACORA EVENTO
class BitacoraCreate(BaseModel):
    ticket_id     : int
    registrado_por: int
    tipo_accion   : str

class BitacoraResponse(BaseModel):
    id            : int
    tipo_accion   : str
    fecha_hora    : datetime
    ticket_id     : int
    registrador   : UsuarioResponse

    model_config = {"from_attributes": True}

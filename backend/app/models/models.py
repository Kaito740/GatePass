from sqlalchemy import (
    Boolean, Column, Date, ForeignKey,
    Integer, String, Text, Time, DateTime
)
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional

# --- BASE ---
class Base(DeclarativeBase):
    pass

# IDENTIDAD Y ACCESO
class Rol(Base):
    __tablename__ = "roles"

    id    : Mapped[int]         = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str]         = mapped_column(String(50), nullable=False)

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="rol")

class Area(Base):
    __tablename__ = "areas"

    id    : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="area")

class Usuario(Base):
    __tablename__ = "usuarios"

    id         : Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    dni        : Mapped[str]           = mapped_column(String(8), unique=True, nullable=False)
    nombres    : Mapped[str]           = mapped_column(String(100), nullable=False)
    apellidos  : Mapped[str]           = mapped_column(String(100), nullable=False)
    rol_id     : Mapped[int]           = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    cargo      : Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    area_id    : Mapped[int]           = mapped_column(Integer, ForeignKey("areas.id"), nullable=False)
    telefono_wa: Mapped[Optional[str]] = mapped_column(String(9), unique=True, nullable=True)
    activo     : Mapped[bool]          = mapped_column(Boolean, default=True)
    created_at : Mapped[datetime]      = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    rol      : Mapped["Rol"]                   = relationship(back_populates="usuarios")
    area     : Mapped["Area"]                  = relationship(back_populates="usuarios")
    cuenta   : Mapped[Optional["CuentaAdmin"]] = relationship(back_populates="usuario", uselist=False)
    conductor: Mapped[Optional["Conductor"]]   = relationship(back_populates="usuario", uselist=False)

    tickets_solicitados    : Mapped[list["TicketSalida"]] = relationship(foreign_keys="TicketSalida.solicitante_id",    back_populates="solicitante")
    tickets_aprobados_jefe : Mapped[list["TicketSalida"]] = relationship(foreign_keys="TicketSalida.aprobador_jefe_id", back_populates="aprobador_jefe")
    tickets_aprobados_rrhh : Mapped[list["TicketSalida"]] = relationship(foreign_keys="TicketSalida.aprobador_rrhh_id", back_populates="aprobador_rrhh")
    eventos_registrados    : Mapped[list["BitacoraEvento"]] = relationship(foreign_keys="BitacoraEvento.registrado_por", back_populates="registrador")

class CuentaAdmin(Base):
    __tablename__ = "cuentas_admin"

    id           : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id   : Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="cuenta")

# LOGÍSTICA
class TipoVehiculo(Base):
    __tablename__ = "tipos_vehiculo"

    id    : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)

    vehiculos: Mapped[list["Vehiculo"]] = relationship(back_populates="tipo")

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id                 : Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    placa              : Mapped[str]           = mapped_column(String(10), unique=True, nullable=False)
    tipo_id            : Mapped[int]           = mapped_column(Integer, ForeignKey("tipos_vehiculo.id"), nullable=False)
    capacidad_pasajeros: Mapped[int]           = mapped_column(Integer, nullable=False)
    marca              : Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    modelo             : Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    anio               : Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    color              : Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    soat_vencimiento   : Mapped[datetime]      = mapped_column(Date, nullable=False)
    estado_actual      : Mapped[str]           = mapped_column(String(20), nullable=False, default="disponible")
    activo             : Mapped[bool]          = mapped_column(Boolean, default=True)

    tipo        : Mapped["TipoVehiculo"]              = relationship(back_populates="vehiculos")
    asignaciones: Mapped[list["AsignacionTransporte"]] = relationship(back_populates="vehiculo")

class Conductor(Base):
    __tablename__ = "conductores"

    id                  : Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id          : Mapped[int]            = mapped_column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    licencia_categoria  : Mapped[Optional[str]]  = mapped_column(String(10), nullable=True)
    licencia_numero     : Mapped[Optional[str]]  = mapped_column(String(20), nullable=True)
    licencia_vencimiento: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)

    usuario     : Mapped["Usuario"]                   = relationship(back_populates="conductor")
    asignaciones: Mapped[list["AsignacionTransporte"]] = relationship(back_populates="conductor")

class AsignacionTransporte(Base):
    __tablename__ = "asignaciones_transporte"

    id          : Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    conductor_id: Mapped[int]      = mapped_column(Integer, ForeignKey("conductores.id"), nullable=False)
    vehiculo_id : Mapped[int]      = mapped_column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    fecha       : Mapped[datetime] = mapped_column(Date, nullable=False)
    hora_salida : Mapped[datetime] = mapped_column(Time, nullable=False)
    is_active   : Mapped[bool]     = mapped_column(Boolean, default=True)

    conductor: Mapped["Conductor"]           = relationship(back_populates="asignaciones")
    vehiculo : Mapped["Vehiculo"]            = relationship(back_populates="asignaciones")
    tickets  : Mapped[list["TicketSalida"]]  = relationship(back_populates="asignacion")

# OPERACIONES
class TicketSalida(Base):
    __tablename__ = "tickets_salida"

    id               : Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    solicitante_id   : Mapped[int]            = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    aprobador_jefe_id: Mapped[Optional[int]]  = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=True)
    aprobador_rrhh_id: Mapped[Optional[int]]  = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=True)
    asignacion_id    : Mapped[int]            = mapped_column(Integer, ForeignKey("asignaciones_transporte.id"), nullable=False)
    destino          : Mapped[str]            = mapped_column(String(200), nullable=False)
    motivo           : Mapped[str]            = mapped_column(Text, nullable=False)
    status           : Mapped[str]            = mapped_column(String(20), nullable=False, default="pendiente")
    created_at       : Mapped[datetime]       = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    solicitante   : Mapped["Usuario"]              = relationship(foreign_keys=[solicitante_id],    back_populates="tickets_solicitados")
    aprobador_jefe: Mapped[Optional["Usuario"]]    = relationship(foreign_keys=[aprobador_jefe_id], back_populates="tickets_aprobados_jefe")
    aprobador_rrhh: Mapped[Optional["Usuario"]]    = relationship(foreign_keys=[aprobador_rrhh_id], back_populates="tickets_aprobados_rrhh")
    asignacion    : Mapped["AsignacionTransporte"]  = relationship(back_populates="tickets")
    eventos       : Mapped[list["BitacoraEvento"]]  = relationship(back_populates="ticket")

class BitacoraEvento(Base):
    __tablename__ = "bitacora_eventos"

    id            : Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id     : Mapped[int]      = mapped_column(Integer, ForeignKey("tickets_salida.id"), nullable=False)
    registrado_por: Mapped[int]      = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_accion   : Mapped[str]      = mapped_column(String(30), nullable=False)
    fecha_hora    : Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    ticket     : Mapped["TicketSalida"] = relationship(back_populates="eventos")
    registrador: Mapped["Usuario"]      = relationship(foreign_keys=[registrado_por], back_populates="eventos_registrados")

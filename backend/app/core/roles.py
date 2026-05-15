from enum import Enum


class Rol(str, Enum):
    SUPERADMIN = "superadmin"
    RRHH = "rrhh"
    JEFE_AREA = "jefe_area"
    CONDUCTOR = "conductor"
    VIGILANTE = "vigilante"

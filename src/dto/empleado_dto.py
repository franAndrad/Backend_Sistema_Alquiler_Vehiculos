from dataclasses import dataclass
from ..models.enums import RolEmpleado


@dataclass
class EmpleadoCreateDTO:
    nombre: str
    apellido: str
    dni: str
    direccion: str | None
    telefono: str | None
    email: str
    rol: RolEmpleado


@dataclass
class EmpleadoResponseDTO:
    id: int
    nombre: str
    apellido: str
    rol: str

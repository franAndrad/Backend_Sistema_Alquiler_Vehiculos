from dataclasses import dataclass
from datetime import date


@dataclass
class ClienteCreateDTO:
    nombre: str
    apellido: str
    dni: str
    direccion: str | None
    telefono: str | None
    email: str
    licencia_numero: str
    licencia_categoria: str
    licencia_vencimiento: date


@dataclass
class ClienteResponseDTO:
    id: int
    nombre: str
    apellido: str
    dni: str
    email: str
    licencia_vencimiento: date

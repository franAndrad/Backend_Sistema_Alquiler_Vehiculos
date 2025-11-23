from dataclasses import dataclass
from datetime import date

@dataclass
class ClienteResponseDTO:
    id: int
    nombre: str
    apellido: str
    dni: str
    email: str
    telefono: int
    licencia_numero: str
    licencia_categoria: str
    licencia_vencimiento: date

from dataclasses import dataclass
from datetime import date

@dataclass
class MultaCreateDTO:
    id_alquiler: int
    descripcion: str
    monto: float
    fecha: date

@dataclass
class MultaResponseDTO:
    id: int
    id_alquiler: int
    descripcion: str
    monto: float
    fecha: date


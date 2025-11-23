from dataclasses import dataclass
from datetime import date

@dataclass
class MultaResponseDTO:
    id: int
    id_alquiler: int
    descripcion: str
    monto: float
    fecha: date


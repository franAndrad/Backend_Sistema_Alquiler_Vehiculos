from .modelo_dto import ModeloResponseDTO
from dataclasses import dataclass

@dataclass
class VehiculoResponseDTO:
    id: int
    patente: str
    modelo: ModeloResponseDTO
    anio: int
    tipo: str
    estado: str
    costo_diario: float

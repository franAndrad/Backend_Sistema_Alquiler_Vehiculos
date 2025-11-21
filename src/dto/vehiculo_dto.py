from dataclasses import dataclass
from .modelo_dto import ModeloResponseDTO
@dataclass
class VehiculoCreateDTO:
    id_modelo: int
    anio: int
    tipo: str
    patente: str
    costo_diario: float


@dataclass
class VehiculoResponseDTO:
    id: int
    patente: str
    modelo: ModeloResponseDTO
    anio: int
    tipo: str
    estado: str
    costo_diario: float

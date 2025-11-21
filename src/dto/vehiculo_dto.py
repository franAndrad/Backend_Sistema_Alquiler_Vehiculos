from dataclasses import dataclass
from ..models.enums import EstadoVehiculo

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
    modelo: str
    marca: str
    anio: int
    tipo: str
    estado: EstadoVehiculo
    costo_diario: float

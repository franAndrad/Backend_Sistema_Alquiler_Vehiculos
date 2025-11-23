from ..dto.vehiculo_dto import VehiculoResponseDTO
from ..dto.cliente_dto import ClienteResponseDTO
from dataclasses import dataclass
from datetime import date

@dataclass
class ReservaResponseDTO:
    id: int
    cliente: ClienteResponseDTO
    vehiculo: VehiculoResponseDTO
    fecha_inicio: date
    fecha_fin: date
    estado: str
    
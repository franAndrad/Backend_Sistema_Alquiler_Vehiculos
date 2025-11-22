from dataclasses import dataclass
from datetime import date
from ..dto.cliente_dto import ClienteResponseDTO
from ..dto.vehiculo_dto import VehiculoResponseDTO

@dataclass
class ReservaCreateDTO:
    id_cliente: int
    id_vehiculo: int
    fecha_inicio: date
    fecha_fin: date


@dataclass
class ReservaResponseDTO:
    id: int
    id_cliente: ClienteResponseDTO
    id_vehiculo: VehiculoResponseDTO
    fecha_inicio: date
    fecha_fin: date
    estado: str
    
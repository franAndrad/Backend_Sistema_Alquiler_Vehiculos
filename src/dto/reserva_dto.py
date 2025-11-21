from dataclasses import dataclass
from datetime import date


@dataclass
class ReservaCreateDTO:
    id_cliente: int
    id_vehiculo: int
    fecha_inicio: date
    fecha_fin: date


@dataclass
class ReservaResponseDTO:
    id: int
    id_cliente: int
    id_vehiculo: int
    fecha_inicio: date
    fecha_fin: date
    estado: str
    
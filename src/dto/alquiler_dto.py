from dataclasses import dataclass
from .cliente_dto import ClienteResponseDTO
from .vehiculo_dto import VehiculoResponseDTO
from .empleado_dto import EmpleadoResponseDTO
from datetime import date

@dataclass
class AlquilerCreateDTO:
    id_cliente: int
    id_vehiculo: int
    id_empleado: int
    fecha_inicio: date
    fecha_fin: date | None = None


@dataclass
class AlquilerResponseDTO:
    id: int
    cliente: ClienteResponseDTO
    vehiculo: VehiculoResponseDTO
    empleado: EmpleadoResponseDTO
    fecha_inicio: date
    fecha_fin: date | None
    costo_total: float | None
    estado: str

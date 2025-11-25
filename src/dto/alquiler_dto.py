from .vehiculo_dto import VehiculoResponseDTO
from .empleado_dto import EmpleadoResponseDTO
from .cliente_dto import ClienteResponseDTO
from dataclasses import dataclass
from datetime import date

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


@dataclass
class AlquilerFinalizadoResponseDTO:
    id: int
    cliente: dict
    vehiculo: dict
    empleado: dict
    fecha_inicio: date
    fecha_fin: date
    dias_utilizados: int
    costo_base: float
    multas: list
    costo_total_multas: float
    costo_total: float
    estado: str
    

@dataclass
class FacturacionMensualDTO:
    mes: str
    total: float

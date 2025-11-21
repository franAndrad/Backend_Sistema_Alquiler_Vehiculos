from dataclasses import dataclass
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
    cliente: str
    vehiculo: str
    empleado: str
    fecha_inicio: date
    fecha_fin: date | None
    costo_total: float | None
    estado: str

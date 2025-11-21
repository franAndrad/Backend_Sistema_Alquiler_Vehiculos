from dataclasses import dataclass
from datetime import date


@dataclass
class MarcaCreateDTO:
    nombre: str


@dataclass
class MarcaResponseDTO:
    id: int
    nombre: str

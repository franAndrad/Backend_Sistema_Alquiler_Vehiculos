from .marca_dto import MarcaResponseDTO
from dataclasses import dataclass

@dataclass
class ModeloResponseDTO:
    id: int
    nombre: str
    descripcion: str
    marca: MarcaResponseDTO
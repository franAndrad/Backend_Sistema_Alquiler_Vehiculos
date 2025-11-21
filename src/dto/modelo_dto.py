from dataclasses import dataclass
from .marca_dto import MarcaResponseDTO

@dataclass
class ModeloCreateDTO:
    id_marca: int
    nombre: str
    descripcion: str


@dataclass
class ModeloResponseDTO:
    id: int
    nombre: str
    descripcion: str
    marca: MarcaResponseDTO
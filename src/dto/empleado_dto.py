from dataclasses import dataclass

@dataclass
class EmpleadoResponseDTO:
    id: int
    nombre: str
    apellido: str
    dni: str
    direccion: str
    telefono: str
    email: str
    rol: str
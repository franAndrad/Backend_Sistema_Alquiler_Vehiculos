from ...exceptions.domain_exceptions import ValidationException
from .comunes_helpers import normalizar_strings

def normalizar_campos_basicos(body: dict) -> dict:
    return normalizar_strings(
        body,
        campos=["nombre"],
        to_lower=["nombre"]
    )

 
def validar_nombre(body: dict):
    if "nombre" in body and body["nombre"] is not None:
        if len(body["nombre"]) < 2 or len(body["nombre"]) > 30:
            raise ValidationException("El nombre de la marca debe tener entre 2 y 30 caracteres")
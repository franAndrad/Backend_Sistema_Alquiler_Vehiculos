from ...exceptions.domain_exceptions import ValidationException, NotFoundException
from ...repository.marca_repository import MarcaRepository
from .comunes_utils import normalizar_strings


def normalizar_campos_basicos(body: dict) -> dict:
    return normalizar_strings(
        body,
        campos=["nombre", "descripcion"],
        to_lower=["nombre", "descripcion"]
    )


def validar_nombre(nombre):
    if not nombre or len(nombre) < 2:
        raise ValidationException(
            "El nombre debe tener al menos 2 caracteres")


def validar_descripcion(descripcion):
    if not descripcion or len(descripcion) < 2:
        raise ValidationException(
            "La descripción debe tener al menos 2 caracteres")
        
        
def validar_marca_existente(id_marca):
    marca_repository = MarcaRepository()
    marca = marca_repository.get_by_id(id_marca)
    if not marca:
        raise NotFoundException("La marca asociada no existe")
        


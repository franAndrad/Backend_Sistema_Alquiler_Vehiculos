from ...exceptions.domain_exceptions import ValidationException, NotFoundException
from ...repository.marca_repository import MarcaRepository


def normalizar_campos_basicos(body: dict) -> dict:
    if "nombre" in body and body["nombre"] is not None:
        body["nombre"] = body["nombre"].strip()
    if "descripcion" in body and body["descripcion"] is not None:
        body["descripcion"] = body["descripcion"].strip()
    return body


def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    faltantes = [
        c for c in campos_obligatorios if c not in body or not body[c]]
    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios para {entidad}: {', '.join(faltantes)}"
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
        


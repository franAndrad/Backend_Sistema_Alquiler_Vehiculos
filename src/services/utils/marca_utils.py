from ...exceptions.domain_exceptions import ValidationException

def normalizar_campos_basicos(body: dict) -> dict:
    if "nombre" in body and body["nombre"] is not None:
        body["nombre"] = body["nombre"].strip()
    return body

def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    for campo in campos_obligatorios:
        if campo not in body or not body[campo]:
            raise ValidationException(f"El campo '{campo}' es obligatorio en la entidad '{entidad}'")
        
def validar_nombre(body: dict):
    if "nombre" in body and body["nombre"] is not None:
        if len(body["nombre"]) < 2 or len(body["nombre"]) > 30:
            raise ValidationException("El nombre de la marca debe tener entre 2 y 30 caracteres")
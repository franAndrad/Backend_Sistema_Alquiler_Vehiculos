from ...exceptions.domain_exceptions import ValidationException


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


def validar_long_nombre(body: dict):
    nombre = body.get("nombre")
    if not nombre or len(nombre) < 2:
        raise ValidationException(
            "El nombre debe tener al menos 2 caracteres")


def validar_long_descripcion(body: dict):
    desc = body.get("descripcion")
    if not desc or len(desc) < 2:
        raise ValidationException(
            "La descripción debe tener al menos 2 caracteres")


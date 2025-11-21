from ...exceptions.domain_exceptions import ValidationException


def normalizar_campos_basicos(body: dict) -> dict:
    """Quita espacios y normaliza email a minúsculas si están presentes."""
    if "nombre" in body and body["nombre"] is not None:
        body["nombre"] = body["nombre"].strip()
    if "apellido" in body and body["apellido"] is not None:
        body["apellido"] = body["apellido"].strip()
    if "email" in body and body["email"] is not None:
        body["email"] = body["email"].strip().lower()
    return body


def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    faltantes = [
        c for c in campos_obligatorios if c not in body or not body[c]]
    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios para {entidad}: {', '.join(faltantes)}"
        )


def validar_nombre_apellido(body: dict):
    if "nombre" in body and body["nombre"] is not None:
        if len(body["nombre"]) < 2:
            raise ValidationException(
                "El nombre debe tener al menos 2 caracteres")
    if "apellido" in body and body["apellido"] is not None:
        if len(body["apellido"]) < 2:
            raise ValidationException(
                "El apellido debe tener al menos 2 caracteres")


def validar_email_formato(body: dict):
    if "email" not in body or body["email"] is None:
        return
    email = body["email"]
    # ya viene en minúsculas por normalización
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValidationException("El email no tiene un formato válido")


def validar_dni_formato(body: dict, longitud_exacto: int = 8):
    if "dni" not in body or body["dni"] is None:
        return

    dni_str = str(body["dni"])
    if not dni_str.isdigit() or len(dni_str) != longitud_exacto:
        raise ValidationException(
            f"El DNI debe ser un número de {longitud_exacto} dígitos")


def validar_telefono(body: dict):
    telefono = body.get("telefono")
    if telefono:
        tel_str = str(telefono)
        if not tel_str.isdigit() or len(tel_str) < 7:
            raise ValidationException("El teléfono no es válido")

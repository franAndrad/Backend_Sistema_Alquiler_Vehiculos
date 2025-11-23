from ...exceptions.domain_exceptions import ValidationException
from ...models.enums import RolEmpleado
from .comunes_utils import (
    normalizar_strings, 
    validar_enum
    )


def normalizar_campos_basicos(body: dict) -> dict:
    return normalizar_strings(
        body,
        campos=["nombre", "apellido", "email"],
        to_lower=["email"]
    )


def validar_nombre_apellido(nombre, apellido):
    if nombre is not None:
        if len(nombre) < 2:
            raise ValidationException("El nombre debe tener al menos 2 caracteres")
    if apellido is not None:
        if len(apellido) < 2:
            raise ValidationException("El apellido debe tener al menos 2 caracteres")


def validar_email_formato(email):
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValidationException("El email no tiene un formato válido")


def validar_dni_formato(dni, longitud_exacto: int = 8):
    dni_str = str(dni)
    if not dni_str.isdigit() or len(dni_str) != longitud_exacto:
        raise ValidationException(
            f"El DNI debe ser un número de {longitud_exacto} dígitos")


def validar_telefono(telefono):
    if telefono:
        tel_str = str(telefono)
        if not tel_str.isdigit() or len(tel_str) < 7:
            raise ValidationException("El teléfono no es válido")


def validar_rol(rol):
    validar_enum(rol, RolEmpleado, "rol de empleado")

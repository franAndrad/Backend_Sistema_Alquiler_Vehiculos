from ...exceptions.domain_exceptions import ValidationException
from datetime import datetime


def normalizar_campos(body: dict) -> dict:
    """Limpia espacios y normaliza strings."""
    if "tipo" in body and body["tipo"]:
        body["tipo"] = body["tipo"].strip()
    if "patente" in body and body["patente"]:
        body["patente"] = body["patente"].strip().upper()
    return body


def validar_obligatorios(body: dict):
    faltan = [
        c for c in ["id_modelo", "anio", "tipo", "patente", "costo_diario"]
        if c not in body or body[c] is None
    ]

    if faltan:
        raise ValidationException(f"Faltan campos obligatorios: {', '.join(faltan)}")


def validar_anio(body: dict):
    anio = body.get("anio")
    if not isinstance(anio, int) or anio < 1980 or anio > datetime.now().year + 1:
        raise ValidationException("El año del vehículo no es válido")


def validar_patente(body: dict):
    patente = body.get("patente")
    if not patente or len(patente) < 6:
        raise ValidationException("La patente es inválida")

    if " " in patente:
        raise ValidationException("La patente no debe contener espacios")


def validar_costo(body: dict):
    costo = body.get("costo_diario")
    if not isinstance(costo, (int, float)) or costo <= 0:
        raise ValidationException("El costo diario debe ser un número mayor a cero")


def validar_vehiculo_create(body: dict):
    validar_obligatorios(body)
    validar_anio(body)
    validar_patente(body)
    validar_costo(body)

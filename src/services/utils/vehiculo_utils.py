from ...exceptions.domain_exceptions import ValidationException
from ...models.enums import TipoVehiculo
from datetime import datetime

from ...models.enums import EstadoVehiculo
from ...states.vehiculo_state import (
    VehiculoStateMachine,
    Disponible,
    Alquilado,
)

def normalizar_campos(body: dict) -> dict:
    """Limpia espacios y normaliza strings."""
    if "tipo" in body and body["tipo"]:
        body["tipo"] = body["tipo"].strip()
    if "patente" in body and body["patente"]:
        body["patente"] = body["patente"].strip().upper()
    return body


def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    faltantes = [
        c for c in campos_obligatorios if c not in body or not body[c]]
    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios para {entidad}: {', '.join(faltantes)}"
        )
        

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
    

def validar_tipo(body: dict):
    if "tipo" not in body or not body["tipo"]:
        raise ValidationException("El tipo de vehículo es obligatorio")

    try:
        TipoVehiculo(body["tipo"])
    except ValueError:
        raise ValidationException(
            f"El tipo '{body['tipo']}' no es válido. Tipos válidos: "
            + ", ".join([t.value for t in TipoVehiculo])
        )

def obtener_estado_vehiculo_enum(estado_enum):
    if estado_enum == EstadoVehiculo.DISPONIBLE:
        return VehiculoStateMachine(Disponible())
    if estado_enum == EstadoVehiculo.ALQUILADO:
        return VehiculoStateMachine(Alquilado())
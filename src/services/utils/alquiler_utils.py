from ...exceptions.domain_exceptions import ValidationException, BusinessException
from ...models.enums import EstadoAlquiler
from datetime import date

from ...states.alquiler_state import (
    AlquilerStateMachine,
    Activo,
    Finalizado,
    Cancelado
)

def normalizar_campos_basicos(body: dict) -> dict:
    """Quita espacios de los campos básicos si están presentes."""
    if "fecha_inicio" in body and body["fecha_inicio"] is not None:
        body["fecha_inicio"] = body["fecha_inicio"].strip()
    if "fecha_fin" in body and body["fecha_fin"] is not None:
        body["fecha_fin"] = body["fecha_fin"].strip()
    if "estado" in body and body["estado"] is not None:
        body["estado"] = body["estado"].strip()
    return body


def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    faltantes = [
        c for c in campos_obligatorios if c not in body or not body[c]]
    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios para {entidad}: {', '.join(faltantes)}"
        )


def validar_ids_foreign_keys(body: dict):
    fk_campos = ["id_cliente", "id_empleado", "id_vehiculo"]
    for campo in fk_campos:
        if campo not in body or not isinstance(body[campo], int) or body[campo] <= 0:
            raise ValidationException(f"El campo {campo} debe ser un ID válido (entero positivo)")
        
        
def validar_fechas(body: dict):
    if "fecha_inicio" not in body or "fecha_fin" not in body:
        raise ValidationException("fecha_inicio y fecha_fin son obligatorios")
    
    try:
        fecha_inicio = date.fromisoformat(body["fecha_inicio"])
        fecha_fin = date.fromisoformat(body["fecha_fin"])
    except ValueError:
        raise ValidationException("Formato de fecha inválido (usar YYYY-MM-DD)")
    
    return fecha_inicio, fecha_fin


def validar_costo(body: dict):
    if "costo_total" not in body:
        raise ValidationException("costo_total es obligatorio")
    
    try:
        costo = float(body["costo_total"])
        if costo < 0:
            raise ValidationException("costo_total no puede ser negativo")
    except (ValueError, TypeError):
        raise ValidationException("costo_total debe ser un número válido")


def validar_estado(body: dict):
    if "estado" not in body or not body["estado"]:
        raise ValidationException("El estado es obligatorio")

    try:
        EstadoAlquiler(body["estado"])
    except ValueError:
        raise ValidationException(
            f"El estado '{body['estado']}' no es válido. Estados válidos: "
            + ", ".join([r.value for r in EstadoAlquiler])
        )


def obtener_estado_enum(estado_enum):
    if estado_enum == EstadoAlquiler.ACTIVO:
        return AlquilerStateMachine(Activo())
    if estado_enum == EstadoAlquiler.FINALIZADO:
        return AlquilerStateMachine(Finalizado())
    if estado_enum == EstadoAlquiler.CANCELADO:
        return AlquilerStateMachine(Cancelado())
    raise BusinessException("Estado de alquiler no soportado")

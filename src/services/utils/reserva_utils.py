from datetime import date
from ...exceptions.domain_exceptions import ValidationException, BusinessException

def normalizar_campos_reserva(body: dict) -> dict:
    """Convierte fechas de string -> date y limpia campos básicos."""
    if "fecha_inicio" in body and isinstance(body["fecha_inicio"], str):
        body["fecha_inicio"] = date.fromisoformat(body["fecha_inicio"])

    if "fecha_fin" in body and isinstance(body["fecha_fin"], str):
        body["fecha_fin"] = date.fromisoformat(body["fecha_fin"])

    return body

def validar_campos_obligatorios_reserva(body: dict):
    faltantes = [
        c for c in ["id_cliente", "id_vehiculo", "fecha_inicio", "fecha_fin"]
        if c not in body or body[c] is None
    ]

    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios en la reserva: {', '.join(faltantes)}"
        )

def validar_fechas_reserva(fecha_inicio: date, fecha_fin: date):
    if not isinstance(fecha_inicio, date) or not isinstance(fecha_fin, date):
        raise ValidationException("Las fechas deben tener formato YYYY-MM-DD")

    if fecha_inicio < date.today():
        raise ValidationException("La fecha de inicio no puede ser en el pasado")

    if fecha_fin <= fecha_inicio:
        raise ValidationException("La fecha fin debe ser posterior a fecha inicio")

def validar_no_solapamiento(fecha_inicio, fecha_fin, reservas_existentes):
    for reserva in reservas_existentes:
        if not isinstance(reserva.fecha_inicio, date) or not isinstance(reserva.fecha_fin, date):
            continue

        if (
            fecha_inicio <= reserva.fecha_fin and
            fecha_fin >= reserva.fecha_inicio
        ):
            raise BusinessException(
                f"El vehículo ya está reservado entre {reserva.fecha_inicio} y {reserva.fecha_fin}"
            )

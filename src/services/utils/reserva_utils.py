from datetime import date
from ...exceptions.domain_exceptions import ValidationException, BusinessException
from ...repository.cliente_repository import ClienteRepository
from ...repository.reserva_repository import ReservaRepository
from ...models.enums import EstadoReserva
from ...states.reserva_state import (
    ReservaStateMachine,
    Pendiente,
    Confirmada,
    Cancelada,
    Finalizada,
)


def normalizar_campos_reserva(body: dict) -> dict:
    if "fecha_inicio" in body and isinstance(body["fecha_inicio"], str):
        body["fecha_inicio"] = date.fromisoformat(body["fecha_inicio"])

    if "fecha_fin" in body and isinstance(body["fecha_fin"], str):
        body["fecha_fin"] = date.fromisoformat(body["fecha_fin"])
    
    return body


def obtener_estado_enum(estado_enum):
    if estado_enum == EstadoReserva.PENDIENTE:
        return ReservaStateMachine(Pendiente())
    if estado_enum == EstadoReserva.CONFIRMADA:
        return ReservaStateMachine(Confirmada())
    if estado_enum == EstadoReserva.CANCELADA:
        return ReservaStateMachine(Cancelada())
    if estado_enum == EstadoReserva.FINALIZADA:
        return ReservaStateMachine(Finalizada())
    raise BusinessException("Estado de alquiler no soportado")


def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    faltantes = [
        c for c in campos_obligatorios if c not in body or not body[c]]
    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios para {entidad}: {', '.join(faltantes)}"
        )


def validar_fechas_reserva(fecha_inicio: date, fecha_fin: date):
    if not isinstance(fecha_inicio, date) or not isinstance(fecha_fin, date):
        raise ValidationException("Las fechas deben tener formato YYYY-MM-DD")

    if fecha_inicio < date.today():
        raise ValidationException("La fecha de inicio no puede ser en el pasado")

    if fecha_fin <= fecha_inicio:
        raise ValidationException("La fecha fin debe ser posterior a fecha inicio")


def validar_no_solapamiento(fecha_inicio, fecha_fin):
    reservas_repo = ReservaRepository()
    reservas_existentes = reservas_repo.get_by_estado(
        ["PENDIENTE", "CONFIRMADA"]
    )

    for reserva in reservas_existentes:
        if not (fecha_fin <= reserva.fecha_inicio or fecha_inicio >= reserva.fecha_fin):
            raise BusinessException(
                "La reserva se solapa con una reserva existente"
            )
            

def validar_cliente_existente(id_cliente):
    if id_cliente is None:
        raise ValidationException("El id_cliente es obligatorio para crear una reserva")
    
    cliente_repository = ClienteRepository()
    cliente = cliente_repository.get_by_id(id_cliente)
    if not cliente:
        raise ValidationException("El cliente indicado no existe")
    
    
def validar_reserva_pendiente(reserva):
    if reserva.estado != EstadoReserva.PENDIENTE:
        raise BusinessException("Solo se pueden eliminar reservas en estado PENDIENTE")
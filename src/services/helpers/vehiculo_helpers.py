from ...exceptions.domain_exceptions import ValidationException, BusinessException
from ...repository.vehiculo_repository import VehiculoRepository
from ...repository.reserva_repository import ReservaRepository
from ...repository.alquiler_repository import AlquilerRepository
from ...models.enums import TipoVehiculo
from datetime import date
from datetime import datetime
from .comunes_helpers import (
    normalizar_strings, 
    validar_enum,
    validar_campos_obligatorios
    )


def normalizar_campos(body: dict) -> dict:
    return normalizar_strings(
        body,
        campos=["patente", "tipo"]
    )
    
    
def validar_tipo(body: dict):
    validar_enum(body.get("tipo"), TipoVehiculo, "tipo de vehículo")
    
    
def validar_datos_vehiculo(body: dict):
    campos_obligatorios = [
        "id_modelo", "anio", "tipo", "patente", "costo_diario",
    ]
    validar_campos_obligatorios(body, campos_obligatorios, "vehiculo")
    validar_anio(body)
    validar_patente(body)
    validar_costo(body)
    validar_tipo(body)


def validar_anio(body: dict):
    anio = body.get("anio")
    if not isinstance(anio, int) or anio < 1980 or anio > datetime.now().year + 1:
        raise ValidationException("El año del vehículo no es válido")


def validar_vehiculo_disponible(
    id_vehiculo: int,
    fecha_inicio: str | date | None = None,
    fecha_fin: str | date | None = None,
):
    """
    Valida que el vehículo:
    - exista
    - esté en estado DISPONIBLE
    - no tenga reservas activas solapadas
    - no tenga alquileres activos solapados
    """

    vehiculo_repo = VehiculoRepository()
    reserva_repo = ReservaRepository()
    alquiler_repo = AlquilerRepository()

    vehiculo = vehiculo_repo.get_by_id(id_vehiculo)
    if not vehiculo:
        raise ValidationException("El vehículo no existe")

    # Si no me mandan fechas, hasta acá llega la validación
    if fecha_inicio is None or fecha_fin is None:
        return

    # Normalizo a date si vienen como string
    if isinstance(fecha_inicio, str):
        fecha_inicio = date.fromisoformat(fecha_inicio)
    if isinstance(fecha_fin, str):
        fecha_fin = date.fromisoformat(fecha_fin)

    # 2) Reservas activas que se solapen
    reservas_activas = reserva_repo.find_activas_por_vehiculo(
        id_vehiculo,
        fecha_inicio,
        fecha_fin,
    )
    if reservas_activas:
        raise BusinessException(
            "El vehículo tiene reservas activas en ese período")

    # 3) Alquileres activos que se solapen
    alquileres_activos = alquiler_repo.find_activos_por_vehiculo(
        id_vehiculo,
        fecha_inicio,
        fecha_fin,
    )
    if alquileres_activos:
        raise BusinessException(
            "El vehículo tiene alquileres activos en ese período")
        

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
    


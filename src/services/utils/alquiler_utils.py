from ...exceptions.domain_exceptions import ValidationException, BusinessException
from ...repository.cliente_repository import ClienteRepository
from ...repository.empleado_repository import EmpleadoRepository
from ...repository.vehiculo_repository import VehiculoRepository
from ...states.vehiculo_state import VehiculoStateMachine
from ...models.enums import EstadoVehiculo
from ...models.enums import EstadoAlquiler
from datetime import date


def normalizar_campos_basicos(body: dict) -> dict:
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


def validar_ids_foreign_keys(id_cliente, id_empleado, id_vehiculo):
    if not isinstance(id_cliente, int) or id_cliente <= 0:
        raise ValidationException("El campo id_cliente debe ser un ID válido (entero positivo)")
    if not isinstance(id_empleado, int) or id_empleado <= 0:
        raise ValidationException("El campo id_empleado debe ser un ID válido (entero positivo)")
    if not isinstance(id_vehiculo, int) or id_vehiculo <= 0:
        raise ValidationException("El campo id_vehiculo debe ser un ID válido (entero positivo)")
        
        
def validar_fechas(fecha_inicio, fecha_fin):
    if fecha_inicio is None or fecha_fin is None:
        raise ValidationException("fecha_inicio y fecha_fin son obligatorios")
    
    try:
        fecha_inicio = date.fromisoformat(fecha_inicio)
        fecha_fin = date.fromisoformat(fecha_fin)
    except ValueError:
        raise ValidationException("Formato de fecha inválido (usar YYYY-MM-DD)")
    
    return fecha_inicio, fecha_fin


def validar_cliente_existente(id_cliente):
    cliente_repository = ClienteRepository()
    cliente = cliente_repository.get_by_id(id_cliente)
    if not cliente:
        raise ValidationException("El cliente asociado no existe")
    

def validar_empleado_existente(id_empleado):
    empleado_repository = EmpleadoRepository()
    empleado = empleado_repository.get_by_id(id_empleado)
    if not empleado:
        raise ValidationException("El empleado asociado no existe")
    
    
def validar_vehiculo_disponible(id_vehiculo):
    vehiculo_repository = VehiculoRepository()
    vehiculo = vehiculo_repository.get_by_id(id_vehiculo)
    if not vehiculo:
        raise ValidationException("El vehículo asociado no existe")
    
    maquina_estado = VehiculoStateMachine(vehiculo.estado)
    
    if not maquina_estado.state_enum == EstadoVehiculo.DISPONIBLE:
        raise ValidationException("El vehículo asociado no está disponible para alquiler")



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

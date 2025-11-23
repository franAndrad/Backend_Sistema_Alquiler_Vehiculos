from ...exceptions.domain_exceptions import ValidationException, BusinessException
from ...repository.cliente_repository import ClienteRepository
from ...repository.empleado_repository import EmpleadoRepository
from ...repository.vehiculo_repository import VehiculoRepository
from ...states.vehiculo_state import VehiculoStateMachine
from ...models.enums import EstadoVehiculo, EstadoAlquiler
from .comunes_utils import (
    normalizar_strings, 
    validar_campos_obligatorios
    )


def normalizar_campos_basicos(body: dict) -> dict:
    return normalizar_strings(
        body,
        campos=["id_cliente", "id_empleado", "id_vehiculo"]
    )
    

def validar_datos_alquiler(body: dict):
    campos_obligatorios = ["id_cliente", "id_empleado", "id_vehiculo"]

    validar_campos_obligatorios(body, campos_obligatorios, "alquiler")
    validar_ids_foreign_keys(
        body["id_cliente"],
        body["id_empleado"],
        body["id_vehiculo"],
    )
    validar_cliente_existente(body["id_cliente"])
    validar_empleado_existente(body["id_empleado"])


def validar_ids_foreign_keys(id_cliente, id_empleado, id_vehiculo):
    if not isinstance(id_cliente, int) or id_cliente <= 0:
        raise ValidationException("El campo id_cliente debe ser un ID válido (entero positivo)")
    if not isinstance(id_empleado, int) or id_empleado <= 0:
        raise ValidationException("El campo id_empleado debe ser un ID válido (entero positivo)")
    if not isinstance(id_vehiculo, int) or id_vehiculo <= 0:
        raise ValidationException("El campo id_vehiculo debe ser un ID válido (entero positivo)")
        
        
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
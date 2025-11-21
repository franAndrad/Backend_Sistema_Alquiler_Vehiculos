from ..models.enums import TipoVehiculo, EstadoVehiculo, RolEmpleado
from ..models.cliente import Cliente
from ..models.vehiculo import Vehiculo
from ..models.alquiler import Alquiler
from ..models.reserva import Reserva
from ..models.empleado import Empleado
from ..models.marca import Marca
from ..models.modelo import Modelo
from ..models.multa import Multa

from ..dto.cliente_dto import ClienteResponseDTO
from ..dto.vehiculo_dto import VehiculoResponseDTO
from ..dto.alquiler_dto import AlquilerResponseDTO
from ..dto.reserva_dto import ReservaResponseDTO
from ..dto.empleado_dto import EmpleadoResponseDTO
from ..dto.marca_dto import MarcaResponseDTO
from ..dto.modelo_dto import ModeloResponseDTO
from ..dto.multa_dto import MultaResponseDTO


def cliente_to_response_dto(cliente: Cliente) -> ClienteResponseDTO:
    return ClienteResponseDTO(
        id=cliente.id,
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        dni=cliente.dni,
        email=cliente.email,
        licencia_vencimiento=cliente.licencia_vencimiento,
    )
    
def empleado_to_response_dto(empleado: Empleado) -> EmpleadoResponseDTO:
    return EmpleadoResponseDTO(
        id=empleado.id,
        nombre=empleado.nombre,
        apellido=empleado.apellido,
        direccion=empleado.direccion,
        telefono=empleado.telefono,
        rol=empleado.rol.value if isinstance(empleado.rol, RolEmpleado) else str(empleado.rol),
    )


def vehiculo_to_response_dto(vehiculo: Vehiculo) -> VehiculoResponseDTO:
    return VehiculoResponseDTO(
        id=vehiculo.id,
        patente=vehiculo.patente,
        modelo=modelo_to_response_dto(vehiculo.modelo),
        anio=vehiculo.anio,
        tipo=vehiculo.tipo.value if isinstance(vehiculo.tipo, TipoVehiculo) else str(vehiculo.tipo),
        estado=vehiculo.estado.value if isinstance(vehiculo.estado, EstadoVehiculo) else str(vehiculo.estado),
        costo_diario=vehiculo.costo_diario,
    )


def alquiler_to_response_dto(alquiler: Alquiler) -> AlquilerResponseDTO:
    return AlquilerResponseDTO(
        id=alquiler.id,
        cliente=cliente_to_response_dto(alquiler.cliente),
        vehiculo=vehiculo_to_response_dto(alquiler.vehiculo),
        empleado=empleado_to_response_dto(alquiler.empleado),
        fecha_inicio=alquiler.fecha_inicio,
        fecha_fin=alquiler.fecha_fin,
        costo_total=alquiler.costo_total,
        estado=alquiler.estado.value,
    )


def reserva_to_response_dto(reserva: Reserva) -> ReservaResponseDTO:
    return ReservaResponseDTO(
        id=reserva.id,
        cliente=f"{reserva.cliente.nombre} {reserva.cliente.apellido}",
        vehiculo=reserva.vehiculo.patente,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
        estado=reserva.estado.value,
    )
    
    
def marca_to_response_dto(marca: Marca) -> MarcaResponseDTO:
    return MarcaResponseDTO(
        id=marca.id,
        nombre=marca.nombre,
    )
    

def modelo_to_response_dto(modelo: Modelo) -> ModeloResponseDTO:
    return ModeloResponseDTO(
        id=modelo.id,
        nombre=modelo.nombre,
        descripcion=modelo.descripcion,
        marca=marca_to_response_dto(modelo.marca)
    )


def multa_to_response_dto(multa: Multa) -> dict:
    return MultaResponseDTO(
        id=multa.id,
        id_alquiler=multa.id_alquiler,
        descripcion=multa.descripcion,
        monto=multa.monto,
        fecha=multa.fecha
    )
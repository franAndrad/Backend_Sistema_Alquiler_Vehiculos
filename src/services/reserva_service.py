from ..repository.reserva_repository import ReservaRepository
from ..repository.vehiculo_repository import VehiculoRepository
from ..utils.mappers import reserva_to_response_dto
from ..exceptions.domain_exceptions import ValidationException, NotFoundException, BusinessException
from ..models.enums import  EstadoVehiculo
from ..models.reserva import Reserva
from ..states.reserva_state import ReservaStateMachine
from ..states.vehiculo_state import VehiculoStateMachine
from datetime import date
from ..services.utils.reserva_utils import (
    normalizar_campos_reserva,
    validar_campos_obligatorios,
    validar_cliente_existente,
    validar_fechas_reserva,
    validar_no_solapamiento,
    validar_reserva_pendiente,
    )
from ..services.utils.vehiculo_utils import (
    validar_vehiculo_disponible,
)
    

class ReservaService:
    
    def __init__(self):
        self.reserva_repo = ReservaRepository()
        self.vehiculo_repo = VehiculoRepository()
        
        
    def listar_reservas(self):
        reservas = self.reserva_repo.list_all()
        return [reserva_to_response_dto(r) for r in reservas]
    
    
    def obtener_reserva(self, reserva_id):
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValidationException("La reserva no existe")
        return reserva_to_response_dto(reserva)
    
    
    def obtener_reservas_por_estado(self, estados):
        reservas = self.reserva_repo.get_by_estado(estados)
        if not reservas:
            raise ValidationException("No hay reservas con los estados indicados")
        return [reserva_to_response_dto(r) for r in reservas]
    
    
    def obtener_reservas_por_cliente(self, cliente_id):
        reservas = self.reserva_repo.list_by_cliente(cliente_id)
        if not reservas:
            raise ValidationException("El cliente no tiene reservas")
        return [reserva_to_response_dto(r) for r in reservas]
    
    
    def crear_reserva(self, body):
        body = dict(body)
        body = normalizar_campos_reserva(body)

        campos_obligatiorios = ["id_cliente", "id_vehiculo", "fecha_inicio", "fecha_fin"]
        validar_campos_obligatorios(body, campos_obligatiorios, "reserva")
        validar_fechas_reserva(body["fecha_inicio"], body["fecha_fin"])
        validar_no_solapamiento(body["fecha_inicio"], body["fecha_fin"])
        validar_cliente_existente(body["id_cliente"])
        validar_vehiculo_disponible(body["id_vehiculo"], body["fecha_inicio"], body["fecha_fin"])

        vehiculo = VehiculoRepository.get_by_id(body["id_vehiculo"])
        if vehiculo.estado != EstadoVehiculo.DISPONIBLE:
            raise BusinessException("El vehículo no se encuentra disponible")
        
        maquina_reserva = ReservaStateMachine()
        
        nueva_reserva = Reserva(
            id_cliente=body["id_cliente"],
            id_vehiculo=body["id_vehiculo"],
            fecha_inicio=body["fecha_inicio"],
            fecha_fin=body["fecha_fin"],
            estado=maquina_reserva.state_enum
        )
        
        vehiculo = self.vehiculo_repo.get_by_id(body["id_vehiculo"])
        if not vehiculo:
            raise NotFoundException("Vehículo asociado no encontrado")

        maquina_estado_vehiculo = VehiculoStateMachine(vehiculo.estado)
        
        maquina_estado_vehiculo.reservar()
        vehiculo.estado = maquina_estado_vehiculo.state_enum
        
        self.reserva_repo.add(nueva_reserva)
        self.reserva_repo.save_changes()
        return reserva_to_response_dto(nueva_reserva)
    
        
    def actualizar_reserva(self, reserva_id, body):
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValidationException("La reserva no existe")
        
        body = dict(body)
        body = normalizar_campos_reserva(body)
        
        campos_obligatorios = ["id_cliente", "id_vehiculo", "fecha_inicio", "fecha_fin"]
        validar_campos_obligatorios(body, campos_obligatorios, "reserva")
        validar_fechas_reserva(body["fecha_inicio"], body["fecha_fin"])
        validar_no_solapamiento(body["fecha_inicio"], body["fecha_fin"])
        validar_cliente_existente(body["id_cliente"])
        validar_vehiculo_disponible(body["id_vehiculo"], body["fecha_inicio"], body["fecha_fin"])

        vehiculo_existente = self.vehiculo_repo.get_by_id(body["id_vehiculo"])
        if vehiculo_existente and vehiculo_existente.id != reserva.id_vehiculo:
            raise BusinessException("El vehículo no se encuentra disponible")
        
        reserva.id_cliente = body["id_cliente"]
        reserva.id_vehiculo = body["id_vehiculo"]
        reserva.fecha_inicio = body["fecha_inicio"]
        reserva.fecha_fin = body["fecha_fin"]
        
        self.reserva_repo.save_changes()
        return reserva_to_response_dto(reserva)
    
    
    def cancelar_reserva(self, reserva_id):
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValidationException("La reserva no existe")
        
        maquina_estado = ReservaStateMachine(reserva.estado)
        mensaje = maquina_estado.cancelar()
        reserva.estado = maquina_estado.state_enum
        
        vehiculo = self.vehiculo_repo.get_by_id(reserva.id_vehiculo)
        maquina_vehiculo = VehiculoStateMachine(vehiculo.estado)
        maquina_vehiculo.devolver()
        vehiculo.estado = maquina_vehiculo.state_enum
        
        self.reserva_repo.save_changes()
        self.vehiculo_repo.save_changes()
        return {"mensaje": mensaje}
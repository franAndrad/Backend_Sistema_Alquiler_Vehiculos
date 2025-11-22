from ..repository.reserva_repository import ReservaRepository
from ..utils.mappers import reserva_to_response_dto
from ..exceptions.domain_exceptions import ValidationException
from ..models.enums import EstadoReserva
from ..models.reserva import Reserva
from datetime import date
from ..services.utils.reserva_utils import (
    normalizar_campos_reserva,
    validar_campos_obligatorios,
    validar_cliente_existente,
    validar_vehiculo_disponible,
    validar_fechas_reserva,
    validar_no_solapamiento,
    validar_reserva_pendiente,
    obtener_estado_enum,
    )
    

class ReservaService:
    
    def __init__(self):
        self.reserva_repo = ReservaRepository()
        
        
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
        return [reserva_to_response_dto(r) for r in reservas]
    
    
    def crear_reserva(self, body):
        body = dict(body)
        body = normalizar_campos_reserva(body)
        
        campos_obligatiorios = ["id_cliente", "id_vehiculo", "fecha_inicio", "fecha_fin"]
        validar_campos_obligatorios(body, campos_obligatiorios, "reserva")
        validar_fechas_reserva(body["fecha_inicio"], body["fecha_fin"])
        validar_no_solapamiento(body["fecha_inicio"], body["fecha_fin"])
        validar_cliente_existente(body["id_cliente"])
        validar_vehiculo_disponible(body["id_vehiculo"])
        
        enum_estado = obtener_estado_enum(EstadoReserva.PENDIENTE)
        
        nueva_reserva = Reserva(
            id_cliente=body["id_cliente"],
            id_vehiculo=body["id_vehiculo"],
            fecha_inicio=body["fecha_inicio"],
            fecha_fin=body["fecha_fin"],
            estado=enum_estado.state_enum
        )
        
        self.reserva_repo.add(nueva_reserva)
        return reserva_to_response_dto(nueva_reserva)
    
        
    def actualizar_reserva(self, reserva_id, body):
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValidationException("La reserva no existe")
        
        body = dict(body)
        body = normalizar_campos_reserva(body)
        
        campos_obligatorios = ["id_cliente", "id_vehiculo", "fecha_inicio", "fecha_fin", "estado"]
        validar_campos_obligatorios(body, campos_obligatorios, "reserva")
        validar_fechas_reserva(body["fecha_inicio"], body["fecha_fin"])
        validar_no_solapamiento(body["fecha_inicio"], body["fecha_fin"])
        validar_cliente_existente(body["id_cliente"])
        validar_vehiculo_disponible(body["id_vehiculo"])
        
        reserva.id_cliente = body["id_cliente"]
        reserva.id_vehiculo = body["id_vehiculo"]
        reserva.fecha_inicio = date.fromisoformat(body["fecha_inicio"])
        reserva.fecha_fin = date.fromisoformat(body["fecha_fin"])
        
        self.reserva_repo.save_changes()
        return reserva_to_response_dto(reserva)
    
        
    def eliminar_reserva(self, reserva_id):
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValidationException("La reserva no existe")
        
        enum_estado = obtener_estado_enum(reserva.estado)
        validar_reserva_pendiente(enum_estado.state_enum)
        
        self.reserva_repo.delete(reserva)
        return {"mensaje": "Reserva eliminada correctamente"}
    

    def confirmar_reserva(self, reserva_id):
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValidationException("La reserva no existe")
        
        enum_estado = obtener_estado_enum(reserva.estado)
        enum_estado.confirmar()
        
        reserva.estado = enum_estado.state_enum
        self.reserva_repo.save_changes()
        return reserva_to_response_dto(reserva)
    
    
    def cancelar_reserva(self, reserva_id):
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValidationException("La reserva no existe")
        
        enum_estado = obtener_estado_enum(reserva.estado)
        enum_estado.cancelar()
        
        reserva.estado = enum_estado.state_enum
        self.reserva_repo.save_changes()
        return reserva_to_response_dto(reserva)
    
    
    def finalizar_reserva(self, reserva_id):
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValidationException("La reserva no existe")
        
        enum_estado = obtener_estado_enum(reserva.estado)
        enum_estado.finalizar()
        
        reserva.estado = enum_estado.state_enum
        self.reserva_repo.save_changes()
        return reserva_to_response_dto(reserva)
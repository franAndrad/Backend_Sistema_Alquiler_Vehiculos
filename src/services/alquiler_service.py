from datetime import date
from ..repository.alquiler_repository import AlquilerRepository
from ..repository.vehiculo_repository import VehiculoRepository
from ..repository.reserva_repository import ReservaRepository
from ..exceptions.domain_exceptions import NotFoundException, BusinessException
from ..states.alquiler_state import AlquilerStateMachine
from ..states.vehiculo_state import VehiculoStateMachine
from ..states.reserva_state import ReservaStateMachine
from ..models.alquiler import Alquiler
from ..utils.mappers import alquiler_to_response_dto
from .utils.alquiler_utils import (
    normalizar_campos_basicos,
    validar_campos_obligatorios,
    validar_ids_foreign_keys,
    validar_fechas,
    validar_cliente_existente,
    validar_empleado_existente,
)

from .utils.vehiculo_utils import (
    validar_vehiculo_disponible,
)


class AlquilerService:

    def __init__(self, alquiler_repository=None):
        self.alquiler_repo = alquiler_repository or AlquilerRepository()
        self.vehiculo_repo = VehiculoRepository()
        self.reserva_repo = ReservaRepository()


    def listar_alquileres(self):
        alquileres = self.alquiler_repo.list_all()
        return [alquiler_to_response_dto(a) for a in alquileres]
    
    
    def obtener_alquiler(self, alquiler_id):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")
        return alquiler_to_response_dto(alquiler)
    
    
    def listar_alquileres_por_cliente(self, cliente_id):
        alquileres = self.alquiler_repo.find_by_cliente_id(cliente_id)
        return [alquiler_to_response_dto(a) for a in alquileres]
    
    
    def listar_alquileres_por_vehiculo(self, vehiculo_id):
        alquileres = self.alquiler_repo.find_by_vehiculo_id(vehiculo_id)
        return [alquiler_to_response_dto(a) for a in alquileres]


    def crear_alquiler(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        maquina_estado = AlquilerStateMachine()
        
        campos_obligatorios = [
            "id_cliente", "id_empleado", "id_vehiculo"
        ]

        validar_campos_obligatorios(body, campos_obligatorios, "alquiler")
        validar_ids_foreign_keys(body["id_cliente"], body["id_empleado"], body["id_vehiculo"])
        validar_cliente_existente(body["id_cliente"])
        validar_empleado_existente(body["id_empleado"])

        
        
        # si viene id_reserva, la buscamos y validamos
        id_reserva = body.get("id_reserva")
        reserva = None
        if id_reserva is not None:
            reserva = self.reserva_repo.get_by_id(id_reserva)
            if not reserva:
                raise NotFoundException("La reserva asociada no existe")

            # verificamos que coincidan cliente y vehículo
            if reserva.id_cliente != body["id_cliente"] or reserva.id_vehiculo != body["id_vehiculo"]:
                raise BusinessException("La reserva no corresponde a ese cliente/vehículo")

            # reserva pasa a finalizada
            maquina_reserva = ReservaStateMachine(reserva.estado)
            maquina_reserva.finalizada()
            reserva.estado = maquina_reserva.state_enum
        
        vehiculo = self.vehiculo_repo.get_by_id(body["id_vehiculo"])
        if not vehiculo:
            raise NotFoundException("Vehículo asociado no encontrado")

        # pasar vehiculo a alquilado
        maquina_estado_vehiculo = VehiculoStateMachine(vehiculo.estado)
        mensaje = maquina_estado_vehiculo.alquilar()
        vehiculo.estado = maquina_estado_vehiculo.state_enum
        
            
        nuevo_alquiler = Alquiler(
            id_cliente=body["id_cliente"],
            id_empleado=body["id_empleado"],
            id_vehiculo=body["id_vehiculo"],
            id_reserva=id_reserva if reserva else None,
            fecha_inicio=date.today(),
            fecha_fin=None,
            estado=maquina_estado.state_enum,
            costo_total=0.0
        )

        self.alquiler_repo.add(nuevo_alquiler)
        self.alquiler_repo.save_changes()
        self.vehiculo_repo.save_changes()
        self.reserva_repo.save_changes()
        return alquiler_to_response_dto(nuevo_alquiler)


    def actualizar_alquiler(self, alquiler_id, body):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")

        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = [
            "id_cliente", "id_empleado", "id_vehiculo",
            "fecha_inicio", "fecha_fin"
        ]

        validar_campos_obligatorios(body, campos_obligatorios, "alquiler")
        validar_ids_foreign_keys(body["id_cliente"], body["id_empleado"], body["id_vehiculo"])
        validar_fechas(body["fecha_inicio"], body["fecha_fin"])
        validar_cliente_existente(body["id_cliente"])
        validar_empleado_existente(body["id_empleado"])
        validar_vehiculo_disponible(body["id_vehiculo"])
        
        # Si se cambia el vehículo, hay que actualizar su estado!!!!!!!

        alquiler.id_cliente = body["id_cliente"]
        alquiler.id_empleado = body["id_empleado"]
        alquiler.id_vehiculo = body["id_vehiculo"]
        alquiler.fecha_inicio = date.fromisoformat(body["fecha_inicio"])
        alquiler.fecha_fin = date.fromisoformat(body["fecha_fin"])

        self.alquiler_repo.save_changes()
        return alquiler_to_response_dto(alquiler)
    
    
    def finalizar_alquiler(self, alquiler_id):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")


        vehiculo = self.vehiculo_repo.get_by_id(alquiler.id_vehiculo)
        if not vehiculo:
            raise NotFoundException("Vehículo asociado no encontrado")
        
        alquiler.fecha_fin = date.today()
        
        maquina_estado = AlquilerStateMachine(alquiler.estado)
        mensaje = maquina_estado.finalizar()
        alquiler.estado = maquina_estado.state_enum
        
        maquina_vehiculo = VehiculoStateMachine(vehiculo.estado)
        maquina_vehiculo.devolver()
        vehiculo.estado = maquina_vehiculo.state_enum

        self.alquiler_repo.save_changes()
        return {"mensaje": mensaje}
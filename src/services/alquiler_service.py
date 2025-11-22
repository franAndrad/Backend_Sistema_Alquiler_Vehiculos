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
    validar_cliente_existente,
    validar_empleado_existente,
)
from .utils.vehiculo_utils import validar_vehiculo_disponible


class AlquilerService:

    def __init__(self):
        self.alquiler_repo = AlquilerRepository()
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
        if not alquileres:
            raise NotFoundException("El cliente no tiene alquileres")
        return [alquiler_to_response_dto(a) for a in alquileres]


    def listar_alquileres_por_vehiculo(self, vehiculo_id):
        alquileres = self.alquiler_repo.find_by_vehiculo_id(vehiculo_id)
        if not alquileres:
            raise NotFoundException("El vehículo no tiene alquileres")
        return [alquiler_to_response_dto(a) for a in alquileres]
    
    
    def listar_alquileres_por_estado(self, estados):
        alquileres = self.alquiler_repo.list_by_estado(estados)
        if not alquileres:
            raise NotFoundException("No hay alquileres con el estado indicado")
        return [alquiler_to_response_dto(a) for a in alquileres]


    def crear_alquiler(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        maquina_estado = AlquilerStateMachine()

        campos_obligatorios = ["id_cliente", "id_empleado", "id_vehiculo"]
        validar_campos_obligatorios(body, campos_obligatorios, "alquiler")

        validar_ids_foreign_keys(
            body["id_cliente"], body["id_empleado"], body["id_vehiculo"])
        validar_cliente_existente(body["id_cliente"])
        validar_empleado_existente(body["id_empleado"])

        fecha_actual = date.today()

        # validar disponibilidad
        id_reserva = body.get("id_reserva")

        if id_reserva is None:
            # SIN reserva → debe estar disponible HOY
            validar_vehiculo_disponible(
                body["id_vehiculo"], fecha_actual, fecha_actual)

        # si tiene reserva
        reserva = None
        id_reserva_final = None

        if id_reserva is not None:
            reserva = self.reserva_repo.get_by_id(id_reserva)
            if not reserva:
                raise NotFoundException("La reserva asociada no existe")

            # cliente y vehículo deben coincidir
            if reserva.id_cliente != body["id_cliente"] or reserva.id_vehiculo != body["id_vehiculo"]:
                raise BusinessException(
                    "La reserva no corresponde a ese cliente/vehículo")

            fi_res = reserva.fecha_inicio
            ff_res = reserva.fecha_fin

            if fi_res <= fecha_actual <= ff_res:
                # La reserva está vigente → finalizarla
                maquina_reserva = ReservaStateMachine(reserva.estado)
                maquina_reserva.finalizar()
                reserva.estado = maquina_reserva.state_enum
                id_reserva_final = id_reserva

            elif fecha_actual < fi_res:
                # El alquiler se crea ANTES de la fecha reservada
                # Se ignora la reserva, se deja intacta
                id_reserva_final = None

            else:
                # El alquiler comienza DESPUÉS de la fecha de la reserva
                # → venció
                maquina_reserva = ReservaStateMachine(reserva.estado)
                maquina_reserva.expirar()
                reserva.estado = maquina_reserva.state_enum
                raise BusinessException(
                    "La reserva asociada ya venció para la fecha de inicio del alquiler")

        # ocupar vehículo
        vehiculo = self.vehiculo_repo.get_by_id(body["id_vehiculo"])
        if not vehiculo:
            raise NotFoundException("Vehículo asociado no encontrado")

        maquina_vehiculo = VehiculoStateMachine(vehiculo.estado)
        maquina_vehiculo.alquilar()
        vehiculo.estado = maquina_vehiculo.state_enum

        nuevo_alquiler = Alquiler(
            id_cliente=body["id_cliente"],
            id_empleado=body["id_empleado"],
            id_vehiculo=body["id_vehiculo"],
            id_reserva=id_reserva_final,
            fecha_inicio=fecha_actual,
            fecha_fin=None,
            estado=maquina_estado.state_enum,
            costo_total=0.0,
        )

        self.alquiler_repo.add(nuevo_alquiler)
        self.alquiler_repo.save_changes()

        return alquiler_to_response_dto(nuevo_alquiler)


    def actualizar_alquiler(self, alquiler_id, body):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")

        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = ["id_cliente", "id_empleado", "id_vehiculo"]
        validar_campos_obligatorios(body, campos_obligatorios, "alquiler")

        validar_ids_foreign_keys(
            body["id_cliente"], body["id_empleado"], body["id_vehiculo"])
        validar_cliente_existente(body["id_cliente"])
        validar_empleado_existente(body["id_empleado"])

        fecha_actual = date.today()

        id_vehiculo_nuevo = body["id_vehiculo"]
        id_vehiculo_actual = alquiler.id_vehiculo

        # Si cambia el vehículo
        if id_vehiculo_nuevo != id_vehiculo_actual:
            validar_vehiculo_disponible(
                id_vehiculo_nuevo, fecha_actual, fecha_actual)

            # liberar vehículo viejo
            vehiculo_viejo = self.vehiculo_repo.get_by_id(id_vehiculo_actual)
            maquina_viejo = VehiculoStateMachine(vehiculo_viejo.estado)
            maquina_viejo.devolver()
            vehiculo_viejo.estado = maquina_viejo.state_enum

            # ocupar vehículo nuevo
            vehiculo_nuevo = self.vehiculo_repo.get_by_id(id_vehiculo_nuevo)
            maquina_nuevo = VehiculoStateMachine(vehiculo_nuevo.estado)
            maquina_nuevo.alquilar()
            vehiculo_nuevo.estado = maquina_nuevo.state_enum

            alquiler.id_vehiculo = id_vehiculo_nuevo

        # actualizar datos del alquiler
        alquiler.id_cliente = body["id_cliente"]
        alquiler.id_empleado = body["id_empleado"]
        alquiler.fecha_inicio = fecha_actual

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

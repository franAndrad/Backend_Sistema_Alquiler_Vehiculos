from datetime import date

from ..repository.reserva_repository import ReservaRepository
from ..repository.cliente_repository import ClienteRepository
from ..repository.vehiculo_repository import VehiculoRepository

from ..dto.reserva_dto import ReservaCreateDTO, ReservaResponseDTO
from ..models.reserva import Reserva

from ..exceptions.domain_exceptions import (
    ValidationException,
    NotFoundException,
    BusinessException,
)

from .utils.reserva_utils import (
    normalizar_campos_reserva,
    validar_campos_obligatorios_reserva,
    validar_fechas_reserva,
    validar_no_solapamiento
)

class ReservaService:
    def __init__(self):
        self.reserva_repo = ReservaRepository()
        self.cliente_repo = ClienteRepository()
        self.vehiculo_repo = VehiculoRepository()

    def crear_reserva(self, body: dict) -> ReservaResponseDTO:

        body = normalizar_campos_reserva(body)

        validar_campos_obligatorios_reserva(body)

        try:
            dto = ReservaCreateDTO(
                id_cliente=int(body["id_cliente"]),
                id_vehiculo=int(body["id_vehiculo"]),
                fecha_inicio=body["fecha_inicio"],
                fecha_fin=body["fecha_fin"]
            )
        except Exception:
            raise ValidationException("Los datos enviados no tienen formatos válidos.")

        cliente = self.cliente_repo.find_by_id(dto.id_cliente)
        if not cliente:
            raise NotFoundException(f"Cliente con id {dto.id_cliente} no existe")

        vehiculo = self.vehiculo_repo.find_by_id(dto.id_vehiculo)
        if not vehiculo:
            raise NotFoundException(f"Vehículo con id {dto.id_vehiculo} no existe")

        validar_fechas_reserva(dto.fecha_inicio, dto.fecha_fin)

        reservas_existentes = self.reserva_repo.find_reservas_por_vehiculo(dto.id_vehiculo)
        validar_no_solapamiento(dto.fecha_inicio, dto.fecha_fin, reservas_existentes)

        nueva_reserva = Reserva(
            id_cliente=dto.id_cliente,
            id_vehiculo=dto.id_vehiculo,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            estado="pendiente"
        )

        self.reserva_repo.save(nueva_reserva)

        return ReservaResponseDTO(
            id=nueva_reserva.id,
            id_cliente=nueva_reserva.id_cliente,
            id_vehiculo=nueva_reserva.id_vehiculo,
            fecha_inicio=nueva_reserva.fecha_inicio,
            fecha_fin=nueva_reserva.fecha_fin,
            estado=nueva_reserva.estado
        )

    def listar_reservas(self):
        reservas = self.reserva_repo.find_all()
        return [
            ReservaResponseDTO(
                id=r.id,
                id_cliente=r.id_cliente,
                id_vehiculo=r.id_vehiculo,
                fecha_inicio=r.fecha_inicio,
                fecha_fin=r.fecha_fin,
                estado=r.estado
            )
            for r in reservas
        ]

    def obtener_reserva(self, reserva_id):
        r = self.reserva_repo.find_by_id(reserva_id)
        if not r:
            raise NotFoundException(f"Reserva con id {reserva_id} no existe")

        return ReservaResponseDTO(
            id=r.id,
            id_cliente=r.id_cliente,
            id_vehiculo=r.id_vehiculo,
            fecha_inicio=r.fecha_inicio,
            fecha_fin=r.fecha_fin,
            estado=r.estado
        )

    def eliminar_reserva(self, reserva_id):
        eliminada = self.reserva_repo.delete(reserva_id)
        if not eliminada:
            raise NotFoundException(f"No existe reserva con id {reserva_id}")

        return {"mensaje": "Reserva eliminada correctamente"}
    
    def obtener_reservas_por_cliente(self, cliente_id):
        reservas = self.reserva_repo.find_by_cliente(cliente_id)

        return [
            ReservaResponseDTO(
                id=r.id,
                id_cliente=r.id_cliente,
                id_vehiculo=r.id_vehiculo,
                fecha_inicio=r.fecha_inicio,
                fecha_fin=r.fecha_fin,
                estado=r.estado
            )
            for r in reservas
        ]

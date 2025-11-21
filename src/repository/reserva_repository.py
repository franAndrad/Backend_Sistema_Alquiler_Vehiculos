from sqlalchemy import or_
from .base_repository import BaseRepository
from ..models.reserva import Reserva
from ..models.enums import EstadoReserva


class ReservaRepository(BaseRepository):

    def __init__(self):
        super().__init__(Reserva)

    def list_by_cliente(self, id_cliente):
        return Reserva.query.filter_by(id_cliente=id_cliente)\
            .order_by(Reserva.fecha_inicio.desc())\
            .all()

    def list_pendientes_o_confirmadas(self):
        return Reserva.query.filter(
            Reserva.estado.in_(
                [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA])
        ).all()

    def reservas_superpuestas(self, vehiculo_id, desde, hasta):
        return Reserva.query.filter(
            Reserva.id_vehiculo == vehiculo_id,
            Reserva.estado.in_(
                [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]),
            Reserva.fecha_inicio <= hasta,
            Reserva.fecha_fin >= desde
        ).all()
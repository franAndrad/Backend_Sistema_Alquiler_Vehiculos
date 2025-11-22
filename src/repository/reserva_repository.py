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

    def get_by_estado(self, estados):
        return Reserva.query.filter(Reserva.estado.in_(estados)).all()
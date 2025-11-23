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
    
    
    # un vehículo está reservado solo cuando hay una reserva CONFIRMADA que se solapa con ese período
    def find_activas_por_vehiculo(
        self,
        id_vehiculo: int,
        fecha_inicio=None,
        fecha_fin=None,
    ) -> list[Reserva]:
        query = Reserva.query.filter(
            Reserva.id_vehiculo == id_vehiculo,
            Reserva.estado.in_(
                [EstadoReserva.CONFIRMADA]),
        )

        # Si paso fechas, filtro por solapamiento
        if fecha_inicio is not None and fecha_fin is not None:
            query = query.filter(
                # solapamiento de intervalos: [A,B] con [C,D]
                Reserva.fecha_fin >= fecha_inicio,
                Reserva.fecha_inicio <= fecha_fin,
            )

        return query.all()
    

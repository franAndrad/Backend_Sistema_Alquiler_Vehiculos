from datetime import date
from sqlalchemy import func, or_
from .base_repository import BaseRepository
from ..extensions.db import db
from ..models.alquiler import Alquiler
from ..models.enums import EstadoAlquiler


class AlquilerRepository(BaseRepository):

    def __init__(self):
        super().__init__(Alquiler)

    def list_by_cliente(self, id_cliente, desde=None, hasta=None):
        q = Alquiler.query.filter_by(id_cliente=id_cliente)

        if desde is not None:
            q = q.filter(Alquiler.fecha_inicio >= desde)
        if hasta is not None:
            q = q.filter(Alquiler.fecha_inicio <= hasta)

        return q.order_by(Alquiler.fecha_inicio.desc()).all()

    def list_by_vehiculo(self, id_vehiculo):
        return (
            Alquiler.query
            .filter_by(id_vehiculo=id_vehiculo)
            .order_by(Alquiler.fecha_inicio.desc())
            .all()
        )

    def list_by_rango_fechas(self, desde, hasta):
        return (
            Alquiler.query
            .filter(
                Alquiler.fecha_inicio >= desde,
                Alquiler.fecha_inicio <= hasta
            )
            .order_by(Alquiler.fecha_inicio.asc())
            .all()
        )

    def facturacion_mensual(self, anio):
        result = (
            db.session.query(
                func.extract("month", Alquiler.fecha_fin).label("mes"),
                func.coalesce(func.sum(Alquiler.costo_total), 0).label("total")
            )
            .filter(
                func.extract("year", Alquiler.fecha_fin) == anio,
                Alquiler.costo_total != None
            )
            .group_by("mes")
            .order_by("mes")
            .all()
        )
        return result


    def find_activos_por_vehiculo(
        self,
        id_vehiculo: int,
        fecha_inicio: date | None = None,
        fecha_fin: date | None = None,
    ) -> list[Alquiler]:
        """
        Devuelve los alquileres ACTIVOS de un vehículo.
        Si se pasan fecha_inicio y fecha_fin, filtra por solapamiento
        de intervalos con [fecha_inicio, fecha_fin].
        """

        q = Alquiler.query.filter(
            Alquiler.id_vehiculo == id_vehiculo,
            Alquiler.estado == EstadoAlquiler.ACTIVO,
        )

        if fecha_inicio is not None and fecha_fin is not None:
            q = q.filter(
                # Alquiler cuya fecha_fin es nula (sigue activo hoy)
                # o termina después del inicio del intervalo
                or_(Alquiler.fecha_fin == None,
                    Alquiler.fecha_fin >= fecha_inicio),
                # y empezó antes o el mismo día del fin del intervalo
                Alquiler.fecha_inicio <= fecha_fin,
            )

        return q.all()

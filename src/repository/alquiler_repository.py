from datetime import date
from sqlalchemy import func
from .base_repository import BaseRepository
from ..extensions.db import db
from ..models.alquiler import Alquiler


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
        return Alquiler.query.filter_by(id_vehiculo=id_vehiculo)\
            .order_by(Alquiler.fecha_inicio.desc())\
            .all()

    def list_by_rango_fechas(self, desde, hasta):
        return Alquiler.query.filter(
            Alquiler.fecha_inicio >= desde,
            Alquiler.fecha_inicio <= hasta
        ).order_by(Alquiler.fecha_inicio.asc()).all()

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
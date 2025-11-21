from datetime import date
from sqlalchemy import or_
from .base_repository import BaseRepository
from ..extensions.db import db
from ..models.vehiculo import Vehiculo
from ..models.alquiler import Alquiler
from ..models.reserva import Reserva
from ..models.enums import EstadoVehiculo, EstadoAlquiler, EstadoReserva


class VehiculoRepository(BaseRepository):

    def __init__(self):
        super().__init__(Vehiculo)

    def find_by_patente(self, patente):
        return Vehiculo.query.filter_by(patente=patente).first()

    def existe_patente_en_otro_vehiculo(self, patente, vehiculo_id):
        return (
            Vehiculo.query
            .filter(Vehiculo.patente == patente, Vehiculo.id != vehiculo_id)
            .first()
        )

    def list_disponibles(self):
        return Vehiculo.query.filter_by(estado=EstadoVehiculo.DISPONIBLE).all()

    def list_by_estado(self, estado):
        return Vehiculo.query.filter_by(estado=estado).all()

    def tiene_alquiler_superpuesto(self, vehiculo_id, desde, hasta):
        q = Alquiler.query.filter(
            Alquiler.id_vehiculo == vehiculo_id,
            Alquiler.estado == EstadoAlquiler.ACTIVO,
            Alquiler.fecha_inicio <= hasta,
            or_(Alquiler.fecha_fin == None, Alquiler.fecha_fin >= desde)
        )
        return db.session.query(q.exists()).scalar()

    def tiene_reserva_superpuesta(self, vehiculo_id, desde, hasta):
        q = Reserva.query.filter(
            Reserva.id_vehiculo == vehiculo_id,
            Reserva.estado.in_([EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]),
            Reserva.fecha_inicio <= hasta,
            Reserva.fecha_fin >= desde
        )
        return db.session.query(q.exists()).scalar()

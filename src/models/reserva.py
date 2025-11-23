from ..extensions.db import db
from .enums import EstadoReserva

class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Enum(EstadoReserva), default=EstadoReserva.CONFIRMADA, nullable=False)

    cliente = db.relationship("Cliente", back_populates="reservas")
    vehiculo = db.relationship("Vehiculo", back_populates="reservas")

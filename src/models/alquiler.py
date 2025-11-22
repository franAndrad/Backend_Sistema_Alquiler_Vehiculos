from ..extensions.db import db
from .enums import EstadoAlquiler


class Alquiler(db.Model):
    __tablename__ = "alquileres"

    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey("empleados.id"), nullable=False)
    id_reserva = db.Column(db.Integer, db.ForeignKey("reservas.id"), nullable=True) 

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    costo_total = db.Column(db.Float)
    estado = db.Column(db.Enum(EstadoAlquiler), default=EstadoAlquiler.ACTIVO, nullable=False)

    cliente = db.relationship("Cliente", back_populates="alquileres")
    vehiculo = db.relationship("Vehiculo", back_populates="alquileres")
    empleado = db.relationship("Empleado", back_populates="alquileres")
    multas = db.relationship("Multa", back_populates="alquiler")
from ..extensions.db import db
from ..models.enums import EstadoVehiculo


class Vehiculo(db.Model):
    __tablename__ = "vehiculos"

    id = db.Column(db.Integer, primary_key=True)
    id_modelo = db.Column(db.Integer, db.ForeignKey("modelos.id"), nullable=False)
    anio = db.Column(db.Integer)
    tipo = db.Column(db.String(50))
    patente = db.Column(db.String(20), unique=True, nullable=False)
    estado = db.Column(db.Enum(EstadoVehiculo), default=EstadoVehiculo.DISPONIBLE, nullable=False)
    costo_diario = db.Column(db.Float, nullable=False)

    modelo = db.relationship("Modelo", back_populates="vehiculos")
    alquileres = db.relationship("Alquiler", back_populates="vehiculo")
    reservas = db.relationship("Reserva", back_populates="vehiculo")

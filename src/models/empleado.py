from ..extensions.db import db
from .enums import RolEmpleado


class Empleado(db.Model):
    __tablename__ = "empleados"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol = db.Column(db.Enum(RolEmpleado), nullable=False)

    alquileres = db.relationship("Alquiler", back_populates="empleado")
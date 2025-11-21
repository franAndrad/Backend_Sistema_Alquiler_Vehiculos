from ..extensions.db import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    licencia_numero = db.Column(db.String(50), nullable=False)
    licencia_categoria = db.Column(db.String(20), nullable=False)
    licencia_vencimiento = db.Column(db.Date, nullable=False)

    alquileres = db.relationship("Alquiler", back_populates="cliente")
    reservas = db.relationship("Reserva", back_populates="cliente")

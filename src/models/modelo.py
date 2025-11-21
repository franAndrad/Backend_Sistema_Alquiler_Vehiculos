from ..extensions.db import db


class Modelo(db.Model):
    __tablename__ = "modelos"

    id = db.Column(db.Integer, primary_key=True)
    id_marca = db.Column(db.Integer, db.ForeignKey("marcas.id"), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)

    marca = db.relationship("Marca", back_populates="modelos")
    vehiculos = db.relationship("Vehiculo", back_populates="modelo")

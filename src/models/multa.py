from ..extensions.db import db


class Multa(db.Model):
    __tablename__ = "multas"

    id = db.Column(db.Integer, primary_key=True)
    id_alquiler = db.Column(db.Integer, db.ForeignKey("alquileres.id"), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    alquiler = db.relationship("Alquiler", back_populates="multas")

from ..extensions.db import db

class Marca(db.Model):
    __tablename__ = "marcas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)

    modelos = db.relationship("Modelo", back_populates="marca")

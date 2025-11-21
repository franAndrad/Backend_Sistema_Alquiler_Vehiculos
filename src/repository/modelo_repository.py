from .base_repository import BaseRepository
from ..models.modelo import Modelo


class ModeloRepository(BaseRepository):

    def __init__(self):
        super().__init__(Modelo)

    def list_by_marca(self, id_marca):
        return Modelo.query.filter_by(id_marca=id_marca).all()
    
    def find_by_nombre(self, nombre):
        return Modelo.query.filter_by(
            nombre=nombre
        ).first()

    def find_by_descripcion_and_marca(self, descripcion, id_marca):
        return Modelo.query.filter_by(
            descripcion=descripcion,
            id_marca=id_marca
        ).first()
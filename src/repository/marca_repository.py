from .base_repository import BaseRepository
from ..models.marca import Marca

class MarcaRepository(BaseRepository):

    def __init__(self):
        super().__init__(Marca)


    def find_by_nombre(self, nombre):
        return Marca.query.filter_by(nombre=nombre).first()
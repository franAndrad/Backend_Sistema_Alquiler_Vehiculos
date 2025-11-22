from .base_repository import BaseRepository
from ..models.multa import Multa


class MultaRepository(BaseRepository):

    def __init__(self):
        super().__init__(Multa)


    def list_by_alquiler(self, id_alquiler):
        return Multa.query.filter_by(id_alquiler=id_alquiler).all()
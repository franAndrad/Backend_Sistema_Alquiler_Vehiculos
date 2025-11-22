from .base_repository import BaseRepository
from ..models.cliente import Cliente


class ClienteRepository(BaseRepository):

    def __init__(self):
        super().__init__(Cliente)


    def find_by_dni(self, dni):
        return Cliente.query.filter_by(dni=dni).first()


    def find_by_email(self, email):
        return Cliente.query.filter_by(email=email).first()


    def search_by_nombre(self, termino):
        like = f"%{termino}%"
        return Cliente.query.filter(
            (Cliente.nombre.ilike(like)) | (Cliente.apellido.ilike(like))
        ).all()
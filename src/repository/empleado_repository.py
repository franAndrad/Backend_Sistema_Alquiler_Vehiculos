from .base_repository import BaseRepository
from ..models.empleado import Empleado


class EmpleadoRepository(BaseRepository):

    def __init__(self):
        super().__init__(Empleado)


    def find_by_dni(self, dni):
        return Empleado.query.filter_by(dni=dni).first()


    def find_by_email(self, email):
        return Empleado.query.filter_by(email=email).first()


    def list_by_rol(self, rol):
        return Empleado.query.filter_by(rol=rol).all()
from .base_repository import BaseRepository
from ..models.enums import EstadoVehiculo
from ..models.vehiculo import Vehiculo

class VehiculoRepository(BaseRepository):

    def __init__(self):
        super().__init__(Vehiculo)


    def find_by_patente(self, patente):
        return Vehiculo.query.filter_by(patente=patente).first()


    def list_disponibles(self):
        return Vehiculo.query.filter_by(estado=EstadoVehiculo.DISPONIBLE).all()


    def list_by_estado(self, estados):
        return Vehiculo.query.filter(Vehiculo.estado.in_(estados)).all()
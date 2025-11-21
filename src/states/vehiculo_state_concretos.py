from .vehiculo_state import VehiculoState
from ..models.enums import EstadoVehiculo


class VehiculoDisponibleState(VehiculoState):

    def alquilar(self, ctx):
        ctx.vehiculo.estado = EstadoVehiculo.ALQUILADO

class VehiculoAlquiladoState(VehiculoState):

    def devolver(self, ctx):
        ctx.vehiculo.estado = EstadoVehiculo.DISPONIBLE


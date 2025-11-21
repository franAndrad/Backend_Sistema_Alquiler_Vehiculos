from ..models.enums import EstadoVehiculo
from .vehiculo_state_concretos import (
    VehiculoDisponibleState,
    VehiculoAlquiladoState,
)

class VehiculoContext:

    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.state = self._state_from_enum(vehiculo.estado)

    def _state_from_enum(self, estado):
        if estado == EstadoVehiculo.DISPONIBLE:
            return VehiculoDisponibleState()
        if estado == EstadoVehiculo.ALQUILADO:
            return VehiculoAlquiladoState()
        return VehiculoDisponibleState()

    def alquilar(self):
        self.state.alquilar(self)

    def devolver(self):
        self.state.devolver(self)


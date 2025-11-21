from ..models.enums import EstadoVehiculo
from ..exceptions.domain_exceptions import BusinessException


class VehiculoState:

    def alquilar(self, ctx):
        raise BusinessException(
            "Operación no permitida para el estado actual del vehículo")

    def devolver(self, ctx):
        raise BusinessException(
            "Operación no permitida para el estado actual del vehículo")

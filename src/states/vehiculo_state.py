from __future__ import annotations
from abc import ABC, abstractmethod
from ..exceptions.domain_exceptions import BusinessException
from ..models.enums import EstadoVehiculo  


class VehiculoStateMachine:
    """
    Máquina de estados para un vehículo.
    Maneja las transiciones entre DISPONIBLE y ALQUILADO.
    """

    _state: EstadoVehiculoState = None

    def __init__(self, state: EstadoVehiculoState) -> None:
        self.transition_to(state)

    def transition_to(self, state: EstadoVehiculoState):
        self._state = state
        self._state.context = self

    def alquilar(self) -> str:
        return self._state.alquilar()

    def devolver(self) -> str:
        return self._state.devolver()

    @property
    def estado_enum(self) -> EstadoVehiculo:
        """
        Devuelve el valor del enum asociado al estado actual
        (DISPONIBLE, ALQUILADO, MANTENIMIENTO si lo agregás después).
        """
        return self._state.state_value


class EstadoVehiculoState(ABC):
    """
    Estado abstracto del vehículo.
    Cada subclase representa un estado concreto.
    """

    state_value: EstadoVehiculo = None

    @property
    def context(self) -> VehiculoStateMachine:
        return self._context

    @context.setter
    def context(self, context: VehiculoStateMachine) -> None:
        self._context = context

    @abstractmethod
    def alquilar(self) -> str:
        pass

    @abstractmethod
    def devolver(self) -> str:
        pass


class Disponible(EstadoVehiculoState):
    state_value = EstadoVehiculo.DISPONIBLE

    def alquilar(self) -> str:
        self.context.transition_to(Alquilado())
        return "El vehiculo fue alquilado"

    def devolver(self) -> str:
        raise BusinessException("El vehiculo ya está disponible")


class Alquilado(EstadoVehiculoState):
    state_value = EstadoVehiculo.ALQUILADO

    def alquilar(self) -> str:
        raise BusinessException("El vehiculo ya está alquilado")

    def devolver(self) -> str:
        self.context.transition_to(Disponible())
        return "El vehiculo fue devuelto"

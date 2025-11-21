from __future__ import annotations
from abc import ABC, abstractmethod
from ..exceptions.domain_exceptions import BusinessException


class Vehiculo:
    _state: EstadoVehiculo = None

    def __init__(self, state: EstadoVehiculo) -> None:
        self.transition_to(state)

    def transition_to(self, state: EstadoVehiculo):
        self._state = state
        self._state.context = self

    def alquilar(self):
        return self._state.alquilar()

    def devolver(self):
        return self._state.devolver()


class EstadoVehiculo(ABC):

    @property
    def context(self) -> Vehiculo:
        return self._context

    @context.setter
    def context(self, context: Vehiculo) -> None:
        self._context = context

    @abstractmethod
    def alquilar(self) -> str:
        pass

    @abstractmethod
    def devolver(self) -> str:
        pass


class Disponible(EstadoVehiculo):
    def alquilar(self) -> str:
        self.context.transition_to(Alquilado())
        return "El vehiculo fue alquilado"

    def devolver(self) -> str:
        raise BusinessException("El vehiculo ya está disponible")


class Alquilado(EstadoVehiculo):
    def alquilar(self) -> str:
        raise BusinessException("El vehiculo ya está alquilado")

    def devolver(self) -> str:
        self.context.transition_to(Disponible())
        return "El vehiculo fue devuelto"
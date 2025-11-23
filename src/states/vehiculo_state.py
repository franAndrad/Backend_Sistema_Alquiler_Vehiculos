from __future__ import annotations
from abc import ABC, abstractmethod
from ..exceptions.domain_exceptions import BusinessException
from ..models.enums import EstadoVehiculo  


class VehiculoStateMachine:
    def __init__(self, state: EstadoVehiculo = None) -> None:
        # Estado por instancia
        self._state: EstadoVehiculoState | None = None

        if state is None:
            self.transition_to(Disponible())
        else:
            self._init_from_enum(state)

    # inicializa el estado a partir de un enum
    def _init_from_enum(self, state: EstadoVehiculo):
        if state == EstadoVehiculo.DISPONIBLE:
            self.transition_to(Disponible())
        elif state == EstadoVehiculo.RESERVADO:
            self.transition_to(Reservado())  # Asumiendo que RESERVADO se maneja como DISPONIBLE
        elif state == EstadoVehiculo.ALQUILADO:
            self.transition_to(Alquilado())
        else:
            raise ValueError(f"Estado no soportado: {state}")

    def transition_to(self, state: EstadoVehiculoState):
        self._state = state
        self._state.context = self
        
    def reservar(self) -> str:
        return self._state.reservar()

    def alquilar(self) -> str:
        return self._state.alquilar()

    def devolver(self) -> str:
        return self._state.devolver()

    @property
    def state_enum(self) -> EstadoVehiculo:
        """Devuelve el estado actual como enum."""
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
    def reservar(self) -> str:
        pass
    
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
    
    def reservar(self) -> str:
        self.context.transition_to(Reservado())
        return "El vehiculo fue reservado"
    

class Reservado(EstadoVehiculoState):
    state_value = EstadoVehiculo.RESERVADO

    def alquilar(self) -> str:
        self.context.transition_to(Alquilado())
        return "El vehiculo fue alquilado desde reservado"

    def devolver(self) -> str:
        self.context.transition_to(Disponible())
        return "El vehiculo reservado fue cancelado y ahora está disponible"
    
    def reservar(self) -> str:
        raise BusinessException("El vehiculo ya está reservado")


class Alquilado(EstadoVehiculoState):
    state_value = EstadoVehiculo.ALQUILADO

    def alquilar(self) -> str:
        raise BusinessException("El vehiculo ya está alquilado")

    def devolver(self) -> str:
        self.context.transition_to(Disponible())
        return "El vehiculo fue devuelto"
    
    def reservar(self) -> str:
        raise BusinessException("El vehiculo está alquilado, no puede ser reservado")

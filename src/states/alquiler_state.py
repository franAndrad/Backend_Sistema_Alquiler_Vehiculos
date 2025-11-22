from __future__ import annotations
from abc import ABC, abstractmethod
from ..exceptions.domain_exceptions import BusinessException
from ..models.enums import EstadoAlquiler


class AlquilerStateMachine:
    def __init__(self, state: EstadoAlquiler = None) -> None:
        # Estado por instancia
        self._state: EstadoBase | None = None

        if state is None:
            self.transition_to(Activo())
        else:
            self._init_from_enum(state)
    
    def _init_from_enum(self, state: EstadoAlquiler):
        if state == EstadoAlquiler.ACTIVO:
            self.transition_to(Activo())
        elif state == EstadoAlquiler.FINALIZADO:
            self.transition_to(Finalizado())
        else:
            raise ValueError(f"Estado no soportado: {state}")
    
    def transition_to(self, state: EstadoBase):
        self._state = state
        self._state.context = self
        
    def finalizar(self) -> str:
        return self._state.finalizar()

    @property
    def state_enum(self) -> EstadoAlquiler:
        return self._state.state_value



class EstadoBase(ABC):
    state_value: EstadoAlquiler = None

    @property
    def context(self) -> AlquilerStateMachine:
        return self._context

    @context.setter
    def context(self, context: AlquilerStateMachine) -> None:
        self._context = context

    @abstractmethod
    def finalizar(self) -> str:
        pass


class Activo(EstadoBase):
    state_value = EstadoAlquiler.ACTIVO

    def finalizar(self) -> str:
        self.context.transition_to(Finalizado())
        return "El alquiler fue finalizado"


class Finalizado(EstadoBase):
    state_value = EstadoAlquiler.FINALIZADO

    def finalizar(self) -> str:
        raise BusinessException("El alquiler ya está finalizado")


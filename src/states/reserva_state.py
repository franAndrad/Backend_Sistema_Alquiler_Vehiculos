from __future__ import annotations
from abc import ABC, abstractmethod
from ..models.enums import EstadoReserva
from ..exceptions.domain_exceptions import BusinessException


class ReservaStateMachine:
    def __init__(self, state: EstadoReserva = None) -> None:
        # Estado por instancia
        self._state: EstadoReservaState | None = None

        if state is None:
            self.transition_to(Confirmada())
        else:
            self._init_from_enum(state)
        
    def _init_from_enum(self, estado: EstadoReserva):
        if estado == EstadoReserva.CONFIRMADA:
            self.transition_to(Confirmada())
        elif estado == EstadoReserva.CANCELADA:
            self.transition_to(Cancelada())
        elif estado == EstadoReserva.FINALIZADA:
            self.transition_to(Finalizada())
        else:
            raise ValueError(f"Estado de reserva no soportado: {estado}")
    
    def transition_to(self, state: EstadoReservaState):
        self.__state = state
        self.__state.context = self
        
    def confirmar(self) -> str:
        return self.__state.confirmar()
    
    def cancelar(self) -> str:
        return self.__state.cancelar()
    
    def finalizada(self) -> str:
        return self.__state.finalizada()
    
    @property
    def state_enum(self) -> EstadoReserva:
        return self.__state.state_value
    

class EstadoReservaState(ABC):
    state_value: EstadoReserva = None
    
    @property
    def context(self) -> ReservaStateMachine:
        return self._context
    
    @context.setter
    def context(self, context: ReservaStateMachine) -> None:
        self._context = context
        
    @abstractmethod
    def confirmar(self) -> str:
        pass
    
    @abstractmethod
    def cancelar(self) -> str:
        pass
    
    @abstractmethod
    def finalizada(self) -> str:
        pass
     
class Confirmada(EstadoReservaState):
    state_value = EstadoReserva.CONFIRMADA
    
    def confirmar(self) -> str:
        raise BusinessException("La reserva ya está confirmada.")
    
    def cancelar(self) -> str:
        self.context.transition_to(Cancelada())
        return "Reserva cancelada exitosamente."
    
    def finalizada(self):
        self.context.transition_to(Finalizada())
        return "Reserva finalizada exitosamente."
    
    
class Cancelada(EstadoReservaState):
    state_value = EstadoReserva.CANCELADA
    
    def confirmar(self) -> str:
        raise BusinessException("No se puede confirmar una reserva cancelada.")
    
    def cancelar(self) -> str:
        raise BusinessException("La reserva ya está cancelada.")
    
    def finalizada(self):
        raise BusinessException("No se puede finalizar una reserva cancelada.")
    
    
class Finalizada(EstadoReservaState):
    state_value = EstadoReserva.FINALIZADA
    
    def confirmar(self) -> str:
        raise BusinessException("No se puede confirmar una reserva finalizada.")
    
    def cancelar(self) -> str:
        raise BusinessException("No se puede cancelar una reserva finalizada.")
    
    def finalizada(self) -> str:
        raise BusinessException("La reserva ya está finalizada.")
    
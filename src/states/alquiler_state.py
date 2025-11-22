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
        elif state == EstadoAlquiler.CANCELADO:
            self.transition_to(Cancelado())
        else:
            raise ValueError(f"Estado no soportado: {state}")
    
    def transition_to(self, state: EstadoBase):
        self._state = state
        self._state.context = self
        

    def finalizar(self) -> str:
        return self._state.finalizar()
    

    def cancelar(self) -> str:
        return self._state.cancelar()
    

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


    @abstractmethod
    def cancelar(self) -> str:
        pass



class Activo(EstadoBase):
    state_value = EstadoAlquiler.ACTIVO


    def finalizar(self) -> str:
        self.context.transition_to(Finalizado())
        return "El alquiler fue finalizado"
    

    def cancelar(self) -> str:
        self.context.transition_to(Cancelado())
        return "El alquiler fue cancelado"



class Finalizado(EstadoBase):
    state_value = EstadoAlquiler.FINALIZADO
    

    def finalizar(self) -> str:
        raise BusinessException("El alquiler ya está finalizado")
    

    def cancelar(self) -> str:
        raise BusinessException("No se puede cancelar un alquiler finalizado")


class Cancelado(EstadoBase):
    state_value = EstadoAlquiler.CANCELADO


    def finalizar(self) -> str:
        raise BusinessException("No se puede finalizar un alquiler cancelado")


    def cancelar(self) -> str:
        raise BusinessException("El alquiler ya está cancelado")

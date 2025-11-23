from typing import List
from .observer import Observer


class Sujeto:
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def suscribir(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def quitar(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notificar(self, reserva) -> None:
        for observer in self._observers:
            observer.actualizar(reserva)

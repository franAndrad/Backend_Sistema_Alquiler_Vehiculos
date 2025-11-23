from typing import List
from .observer import Observer


class Sujeto:
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, reserva) -> None:
        for observer in self._observers:
            observer.update(reserva)

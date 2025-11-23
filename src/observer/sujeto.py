from .observer import Observer

# Patron Observer
class Sujeto:
    
    # Singleton implementation para que haya una sola instancia de Sujeto
    _instance = None  
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sujeto, cls).__new__(cls)
            cls._instance._observers = []  
        return cls._instance

    def suscribir(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def quitar(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notificar(self, entidad) -> None:
        for observer in self._observers:
            observer.actualizar(entidad)

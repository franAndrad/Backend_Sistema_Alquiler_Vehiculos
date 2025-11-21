import pytest
from src.states.vehiculo_state import Vehiculo, Disponible, Alquilado
from src.exceptions.domain_exceptions import BusinessException


def test_alquilar_vehiculo_disponible():
    vehiculo = Vehiculo(Disponible())
    assert vehiculo.alquilar() == "El vehiculo fue alquilado"


def test_no_alquilar_vehiculo_alquilado():
    vehiculo = Vehiculo(Disponible())
    vehiculo.alquilar() 
    with pytest.raises(BusinessException):
        vehiculo.alquilar()


def test_devolver_vehiculo_alquilado():
    vehiculo = Vehiculo(Disponible())
    vehiculo.alquilar()
    assert vehiculo.devolver() == "El vehiculo fue devuelto"


def test_no_devolver_vehiculo_disponible():
    vehiculo = Vehiculo(Disponible())
    with pytest.raises(BusinessException):
        vehiculo.devolver()

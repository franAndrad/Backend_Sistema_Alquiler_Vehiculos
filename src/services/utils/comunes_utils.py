from datetime import date
from ...exceptions.domain_exceptions import ValidationException

def validar_fecha(fecha):
    try:
        fecha = date.fromisoformat(fecha)
    except ValueError:
        raise ValidationException("Formato de fecha inválido (usar YYYY-MM-DD)")
    
    return fecha


def validar_tamaño(cadena, maximo):
    if len(cadena) > maximo:
        raise ValidationException(f"El tamaño máximo permitido es {maximo} caracteres")
    

def validar_mayor_0(valor, campo):
    if valor is None or not isinstance(valor, (int, float)) or valor <= 0:
        raise ValidationException(f"El campo {campo} debe ser un número mayor a 0")
    
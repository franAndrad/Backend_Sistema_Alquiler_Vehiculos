class DomainException(Exception):
    status_code = 400


class BusinessException(DomainException):
    """Errores de reglas de negocio (vehículo no disponible, etc.)"""
    pass


class NotFoundException(DomainException):
    """Entidad no encontrada"""
    status_code = 404


class ValidationException(DomainException):
    """Errores de validación de entrada (más allá de Flask/Marshmallow)"""
    status_code = 422

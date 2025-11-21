class DomainException(Exception):
    status_code = 400


class BusinessException(DomainException):
    """Error de reglas de negocio"""
    pass


class NotFoundException(DomainException):
    """Entidad no encontrada"""
    status_code = 404


class ValidationException(DomainException):
    """Error de validación de entrada"""
    status_code = 422

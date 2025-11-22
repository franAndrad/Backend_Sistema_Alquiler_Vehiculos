# src/utils/auth_utils.py
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt
from ..exceptions.domain_exceptions import DomainException


class AuthorizationException(DomainException):
    status_code = 403


def roles_required(*roles_permitidos):
    """
    Uso:
    @roles_required("ADMIN")
    @roles_required("ADMIN", "ATENCION")
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            rol_token = claims.get("rol")
            if rol_token not in roles_permitidos:
                raise AuthorizationException(
                    "No tiene permisos para realizar esta operación")
            return fn(*args, **kwargs)
        return wrapper
    return decorator

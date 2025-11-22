from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from ..repository.empleado_repository import EmpleadoRepository
from ..exceptions.domain_exceptions import NotFoundException, BusinessException

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
empleado_repo = EmpleadoRepository()


@auth_bp.post("/login")
def login():
    body = request.get_json() or {}

    email = body.get("email")
    password = body.get("password")

    if not email:
        raise BusinessException("El email es obligatorio para iniciar sesión")

    if not password:
        raise BusinessException(
            "La contraseña es obligatoria para iniciar sesión")

    empleado = empleado_repo.find_by_email(email)
    if not empleado:
        raise NotFoundException("Empleado no encontrado")

    if not empleado.check_password(password):
        raise BusinessException("Contraseña incorrecta")

    claims = {
        "email": empleado.email,
        "rol": empleado.rol.value
    }

    token = create_access_token(
        identity=str(empleado.id),
        additional_claims=claims
    )

    return jsonify({"access_token": token}), 200



@auth_bp.get("/me")
@jwt_required()
def obtener_usuario_actual():
    claims = get_jwt()

    return jsonify({
        "id": int(get_jwt_identity()),
        "email": claims.get("email"),
        "rol": claims.get("rol"),
    }), 200

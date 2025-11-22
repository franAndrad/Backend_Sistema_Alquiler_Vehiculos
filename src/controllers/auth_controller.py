from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..repository.empleado_repository import EmpleadoRepository
from ..exceptions.domain_exceptions import NotFoundException, BusinessException
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
empleado_repo = EmpleadoRepository()


@auth_bp.post("/login")
def login():
    body = request.get_json() or {}
    email = body.get("email")
    password = body.get("password")

    if not email:
        raise BusinessException("El email es obligatorio para login")

    if not password:
        raise BusinessException("La contraseña es obligatoria para login")

    empleado = empleado_repo.find_by_email(email)
    if not empleado:
        raise NotFoundException("Empleado no encontrado")

    if not empleado.check_password(password):
        raise BusinessException("Contraseña incorrecta")

    additional_claims = {
        "email": empleado.email,
        "rol": empleado.rol.value
    }

    access_token = create_access_token(
        identity=str(empleado.id),
        additional_claims=additional_claims
    )

    return jsonify({"access_token": access_token}), 200


@auth_bp.get("/me")
@jwt_required()
def get_me():
    claims = get_jwt()
    empleado_id = int(get_jwt_identity())

    return {
        "id": empleado_id,
        "email": claims.get("email"),
        "rol": claims.get("rol")
    }, 200

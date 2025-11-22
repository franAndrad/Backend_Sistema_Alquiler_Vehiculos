from flask import Blueprint, request, jsonify
from ..services.empleado_service import EmpleadoService
from ..utils.auth_utils import roles_required

empleado_bp = Blueprint("empleados", __name__, url_prefix="/empleados")
empleado_service = EmpleadoService()


@empleado_bp.get("")
@roles_required("ADMIN")
def listar_empleados():
    dtos = empleado_service.listar_empleados()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@empleado_bp.get("/rol/<string:empleado_rol>")
@roles_required("ADMIN")
def listar_empleados_por_rol(empleado_rol):
    dtos = empleado_service.listar_empleados_por_rol(empleado_rol)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@empleado_bp.get("/<int:empleado_id>")
@roles_required("ADMIN")
def obtener_empleado(empleado_id):
    dto = empleado_service.obtener_empleado(empleado_id)
    return jsonify(dto.__dict__), 200


@empleado_bp.get("/dni/<int:empleado_dni>")
@roles_required("ADMIN")
def obtener_empleado_por_dni(empleado_dni):
    dto = empleado_service.obtener_empleado_por_dni(empleado_dni)
    return jsonify(dto.__dict__), 200


@empleado_bp.get("/email/<string:empleado_email>")
@roles_required("ADMIN")
def obtener_empleado_por_email(empleado_email):
    dto = empleado_service.obtener_empleado_por_email(empleado_email)
    return jsonify(dto.__dict__), 200


@empleado_bp.post("")
@roles_required("ADMIN")
def crear_empleado():
    body = request.get_json() or {}
    dto = empleado_service.crear_empleado(body)
    return jsonify(dto.__dict__), 201


@empleado_bp.put("/<int:empleado_id>")
@roles_required("ADMIN")
def actualizar_empleado(empleado_id):
    body = request.get_json() or {}
    dto = empleado_service.actualizar_empleado(empleado_id, body)
    return jsonify(dto.__dict__), 200


@empleado_bp.delete("/<int:empleado_id>")
@roles_required("ADMIN")
def eliminar_empleado(empleado_id):
    resultado = empleado_service.eliminar_empleado(empleado_id)
    return jsonify(resultado), 200


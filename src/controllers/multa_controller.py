from flask import Blueprint, request, jsonify
from ..services.multa_service import MultaService
from ..utils.auth_utils import roles_required

multa_bp = Blueprint("multas", __name__, url_prefix="/multas")
multa_service = MultaService()


@multa_bp.get("")
@roles_required("ADMIN")
def listar_multas():
    dtos = multa_service.listar_multas()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@multa_bp.get("/<int:multa_id>")
@roles_required("ADMIN")
def obtener_multa(multa_id):
    dto = multa_service.obtener_multa(multa_id)
    return jsonify(dto.__dict__), 200   


@multa_bp.post("")
@roles_required("ADMIN")
def crear_multa():
    body = request.get_json() or {}
    dto = multa_service.crear_multa(body)
    return jsonify(dto.__dict__), 201


@multa_bp.put("/<int:multa_id>")
@roles_required("ADMIN")
def actualizar_multa(multa_id):
    body = request.get_json() or {}
    dto = multa_service.actualizar_multa(multa_id, body)
    return jsonify(dto.__dict__), 200


@multa_bp.delete("/<int:multa_id>")
@roles_required("ADMIN")
def eliminar_multa(multa_id):
    resultado = multa_service.eliminar_multa(multa_id)
    return jsonify(resultado), 200
from flask import Blueprint, request, jsonify
from ..services.modelo_service import ModeloService
from ..utils.auth_utils import roles_required

modelo_bp = Blueprint("modelos", __name__, url_prefix="/modelos")
modelo_service = ModeloService()

@modelo_bp.get("")
@roles_required("ADMIN")
def listar_modelos():
    dtos = modelo_service.listar_modelos()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@modelo_bp.get("/<int:modelo_id>")
@roles_required("ADMIN")
def obtener_modelo(modelo_id):
    dto = modelo_service.obtener_modelo(modelo_id)
    return jsonify(dto.__dict__), 200


@modelo_bp.post("")
@roles_required("ADMIN")
def crear_modelo():
    body = request.get_json() or {}
    dto = modelo_service.crear_modelo(body)
    return jsonify(dto.__dict__), 201


@modelo_bp.put("/<int:modelo_id>")
@roles_required("ADMIN")
def actualizar_modelo(modelo_id):
    body = request.get_json() or {}
    dto = modelo_service.actualizar_modelo(modelo_id, body)
    return jsonify(dto.__dict__), 200


@modelo_bp.delete("/<int:modelo_id>")
@roles_required("ADMIN")
def eliminar_modelo(modelo_id):
    resultado = modelo_service.eliminar_modelo(modelo_id)
    return jsonify(resultado), 200
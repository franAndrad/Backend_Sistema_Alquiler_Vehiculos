from ..services.marca_service import MarcasService
from flask import Blueprint, request, jsonify
from ..utils.auth_utils import roles_required

marca_bp = Blueprint("marcas", __name__, url_prefix="/marcas")
marca_service = MarcasService()

@marca_bp.get("")
@roles_required("ADMIN")
def listar_marcas():
    dtos = marca_service.listar_marcas()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@marca_bp.get("/<int:marca_id>")
@roles_required("ADMIN")
def obtener_marca(marca_id):
    dto = marca_service.obtener_marca(marca_id)
    return jsonify(dto.__dict__), 200


@marca_bp.get("/nombre/<string:marca_nombre>")
@roles_required("ADMIN")    
def obtener_marca_por_nombre(marca_nombre):
    dto = marca_service.obtener_marca_por_nombre(marca_nombre)
    return jsonify(dto.__dict__), 200


@marca_bp.post("")
@roles_required("ADMIN")
def crear_marca():
    body = request.get_json() or {}
    dto = marca_service.crear_marca(body)
    return jsonify(dto.__dict__), 201


@marca_bp.put("/<int:marca_id>")
@roles_required("ADMIN")
def actualizar_marca(marca_id):
    body = request.get_json() or {}
    dto = marca_service.actualizar_marca(marca_id, body)
    return jsonify(dto.__dict__), 200


@marca_bp.delete("/<int:marca_id>")
@roles_required("ADMIN")
def eliminar_marca(marca_id):
    resultado = marca_service.eliminar_marca(marca_id)
    return jsonify(resultado), 200
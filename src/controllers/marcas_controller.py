from flask import Blueprint, request, jsonify
from ..services.marcas_service import MarcasService

marcas_bp = Blueprint("marcas", __name__, url_prefix="/marcas")
marcas_service = MarcasService()

@marcas_bp.get("")
def listar_marcas():
    dtos = marcas_service.listar_marcas()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200

@marcas_bp.get("/<int:marca_id>")
def obtener_marca(marca_id):
    dtos = marcas_service.obtener_marca(marca_id)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200

@marcas_bp.get("/nombre/<string:marca_nombre>")
def obtener_marca_por_nombre(marca_nombre):
    dtos = marcas_service.obtener_marca_por_nombre(marca_nombre)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200

@marcas_bp.post("")
def crear_marca():
    body = request.get_json() or {}
    dto = marcas_service.crear_marca(body)
    return jsonify(dto.__dict__), 201

@marcas_bp.put("/<int:marca_id>")
def actualizar_marca(marca_id):
    body = request.get_json() or {}
    dto = marcas_service.actualizar_marca(marca_id, body)
    return jsonify(dto.__dict__), 200

@marcas_bp.delete("/<int:marca_id>")
def eliminar_marca(marca_id):
    resultado = marcas_service.eliminar_marca(marca_id)
    return jsonify(resultado), 200
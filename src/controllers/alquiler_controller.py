from flask import Blueprint, request, jsonify
from ..services.alquiler_service import AlquilerService

alquiler_bp = Blueprint("alquileres", __name__, url_prefix="/alquileres")
alquiler_service = AlquilerService()

@alquiler_bp.get("")
def listar_alquileres():
    dtos = alquiler_service.listar_alquileres()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200

@alquiler_bp.get("/<int:alquiler_id>")
def obtener_alquiler(alquiler_id):
    dto = alquiler_service.obtener_alquiler(alquiler_id)
    return jsonify(dto.__dict__), 200

@alquiler_bp.get("/cliente/<int:cliente_id>")
def listar_alquileres_por_cliente(cliente_id):
    dtos = alquiler_service.listar_alquileres_por_cliente(cliente_id)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200

@alquiler_bp.get("/vehiculo/<int:vehiculo_id>")
def listar_alquileres_por_vehiculo(vehiculo_id):
    dtos = alquiler_service.listar_alquileres_por_vehiculo(vehiculo_id)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200

@alquiler_bp.post("")
def crear_alquiler():
    body = request.get_json() or {}
    dto = alquiler_service.crear_alquiler(body)
    return jsonify(dto.__dict__), 201

@alquiler_bp.put("/<int:alquiler_id>")
def actualizar_alquiler(alquiler_id):
    body = request.get_json() or {}
    dto = alquiler_service.actualizar_alquiler(alquiler_id, body)
    return jsonify(dto.__dict__), 200

@alquiler_bp.delete("/<int:alquiler_id>")
def eliminar_alquiler(alquiler_id):
    resultado = alquiler_service.eliminar_alquiler(alquiler_id)
    return jsonify(resultado), 200

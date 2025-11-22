from flask import Blueprint, request, jsonify
from ..services.vehiculo_service import VehiculoService

vehiculo_bp = Blueprint("vehiculos", __name__, url_prefix="/vehiculos")
vehiculo_service = VehiculoService()


@vehiculo_bp.get("")
def listar_vehiculos():
    dtos = vehiculo_service.listar_vehiculos()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@vehiculo_bp.get("/<int:vehiculo_id>")
def obtener_vehiculo(vehiculo_id):
    dto = vehiculo_service.obtener_vehiculo(vehiculo_id)
    return jsonify(dto.__dict__), 200


@vehiculo_bp.get("/estado/<string:estados>")
def obtener_vehiculos_por_estado(estados):
    estados_list = estados.split(",")
    dtos = vehiculo_service.obtener_vehiculos_por_estado(estados_list)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@vehiculo_bp.post("")
def crear_vehiculo():
    body = request.get_json() or {}
    dto = vehiculo_service.crear_vehiculo(body)
    return jsonify(dto.__dict__), 201


@vehiculo_bp.put("/<int:vehiculo_id>")
def actualizar_vehiculo(vehiculo_id):
    body = request.get_json() or {}
    dto = vehiculo_service.actualizar_vehiculo(vehiculo_id, body)
    return jsonify(dto.__dict__), 200


@vehiculo_bp.delete("/<int:vehiculo_id>")
def eliminar_vehiculo(vehiculo_id):
    resultado = vehiculo_service.eliminar_vehiculo(vehiculo_id)
    return jsonify(resultado), 200

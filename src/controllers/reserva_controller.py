from flask import Blueprint, request, jsonify
from ..services.reserva_service import ReservaService

reserva_bp = Blueprint("reservas", __name__, url_prefix="/reservas")
reserva_service = ReservaService()


@reserva_bp.get("")
def listar_reservas():
    dtos = reserva_service.listar_reservas()
    data = [dto._dict_ for dto in dtos]
    return jsonify(data), 200


@reserva_bp.get("/<int:reserva_id>")
def obtener_reserva(reserva_id):
    dto = reserva_service.obtener_reserva(reserva_id)
    return jsonify(dto._dict_), 200


@reserva_bp.post("")
def crear_reserva():
    body = request.get_json() or {}
    dto = reserva_service.crear_reserva(body)
    return jsonify(dto._dict_), 201


@reserva_bp.put("/<int:reserva_id>")
def actualizar_reserva(reserva_id):
    body = request.get_json() or {}
    dto = reserva_service.actualizar_reserva(reserva_id, body)
    return jsonify(dto._dict_), 200


@reserva_bp.delete("/<int:reserva_id>")
def eliminar_reserva(reserva_id):
    resultado = reserva_service.eliminar_reserva(reserva_id)
    return jsonify(resultado), 200


@reserva_bp.get("/cliente/<int:cliente_id>")
def obtener_reservas_por_cliente(cliente_id):
    dtos = reserva_service.obtener_reservas_por_cliente(cliente_id)
    data = [dto._dict_ for dto in dtos]
    return jsonify(data), 200
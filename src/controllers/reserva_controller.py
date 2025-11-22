from flask import Blueprint, request, jsonify
from ..services.reserva_service import ReservaService
from ..utils.auth_utils import roles_required

reserva_bp = Blueprint("reservas", __name__, url_prefix="/reservas")
reserva_service = ReservaService()


@reserva_bp.get("")
@roles_required("ADMIN", "ATENCION")
def listar_reservas():
    dtos = reserva_service.listar_reservas()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@reserva_bp.get("/<int:reserva_id>")
@roles_required("ADMIN", "ATENCION")
def obtener_reserva(reserva_id):
    dto = reserva_service.obtener_reserva(reserva_id)
    return jsonify(dto.__dict__), 200


@reserva_bp.get("/estado/<string:estados>")
@roles_required("ADMIN", "ATENCION")
def obtener_reservas_por_estado(estados):
    estados_list = estados.split(",")
    dtos = reserva_service.obtener_reservas_por_estado(estados_list)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@reserva_bp.post("")
@roles_required("ADMIN", "ATENCION")
def crear_reserva():
    body = request.get_json() or {}
    dto = reserva_service.crear_reserva(body)
    return jsonify(dto.__dict__), 201


@reserva_bp.put("/<int:reserva_id>")
@roles_required("ADMIN", "ATENCION")
def actualizar_reserva(reserva_id):
    body = request.get_json() or {}
    dto = reserva_service.actualizar_reserva(reserva_id, body)
    return jsonify(dto.__dict__), 200


@reserva_bp.get("/cliente/<int:cliente_id>")
@roles_required("ADMIN", "ATENCION")
def obtener_reservas_por_cliente(cliente_id):
    dtos = reserva_service.obtener_reservas_por_cliente(cliente_id)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@reserva_bp.patch("/<int:reserva_id>/cancelar")
@roles_required("ADMIN", "ATENCION")
def cancelar_reserva(reserva_id):
    resultado = reserva_service.cancelar_reserva(reserva_id)
    return jsonify(resultado), 200

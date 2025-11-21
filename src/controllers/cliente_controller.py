from flask import Blueprint, request, jsonify

from ..services.cliente_service import ClienteService

cliente_bp = Blueprint("clientes", __name__, url_prefix="/clientes")

cliente_service = ClienteService()


@cliente_bp.get("")
def listar_clientes():
    dtos = cliente_service.listar_clientes()
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@cliente_bp.get("/<int:cliente_id>")
def obtener_cliente(cliente_id):
    dto = cliente_service.obtener_cliente(cliente_id)
    return jsonify(dto.__dict__), 200


@cliente_bp.post("")
def crear_cliente():
    body = request.get_json() or {}
    dto = cliente_service.crear_cliente(body)
    return jsonify(dto.__dict__), 201

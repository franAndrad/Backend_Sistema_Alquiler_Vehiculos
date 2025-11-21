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


@cliente_bp.put("/<int:cliente_id>")
def actualizar_cliente(cliente_id):
    body = request.get_json() or {}
    dto = cliente_service.actualizar_cliente(cliente_id, body)
    return jsonify(dto.__dict__), 200


@cliente_bp.delete("/<int:cliente_id>")
def eliminar_cliente(cliente_id):
    resultado =cliente_service.eliminar_cliente(cliente_id)
    return jsonify(resultado), 200


@cliente_bp.get("/dni/<int:cliente_dni>")
def obtener_cliente_por_dni(cliente_dni):
    dto = cliente_service.obtener_cliente_por_dni(cliente_dni)
    return jsonify(dto.__dict__), 200


@cliente_bp.get("/email/<string:cliente_email>")
def obtener_cliente_por_email(cliente_email):
    dto = cliente_service.obtener_cliente_por_email(cliente_email)
    return jsonify(dto.__dict__), 200
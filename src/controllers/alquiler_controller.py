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


@alquiler_bp.get("/estado/<string:estados>")
def listar_alquileres_por_estado(estados):
    estados_list = estados.split(",")
    dtos = alquiler_service.listar_alquileres_por_estado(estados_list)
    data = [dto.__dict__ for dto in dtos]
    return jsonify(data), 200


@alquiler_bp.get("/periodo")
def listar_por_periodo():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if not desde or not hasta:
        return jsonify({"error": "Debe indicar ?desde=YYYY-MM-DD&hasta=YYYY-MM-DD"}), 400

    dtos = alquiler_service.listar_alquileres_por_periodo(desde, hasta)
    return jsonify([dto.__dict__ for dto in dtos]), 200


@alquiler_bp.get("/vehiculos-mas-alquilados")
def vehiculos_mas_alquilados():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    limite = request.args.get("limit")

    data = alquiler_service.vehiculos_mas_alquilados(
        fecha_desde=desde,
        fecha_hasta=hasta,
        limite=limite,
    )

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


@alquiler_bp.patch("/<int:alquiler_id>/finalizar")
def finalizar_alquiler(alquiler_id):
    resultado = alquiler_service.finalizar_alquiler(alquiler_id)
    return jsonify(resultado), 200

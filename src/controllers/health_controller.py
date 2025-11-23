from ..utils.auth_utils import roles_required
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.get("/health")
@roles_required("ATENCION")
def health():
    return jsonify({"message": "ok!"}), 200

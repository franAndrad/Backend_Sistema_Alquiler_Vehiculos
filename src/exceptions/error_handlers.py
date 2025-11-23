from ..utils.auth_utils import AuthorizationException 
from .domain_exceptions import (
    DomainException,
    BusinessException,
    NotFoundException,
    ValidationException,
)

from flask import jsonify

def register_error_handlers(app):

    @app.errorhandler(BusinessException)
    def handle_business(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(NotFoundException)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(ValidationException)
    def handle_validation(e):
        return jsonify({"error": str(e)}), 422

    @app.errorhandler(AuthorizationException)
    def handle_authz(e):
        return jsonify({"error": str(e)}), 403

    @app.errorhandler(DomainException)
    def handle_domain(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Error interno del servidor"}), 500

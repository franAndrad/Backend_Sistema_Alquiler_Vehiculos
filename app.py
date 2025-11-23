import os
from dotenv import load_dotenv

if os.getenv("RUN_ENV") != "docker":
    load_dotenv()

from flask import Flask
from flask_cors import CORS
from src.exceptions.error_handlers import register_error_handlers
from src.extensions.jwt_ext import init_jwt
from src.extensions.db import db
from config import Config 

from src.controllers.empleado_controller import empleado_bp
from src.controllers.alquiler_controller import alquiler_bp
from src.controllers.vehiculo_controller import vehiculo_bp
from src.controllers.reserva_controller import reserva_bp
from src.controllers.cliente_controller import cliente_bp
from src.controllers.modelo_controller import modelo_bp
from src.controllers.health_controller import health_bp
from src.controllers.marca_controller import marca_bp
from src.controllers.multa_controller import multa_bp
from src.controllers.auth_controller import auth_bp

from src.utils.utf8_json_provider import UTF8JSONProvider
from src.utils.db_initilizer import DBInitializer


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    app.json_provider_class = UTF8JSONProvider
    app.json = app.json_provider_class(app)

    db.init_app(app)
    init_jwt(app)
    register_error_handlers(app)

    with app.app_context():
        initializer = DBInitializer()
        initializer.init_database(app.config["SQLALCHEMY_DATABASE_URI"])
        initializer.init_tables(app, db)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(empleado_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(modelo_bp)
    app.register_blueprint(multa_bp)
    app.register_blueprint(alquiler_bp)
    app.register_blueprint(vehiculo_bp)
    app.register_blueprint(reserva_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

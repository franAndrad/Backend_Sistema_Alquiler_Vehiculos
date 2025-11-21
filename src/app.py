from flask import Flask
from .config import Config
from .extensions.db import db
from .exceptions.error_handlers import register_error_handlers
from .controllers.health_controller import health_bp
from .controllers.cliente_controller import cliente_bp
from . import models
from .utils.db_initilizer import DBInitializer

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    initializer = DBInitializer()
    
    initializer.init_database(app.config["SQLALCHEMY_DATABASE_URI"])
    
    db.init_app(app)
    
    initializer.init_tables(app, db)
    
    register_error_handlers(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(cliente_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

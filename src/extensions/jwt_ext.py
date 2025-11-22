# src/extensions/jwt_ext.py
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_jwt(app):
    jwt.init_app(app)

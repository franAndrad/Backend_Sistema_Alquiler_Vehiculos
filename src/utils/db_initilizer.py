import pymysql
import urllib.parse

from src.models.empleado import Empleado
from src.models.enums import RolEmpleado
from src.extensions.db import db


class DBInitializer:
    """
    Implementación tipo Singleton para inicializar la base de datos,
    crear tablas y generar datos iniciales como el usuario administrador.
    """
    _instancia = None


    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(DBInitializer, cls).__new__(cls)
        return cls._instancia

    def init_database(self, uri: str):
        parsed = urllib.parse.urlparse(uri)

        host = parsed.hostname
        usuario = parsed.username
        contraseña = parsed.password
        nombre_bd = parsed.path.replace("/", "")

        conexion = pymysql.connect(
            host=host,
            user=usuario,
            password=contraseña,
            autocommit=True
        )

        with conexion.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_bd};")

        conexion.close()

    def init_tables(self, app, db):
        with app.app_context():
            db.create_all()
            self._asegurar_admin()
            db.session.commit()


    def _asegurar_admin(self):
        """
        Verifica si existe el usuario administrador.
        Si no existe, lo crea.
        Si existe pero su contraseña no está hasheada, la corrige.
        """
        email_admin = "admin@empresa.com"
        admin = Empleado.query.filter_by(email=email_admin).first()

        if admin is None:
            self._crear_admin(email_admin)
            return

        if not admin.password_hash or not admin.password_hash.startswith("pbkdf2"):
            admin.set_password("admin123")
            

    def _crear_admin(self, email: str):
        admin = Empleado(
            nombre="Administrador",
            apellido="Principal",
            dni="00000000",
            direccion="",
            telefono="",
            email=email,
            rol=RolEmpleado.ADMIN,
        )
        admin.set_password("admin123")

        db.session.add(admin)

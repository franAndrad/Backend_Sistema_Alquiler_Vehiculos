# services/empleado_service.py
from ..repository.empleado_repository import EmpleadoRepository
from ..exceptions.domain_exceptions import ValidationException, NotFoundException, BusinessException
from ..models.empleado import Empleado
from ..utils.mappers import empleado_to_response_dto
from .utils.persona_utils import (
    normalizar_campos_basicos,
    validar_campos_obligatorios,
    validar_nombre_apellido,
    validar_email_formato,
    validar_dni_formato,
    validar_telefono,
)


class EmpleadoService:

    def __init__(self, empleado_repository=None):
        self.empleado_repo = empleado_repository or EmpleadoRepository()


    def listar_empleados(self):
        empleados = self.empleado_repo.list_all()
        return [empleado_to_response_dto(e) for e in empleados]


    def listar_empleados_por_rol(self, empleado_rol):
        empleados = self.empleado_repo.find_by_rol(empleado_rol)
        return [empleado_to_response_dto(e) for e in empleados]


    def obtener_empleado(self, empleado_id):
        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise NotFoundException("Empleado no encontrado")
        return empleado_to_response_dto(empleado)


    def obtener_empleado_por_dni(self, empleado_dni):
        empleado = self.empleado_repo.find_by_dni(empleado_dni)
        if not empleado:
            raise NotFoundException("Empleado no encontrado")
        return empleado_to_response_dto(empleado)


    def obtener_empleado_por_email(self, empleado_email):
        empleado = self.empleado_repo.find_by_email(empleado_email)
        if not empleado:
            raise NotFoundException("Empleado no encontrado")
        return empleado_to_response_dto(empleado)


    def crear_empleado(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = ["nombre", "apellido", "dni", "email", "rol"]
        validar_campos_obligatorios(body, campos_obligatorios, "empleado")
        validar_nombre_apellido(body)
        validar_email_formato(body)
        validar_dni_formato(body, longitud_exacto=8)
        validar_telefono(body)


        if self.empleado_repo.find_by_dni(body["dni"]):
            raise BusinessException("Ya existe un empleado con ese DNI")

        if self.empleado_repo.find_by_email(body["email"]):
            raise BusinessException("Ya existe un empleado con ese email")

        empleado = Empleado(
            nombre=body["nombre"],
            apellido=body["apellido"],
            dni=body["dni"],
            direccion=body.get("direccion"),
            telefono=body.get("telefono"),
            email=body["email"],
            rol=body["rol"],
        )

        self.empleado_repo.add(empleado)
        return empleado_to_response_dto(empleado)


    def actualizar_empleado(self, empleado_id, body):
        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise NotFoundException("Empleado no encontrado")

        body = dict(body)
        body = normalizar_campos_basicos(body)

        validar_nombre_apellido(body)
        validar_email_formato(body)
        validar_dni_formato(body, longitud_exacto=8)
        validar_telefono(body)

        if "dni" in body and body["dni"] is not None:
            existente_dni = self.empleado_repo.find_by_dni(body["dni"])
            if existente_dni and existente_dni.id != empleado.id:
                raise BusinessException("Ya existe otro empleado con ese DNI")

        if "email" in body and body["email"] is not None:
            existente_email = self.empleado_repo.find_by_email(body["email"])
            if existente_email and existente_email.id != empleado.id:
                raise BusinessException(
                    "Ya existe otro empleado con ese email")

        if "nombre" in body:
            empleado.nombre = body["nombre"]
        if "apellido" in body:
            empleado.apellido = body["apellido"]
        if "direccion" in body:
            empleado.direccion = body["direccion"]
        if "telefono" in body:
            empleado.telefono = body["telefono"]
        if "dni" in body:
            empleado.dni = body["dni"]
        if "email" in body:
            empleado.email = body["email"]
        if "rol" in body:
            empleado.rol = body["rol"]

        self.empleado_repo.save_changes()
        return empleado_to_response_dto(empleado)

from sqlalchemy.exc import IntegrityError

from ..exceptions.domain_exceptions import NotFoundException, BusinessException
from ..repository.modelo_repository import ModeloRepository
from ..models.modelo import Modelo
from ..utils.mappers import modelo_to_response_dto
from .helpers.modelo_helpers import (
    normalizar_campos_basicos,
    validar_descripcion,
    validar_marca_existente,
    validar_nombre,
)
from ..services.helpers.comunes_helpers import validar_campos_obligatorios


class ModeloService:

    def __init__(self, modelo_repository=None):
        self.modelo_repo = modelo_repository or ModeloRepository()


    def listar_modelos(self):
        modelos = self.modelo_repo.list_all()
        return [modelo_to_response_dto(m) for m in modelos]


    def obtener_modelo(self, modelo_id):
        modelo = self.modelo_repo.get_by_id(modelo_id)
        if not modelo:
            raise NotFoundException("Modelo no encontrado")
        return modelo_to_response_dto(modelo)


    def obtener_modelo_por_descripcion(self, descripcion):
        modelo = self.modelo_repo.find_by_descripcion(descripcion)
        if not modelo:
            raise NotFoundException("Modelo no encontrado")
        return modelo_to_response_dto(modelo)


    def eliminar_modelo(self, modelo_id):
        modelo = self.modelo_repo.get_by_id(modelo_id)
        if not modelo:
            raise NotFoundException("Modelo no encontrado")

        try:
            self.modelo_repo.delete(modelo)
        except IntegrityError:
            # mensaje más claro al front
            raise BusinessException(
                "No se puede eliminar el modelo porque tiene vehículos asociados."
            )

        return {"mensaje": "Modelo eliminado correctamente"}


    def crear_modelo(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = ["id_marca", "nombre", "descripcion"]

        validar_campos_obligatorios(body, campos_obligatorios, "modelo")
        validar_nombre(body["nombre"])
        validar_descripcion(body["descripcion"])
        validar_marca_existente(body["id_marca"])

        if self.modelo_repo.find_by_nombre(body["nombre"]):
            raise BusinessException("Ya existe un modelo con ese nombre")

        nuevo_modelo = Modelo(
            id_marca=body["id_marca"],
            nombre=body["nombre"],
            descripcion=body["descripcion"],
        )

        self.modelo_repo.add(nuevo_modelo)
        return modelo_to_response_dto(nuevo_modelo)

    def actualizar_modelo(self, modelo_id, body):
        modelo = self.modelo_repo.get_by_id(modelo_id)
        if not modelo:
            raise NotFoundException("Modelo no encontrado")

        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = ["nombre", "id_marca", "descripcion"]

        validar_campos_obligatorios(body, campos_obligatorios, "modelo")
        validar_nombre(body["nombre"])
        validar_descripcion(body["descripcion"])
        validar_marca_existente(body["id_marca"])

        modelo_existente = self.modelo_repo.find_by_nombre(body["nombre"])
        if modelo_existente and modelo_existente.id != modelo.id:
            raise BusinessException("Ya existe un modelo con ese nombre")

        modelo.id_marca = body["id_marca"]
        modelo.nombre = body["nombre"]
        modelo.descripcion = body["descripcion"]

        self.modelo_repo.save_changes()
        return modelo_to_response_dto(modelo)

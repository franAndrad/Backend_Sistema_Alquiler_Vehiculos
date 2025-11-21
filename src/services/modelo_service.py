from ..repository.modelo_repository import ModeloRepository
from ..repository.marca_repository import MarcaRepository
from ..exceptions.domain_exceptions import NotFoundException, BusinessException
from ..models.modelo import Modelo
from ..utils.mappers import modelo_to_response_dto
from .utils.modelo_utlis import (
    normalizar_campos_basicos,
    validar_campos_obligatorios,
    validar_long_descripcion,
)


class ModeloService:

    def __init__(self, modelo_repository=None, marca_repository=None):
        self.modelo_repo = modelo_repository or ModeloRepository()
        self.marca_repo = marca_repository or MarcaRepository()


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

        self.modelo_repo.delete(modelo)
        return {"mensaje": "Modelo eliminado correctamente"}


    def crear_modelo(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = ["id_marca", "descripcion"]
        validar_campos_obligatorios(body, campos_obligatorios, "modelo")
        validar_long_descripcion(body)
        
        marca = self.marca_repo.get_by_id(body["id_marca"])
        if not marca:
            raise NotFoundException("La marca asociada no existe")
        
        if self.modelo_repo.find_by_nombre(body["nombre"]):
            raise BusinessException("Ya existe una marca con ese nombre")
        
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

        campos_obligatorios = ["descripcion"]
        validar_campos_obligatorios(body, campos_obligatorios, "modelo")
        validar_long_descripcion(body)
        
        modelo_existente = self.modelo_repo.find_by_nombre(body["nombre"])
        if modelo_existente and modelo_existente.id != modelo.id:
            raise BusinessException("Ya existe un modelo con ese nombre")

        if "id_marca" in body and body["id_marca"] is not None:
            marca = self.marca_repo.get_by_id(body["id_marca"])
            if not marca:
                raise NotFoundException("La marca asociada no existe")
            modelo.id_marca = body["id_marca"]

        modelo.nombre = body["nombre"]
        modelo.descripcion = body["descripcion"]

        self.modelo_repo.save_changes()
        return modelo_to_response_dto(modelo)

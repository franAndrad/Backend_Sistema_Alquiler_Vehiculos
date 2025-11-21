from datetime import date

from ..repository.marca_repository import MarcaRepository
from ..exceptions.domain_exceptions import NotFoundException, BusinessException
from ..models.marca import Marca
from ..utils.mappers import marca_to_response_dto
from .utils.marca_utils import (
    normalizar_campos_basicos, 
    validar_campos_obligatorios,
    validar_long_nombre
)

class MarcasService:

    def __init__(self, marca_repository=None):
        self.marca_repo = marca_repository or MarcaRepository()


    def listar_marcas(self):
        marcas = self.marca_repo.list_all()
        return [marca_to_response_dto(m) for m in marcas]
    
    
    def obtener_marca(self, marca_id):
        marca = self.marca_repo.get_by_id(marca_id)
        if not marca:
            raise NotFoundException("Marca no encontrada")
        return marca_to_response_dto(marca)
    
    
    def obtener_marca_por_nombre(self, marca_nombre):
        marca = self.marca_repo.find_by_nombre(marca_nombre)
        if not marca:
            raise NotFoundException("Marca no encontrada")
        return marca_to_response_dto(marca)
    

    def eliminar_marca(self, marca_id):
        marca = self.marca_repo.get_by_id(marca_id)
        if not marca:
            raise NotFoundException("Marca no encontrada")
        
        self.marca_repo.delete(marca)
        return {"mensaje": "Marca eliminada correctamente"}
    
    
    def crear_marca(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = ["nombre"]
        
        validar_campos_obligatorios(body, campos_obligatorios, "marca")
        validar_long_nombre(body)
        
        if self.marca_repo.find_by_nombre(body["nombre"]):
            raise BusinessException("Ya existe una marca con ese nombre")

        nueva_marca = Marca(nombre=body["nombre"])
        
        self.marca_repo.add(nueva_marca)
        return marca_to_response_dto(nueva_marca)
    

    def actualizar_marca(self, marca_id, body):
        marca = self.marca_repo.get_by_id(marca_id)
        if not marca:
            raise NotFoundException("Marca no encontrada")
        
        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = ["nombre"]

        validar_campos_obligatorios(body, campos_obligatorios, "marca")
        validar_long_nombre(body)
        
        marca_existente = self.marca_repo.find_by_nombre(body["nombre"])
        if marca_existente and marca_existente.id != marca.id:
            raise BusinessException("Ya existe una marca con ese nombre")
            
        marca.nombre = body["nombre"]
        
        self.marca_repo.save_changes()
        return marca_to_response_dto(marca)
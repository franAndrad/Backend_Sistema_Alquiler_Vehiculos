from ..repository.vehiculo_repository import VehiculoRepository
from ..repository.modelo_repository import ModeloRepository
from ..exceptions.domain_exceptions import ValidationException, NotFoundException, BusinessException
from ..models.vehiculo import Vehiculo
from ..utils.mappers import vehiculo_to_response_dto



from .utils.vehiculo_utils import (
    normalizar_campos,
    validar_campos_obligatorios,
    validar_anio,
    validar_patente,
    validar_costo,
    validar_tipo,
)


class VehiculoService:

    def __init__(self):
        self.vehiculo_repo = VehiculoRepository()
        self.modelo_repo = ModeloRepository()

    def listar_vehiculos(self):
        vehiculos = self.vehiculo_repo.list_all()
        return [vehiculo_to_response_dto.from_entity(v) for v in vehiculos]

    def obtener_vehiculo(self, vehiculo_id):
        vehiculo = self.vehiculo_repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise ValidationException("El vehículo no existe")
        return vehiculo_to_response_dto.from_entity(vehiculo)

    def crear_vehiculo(self, body):
        body = dict(body)
        body = normalizar_campos(body)

        campos_obligatorios = [
            "id_modelo", "anio", "tipo", "patente", "costo_diario"
        ]
        validar_campos_obligatorios(body, campos_obligatorios, "vehiculo")
        validar_anio(body)
        validar_patente(body)
        validar_costo(body)
        validar_tipo(body)

        if self.vehiculo_repo.find_by_patente(body["patente"]):
            raise BusinessException("Ya existe un vehiculo con esa patente")


        modelo = self.modelo_repo.get_by_id(body["id_modelo"])
        if not modelo:
            raise NotFoundException("El modelo asociado no existe")
        
        vehiculo = Vehiculo (
            id_modelo=body["id_modelo"],
            anio=body["anio"],
            tipo=body["tipo"],
            patente=body["patente"],
            costo_diario=body["costo_diario"]
        )

        self.vehiculo_repo.add(vehiculo)
        return vehiculo_to_response_dto(vehiculo)
    
    def actualizar_vehiculo(self, vehiculo_id, body):
        vehiculo = self.vehiculo_repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise NotFoundException("Vehiculo no encontrado")
        
        body = dict(body)
        body = normalizar_campos(body)

        campos_obligatorios = [
            "id_modelo", "anio", "tipo", "patente", "costo_diario"
        ]
        validar_campos_obligatorios(body, campos_obligatorios, "vehiculo")
        validar_anio(body)
        validar_patente(body)
        validar_costo(body)
        validar_tipo(body)

        existente_patente = self.vehiculo_repo.find_by_patente(body["patente"])
        if existente_patente and existente_patente.patente != vehiculo.patente:
            raise BusinessException("Ya existe otro vehiculo con esa patente")
        
        vehiculo.id_modelo = body["id_modelo"]
        vehiculo.anio = body["anio"]
        vehiculo.tipo = body["tipo"]
        vehiculo.patente = body["patente"]
        vehiculo.costo_diario = body["costo_diario"]

        self.vehiculo_repo.save_changes()
        return vehiculo_to_response_dto(vehiculo)


    def eliminar_vehiculo(self, vehiculo_id):
        vehiculo = self.vehiculo_repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise ValidationException("El vehículo no existe")

        self.vehiculo_repo.delete(vehiculo_id)
        return {"message": "Vehículo eliminado correctamente"}

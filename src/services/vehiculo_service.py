from ..repository.vehiculo_repository import VehiculoRepository
from ..dto.vehiculo_dto import VehiculoDTO
from ..exceptions.domain_exceptions import ValidationException
from .utils.vehiculo_utils import (
    normalizar_campos,
    validar_vehiculo_create,
    validar_anio,
    validar_patente,
    validar_costo,
)


class VehiculoService:

    def __init__(self):
        self.repo = VehiculoRepository()

    def listar_vehiculos(self):
        vehiculos = self.repo.get_all()
        return [VehiculoDTO.from_entity(v) for v in vehiculos]

    def obtener_vehiculo(self, vehiculo_id):
        vehiculo = self.repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise ValidationException("El vehículo no existe")
        return VehiculoDTO.from_entity(vehiculo)

    def crear_vehiculo(self, body):
        body = normalizar_campos(body)

        # 🧪 Validaciones
        validar_vehiculo_create(body)

        # 🔍 Verificar patente duplicada
        if self.repo.find_by_patente(body["patente"]):
            raise ValidationException("Ya existe un vehículo con esa patente")

        # Crear
        vehiculo = self.repo.create(body)
        return VehiculoDTO.from_entity(vehiculo)

    def actualizar_vehiculo(self, vehiculo_id, body):
        body = normalizar_campos(body)

        vehiculo = self.repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise ValidationException("El vehículo no existe")

        # Validaciones individuales si vienen en el body
        if "anio" in body:
            validar_anio(body)
        if "patente" in body:
            validar_patente(body)
        if "costo_diario" in body:
            validar_costo(body)

        # 🔍 Validar patente repetida en otro vehículo
        if "patente" in body:
            if self.repo.existe_patente_en_otro_vehiculo(body["patente"], vehiculo_id):
                raise ValidationException("La patente pertenece a otro vehículo")

        # Actualizar
        vehiculo = self.repo.update(vehiculo_id, body)
        return VehiculoDTO.from_entity(vehiculo)

    def eliminar_vehiculo(self, vehiculo_id):
        vehiculo = self.repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise ValidationException("El vehículo no existe")

        self.repo.delete(vehiculo_id)
        return {"message": "Vehículo eliminado correctamente"}

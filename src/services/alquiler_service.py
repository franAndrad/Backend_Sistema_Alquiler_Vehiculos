from datetime import date

from ..repository.alquiler_repository import AlquilerRepository
from ..exceptions.domain_exceptions import NotFoundException, BusinessException
from ..models.alquiler import Alquiler
from ..utils.mappers import alquiler_to_response_dto
from .utils.alquiler_utils import (
    normalizar_campos_basicos,
    validar_campos_obligatorios,
    validar_ids_foreign_keys,
    validar_fechas,
    validar_costo,
)

class AlquilerService:

    def __init__(self, alquiler_repository=None):
        self.alquiler_repo = alquiler_repository or AlquilerRepository()

    def listar_alquileres(self):
        alquileres = self.alquiler_repo.list_all()
        return [alquiler_to_response_dto(a) for a in alquileres]
    
    def obtener_alquiler(self, alquiler_id):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")
        return alquiler_to_response_dto(alquiler)
    
    def listar_alquileres_por_cliente(self, cliente_id):
        alquileres = self.alquiler_repo.find_by_cliente_id(cliente_id)
        return [alquiler_to_response_dto(a) for a in alquileres]
    
    def listar_alquileres_por_vehiculo(self, vehiculo_id):
        alquileres = self.alquiler_repo.find_by_vehiculo_id(vehiculo_id)
        return [alquiler_to_response_dto(a) for a in alquileres]
    
    def eliminar_alquiler(self, alquiler_id):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")

        self.alquiler_repo.delete(alquiler)
        return {"mensaje": "Alquiler eliminado correctamente"}
    
    def crear_alquiler(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = [
            "id_cliente", "id_empleado", "id_vehiculo",
            "fecha_inicio", "fecha_fin", "estado"
        ]

        validar_campos_obligatorios(body, campos_obligatorios, "alquiler")
        validar_ids_foreign_keys(body)
        validar_fechas(body)
        validar_costo(body)
        
        nuevo_alquiler = Alquiler(
            id_cliente=body["id_cliente"],
            id_empleado=body["id_empleado"],
            id_vehiculo=body["id_vehiculo"],
            fecha_inicio=date.fromisoformat(body["fecha_inicio"]),
            fecha_fin=date.fromisoformat(body["fecha_fin"]),
            costo_total=float(body["costo_total"]),
            estado=body["estado"]
        )

        self.alquiler_repo.add(nuevo_alquiler)
        return alquiler_to_response_dto(nuevo_alquiler)

    def actualizar_alquiler(self, alquiler_id, body):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")

        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = [
            "id_cliente", "id_empleado", "id_vehiculo",
            "fecha_inicio", "fecha_fin", "estado"
        ]

        validar_campos_obligatorios(body, campos_obligatorios, "alquiler")
        validar_ids_foreign_keys(body)
        validar_fechas(body)
        validar_costo(body)

        alquiler.id_cliente = body["id_cliente"]
        alquiler.id_empleado = body["id_empleado"]
        alquiler.id_vehiculo = body["id_vehiculo"]
        alquiler.fecha_inicio = date.fromisoformat(body["fecha_inicio"])
        alquiler.fecha_fin = date.fromisoformat(body["fecha_fin"])
        alquiler.costo_total = float(body["costo_total"])
        alquiler.estado = body["estado"]

        self.alquiler_repo.add(alquiler)
        return alquiler_to_response_dto(alquiler)
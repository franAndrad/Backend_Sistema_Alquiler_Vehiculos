from datetime import date
from ..repository.alquiler_repository import AlquilerRepository
from ..exceptions.domain_exceptions import NotFoundException
from ..models.enums import EstadoAlquiler
from ..models.alquiler import Alquiler
from ..utils.mappers import alquiler_to_response_dto
from .utils.alquiler_utils import (
    normalizar_campos_basicos,
    validar_campos_obligatorios,
    validar_ids_foreign_keys,
    validar_fechas,
    obtener_estado_enum,
    validar_cliente_existente,
    validar_empleado_existente,
    validar_vehiculo_disponible,
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
    
    
    # No se pueden eliminar alquileres, solo finalizar o cancelar
    # def eliminar_alquiler(self, alquiler_id):
    #     alquiler = self.alquiler_repo.get_by_id(alquiler_id)
    #     if not alquiler:
    #         raise NotFoundException("Alquiler no encontrado")

    #     self.alquiler_repo.delete(alquiler)
    #     return {"mensaje": "Alquiler eliminado correctamente"}
    
    
    def crear_alquiler(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = [
            "id_cliente", "id_empleado", "id_vehiculo",
            "fecha_inicio", "fecha_fin", "estado"
        ]

        validar_campos_obligatorios(body, campos_obligatorios, "alquiler")
        validar_ids_foreign_keys(body["id_cliente"], body["id_empleado"], body["id_vehiculo"])
        validar_fechas(body["fecha_inicio"], body["fecha_fin"])
        validar_cliente_existente(body["id_cliente"])
        validar_empleado_existente(body["id_empleado"])
        validar_vehiculo_disponible(body["id_vehiculo"])
        
        estado_enum = obtener_estado_enum(EstadoAlquiler.ACTIVO)
              
        nuevo_alquiler = Alquiler(
            id_cliente=body["id_cliente"],
            id_empleado=body["id_empleado"],
            id_vehiculo=body["id_vehiculo"],
            fecha_inicio=date.fromisoformat(body["fecha_inicio"]),
            fecha_fin=date.fromisoformat(body["fecha_fin"]),
            estado=estado_enum.estado_enum,
            costo_total=0.0
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
        validar_ids_foreign_keys(body["id_cliente"], body["id_empleado"], body["id_vehiculo"])
        validar_fechas(body["fecha_inicio"], body["fecha_fin"])
        validar_cliente_existente(body["id_cliente"])
        validar_empleado_existente(body["id_empleado"])
        validar_vehiculo_disponible(body["id_vehiculo"])

        alquiler.id_cliente = body["id_cliente"]
        alquiler.id_empleado = body["id_empleado"]
        alquiler.id_vehiculo = body["id_vehiculo"]
        alquiler.fecha_inicio = date.fromisoformat(body["fecha_inicio"])
        alquiler.fecha_fin = date.fromisoformat(body["fecha_fin"])

        self.alquiler_repo.save_changes()
        return alquiler_to_response_dto(alquiler)
    
    
    def finalizar_alquiler(self, alquiler_id):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")

        estado_enum = obtener_estado_enum(alquiler.estado)

        estado_enum.finalizar()
        alquiler.estado = estado_enum.estado_enum

        self.alquiler_repo.save_changes()
        return alquiler_to_response_dto(alquiler)
    
    
    def cancelar_alquiler(self, alquiler_id):
        alquiler = self.alquiler_repo.get_by_id(alquiler_id)
        if not alquiler:
            raise NotFoundException("Alquiler no encontrado")

        estado_enum = obtener_estado_enum(alquiler.estado)

        estado_enum.cancelar()
        alquiler.estado = estado_enum.estado_enum

        self.alquiler_repo.save_changes()
        return alquiler_to_response_dto(alquiler)
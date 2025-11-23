from datetime import date

from ..repository.multa_repository import MultaRepository
from ..repository.alquiler_repository import AlquilerRepository
from ..exceptions.domain_exceptions import NotFoundException, BusinessException
from ..models.enums import EstadoAlquiler
from ..models.multa import Multa
from datetime import datetime
from ..utils.mappers import multa_to_response_dto
from .utils.multa_utils import (
    normalizar_campos_basicos,
    validar_campos_obligatorios,
    validar_id_alquiler,
    validar_monto,
    validar_fecha,
    validar_descripcion,
    validar_alquiler_existente,
)

class MultaService:
    
    def __init__(self, multa_repository=None):
        self.multa_repo = multa_repository or MultaRepository()
        self.alquiler_repo = AlquilerRepository()


    def listar_multas(self):
        multas = self.multa_repo.list_all()
        return [multa_to_response_dto(m) for m in multas]
    
    
    def obtener_multa(self, multa_id):
        multa = self.multa_repo.get_by_id(multa_id)
        if not multa:
            raise NotFoundException("Multa no encontrada")
        return multa_to_response_dto(multa)
    
    
    def multa_por_alquiler(self, alquiler_id):
        multa = self.multa_repo.find_by_alquiler(alquiler_id)
        if not multa:
            raise NotFoundException("Multa no encontrada")
        return multa_to_response_dto(multa)
    
    
    def multa_por_fecha(self, fecha: date):
        multas = self.multa_repo.find_by_fecha(fecha)
        if not multas:
            raise NotFoundException("No se encontraron multas en la fecha indicada")
        return [multa_to_response_dto(m) for m in multas]
    
    
    def multa_por_monto(self, monto: float):
        multas = self.multa_repo.find_by_monto(monto)
        if not multas:
            raise NotFoundException("No se encontraron multas con el monto indicado")
        return [multa_to_response_dto(m) for m in multas]
    
    
    def eliminar_multa(self, multa_id):
        multa = self.multa_repo.get_by_id(multa_id)
        if not multa:
            raise NotFoundException("Multa no encontrada")

        self.multa_repo.delete(multa)
        return {"mensaje": "Multa eliminada correctamente"}
    
    
    def crear_multa(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = [
            "id_alquiler", "descripcion", "monto", "fecha"
        ]

        validar_campos_obligatorios(body, campos_obligatorios, "multa")
        validar_id_alquiler(body["id_alquiler"])
        validar_monto(body["monto"])
        validar_fecha(body["fecha"])
        validar_descripcion(body["descripcion"])
        validar_alquiler_existente(body["id_alquiler"])

                
        alquiler = self.alquiler_repo.get_by_id(body["id_alquiler"])
        if not alquiler:
            raise NotFoundException("El alquiler asociado no existe")

        if alquiler.estado != EstadoAlquiler.ACTIVO:
            raise BusinessException("Solo se pueden registrar multas para alquileres activos")

        try:
            fecha_multa = datetime.strptime(body["fecha"], "%Y-%m-%d").date()
        except ValueError:
            raise BusinessException("El formato de fecha debe ser YYYY-MM-DD")

        if fecha_multa < alquiler.fecha_inicio:
            raise BusinessException(
                "La fecha de la multa no puede ser anterior al inicio del alquiler"
            )

        nueva_multa = Multa(
            id_alquiler=body["id_alquiler"],
            descripcion=body["descripcion"],
            monto=body["monto"],
            fecha=body["fecha"]
        )

        self.multa_repo.add(nueva_multa)
        return multa_to_response_dto(nueva_multa)
    

    def actualizar_multa(self, multa_id, body):
        multa = self.multa_repo.get_by_id(multa_id)
        if not multa:
            raise NotFoundException("Multa no encontrada")

        body = dict(body)
        body = normalizar_campos_basicos(body)

        campos_obligatorios = [
            "id_alquiler", "descripcion", "monto", "fecha"
        ]

        validar_campos_obligatorios(body, campos_obligatorios, "multa")
        validar_id_alquiler(body["id_alquiler"])
        validar_descripcion(body["descripcion"])
        validar_monto(body["monto"])
        validar_fecha(body["fecha"])

        alquiler = self.alquiler_repo.get_by_id(body["id_alquiler"])
        if not alquiler:
            raise NotFoundException("El alquiler asociado no existe")

        if alquiler.estado != EstadoAlquiler.ACTIVO:
            raise BusinessException("Solo se pueden actualizar multas para alquileres activos")

        try:
            fecha_multa = datetime.strptime(body["fecha"], "%Y-%m-%d").date()
        except ValueError:
            raise BusinessException("El formato de fecha debe ser YYYY-MM-DD")

        if fecha_multa < alquiler.fecha_inicio:
            raise BusinessException(
                "La fecha de la multa no puede ser anterior al inicio del alquiler"
            )

        multa.id_alquiler = body["id_alquiler"]
        multa.descripcion = body["descripcion"]
        multa.monto = body["monto"]
        multa.fecha = body["fecha"]

        self.multa_repo.save_changes()
        return multa_to_response_dto(multa)

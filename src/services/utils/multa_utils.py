from ...exceptions.domain_exceptions import ValidationException, NotFoundException
from ...repository.alquiler_repository import AlquilerRepository


from datetime import date

def normalizar_campos_basicos(body: dict) -> dict:
    """Quita espacios y normaliza campos si están presentes."""
    if "descripcion" in body and body["descripcion"] is not None:
        body["descripcion"] = body["descripcion"].strip()
    return body

def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    faltantes = [
        c for c in campos_obligatorios if c not in body or not body[c]]
    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios para {entidad}: {', '.join(faltantes)}"
        )
    
def validar_id_alquiler(id_alquiler):
    if id_alquiler is not None:
        try:
            alquiler_id = int(id_alquiler)
            if alquiler_id <= 0:
                raise ValidationException("El id_alquiler debe ser un número entero positivo")
        except ValueError:
            raise ValidationException("El id_alquiler debe ser un número entero válido")
        
        
def validar_monto(monto):
    if monto is not None:
        try:
            monto = float(monto)
            if monto < 0:
                raise ValidationException("El monto debe ser un número positivo")
        except ValueError:
            raise ValidationException("El monto debe ser un número válido")


def validar_fecha(fecha):
    if fecha is not None:
        try:
            date.fromisoformat(fecha)
        except ValueError:
            raise ValidationException(f"La fecha no tiene un formato válido (YYYY-MM-DD)")
        

def validar_descripcion(descripcion):
    if descripcion is not None:
        if len(descripcion) < 5:
            raise ValidationException("La descripción debe tener al menos 5 caracteres")


def validar_alquiler_existente(id_alquiler):
    alquiler_repository = AlquilerRepository()
    alquiler = alquiler_repository.get_by_id(id_alquiler)
    if not alquiler:
        raise NotFoundException("El alquiler asociado no existe")


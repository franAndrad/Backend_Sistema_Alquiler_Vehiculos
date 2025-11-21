from ...exceptions.domain_exceptions import ValidationException 
from datetime import date

def normalizar_campos_basicos(body: dict) -> dict:
    """Quita espacios de los campos básicos si están presentes."""
    if "fecha_inicio" in body and body["fecha_inicio"] is not None:
        body["fecha_inicio"] = body["fecha_inicio"].strip()
    if "fecha_fin" in body and body["fecha_fin"] is not None:
        body["fecha_fin"] = body["fecha_fin"].strip()
    if "estado" in body and body["estado"] is not None:
        body["estado"] = body["estado"].strip()
    return body

def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    faltantes = [
        c for c in campos_obligatorios if c not in body or not body[c]]
    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios para {entidad}: {', '.join(faltantes)}"
        )

def validar_ids_foreign_keys(body: dict):
    fk_campos = ["id_cliente", "id_empleado", "id_vehiculo"]
    for campo in fk_campos:
        if campo not in body or not isinstance(body[campo], int) or body[campo] <= 0:
            raise ValidationException(f"El campo {campo} debe ser un ID válido (entero positivo)")
        
def validar_fechas(body: dict):
    if "fecha_inicio" not in body or "fecha_fin" not in body:
        raise ValidationException("fecha_inicio y fecha_fin son obligatorios")
    
    try:
        fecha_inicio = date.fromisoformat(body["fecha_inicio"])
        fecha_fin = date.fromisoformat(body["fecha_fin"])
    except ValueError:
        raise ValidationException("Formato de fecha inválido (usar YYYY-MM-DD)")
    
    return fecha_inicio, fecha_fin

def validar_costo(body: dict):
    if "costo_total" not in body:
        raise ValidationException("costo_total es obligatorio")
    
    try:
        costo = float(body["costo_total"])
        if costo < 0:
            raise ValidationException("costo_total no puede ser negativo")
    except (ValueError, TypeError):
        raise ValidationException("costo_total debe ser un número válido")
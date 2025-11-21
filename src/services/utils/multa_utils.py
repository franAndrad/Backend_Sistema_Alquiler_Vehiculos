from ...exceptions.domain_exceptions import ValidationException


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
    
def validar_id_alquiler(body: dict):
    if "id_alquiler" in body:
        try:
            alquiler_id = int(body["id_alquiler"])
            if alquiler_id <= 0:
                raise ValidationException("El id_alquiler debe ser un número entero positivo")
        except ValueError:
            raise ValidationException("El id_alquiler debe ser un número entero válido")
        
        
def validar_monto(body: dict):
    if "monto" in body:
        try:
            monto = float(body["monto"])
            if monto < 0:
                raise ValidationException("El monto debe ser un número positivo")
        except ValueError:
            raise ValidationException("El monto debe ser un número válido")


def validar_fecha(body: dict):
    if "fecha" in body and body["fecha"] is not None:
        fecha_str = body["fecha"]
        try:
            date.fromisoformat(fecha_str)
        except ValueError:
            raise ValidationException(f"La fecha no tiene un formato válido (YYYY-MM-DD)")
        

def validar_descripcion(body: dict):
    if "descripcion" in body and body["descripcion"] is not None:
        if len(body["descripcion"]) < 5:
            raise ValidationException("La descripción debe tener al menos 5 caracteres")
        


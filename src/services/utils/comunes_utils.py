from datetime import date
from ...exceptions.domain_exceptions import ValidationException

def validar_fecha(fecha):
    try:
        fecha = date.fromisoformat(fecha)
    except ValueError:
        raise ValidationException("Formato de fecha inválido (usar YYYY-MM-DD)")
    
    return fecha


def validar_campos_obligatorios(body: dict, campos_obligatorios: list[str], entidad: str):
    faltantes = [
        campo
        for campo in campos_obligatorios
        if campo not in body or body[campo] in (None, "", [])
    ]
    if faltantes:
        raise ValidationException(
            f"Faltan campos obligatorios para {entidad}: {', '.join(faltantes)}"
        )


def normalizar_strings(body: dict, campos: list[str], to_lower: list[str] | None = None) -> dict:
    to_lower = set(to_lower or [])
    for campo in campos:
        if campo in body and isinstance(body[campo], str):
            body[campo] = body[campo].strip()
            if campo in to_lower:
                body[campo] = body[campo].lower()
    return body


def validar_enum(valor, enum_cls, nombre_campo: str):
    if not valor:
        raise ValidationException(f"El campo {nombre_campo} es obligatorio")

    try:
        enum_cls(valor)
    except ValueError:
        valores_validos = ", ".join([e.value for e in enum_cls])
        raise ValidationException(
            f"El valor '{valor}' no es válido para {nombre_campo}. "
            f"Valores válidos: {valores_validos}"
        )

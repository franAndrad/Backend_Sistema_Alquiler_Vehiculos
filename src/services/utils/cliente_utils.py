from datetime import date
from ...exceptions.domain_exceptions import ValidationException, BusinessException


CATEGORIAS_LICENCIA_VALIDAS = {"A", "B1", "B2", "C1", "C2"}


def parsear_licencia_vencimiento(body: dict) -> date:
    if "licencia_vencimiento" not in body or not body["licencia_vencimiento"]:
        raise ValidationException("licencia_vencimiento es obligatorio")

    try:
        licencia_vencimiento = date.fromisoformat(body["licencia_vencimiento"])
    except ValueError:
        raise ValidationException(
            "Formato de fecha inválido para licencia_vencimiento (usar YYYY-MM-DD)"
        )

    if licencia_vencimiento < date.today():
        raise BusinessException("La licencia se encuentra vencida")

    return licencia_vencimiento


def validar_categoria_licencia(body: dict):
    categoria = body.get("licencia_categoria")
    if not categoria:
        raise ValidationException("La categoría de licencia es obligatoria")

    if categoria not in CATEGORIAS_LICENCIA_VALIDAS:
        raise ValidationException("La categoría de licencia no es válida")

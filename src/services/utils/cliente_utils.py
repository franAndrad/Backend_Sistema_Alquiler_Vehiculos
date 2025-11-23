from datetime import date
from ...exceptions.domain_exceptions import ValidationException, BusinessException
from .comunes_utils import validar_campos_obligatorios
from .persona_utils import (
    validar_nombre_apellido,
    validar_email_formato,
    validar_dni_formato,
    validar_telefono,
)

CATEGORIAS_LICENCIA_VALIDAS = {"A", "B1", "B2", "C1", "C2"}


def parsear_licencia_vencimiento(licencia_vencimiento_str) -> date:
    if not licencia_vencimiento_str:
        raise ValidationException("licencia_vencimiento es obligatorio")

    try:
        licencia_vencimiento = date.fromisoformat(licencia_vencimiento_str)
    except ValueError:
        raise ValidationException(
            "Formato de fecha inválido para licencia_vencimiento (usar YYYY-MM-DD)"
        )

    if licencia_vencimiento < date.today():
        raise BusinessException("La licencia se encuentra vencida")

    return licencia_vencimiento


def validar_categoria_licencia(categoria):
    if not categoria:
        raise ValidationException("La categoría de licencia es obligatoria")

    if categoria not in CATEGORIAS_LICENCIA_VALIDAS:
        raise ValidationException("La categoría de licencia no es válida")


def validar_datos_cliente(body: dict, es_update: bool = False):
    campos_obligatorios = ["nombre", "apellido",
                           "dni", "email", "licencia_categoria"]
    
    validar_campos_obligatorios(body, campos_obligatorios, "cliente")
    validar_nombre_apellido(body.get("nombre"), body.get("apellido"))
    validar_email_formato(body.get("email"))
    validar_dni_formato(body.get("dni"), longitud_exacto=8)

    telefono = body.get("telefono")
    if not es_update or telefono is not None:
        validar_telefono(telefono)

    validar_categoria_licencia(body.get("licencia_categoria"))

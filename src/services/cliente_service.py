from datetime import date

from ..repository.cliente_repository import ClienteRepository
from ..exceptions.domain_exceptions import ValidationException, NotFoundException, BusinessException
from ..models.cliente import Cliente
from ..utils.mappers import cliente_to_response_dto


class ClienteService:

    def __init__(self, cliente_repository=None):
        self.cliente_repo = cliente_repository or ClienteRepository()

    def listar_clientes(self):
        clientes = self.cliente_repo.list_all()
        return [cliente_to_response_dto(c) for c in clientes]

    def obtener_cliente(self, cliente_id):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundException("Cliente no encontrado")
        return cliente_to_response_dto(cliente)


    def crear_cliente(self, body):
        campos_obligatorios = [
            "nombre", "apellido", "dni", "email",
            "licencia_numero", "licencia_categoria", "licencia_vencimiento"
        ]
        
        faltantes = []
        for c in campos_obligatorios:
            if c not in body or not body[c]:
                faltantes.append(c)
                
        if faltantes:
            raise ValidationException(
                "Faltan campos obligatorios: " + ", ".join(faltantes))

        # Normalizar y validar formato básico
        body["nombre"] = body["nombre"].strip()
        body["apellido"] = body["apellido"].strip()
        email = body["email"].strip()

        if len(body["nombre"]) < 2:
            raise ValidationException("El nombre es demasiado corto")

        if len(body["apellido"]) < 2:
            raise ValidationException("El apellido es demasiado corto")

        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationException("El email no tiene un formato válido")
        body["email"] = email.lower()

        dni_str = str(body["dni"])
        if not dni_str.isdigit() or not (7 <= len(dni_str) <= 8):
            raise ValidationException("El DNI debe tener 7 u 8 dígitos numéricos")

        telefono = body.get("telefono")
        if telefono:
            tel_str = str(telefono)
            if not tel_str.isdigit() or len(tel_str) < 7:
                raise ValidationException("El teléfono no es válido")

        # Fecha
        try:
            licencia_vencimiento = date.fromisoformat(body["licencia_vencimiento"])
        except ValueError:
            raise ValidationException(
                "Formato de fecha inválido para licencia_vencimiento (usar YYYY-MM-DD)")

        if licencia_vencimiento < date.today():
            raise BusinessException("La licencia se encuentra vencida")

        categorias_validas = {"A", "B1", "B2", "C1", "C2"}
        if body["licencia_categoria"] not in categorias_validas:
            raise ValidationException("La categoría de licencia no es válida")

        # Reglas de negocio existentes
        if self.cliente_repo.find_by_dni(body["dni"]):
            raise BusinessException("Ya existe un cliente con ese DNI")

        if self.cliente_repo.find_by_email(body["email"]):
            raise BusinessException("Ya existe un cliente con ese email")

        cliente = Cliente(
            nombre=body["nombre"],
            apellido=body["apellido"],
            dni=body["dni"],
            direccion=body.get("direccion"),
            telefono=body.get("telefono"),
            email=body["email"],
            licencia_numero=body["licencia_numero"],
            licencia_categoria=body["licencia_categoria"],
            licencia_vencimiento=licencia_vencimiento,
        )

        self.cliente_repo.add(cliente)
        return cliente_to_response_dto(cliente)  

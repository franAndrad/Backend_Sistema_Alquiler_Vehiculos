
from ..exceptions.domain_exceptions import NotFoundException, BusinessException
from ..repository.cliente_repository import ClienteRepository
from ..models.cliente import Cliente
from ..utils.mappers import (
    cliente_to_response_dto
    )
from .utils.persona_utils import (
    normalizar_campos_basicos,
)

from .utils.cliente_utils import (
    parsear_licencia_vencimiento,
    validar_datos_cliente
    )



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


    def obtener_cliente_por_dni(self, cliente_dni):
        cliente = self.cliente_repo.find_by_dni(cliente_dni)
        if not cliente:
            raise NotFoundException("Cliente no encontrado")
        return cliente_to_response_dto(cliente)


    def obtener_cliente_por_email(self, cliente_email):
        cliente = self.cliente_repo.find_by_email(cliente_email)
        if not cliente:
            raise NotFoundException("Cliente no encontrado")
        return cliente_to_response_dto(cliente)

    
    def eliminar_cliente(self, cliente_id):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundException("Cliente no encontrado")

        self.cliente_repo.delete(cliente)
        return {"mensaje": "Cliente eliminado correctamente"}


    def crear_cliente(self, body):
        body = dict(body)
        body = normalizar_campos_basicos(body)
        
        validar_datos_cliente(body, es_update=False)
        licencia_vencimiento = parsear_licencia_vencimiento(body["licencia_vencimiento"])

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


    def actualizar_cliente(self, cliente_id, body):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundException("Cliente no encontrado")

        body = dict(body)
        body = normalizar_campos_basicos(body)
        
        validar_datos_cliente(body, es_update=True)
        licencia_vencimiento = parsear_licencia_vencimiento(body["licencia_vencimiento"])

        existente_dni = self.cliente_repo.find_by_dni(body["dni"])
        if existente_dni and existente_dni.id != cliente.id:
            raise BusinessException("Ya existe otro cliente con ese DNI")

        existente_email = self.cliente_repo.find_by_email(body["email"])
        if existente_email and existente_email.id != cliente.id:
            raise BusinessException("Ya existe otro cliente con ese email")

        cliente.nombre = body["nombre"]
        cliente.apellido = body["apellido"]
        cliente.dni = body["dni"]
        cliente.direccion = body.get("direccion")
        cliente.telefono = body.get("telefono")
        cliente.email = body["email"]
        cliente.licencia_numero = body["licencia_numero"]
        cliente.licencia_categoria = body["licencia_categoria"]
        cliente.licencia_vencimiento = licencia_vencimiento

        self.cliente_repo.save_changes()
        return cliente_to_response_dto(cliente)
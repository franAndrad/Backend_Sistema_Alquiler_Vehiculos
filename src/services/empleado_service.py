from ..repository.empleado_repository import EmpleadoRepository
from ..exceptions.domain_exceptions import ValidationException, NotFoundException, BusinessException
from ..models.empleado import Empleado
from ..utils.mappers import empleado_to_response_dto

class EmpleadoService:
    
    def __init__(self, empleado_repository=None):
        self.empleado_repo = empleado_repository or EmpleadoRepository()
        
        
    def listar_empleados(self):
        empleados = self.empleado_repo.list_all()
        return [empleado_to_response_dto(e) for e in empleados]
    
    
    def listar_empleados_por_rol(self, empleado_rol):
        empleados = self.empleado_repo.find_by_rol(empleado_rol)
        return [empleado_to_response_dto(e) for e in empleados]
    
    
    def obtener_empleado(self, empleado_id):
        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise NotFoundException("Empleado no encontrado")
        return empleado_to_response_dto(empleado)
    
    
    def obtener_empleado_por_dni(self, empleado_dni):
        empleado = self.empleado_repo.find_by_dni(empleado_dni)
        if not empleado:
            raise NotFoundException("Empleado no encontrado")
        return empleado_to_response_dto(empleado)
    
    
    def obtener_empleado_por_email(self, empleado_email):
        empleado = self.empleado_repo.find_by_email(empleado_email)
        if not empleado:
            raise NotFoundException("Empleado no encontrado")
        return empleado_to_response_dto(empleado)
    
    
    def crear_empleado(self, body):
        campos_obligatorios = [
            "nombre", "apellido", "dni", "email", "rol"
        ]
        
        faltantes = []
        for c in campos_obligatorios:
            if c not in body or not body[c]:
                faltantes.append(c)
        
        if faltantes:
            raise ValidationException(f"Faltan campos obligatorios: {', '.join(faltantes)}")
        
        
        body["nombre"] = body["nombre"].strip()
        body["apellido"] = body["apellido"].strip()
        email = body["email"].strip()
        
        if len(body["nombre"]) < 2:
            raise ValidationException("El nombre debe tener al menos 2 caracteres")
        
        if len(body["apellido"]) < 2:
            raise ValidationException("El apellido debe tener al menos 2 caracteres")
        
        if "@" not in email or "." not in email:
            raise ValidationException("El email no tiene un formato válido")
        body["email"] = email.lower()
        
        dni_str = str(body["dni"])
        if not dni_str.isdigit() or not (len(dni_str) == 8):
            raise ValidationException("El DNI debe ser un número de 8 dígitos")
        
        telefono = body.get("telefono")
        if telefono:
            tel_str = str(telefono)
            if not tel_str.isdigit() or len(tel_str) < 7:
                raise ValidationException("El teléfono no es válido")
            
        if self.empleado_repo.find_by_dni(body["dni"]):
            raise BusinessException("Ya existe un empleado con ese DNI")

        if self.empleado_repo.find_by_email(body["email"]):
            raise BusinessException("Ya existe un empleado con ese email")

        empleado = Empleado(
            nombre=body["nombre"],
            apellido=body["apellido"],
            dni=body["dni"],
            direccion=body.get("direccion"),
            telefono=body.get("telefono"),
            email=body["email"],
            rol=body["rol"]
        )
        
        self.empleado_repo.add(empleado)
        return empleado_to_response_dto(empleado)
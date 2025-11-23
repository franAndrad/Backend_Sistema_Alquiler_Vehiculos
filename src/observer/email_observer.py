from .observer import Observer
from ..repository.empleado_repository import EmpleadoRepository


class EmailClienteObserver(Observer):
    
    def actualizar(self, reserva) -> None:
        cliente = reserva.cliente
        vehiculo = reserva.vehiculo
        fecha_inicio = reserva.fecha_inicio.strftime("%d/%m/%Y")
        fecha_fin = reserva.fecha_fin.strftime("%d/%m/%Y")
        
        mensaje = (
            f"📧 Email enviado a {cliente.email} ({cliente.nombre} {cliente.apellido}):\n"
            f"   Asunto: Confirmación de Reserva\n"
            f"   Tu reserva del vehículo {vehiculo.modelo.marca.nombre} {vehiculo.modelo.descripcion} "
            f"(Patente: {vehiculo.patente}) para el día {fecha_inicio} hasta {fecha_fin} "
            f"se realizó con éxito. ¡Esperamos verte pronto!"
        )
        
        print(mensaje)


class EmailEmpleadosObserver(Observer):

    def __init__(self):
        self.empleado_repo = EmpleadoRepository()
    
    def actualizar(self, reserva) -> None:
        empleados = self.empleado_repo.list_all()
        
        if not empleados:
            print("⚠️  No hay empleados registrados para notificar")
            return
        
        cliente = reserva.cliente
        vehiculo = reserva.vehiculo
        fecha_inicio = reserva.fecha_inicio.strftime("%d/%m/%Y")
        fecha_fin = reserva.fecha_fin.strftime("%d/%m/%Y")
        
        print(f"\n📧 Enviando notificaciones a {len(empleados)} empleado(s):")
        
        for empleado in empleados:
            mensaje = (
                f"   → Email enviado a {empleado.email} ({empleado.nombre} {empleado.apellido} - {empleado.rol.value}):\n"
                f"      Asunto: Nueva Reserva Registrada\n"
                f"      Se registró una reserva nueva para el vehículo {vehiculo.modelo.marca.nombre} "
                f"{vehiculo.modelo.descripcion} (Patente: {vehiculo.patente}), "
                f"desde {fecha_inicio} hasta {fecha_fin}, "
                f"por el cliente {cliente.nombre} {cliente.apellido} (DNI: {cliente.dni})."
            )
            print(mensaje)

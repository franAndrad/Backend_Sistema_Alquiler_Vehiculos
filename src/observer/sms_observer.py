from .observer import Observer


class SMSObserver(Observer):

    def actualizar(self, reserva) -> None:
        cliente = reserva.cliente
        vehiculo = reserva.vehiculo
        fecha_inicio = reserva.fecha_inicio.strftime("%d/%m/%Y")
        fecha_fin = reserva.fecha_fin.strftime("%d/%m/%Y")
        
        mensaje = (
            f"📱 SMS enviado a {cliente.telefono} ({cliente.nombre} {cliente.apellido}):\n"
            f"   Tu reserva del vehículo {vehiculo.modelo.marca.nombre} {vehiculo.modelo.descripcion} "
            f"(Patente: {vehiculo.patente}) para el período del {fecha_inicio} al {fecha_fin} "
            f"se realizó con éxito. ¡Gracias por confiar en nosotros!"
        )
        
        print(mensaje)

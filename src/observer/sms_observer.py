from .observer import Observer


class SMSObserver(Observer):

    def actualizar(self, entidad) -> None:
        cliente = entidad.cliente
        vehiculo = entidad.vehiculo

        fecha_inicio_str = entidad.fecha_inicio.strftime("%d/%m/%Y")
        fecha_fin_str = (
            entidad.fecha_fin.strftime("%d/%m/%Y")
            if getattr(entidad, "fecha_fin", None) is not None
            else None
        )

        nombre_clase = entidad.__class__.__name__.lower()

        if "reserva" in nombre_clase:
            tipo = "reserva"
            texto_periodo = f"para el período del {fecha_inicio_str} al {fecha_fin_str}"
        elif "alquiler" in nombre_clase:
            tipo = "alquiler"
            if fecha_fin_str:
                texto_periodo = f"para el período del {fecha_inicio_str} al {fecha_fin_str}"
            else:
                texto_periodo = (
                    f"iniciado el {fecha_inicio_str}. "
                    f"La fecha de devolución se registrará al finalizar el alquiler."
                )
        else:
            tipo = "operación"
            if fecha_fin_str:
                texto_periodo = f"para el período del {fecha_inicio_str} al {fecha_fin_str}"
            else:
                texto_periodo = f"iniciada el {fecha_inicio_str}"

        mensaje = (
            f"📱 SMS enviado a {cliente.telefono} ({cliente.nombre} {cliente.apellido}):\n"
            f"   Tu {tipo} del vehículo {vehiculo.modelo.marca.nombre} {vehiculo.modelo.descripcion} "
            f"(Patente: {vehiculo.patente}) {texto_periodo} "
            f"se realizó con éxito. ¡Gracias por confiar en nosotros!"
        )

        print(mensaje)

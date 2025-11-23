from src.extensions.mail_ext import mail
from .observer import Observer
from flask_mail import Message


class EmailClienteObserver(Observer):

    def actualizar(self, entidad) -> None:
        """
        `entidad` puede ser:
        - una Reserva
        - un Alquiler
        Siempre que tenga: cliente, vehiculo, fecha_inicio, fecha_fin
        """

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
            subject = "Confirmación de Reserva"
            texto_periodo = f"para el período del {fecha_inicio_str} al {fecha_fin_str}"
        elif "alquiler" in nombre_clase:
            tipo = "alquiler"
            subject = "Confirmación de Alquiler"
            
            if fecha_fin_str:
                texto_periodo = (
                    f"para el período del {fecha_inicio_str} al {fecha_fin_str}"
                )
            else:
                # Alquiler recién iniciado, sin fecha de devolución aún
                texto_periodo = (
                    f"iniciado el {fecha_inicio_str}. "
                    f"La fecha de devolución se registrará al finalizar el alquiler."
                )
        else:
            # fallback genérico
            tipo = "operación"
            subject = "Confirmación de Operación"

        body = (
            f"Hola {cliente.nombre} {cliente.apellido},\n\n"
            f"Tu {tipo} del vehículo {vehiculo.modelo.marca.nombre} "
            f"{vehiculo.modelo.descripcion} (Patente: {vehiculo.patente}) "
            f"{texto_periodo} "
            f"se registró con éxito.\n\n"
            f"¡Gracias por confiar en nosotros!"
        )

        msg = Message(
            subject=subject,
            recipients=[cliente.email],
        )
        msg.body = body

        mail.send(msg)
        
        print(body)

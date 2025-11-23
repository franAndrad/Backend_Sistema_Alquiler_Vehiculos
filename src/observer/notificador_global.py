from .sujeto import Sujeto
from .sms_observer import SMSObserver
from .email_observer import EmailClienteObserver

# Esto crea (o obtiene) la única instancia de Sujeto
notificador_movimientos = Sujeto()

# Registramos los observers una sola vez
notificador_movimientos.suscribir(SMSObserver())
notificador_movimientos.suscribir(EmailClienteObserver())

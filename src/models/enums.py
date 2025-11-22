import enum

class EstadoVehiculo(enum.Enum):
    RESERVADO = "RESERVADO"
    DISPONIBLE = "DISPONIBLE"
    ALQUILADO = "ALQUILADO"


class EstadoAlquiler(enum.Enum):
    ACTIVO = "ACTIVO"
    FINALIZADO = "FINALIZADO"


class EstadoReserva(enum.Enum):
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    FINALIZADA = "FINALIZADA"
    EXPIRADA = "EXPIRADA"


class RolEmpleado(enum.Enum):
    ADMIN = "ADMIN"
    ATENCION = "ATENCION"


class TipoMantenimiento(enum.Enum):
    PREVENTIVO = "PREVENTIVO"
    CORRECTIVO = "CORRECTIVO"


class TipoVehiculo(enum.Enum):
    SEDAN = "SEDAN"
    SUV = "SUV"
    CAMIONETA = "CAMIONETA"
    HATCHBACK = "HATCHBACK"
    CONVERTIBLE = "CONVERTIBLE"

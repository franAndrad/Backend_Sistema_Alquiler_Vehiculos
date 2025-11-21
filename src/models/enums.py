import enum

class EstadoVehiculo(enum.Enum):
    DISPONIBLE = "DISPONIBLE"
    ALQUILADO = "ALQUILADO"


class EstadoAlquiler(enum.Enum):
    ACTIVO = "ACTIVO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"


class EstadoReserva(enum.Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


class RolEmpleado(enum.Enum):
    ADMIN = "ADMIN"
    VENDEDOR = "VENDEDOR"
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

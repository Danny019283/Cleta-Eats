from enum import Enum

# Alias de tipo: representa una contraseña ya "hasheada" (cadena de texto)
Hash = str


class EstadoDeCuenta(Enum):
    """Estado de la cuenta de un Usuario (Cliente o Repartidor)."""
    ACTIVO = "ACTIVO"
    DESACTIVADO = "DESACTIVADO"


class EstadoDelPedido(Enum):
    """Estado en el que se encuentra un Pedido durante su ciclo de vida."""
    EN_PREPARACION = "EN_PREPARACION"
    EN_CAMINO = "EN_CAMINO"
    ENTREGADO = "ENTREGADO"
    SUSPENDIDO = "SUSPENDIDO"
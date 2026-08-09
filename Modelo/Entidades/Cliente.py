from __future__ import annotations

from typing import List

from Enums import EstadoDeCuenta, Hash
from Usuario import Usuario


# EJEMPLO HERENCIA
# Cliente hereda de Usuario
class Cliente(Usuario):
    def __init__(
        self,
        p_cedula: int,
        p_contrasenia: Hash,
        p_nombre: str,
        p_correo: str,
        p_telefono: int,
        p_num_de_tarjeta: int,
        p_estado: EstadoDeCuenta,
        p_direccion: str,
    ):
        super().__init__(
            p_cedula,
            p_contrasenia,
            p_nombre,
            p_correo,
            p_telefono,
            p_num_de_tarjeta,
            p_estado,
        )
        self.__direccion = p_direccion
        # Historial de pedidos realizados por el cliente (para reportes:
        # "Listado de Pedidos por cada cliente" y "cliente con mayor número de pedidos")
        self.__historial_pedidos: List[Pedido] = []

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, p_direccion):
        self.__direccion = p_direccion

    @property
    def historial_pedidos(self):
        return self.__historial_pedidos

    # ── Lógica de entidad ──────────────────────────────────────────────
    # Comportamientos propios de la entidad, relacionados directamente
    # con su estado, atributos e invariantes.

    def puede_realizar_pedido(self) -> bool:
        """
        Lógica de entidad: verifica si el cliente puede realizar un pedido
        según su propio estado de cuenta. La entidad es responsable de
        mantener su propia consistencia.
        """
        return self.estado == EstadoDeCuenta.ACTIVO

    def agregar_pedido_al_historial(self, p_pedido: Pedido):
        """
        Lógica de entidad: modifica el estado interno del cliente
        agregando un pedido a su historial.
        """
        self.__historial_pedidos.append(p_pedido)

    # EJEMPLO POLIMORFISMO
    # Se redefine lo que se declara en la clase padre (Usuario)
    def __str__(self):
        return f"Cliente: {super().__str__()}, dirección: {self.__direccion}"
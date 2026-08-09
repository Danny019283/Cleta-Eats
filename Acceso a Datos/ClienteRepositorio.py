from __future__ import annotations

from typing import List, Optional

from Cliente import Cliente
from Excepciones import ClienteDuplicadoError


class ClienteRepositorio:
    """
    Repositorio para la entidad Cliente.
    Gestiona el almacenamiento en memoria y las operaciones CRUD.
    """

    def __init__(self):
        self.__clientes: List[Cliente] = []

    # ── CRUD ──────────────────────────────────────────────────────────

    def crear(self, p_cliente: Cliente) -> None:
        """Agrega un nuevo cliente al repositorio."""
        if self.obtener_por_cedula(p_cliente.cedula) is not None:
            raise ClienteDuplicadoError(
                f"Ya existe un cliente con la cédula {p_cliente.cedula}"
            )
        self.__clientes.append(p_cliente)

    def obtener_por_cedula(self, p_cedula: int) -> Optional[Cliente]:
        """Busca y retorna un cliente por su cédula, o None si no existe."""
        for cliente in self.__clientes:
            if cliente.cedula == p_cedula:
                return cliente
        return None

    def obtener_todos(self) -> List[Cliente]:
        """Retorna la lista completa de clientes registrados."""
        return list(self.__clientes)

    def actualizar(self, p_cliente: Cliente) -> bool:
        """
        Actualiza un cliente existente (lo reemplaza por cédula).
        Retorna True si se encontró y actualizó, False en caso contrario.
        """
        for i, cliente in enumerate(self.__clientes):
            if cliente.cedula == p_cliente.cedula:
                self.__clientes[i] = p_cliente
                return True
        return False

    def eliminar(self, p_cedula: int) -> bool:
        """
        Elimina un cliente por su cédula.
        Retorna True si se encontró y eliminó, False en caso contrario.
        """
        for i, cliente in enumerate(self.__clientes):
            if cliente.cedula == p_cedula:
                self.__clientes.pop(i)
                return True
        return False

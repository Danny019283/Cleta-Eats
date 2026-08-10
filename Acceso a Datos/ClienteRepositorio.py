from __future__ import annotations

from typing import List, Optional

import pickle
from Cliente import Cliente
from Excepciones import ClienteDuplicadoError
from Database import DatabaseConnection


class ClienteRepositorio:
    """
    Repositorio para la entidad Cliente.
    Gestiona el almacenamiento en memoria y las operaciones CRUD.
    """

    def __init__(self):
        self.db = DatabaseConnection()
        self.__clientes: List[Cliente] = self._cargar()

    def _cargar(self) -> List[Cliente]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT data FROM store WHERE key = 'clientes'")
            row = cursor.fetchone()
            if row:
                return pickle.loads(row[0])
            return []

    def _guardar(self):
        """Guarda el estado actual en la base de datos."""
        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO store (key, data) VALUES (?, ?)",
                ('clientes', pickle.dumps(self.__clientes))
            )

    # ── CRUD ──────────────────────────────────────────────────────────

    def crear(self, p_cliente: Cliente) -> None:
        """Agrega un nuevo cliente al repositorio."""
        if self.obtener_por_cedula(p_cliente.cedula) is not None:
            raise ClienteDuplicadoError(
                f"Ya existe un cliente con la cédula {p_cliente.cedula}"
            )
        self.__clientes.append(p_cliente)
        self._guardar()

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
                self._guardar()
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

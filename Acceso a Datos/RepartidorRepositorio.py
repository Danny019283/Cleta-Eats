from __future__ import annotations

from typing import List, Optional

from Repartidor import Repartidor
from Excepciones import RepartidorDuplicadoError, EntidadNoEncontradaError


class RepartidorRepositorio:
    """
    Repositorio para la entidad Repartidor.
    Gestiona el almacenamiento en memoria y las operaciones CRUD.
    """

    def __init__(self):
        self.__repartidores: List[Repartidor] = []

    # ── CRUD ──────────────────────────────────────────────────────────

    def crear(self, p_repartidor: Repartidor) -> None:
        """Agrega un nuevo repartidor al repositorio."""
        if self.obtener_por_cedula(p_repartidor.cedula) is not None:
            raise RepartidorDuplicadoError(
                f"Ya existe un repartidor con la cédula {p_repartidor.cedula}"
            )
        self.__repartidores.append(p_repartidor)

    def obtener_por_cedula(self, p_cedula: int) -> Optional[Repartidor]:
        """Busca y retorna un repartidor por su cédula, o None si no existe."""
        for repartidor in self.__repartidores:
            if repartidor.cedula == p_cedula:
                return repartidor
        return None

    def obtener_todos(self) -> List[Repartidor]:
        """Retorna la lista completa de repartidores registrados."""
        return list(self.__repartidores)

    def actualizar(self, p_repartidor: Repartidor) -> bool:
        """
        Actualiza un repartidor existente (lo reemplaza por cédula).
        Retorna True si se encontró y actualizó, False en caso contrario.
        """
        for i, repartidor in enumerate(self.__repartidores):
            if repartidor.cedula == p_repartidor.cedula:
                self.__repartidores[i] = p_repartidor
                return True
        return False

    def eliminar(self, p_cedula: int) -> bool:
        """
        Elimina un repartidor por su cédula.
        Retorna True si se encontró y eliminó, False en caso contrario.
        """
        for i, repartidor in enumerate(self.__repartidores):
            if repartidor.cedula == p_cedula:
                self.__repartidores.pop(i)
                return True
        return False

    # ── Métodos extra ─────────────────────────────────────────────────

    def obtener_quejas_por_repartidor(self, p_cedula: int) -> List[str]:
        """
        Retorna la lista de quejas registradas para un repartidor
        identificado por su cédula.
        Lanza ValueError si el repartidor no existe en el repositorio.
        """
        repartidor = self.obtener_por_cedula(p_cedula)
        if repartidor is None:
            raise EntidadNoEncontradaError(
                f"No existe un repartidor con la cédula {p_cedula}"
            )
        return list(repartidor.quejas)

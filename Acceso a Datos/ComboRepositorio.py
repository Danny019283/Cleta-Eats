from __future__ import annotations

from typing import List, Optional

from Combo import Combo
from Excepciones import ComboDuplicadoError


class ComboRepositorio:
    """
    Repositorio para la entidad Combo.
    Gestiona el almacenamiento en memoria y las operaciones CRUD.
    """

    def __init__(self):
        self.__combos: List[Combo] = []

    # ── CRUD ──────────────────────────────────────────────────────────

    def crear(self, p_combo: Combo) -> None:
        """Agrega un nuevo combo al repositorio."""
        if self.obtener_por_numero(p_combo.num_de_combo) is not None:
            raise ComboDuplicadoError(
                f"Ya existe un combo con el número {p_combo.num_de_combo}"
            )
        self.__combos.append(p_combo)

    def obtener_por_numero(self, p_num_de_combo: int) -> Optional[Combo]:
        """Busca y retorna un combo por su número, o None si no existe."""
        for combo in self.__combos:
            if combo.num_de_combo == p_num_de_combo:
                return combo
        return None

    def obtener_todos(self) -> List[Combo]:
        """Retorna la lista completa de combos registrados."""
        return list(self.__combos)

    def actualizar(self, p_combo: Combo) -> bool:
        """
        Actualiza un combo existente (lo reemplaza por número de combo).
        Retorna True si se encontró y actualizó, False en caso contrario.
        """
        for i, combo in enumerate(self.__combos):
            if combo.num_de_combo == p_combo.num_de_combo:
                self.__combos[i] = p_combo
                return True
        return False

    def eliminar(self, p_num_de_combo: int) -> bool:
        """
        Elimina un combo por su número.
        Retorna True si se encontró y eliminó, False en caso contrario.
        """
        for i, combo in enumerate(self.__combos):
            if combo.num_de_combo == p_num_de_combo:
                self.__combos.pop(i)
                return True
        return False

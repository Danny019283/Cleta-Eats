from __future__ import annotations

from typing import List, Optional

import pickle
from Restaurante import Restaurante
from Excepciones import RestauranteDuplicadoError
from Database import DatabaseConnection


class RestauranteRepositorio:
    """
    Repositorio para la entidad Restaurante.
    Gestiona el almacenamiento en memoria y las operaciones CRUD.
    """

    def __init__(self):
        self.db = DatabaseConnection()
        self.__restaurantes: List[Restaurante] = self._cargar()

    def _cargar(self) -> List[Restaurante]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT data FROM store WHERE key = 'restaurantes'")
            row = cursor.fetchone()
            if row:
                return pickle.loads(row[0])
            return []

    def _guardar(self):
        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO store (key, data) VALUES (?, ?)",
                ('restaurantes', pickle.dumps(self.__restaurantes))
            )

    # ── CRUD ──────────────────────────────────────────────────────────

    def crear(self, p_restaurante: Restaurante) -> None:
        """Agrega un nuevo restaurante al repositorio."""
        if self.obtener_por_cedula_juridica(p_restaurante.cedula_juridica) is not None:
            raise RestauranteDuplicadoError(
                f"Ya existe un restaurante con la cédula jurídica "
                f"{p_restaurante.cedula_juridica}"
            )
        self.__restaurantes.append(p_restaurante)
        self._guardar()

    def obtener_por_cedula_juridica(
        self, p_cedula_juridica: int
    ) -> Optional[Restaurante]:
        """Busca y retorna un restaurante por su cédula jurídica, o None si no existe."""
        for restaurante in self.__restaurantes:
            if restaurante.cedula_juridica == p_cedula_juridica:
                return restaurante
        return None

    def obtener_todos(self) -> List[Restaurante]:
        """Retorna la lista completa de restaurantes registrados."""
        return list(self.__restaurantes)

    def actualizar(self, p_restaurante: Restaurante) -> bool:
        """
        Actualiza un restaurante existente (lo reemplaza por cédula jurídica).
        Retorna True si se encontró y actualizó, False en caso contrario.
        """
        for i, restaurante in enumerate(self.__restaurantes):
            if restaurante.cedula_juridica == p_restaurante.cedula_juridica:
                self.__restaurantes[i] = p_restaurante
                self._guardar()
                return True
        return False

    def eliminar(self, p_cedula_juridica: int) -> bool:
        """
        Elimina un restaurante por su cédula jurídica.
        Retorna True si se encontró y eliminó, False en caso contrario.
        """
        for i, restaurante in enumerate(self.__restaurantes):
            if restaurante.cedula_juridica == p_cedula_juridica:
                self.__restaurantes.pop(i)
                self._guardar()
                return True
        return False

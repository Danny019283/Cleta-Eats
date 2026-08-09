from __future__ import annotations

from typing import List, Optional

from Factura import Factura


class FacturaRepositorio:
    """
    Repositorio para la entidad Factura.
    Gestiona el almacenamiento en memoria y las operaciones CRUD.
    Nota: Factura no posee un identificador explícito propio, por lo
    que se usa su índice en la lista interna para las operaciones.
    En un escenario real se le asignaría un id único.
    """

    def __init__(self):
        self.__facturas: List[Factura] = []
        self.__siguiente_id: int = 1
        # Mapa interno de id -> factura para acceso rápido
        self.__mapa_facturas: dict[int, Factura] = {}

    # ── CRUD ──────────────────────────────────────────────────────────

    def crear(self, p_factura: Factura) -> int:
        """
        Agrega una nueva factura al repositorio.
        Retorna el id asignado a la factura.
        """
        id_asignado = self.__siguiente_id
        self.__facturas.append(p_factura)
        self.__mapa_facturas[id_asignado] = p_factura
        self.__siguiente_id += 1
        return id_asignado

    def obtener_por_id(self, p_id: int) -> Optional[Factura]:
        """Busca y retorna una factura por su id, o None si no existe."""
        return self.__mapa_facturas.get(p_id)

    def obtener_todos(self) -> List[Factura]:
        """Retorna la lista completa de facturas registradas."""
        return list(self.__facturas)

    def actualizar(self, p_id: int, p_factura: Factura) -> bool:
        """
        Actualiza una factura existente (la reemplaza por id).
        Retorna True si se encontró y actualizó, False en caso contrario.
        """
        if p_id not in self.__mapa_facturas:
            return False

        factura_anterior = self.__mapa_facturas[p_id]
        indice = self.__facturas.index(factura_anterior)
        self.__facturas[indice] = p_factura
        self.__mapa_facturas[p_id] = p_factura
        return True

    def eliminar(self, p_id: int) -> bool:
        """
        Elimina una factura por su id.
        Retorna True si se encontró y eliminó, False en caso contrario.
        """
        if p_id not in self.__mapa_facturas:
            return False

        factura = self.__mapa_facturas.pop(p_id)
        self.__facturas.remove(factura)
        return True

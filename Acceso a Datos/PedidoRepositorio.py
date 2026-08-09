from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import List, Optional

from Cliente import Cliente
from Pedido import Pedido
from Restaurante import Restaurante
from Excepciones import PedidoDuplicadoError


class PedidoRepositorio:
    """
    Repositorio para la entidad Pedido.
    Gestiona el almacenamiento en memoria, operaciones CRUD y
    consultas de reportes solicitadas.
    """

    def __init__(self):
        self.__pedidos: List[Pedido] = []

    # ── CRUD ──────────────────────────────────────────────────────────

    def crear(self, p_pedido: Pedido) -> None:
        """Agrega un nuevo pedido al repositorio."""
        if self.obtener_por_id(p_pedido.id) is not None:
            raise PedidoDuplicadoError(
                f"Ya existe un pedido con el id {p_pedido.id}"
            )
        self.__pedidos.append(p_pedido)

    def obtener_por_id(self, p_id: int) -> Optional[Pedido]:
        """Busca y retorna un pedido por su id, o None si no existe."""
        for pedido in self.__pedidos:
            if pedido.id == p_id:
                return pedido
        return None

    def obtener_todos(self) -> List[Pedido]:
        """Retorna la lista completa de pedidos registrados."""
        return list(self.__pedidos)

    def actualizar(self, p_pedido: Pedido) -> bool:
        """
        Actualiza un pedido existente (lo reemplaza por id).
        Retorna True si se encontró y actualizó, False en caso contrario.
        """
        for i, pedido in enumerate(self.__pedidos):
            if pedido.id == p_pedido.id:
                self.__pedidos[i] = p_pedido
                return True
        return False

    def eliminar(self, p_id: int) -> bool:
        """
        Elimina un pedido por su id.
        Retorna True si se encontró y eliminó, False en caso contrario.
        """
        for i, pedido in enumerate(self.__pedidos):
            if pedido.id == p_id:
                self.__pedidos.pop(i)
                return True
        return False

    # ── Métodos extra (reportes) ──────────────────────────────────────

    def rest_con_mas_pedidos(self) -> Optional[Restaurante]:
        """
        Retorna el restaurante con mayor cantidad de pedidos registrados.
        Retorna None si no hay pedidos en el repositorio.
        """
        if not self.__pedidos:
            return None

        conteo: Counter = Counter()
        restaurante_map: dict[int, Restaurante] = {}

        for pedido in self.__pedidos:
            cedula = pedido.restaurante.cedula_juridica
            conteo[cedula] += 1
            restaurante_map[cedula] = pedido.restaurante

        cedula_max = conteo.most_common(1)[0][0]
        return restaurante_map[cedula_max]

    def rest_con_menos_pedidos(self) -> Optional[Restaurante]:
        """
        Retorna el restaurante con menor cantidad de pedidos registrados.
        Retorna None si no hay pedidos en el repositorio.
        """
        if not self.__pedidos:
            return None

        conteo: Counter = Counter()
        restaurante_map: dict[int, Restaurante] = {}

        for pedido in self.__pedidos:
            cedula = pedido.restaurante.cedula_juridica
            conteo[cedula] += 1
            restaurante_map[cedula] = pedido.restaurante

        cedula_min = conteo.most_common()[-1][0]
        return restaurante_map[cedula_min]

    def monto_total_vendido_por_rest(
        self, p_cedula_juridica: int
    ) -> float:
        """
        Retorna el monto total vendido por un restaurante específico
        (identificado por su cédula jurídica), sumando los totales de
        las facturas de sus pedidos.
        """
        monto = 0.0
        for pedido in self.__pedidos:
            if pedido.restaurante.cedula_juridica == p_cedula_juridica:
                monto += pedido.factura.total
        return monto

    def monto_total_vendido(self) -> float:
        """
        Retorna el monto total vendido considerando todos los pedidos
        de todos los restaurantes.
        """
        return sum(pedido.factura.total for pedido in self.__pedidos)

    def pedidos_por_cliente(self, p_cedula_cliente: int) -> List[Pedido]:
        """
        Retorna la lista de pedidos realizados por un cliente específico,
        identificado por su cédula.
        """
        return [
            pedido
            for pedido in self.__pedidos
            if pedido.cliente.cedula == p_cedula_cliente
        ]

    def cliente_con_mas_pedidos(self) -> Optional[Cliente]:
        """
        Retorna el cliente con mayor cantidad de pedidos registrados.
        Retorna None si no hay pedidos en el repositorio.
        """
        if not self.__pedidos:
            return None

        conteo: Counter = Counter()
        cliente_map: dict[int, Cliente] = {}

        for pedido in self.__pedidos:
            cedula = pedido.cliente.cedula
            conteo[cedula] += 1
            cliente_map[cedula] = pedido.cliente

        cedula_max = conteo.most_common(1)[0][0]
        return cliente_map[cedula_max]

    def obtener_hora_pico(self) -> Optional[datetime]:
        """
        Retorna la hora (datetime con hora redondeada) en la que se
        concentran más pedidos. Analiza la hora del pedido y retorna
        la hora con mayor frecuencia.
        Retorna None si no hay pedidos en el repositorio.
        """
        if not self.__pedidos:
            return None

        conteo: Counter = Counter()
        hora_map: dict[int, datetime] = {}

        for pedido in self.__pedidos:
            hora = pedido.hora_pedido.hour
            conteo[hora] += 1
            # Guardamos un datetime representativo de esa hora
            if hora not in hora_map:
                hora_map[hora] = pedido.hora_pedido.replace(
                    minute=0, second=0, microsecond=0
                )

        hora_pico = conteo.most_common(1)[0][0]
        return hora_map[hora_pico]

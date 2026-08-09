from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from Cliente import Cliente
from Enums import EstadoDelPedido
from Factura import Factura
from Pedido import Pedido
from PedidoRepositorio import PedidoRepositorio
from Repartidor import Repartidor
from Restaurante import Restaurante
from Excepciones import (
    RepartidorNoDisponibleError,
    SinRepartidorDisponibleError,
    RecursoNoDisponibleError
)


class PedidoServicio:
    """
    Lógica de negocio: coordina el comportamiento del sistema
    relacionado con pedidos, involucrando múltiples entidades
    (Pedido, Repartidor, Factura, Restaurante).

    Recibe el repositorio de pedidos por constructor (inyección de
    dependencias) para acceder y persistir datos.
    """

    def __init__(self, p_pedido_repositorio: PedidoRepositorio):
        self.__pedido_repo = p_pedido_repositorio

    def asignar_repartidor(self, p_pedido: Pedido, p_repartidor: Repartidor) -> bool:
        """
        Lógica de negocio: asigna un repartidor a un pedido.
        Coordina la validación cruzada entre Pedido y Repartidor
        (disponibilidad, amonestaciones) y actualiza el estado de
        ambas entidades.
        """
        if not p_repartidor.esta_disponible_para_pedido():
            raise RepartidorNoDisponibleError(
                f"El repartidor {p_repartidor.nombre} no está disponible "
                f"(ocupado o con demasiadas amonestaciones)."
            )

        p_pedido.asignar_repartidor_interno(p_repartidor)
        p_repartidor.actualizar_disponibilidad(False)
        p_pedido.cambiar_estado(EstadoDelPedido.EN_PREPARACION)
        return True

    def asignar_primer_repartidor_disponible(
        self, p_repartidores: List[Repartidor],
    ) -> Optional[Repartidor]:
        """
        Lógica de negocio: recorre la lista de repartidores y retorna
        el primero disponible. Coordina la búsqueda entre múltiples
        instancias de Repartidor.
        """
        for repartidor in p_repartidores:
            if repartidor.esta_disponible_para_pedido():
                return repartidor
        raise SinRepartidorDisponibleError("No hay repartidores disponibles en este momento.")

    def generar_factura(self, p_pedido: Pedido) -> Factura:
        """
        Lógica de negocio: coordina la generación de la factura del
        pedido, orquestando los cálculos entre Pedido y Factura
        (subtotal, transporte según distancia y tipo de día, IVA, total).
        """
        factura = p_pedido.factura
        factura.calcular_subtotal()
        factura.calcular_costo_del_transporte(
            p_pedido.distancia_km, p_pedido.es_feriado
        )
        factura.calcular_iva()
        factura.calcular_total()
        return factura

    def entregar_pedido(self, p_pedido: Pedido):
        """
        Lógica de negocio: marca el pedido como entregado y libera
        al repartidor. Coordina entre Pedido y Repartidor.
        """
        p_pedido.cambiar_estado(EstadoDelPedido.ENTREGADO)
        if p_pedido.tiene_repartidor():
            p_pedido.repartidor.actualizar_disponibilidad(True)

    # ── Métodos de reporte (delegan al repositorio) ───────────────────

    def rest_con_mas_pedidos(self) -> Optional[Restaurante]:
        """
        Reporte: retorna el restaurante con mayor cantidad de pedidos.
        Delega al PedidoRepositorio.
        """
        restaurante = self.__pedido_repo.rest_con_mas_pedidos()
        if restaurante is None:
            raise RecursoNoDisponibleError("No hay pedidos para calcular el restaurante con más pedidos.")
        return restaurante

    def rest_con_menos_pedidos(self) -> Optional[Restaurante]:
        """
        Reporte: retorna el restaurante con menor cantidad de pedidos.
        Delega al PedidoRepositorio.
        """
        restaurante = self.__pedido_repo.rest_con_menos_pedidos()
        if restaurante is None:
            raise RecursoNoDisponibleError("No hay pedidos para calcular el restaurante con menos pedidos.")
        return restaurante

    def monto_total_vendido_por_rest(self, p_cedula_juridica: int) -> float:
        """
        Reporte: retorna el monto total vendido por un restaurante
        específico (identificado por cédula jurídica).
        Delega al PedidoRepositorio.
        """
        return self.__pedido_repo.monto_total_vendido_por_rest(p_cedula_juridica)

    def monto_total_vendido(self) -> float:
        """
        Reporte: retorna el monto total vendido considerando todos
        los pedidos de todos los restaurantes.
        Delega al PedidoRepositorio.
        """
        return self.__pedido_repo.monto_total_vendido()

    def pedidos_por_cliente(self, p_cedula_cliente: int) -> List[Pedido]:
        """
        Reporte: retorna la lista de pedidos de un cliente específico.
        Delega al PedidoRepositorio.
        """
        return self.__pedido_repo.pedidos_por_cliente(p_cedula_cliente)

    def cliente_con_mas_pedidos(self) -> Optional[Cliente]:
        """
        Reporte: retorna el cliente con mayor cantidad de pedidos.
        Delega al PedidoRepositorio.
        """
        cliente = self.__pedido_repo.cliente_con_mas_pedidos()
        if cliente is None:
            raise RecursoNoDisponibleError("No hay pedidos para calcular el cliente con más pedidos.")
        return cliente

    def obtener_hora_pico(self) -> Optional[datetime]:
        """
        Reporte: retorna la hora en la que se concentran más pedidos.
        Delega al PedidoRepositorio.
        """
        hora = self.__pedido_repo.obtener_hora_pico()
        if hora is None:
            raise RecursoNoDisponibleError("No hay pedidos para calcular la hora pico.")
        return hora

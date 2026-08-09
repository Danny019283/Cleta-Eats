from __future__ import annotations

from datetime import datetime
from typing import Optional

from Cliente import Cliente
from Enums import EstadoDelPedido
from Factura import Factura
from Repartidor import Repartidor
from Restaurante import Restaurante
from Excepciones import (
    FormatoInvalidoError,
    TransicionEstadoInvalidaError,
    PedidoSinRepartidorError,
)


class Pedido:
    def __init__(
        self,
        p_id: int,
        p_cliente: Cliente,
        p_repartidor: Optional[Repartidor],
        p_restaurante: Restaurante,
        p_factura: Factura,
        p_estado: EstadoDelPedido,
        p_distancia_km: float = 0.0,
        p_es_feriado: bool = False,
    ):
        self.__id = p_id
        self.__cliente = p_cliente
        self.__repartidor = p_repartidor
        self.__restaurante = p_restaurante
        self.__factura = p_factura
        self.__estado = None
        self.estado = p_estado
        self.__distancia_km = p_distancia_km
        self.__es_feriado = p_es_feriado
        # Trazabilidad del pedido
        self.__hora_pedido = datetime.now()
        self.__hora_entrega: Optional[datetime] = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, p_id):
        self.__id = p_id

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, p_cliente):
        self.__cliente = p_cliente

    @property
    def repartidor(self):
        return self.__repartidor

    @repartidor.setter
    def repartidor(self, p_repartidor):
        self.__repartidor = p_repartidor

    @property
    def restaurante(self):
        return self.__restaurante

    @restaurante.setter
    def restaurante(self, p_restaurante):
        self.__restaurante = p_restaurante

    @property
    def factura(self):
        return self.__factura

    @factura.setter
    def factura(self, p_factura):
        self.__factura = p_factura

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, p_estado):
        if not isinstance(p_estado, EstadoDelPedido):
            raise FormatoInvalidoError("p_estado debe ser un valor de EstadoDelPedido")
        self.__estado = p_estado

    @property
    def distancia_km(self):
        return self.__distancia_km

    @distancia_km.setter
    def distancia_km(self, p_distancia_km):
        self.__distancia_km = p_distancia_km

    @property
    def es_feriado(self):
        return self.__es_feriado

    @property
    def hora_pedido(self):
        return self.__hora_pedido

    @property
    def hora_entrega(self):
        return self.__hora_entrega

    # ── Lógica de entidad ──────────────────────────────────────────────
    # Comportamientos propios de la entidad, relacionados directamente
    # con su estado, atributos e invariantes.

    def cambiar_estado(self, p_estado: EstadoDelPedido):
        """
        Lógica de entidad: actualiza el estado del pedido. Valida el
        invariante de tipo, transiciones válidas y registra la hora de
        entrega cuando se marca como ENTREGADO.
        """
        if not isinstance(p_estado, EstadoDelPedido):
            raise FormatoInvalidoError("p_estado debe ser un valor de EstadoDelPedido")

        if self.__estado == EstadoDelPedido.ENTREGADO:
            raise TransicionEstadoInvalidaError("No se puede cambiar el estado de un pedido entregado.")

        if p_estado in (EstadoDelPedido.EN_CAMINO, EstadoDelPedido.ENTREGADO):
            if not self.tiene_repartidor():
                raise PedidoSinRepartidorError("No se puede avanzar el pedido sin un repartidor asignado.")

        self.__estado = p_estado

        if p_estado == EstadoDelPedido.ENTREGADO:
            ahora = datetime.now()
            if ahora < self.__hora_pedido:
                raise TransicionEstadoInvalidaError("La hora de entrega no puede ser anterior a la de realización.")
            self.__hora_entrega = ahora

    def asignar_repartidor_interno(self, p_repartidor: Repartidor):
        """
        Lógica de entidad: asigna un repartidor al pedido, modificando
        su propio atributo __repartidor. No valida reglas de negocio
        cruzadas (eso lo hace el servicio).
        """
        self.__repartidor = p_repartidor

    def tiene_repartidor(self) -> bool:
        """
        Lógica de entidad: consulta si el pedido tiene un repartidor
        asignado. Opera sobre su propio atributo.
        """
        return self.__repartidor is not None

    def __str__(self):
        repartidor = "Sin asignar" if self.__repartidor is None else str(self.__repartidor)
        entrega = "Pendiente" if self.__hora_entrega is None else str(self.__hora_entrega)
        return (
            f"Pedido: id: {self.__id}, cliente: [{self.__cliente}], "
            f"repartidor: [{repartidor}], restaurante: [{self.__restaurante}], "
            f"factura: [{self.__factura}], estado: {self.__estado.value}, "
            f"hora del pedido: {self.__hora_pedido}, hora de entrega: {entrega}"
        )
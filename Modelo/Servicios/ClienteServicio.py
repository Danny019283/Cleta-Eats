from __future__ import annotations

from typing import List, Optional

from Cliente import Cliente
from ClienteRepositorio import ClienteRepositorio
from Pedido import Pedido
from PedidoRepositorio import PedidoRepositorio
from PedidoServicio import PedidoServicio
from Excepciones import (
    EntidadNoEncontradaError,
    ClienteSuspendidoError,
    RestauranteInconsistenteError,
    RecursoNoDisponibleError,
    ReglaNegocioError
)


class ClienteServicio:
    """
    Lógica de negocio: reglas y decisiones que coordinan el comportamiento
    del sistema para cumplir un objetivo del dominio, especialmente cuando
    involucran varias entidades (Cliente, Pedido, Restaurante, Factura).

    Recibe los repositorios necesarios por constructor (inyección de
    dependencias) para acceder y persistir datos.
    """

    def __init__(
        self,
        p_cliente_repositorio: ClienteRepositorio,
        p_pedido_repositorio: PedidoRepositorio,
    ):
        self.__cliente_repo = p_cliente_repositorio
        self.__pedido_repo = p_pedido_repositorio

    def realizar_pedido(self, p_cliente: Cliente, p_pedido: Pedido) -> bool:
        """
        Lógica de negocio: coordina la realización de un pedido.
        Delega la validación de estado a la propia entidad Cliente y
        se encarga de las validaciones cruzadas entre entidades y la
        orquestación del flujo (factura, restaurante, historial).
        Persiste el pedido en el repositorio al finalizar.
        """
        # Verificar si el cliente está registrado
        if self.__cliente_repo.obtener_por_cedula(p_cliente.cedula) is None:
            raise EntidadNoEncontradaError("El cliente no está registrado. Debe inscribirse primero.")

        # Validación de entidad: ¿el cliente puede hacer pedidos?
        if not p_cliente.puede_realizar_pedido():
            raise ClienteSuspendidoError("Cliente suspendido: no se le acepta la solicitud.")

        # Validación cruzada: el pedido debe pertenecer a este cliente
        if p_pedido.cliente is not p_cliente:
            raise ReglaNegocioError("El pedido no pertenece a este cliente")

        # Validación cruzada: los combos deben pertenecer al restaurante
        restaurante = p_pedido.restaurante
        for combo in p_pedido.factura.combos:
            if not restaurante.combo_pertenece_al_menu(combo.num_de_combo):
                raise RestauranteInconsistenteError(
                    "Todos los combos del pedido deben pertenecer al mismo restaurante"
                )

        # Orquestación: coordina acciones entre Pedido, Restaurante y Cliente
        pedido_servicio = PedidoServicio(self.__pedido_repo)
        pedido_servicio.generar_factura(p_pedido)
        restaurante.registrar_pedido(p_pedido.factura.total)
        p_cliente.agregar_pedido_al_historial(p_pedido)

        # Persistir el pedido en el repositorio
        self.__pedido_repo.crear(p_pedido)
        return True

    # ── Métodos de reporte (delegan al repositorio) ───────────────────

    def pedidos_por_cliente(self, p_cedula_cliente: int) -> List[Pedido]:
        """
        Reporte: retorna la lista de pedidos realizados por un cliente
        específico. Delega al PedidoRepositorio.
        """
        return self.__pedido_repo.pedidos_por_cliente(p_cedula_cliente)

    def cliente_con_mas_pedidos(self) -> Optional[Cliente]:
        """
        Reporte: retorna el cliente con mayor cantidad de pedidos.
        Delega al PedidoRepositorio.
        """
        mejor_cliente = self.__pedido_repo.cliente_con_mas_pedidos()
        if mejor_cliente is None:
            raise RecursoNoDisponibleError("No hay pedidos registrados para generar el reporte.")
        return mejor_cliente

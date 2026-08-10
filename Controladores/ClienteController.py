from __future__ import annotations

from typing import List

from DTOs import (
    CrearClienteDTO,
    CambiarEstadoClienteDTO,
    RealizarPedidoDTO,
    ResultadoDTO,
)
from ClienteServicio import ClienteServicio
from ClienteRepositorio import ClienteRepositorio
from PedidoRepositorio import PedidoRepositorio
from RestauranteRepositorio import RestauranteRepositorio
from Cliente import Cliente
from Combo import Combo
from Enums import EstadoDeCuenta, EstadoDelPedido
from Factura import Factura
from Pedido import Pedido
from Excepciones import CletaEatsError


class ClienteController:
    """
    Controlador para las operaciones relacionadas con clientes.
    Orquesta la comunicación entre la vista y ClienteServicio.
    """

    def __init__(
        self,
        p_cliente_servicio: ClienteServicio,
        p_cliente_repo: ClienteRepositorio,
        p_pedido_repo: PedidoRepositorio,
        p_restaurante_repo: RestauranteRepositorio,
    ):
        self._cliente_servicio = p_cliente_servicio
        self._cliente_repo = p_cliente_repo
        self._pedido_repo = p_pedido_repo
        self._restaurante_repo = p_restaurante_repo

    def registrar_cliente(self, datos: CrearClienteDTO) -> ResultadoDTO:
        """Registra un nuevo cliente en el sistema."""
        try:
            cliente = Cliente(
                p_cedula=datos.cedula,
                p_contrasenia=datos.contrasenia,
                p_nombre=datos.nombre,
                p_correo=datos.correo,
                p_telefono=datos.telefono,
                p_num_de_tarjeta=datos.num_de_tarjeta,
                p_estado=EstadoDeCuenta.ACTIVO,
                p_direccion=datos.direccion,
            )
            self._cliente_repo.crear(cliente)
            return ResultadoDTO(exitoso=True, mensaje="Cliente registrado exitosamente.")
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def cambiar_estado(self, datos: CambiarEstadoClienteDTO) -> ResultadoDTO:
        """Cambia el estado de un cliente (Activar/Suspender)."""
        try:
            cliente = self._cliente_repo.obtener_por_cedula(datos.cedula)
            if cliente is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un cliente con esa cédula.",
                )
            
            nuevo = EstadoDeCuenta.ACTIVO if datos.nuevo_estado == "ACTIVO" else EstadoDeCuenta.DESACTIVADO
            if cliente.estado == nuevo:
                return ResultadoDTO(exitoso=False, mensaje=f"El cliente ya se encuentra en ese estado.")
                
            cliente.cambiar_estado(nuevo)
            return ResultadoDTO(exitoso=True, mensaje=f"Cliente actualizado a estado {datos.nuevo_estado}.")
        except Exception as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def realizar_pedido(self, datos: RealizarPedidoDTO) -> ResultadoDTO:
        """Coordina la realización de un pedido por parte de un cliente."""
        try:
            cliente = self._cliente_repo.obtener_por_cedula(datos.cedula_cliente)
            if cliente is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un cliente con esa cédula.",
                )

            restaurante = self._restaurante_repo.obtener_por_cedula_juridica(
                datos.cedula_juridica_restaurante
            )
            if restaurante is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un restaurante con esa cédula jurídica.",
                )

            factura = Factura()
            for num_combo in datos.numeros_de_combos:
                combo_encontrado = next(
                    (c for c in restaurante.menu if c.num_de_combo == num_combo),
                    None,
                )
                if combo_encontrado is None:
                    return ResultadoDTO(
                        exitoso=False,
                        mensaje=f"El combo #{num_combo} no existe en el menú del restaurante.",
                    )
                factura.agregar_combo(combo_encontrado)

            siguiente_id = len(self._pedido_repo.obtener_todos()) + 1

            pedido = Pedido(
                p_id=siguiente_id,
                p_cliente=cliente,
                p_repartidor=None,
                p_restaurante=restaurante,
                p_factura=factura,
                p_estado=EstadoDelPedido.EN_PREPARACION,
                p_distancia_km=datos.distancia_km,
                p_es_feriado=datos.es_feriado,
            )

            self._cliente_servicio.realizar_pedido(cliente, pedido)
            return ResultadoDTO(
                exitoso=True,
                mensaje="Pedido realizado exitosamente.",
                datos={"id_pedido": pedido.id},
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_pedidos_por_cliente(self, p_cedula: int) -> ResultadoDTO:
        """Obtiene la lista de pedidos de un cliente."""
        try:
            pedidos = self._cliente_servicio.pedidos_por_cliente(p_cedula)
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Se encontraron {len(pedidos)} pedido(s).",
                datos=pedidos,
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_cliente_con_mas_pedidos(self) -> ResultadoDTO:
        """Obtiene el cliente con mayor número de pedidos."""
        try:
            cliente = self._cliente_servicio.cliente_con_mas_pedidos()
            return ResultadoDTO(
                exitoso=True,
                mensaje="Cliente con más pedidos encontrado.",
                datos=cliente,
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_todos_los_clientes(self) -> ResultadoDTO:
        """Obtiene la lista de todos los clientes registrados."""
        clientes = self._cliente_repo.obtener_todos()
        return ResultadoDTO(
            exitoso=True,
            mensaje=f"Se encontraron {len(clientes)} cliente(s).",
            datos=clientes,
        )

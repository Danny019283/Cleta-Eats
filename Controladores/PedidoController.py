from __future__ import annotations

from typing import List

from DTOs import (
    AsignarRepartidorDTO,
    EntregarPedidoDTO,
    ActualizarEstadoPedidoDTO,
    ResultadoDTO,
)
from PedidoServicio import PedidoServicio
from PedidoRepositorio import PedidoRepositorio
from RepartidorRepositorio import RepartidorRepositorio
from Enums import EstadoDelPedido
from Excepciones import CletaEatsError

class PedidoController:
    """
    Controlador para las operaciones relacionadas con pedidos.
    Orquesta la comunicación entre la vista y PedidoServicio.
    """

    def __init__(
        self,
        p_pedido_servicio: PedidoServicio,
        p_pedido_repo: PedidoRepositorio,
        p_repartidor_repo: RepartidorRepositorio,
    ):
        self._pedido_servicio = p_pedido_servicio
        self._pedido_repo = p_pedido_repo
        self._repartidor_repo = p_repartidor_repo

    def asignar_repartidor(self, datos: AsignarRepartidorDTO) -> ResultadoDTO:
        """Asigna un repartidor específico a un pedido."""
        try:
            pedido = self._pedido_repo.obtener_por_id(datos.id_pedido)
            if pedido is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un pedido con ese ID.",
                )

            repartidor = self._repartidor_repo.obtener_por_cedula(datos.cedula_repartidor)
            if repartidor is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un repartidor con esa cédula.",
                )

            self._pedido_servicio.asignar_repartidor(pedido, repartidor)
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Repartidor {repartidor.nombre} asignado al pedido #{pedido.id}.",
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def asignar_repartidor_automatico(self, p_id_pedido: int) -> ResultadoDTO:
        """Busca y asigna el primer repartidor disponible a un pedido."""
        try:
            pedido = self._pedido_repo.obtener_por_id(p_id_pedido)
            if pedido is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un pedido con ese ID.",
                )

            repartidores = self._repartidor_repo.obtener_todos()
            repartidor = self._pedido_servicio.asignar_primer_repartidor_disponible(
                repartidores
            )
            self._pedido_servicio.asignar_repartidor(pedido, repartidor)
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Repartidor {repartidor.nombre} asignado automáticamente al pedido #{pedido.id}.",
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def entregar_pedido(self, datos: EntregarPedidoDTO) -> ResultadoDTO:
        """Marca un pedido como entregado y libera al repartidor."""
        try:
            pedido = self._pedido_repo.obtener_por_id(datos.id_pedido)
            if pedido is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un pedido con ese ID.",
                )

            if datos.calificar:
                self._pedido_servicio.entregar_pedido(
                    pedido,
                    amabilidad=datos.amabilidad,
                    tiempo_de_respuesta=datos.tiempo_de_respuesta,
                    presentacion=datos.presentacion
                )
            else:
                self._pedido_servicio.entregar_pedido(pedido)
                
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Pedido #{pedido.id} entregado exitosamente.",
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def actualizar_estado(self, datos: ActualizarEstadoPedidoDTO) -> ResultadoDTO:
        """Actualiza el estado de un pedido (ej. EN_CAMINO o SUSPENDIDO)."""
        try:
            pedido = self._pedido_repo.obtener_por_id(datos.id_pedido)
            if pedido is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un pedido con ese ID.",
                )

            if datos.nuevo_estado == "EN_CAMINO":
                nuevo = EstadoDelPedido.EN_CAMINO
            elif datos.nuevo_estado == "SUSPENDIDO":
                nuevo = EstadoDelPedido.SUSPENDIDO
            else:
                return ResultadoDTO(exitoso=False, mensaje="Estado no válido.")

            self._pedido_servicio.actualizar_estado(pedido, nuevo)
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Estado del pedido #{pedido.id} actualizado a {datos.nuevo_estado}.",
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_restaurante_con_mas_pedidos(self) -> ResultadoDTO:
        """Obtiene el restaurante con mayor cantidad de pedidos."""
        try:
            restaurante = self._pedido_servicio.rest_con_mas_pedidos()
            return ResultadoDTO(
                exitoso=True,
                mensaje="Restaurante con más pedidos encontrado.",
                datos=restaurante,
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_restaurante_con_menos_pedidos(self) -> ResultadoDTO:
        """Obtiene el restaurante con menor cantidad de pedidos."""
        try:
            restaurante = self._pedido_servicio.rest_con_menos_pedidos()
            return ResultadoDTO(
                exitoso=True,
                mensaje="Restaurante con menos pedidos encontrado.",
                datos=restaurante,
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_monto_total_por_restaurante(self, p_cedula_juridica: int) -> ResultadoDTO:
        """Obtiene el monto total vendido por un restaurante."""
        monto = self._pedido_servicio.monto_total_vendido_por_rest(p_cedula_juridica)
        return ResultadoDTO(
            exitoso=True,
            mensaje=f"Monto total vendido: ₡{monto:.2f}",
            datos=monto,
        )

    def obtener_monto_total_vendido(self) -> ResultadoDTO:
        """Obtiene el monto total vendido en todo el sistema."""
        monto = self._pedido_servicio.monto_total_vendido()
        return ResultadoDTO(
            exitoso=True,
            mensaje=f"Monto total vendido en el sistema: ₡{monto:.2f}",
            datos=monto,
        )

    def obtener_hora_pico(self) -> ResultadoDTO:
        """Obtiene la hora con mayor concentración de pedidos."""
        try:
            hora = self._pedido_servicio.obtener_hora_pico()
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Hora pico: {hora.strftime('%H:%M')}",
                datos=hora,
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_todos_los_pedidos(self) -> ResultadoDTO:
        """Obtiene la lista de todos los pedidos registrados."""
        pedidos = self._pedido_repo.obtener_todos()
        return ResultadoDTO(
            exitoso=True,
            mensaje=f"Se encontraron {len(pedidos)} pedido(s).",
            datos=pedidos,
        )

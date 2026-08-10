from __future__ import annotations

from typing import List

from DTOs import (
    CrearRepartidorDTO,
    QuejaRepartidorDTO,
    CalcularPagoDTO,
    ResultadoDTO,
)
from RepartidorServicio import RepartidorServicio
from RepartidorRepositorio import RepartidorRepositorio
from ClasificaionDelRepartidor import CalificacionDelRepartidor
from Repartidor import Repartidor
from Enums import EstadoDeCuenta
from Excepciones import CletaEatsError


class RepartidorController:
    """
    Controlador para las operaciones relacionadas con repartidores.
    Orquesta la comunicación entre la vista y RepartidorServicio.
    """

    def __init__(
        self,
        p_repartidor_servicio: RepartidorServicio,
        p_repartidor_repo: RepartidorRepositorio,
    ):
        self._repartidor_servicio = p_repartidor_servicio
        self._repartidor_repo = p_repartidor_repo

    def registrar_repartidor(self, datos: CrearRepartidorDTO) -> ResultadoDTO:
        """Registra un nuevo repartidor en el sistema."""
        try:
            calificacion = CalificacionDelRepartidor(
                p_calificacion=0,
                p_amabilidad=0,
                p_tiempo_de_respuesta=0,
                p_presentacion=0,
                p_num_de_pedidos_hechos=0,
            )
            repartidor = Repartidor(
                p_cedula=datos.cedula,
                p_contrasenia=datos.contrasenia,
                p_nombre=datos.nombre,
                p_correo=datos.correo,
                p_telefono=datos.telefono,
                p_num_de_tarjeta=datos.num_de_tarjeta,
                p_estado=EstadoDeCuenta.ACTIVO,
                p_num_de_amonestaciones=0,
                p_calificacion=calificacion,
                p_disponibilidad=True,
            )
            self._repartidor_repo.crear(repartidor)
            return ResultadoDTO(exitoso=True, mensaje="Repartidor registrado exitosamente.")
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def registrar_queja(self, datos: QuejaRepartidorDTO) -> ResultadoDTO:
        """Registra una queja contra un repartidor (incrementa amonestación)."""
        try:
            repartidor = self._repartidor_repo.obtener_por_cedula(datos.cedula_repartidor)
            if repartidor is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un repartidor con esa cédula.",
                )

            repartidor.incrementar_amonestacion(datos.motivo)
            amonestaciones = repartidor.num_de_amonestaciones
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Queja registrada. Amonestaciones: {amonestaciones}.",
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def calcular_pago_diario(self, datos: CalcularPagoDTO) -> ResultadoDTO:
        """Calcula el pago diario de un repartidor según sus km recorridos."""
        try:
            repartidor = self._repartidor_repo.obtener_por_cedula(datos.cedula_repartidor)
            if repartidor is None:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un repartidor con esa cédula.",
                )

            pago = self._repartidor_servicio.calcular_pago_diario(
                repartidor, p_es_feriado=datos.es_feriado
            )
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Pago diario calculado: ₡{pago:.2f}",
                datos=pago,
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_quejas(self, p_cedula: int) -> ResultadoDTO:
        """Obtiene la lista de quejas de un repartidor."""
        try:
            quejas = self._repartidor_servicio.obtener_quejas_por_repartidor(p_cedula)
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Se encontraron {len(quejas)} queja(s).",
                datos=quejas,
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_todos_los_repartidores(self) -> ResultadoDTO:
        """Obtiene la lista de todos los repartidores registrados."""
        repartidores = self._repartidor_repo.obtener_todos()
        return ResultadoDTO(
            exitoso=True,
            mensaje=f"Se encontraron {len(repartidores)} repartidor(es).",
            datos=repartidores,
        )

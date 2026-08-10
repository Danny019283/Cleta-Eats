from __future__ import annotations

from typing import List

from DTOs import (
    CrearRestauranteDTO,
    CrearComboDTO,
    ResultadoDTO,
)
from RestauranteServicio import RestauranteServicio
from RestauranteRepositorio import RestauranteRepositorio
from Combo import Combo
from Restaurante import Restaurante
from Excepciones import CletaEatsError


class RestauranteController:
    """
    Controlador para las operaciones relacionadas con restaurantes.
    Orquesta la comunicación entre la vista y RestauranteServicio.
    """

    def __init__(
        self,
        p_restaurante_servicio: RestauranteServicio,
        p_restaurante_repo: RestauranteRepositorio,
    ):
        self._restaurante_servicio = p_restaurante_servicio
        self._restaurante_repo = p_restaurante_repo

    def registrar_restaurante(self, datos: CrearRestauranteDTO) -> ResultadoDTO:
        """Registra un nuevo restaurante en el sistema."""
        try:
            restaurante = Restaurante(
                p_nombre=datos.nombre,
                p_cedula_juridica=datos.cedula_juridica,
                p_direccion=datos.direccion,
                p_tipo_de_comida=datos.tipo_de_comida,
            )
            self._restaurante_servicio.registrar_restaurante(restaurante)
            return ResultadoDTO(exitoso=True, mensaje="Restaurante registrado exitosamente.")
        except (CletaEatsError, ValueError) as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def agregar_combo(self, p_cedula_juridica: int, datos: CrearComboDTO) -> ResultadoDTO:
        """Agrega un combo al menú de un restaurante."""
        try:
            combo = Combo(p_num_de_combo=datos.num_de_combo, p_nombre=datos.nombre)
            agregado = self._restaurante_servicio.agregar_combo_a_restaurante(
                p_cedula_juridica, combo
            )
            if not agregado:
                return ResultadoDTO(
                    exitoso=False,
                    mensaje="No se encontró un restaurante con esa cédula jurídica.",
                )
            return ResultadoDTO(
                exitoso=True,
                mensaje=f"Combo #{datos.num_de_combo} agregado al menú.",
            )
        except CletaEatsError as e:
            return ResultadoDTO(exitoso=False, mensaje=str(e))

    def obtener_menu(self, p_cedula_juridica: int) -> ResultadoDTO:
        """Obtiene el menú de un restaurante."""
        menu = self._restaurante_servicio.obtener_menu(p_cedula_juridica)
        if menu is None:
            return ResultadoDTO(
                exitoso=False,
                mensaje="No se encontró un restaurante con esa cédula jurídica.",
            )
        return ResultadoDTO(
            exitoso=True,
            mensaje=f"El menú tiene {len(menu)} combo(s).",
            datos=menu,
        )

    def obtener_todos_los_restaurantes(self) -> ResultadoDTO:
        """Obtiene la lista de todos los restaurantes registrados."""
        restaurantes = self._restaurante_repo.obtener_todos()
        return ResultadoDTO(
            exitoso=True,
            mensaje=f"Se encontraron {len(restaurantes)} restaurante(s).",
            datos=restaurantes,
        )

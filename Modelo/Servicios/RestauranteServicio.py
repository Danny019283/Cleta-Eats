from __future__ import annotations

from typing import List, Optional

from Combo import Combo
from Restaurante import Restaurante
from RestauranteRepositorio import RestauranteRepositorio


class RestauranteServicio:
    """
    Lógica de negocio: coordina el comportamiento del sistema
    relacionado con restaurantes, especialmente cuando involucra
    reglas del dominio que no pertenecen a la entidad Restaurante.

    Recibe el repositorio de restaurantes por constructor (inyección
    de dependencias) para acceder y persistir datos.
    """

    def __init__(self, p_restaurante_repositorio: RestauranteRepositorio):
        self.__restaurante_repo = p_restaurante_repositorio

    def registrar_restaurante(self, p_restaurante: Restaurante) -> None:
        """
        Lógica de negocio: registra un nuevo restaurante en el sistema.
        Valida reglas de negocio antes de persistir en el repositorio.
        """
        if not p_restaurante.nombre or not p_restaurante.nombre.strip():
            raise ValueError("El nombre del restaurante no puede estar vacío")
        if not p_restaurante.direccion or not p_restaurante.direccion.strip():
            raise ValueError("La dirección del restaurante no puede estar vacía")
        self.__restaurante_repo.crear(p_restaurante)

    def agregar_combo_a_restaurante(
        self, p_cedula_juridica: int, p_combo: Combo
    ) -> bool:
        """
        Lógica de negocio: busca un restaurante por cédula jurídica y
        le agrega un combo a su menú. Coordina entre el repositorio
        (búsqueda) y la entidad Restaurante (agregar_combo).
        Retorna True si se agregó correctamente, False si no se
        encontró el restaurante.
        """
        restaurante = self.__restaurante_repo.obtener_por_cedula_juridica(
            p_cedula_juridica
        )
        if restaurante is None:
            return False
        restaurante.agregar_combo(p_combo)
        return True

    def obtener_menu(self, p_cedula_juridica: int) -> Optional[List[Combo]]:
        """
        Lógica de negocio: retorna el menú de un restaurante específico.
        Retorna None si el restaurante no existe.
        """
        restaurante = self.__restaurante_repo.obtener_por_cedula_juridica(
            p_cedula_juridica
        )
        if restaurante is None:
            return None
        return restaurante.menu

from __future__ import annotations

from typing import List, Optional

from Combo import Combo
from Excepciones import FormatoInvalidoError, ComboDuplicadoError


class Restaurante:
    def __init__(
        self,
        p_nombre: str,
        p_cedula_juridica: int,
        p_direccion: str,
        p_tipo_de_comida: str,
        p_menu: Optional[List[Combo]] = None,
        p_num_de_pedidos_recibidos: int = 0,
    ):
        self.nombre = p_nombre
        self.cedula_juridica = p_cedula_juridica
        self.direccion = p_direccion
        self.tipo_de_comida = p_tipo_de_comida
        self.menu = [] if p_menu is None else p_menu
        self.num_de_pedidos_recibidos = p_num_de_pedidos_recibidos
        # Monto total vendido, usado en los reportes de mayor/menor venta
        self.__monto_total_vendido: float = 0.0

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, p_nombre):
        self.__nombre = p_nombre

    @property
    def cedula_juridica(self):
        return self.__cedula_juridica

    @cedula_juridica.setter
    def cedula_juridica(self, p_cedula_juridica):
        self.__cedula_juridica = p_cedula_juridica

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, p_direccion):
        self.__direccion = p_direccion

    @property
    def tipo_de_comida(self):
        return self.__tipo_de_comida

    @tipo_de_comida.setter
    def tipo_de_comida(self, p_tipo_de_comida):
        if not p_tipo_de_comida or not p_tipo_de_comida.strip():
            raise FormatoInvalidoError("El tipo de comida no puede estar vacío.")
        self.__tipo_de_comida = p_tipo_de_comida

    @property
    def menu(self):
        return self.__menu

    @menu.setter
    def menu(self, p_menu):
        self.__menu = p_menu

    @property
    def num_de_pedidos_recibidos(self):
        return self.__num_de_pedidos_recibidos

    @num_de_pedidos_recibidos.setter
    def num_de_pedidos_recibidos(self, p_num_de_pedidos_recibidos):
        self.__num_de_pedidos_recibidos = p_num_de_pedidos_recibidos

    @property
    def monto_total_vendido(self):
        return self.__monto_total_vendido

    # ── Lógica de entidad ──────────────────────────────────────────────
    # Comportamientos propios de la entidad, relacionados directamente
    # con su estado, atributos e invariantes.

    def agregar_combo(self, p_combo: Combo):
        """
        Lógica de entidad: agrega un combo al menú del restaurante.
        Mantiene el invariante de no duplicar números de combo y valida
        el tipo. Opera sobre su propio atributo __menu.
        """
        if not isinstance(p_combo, Combo):
            raise FormatoInvalidoError("p_combo debe ser una instancia de Combo")
        if any(c.num_de_combo == p_combo.num_de_combo for c in self.__menu):
            raise ComboDuplicadoError(
                f"Ya existe un combo número {p_combo.num_de_combo} en el menú"
            )
        p_combo.asignar_precio_segun_numero()
        self.__menu.append(p_combo)

    def registrar_pedido(self, p_monto: float = 0.0):
        """
        Lógica de entidad: contabiliza un nuevo pedido recibido y acumula
        el monto vendido. Modifica sus propios atributos
        __num_de_pedidos_recibidos y __monto_total_vendido.
        """
        self.__num_de_pedidos_recibidos += 1
        self.__monto_total_vendido += p_monto

    def combo_pertenece_al_menu(self, p_num_de_combo: int) -> bool:
        """
        Lógica de entidad: verifica si un número de combo existe en
        su propio menú. Consulta sobre su atributo __menu.
        """
        return any(c.num_de_combo == p_num_de_combo for c in self.__menu)

    def __str__(self):
        combos = "; ".join(str(combo) for combo in self.__menu)
        return (
            f"Restaurante: nombre: {self.__nombre}, "
            f"cédula jurídica: {self.__cedula_juridica}, "
            f"dirección: {self.__direccion}, "
            f"tipo de comida: {self.__tipo_de_comida}, "
            f"menú: [{combos}], "
            f"número de pedidos recibidos: {self.__num_de_pedidos_recibidos}, "
            f"monto total vendido: ₡{self.__monto_total_vendido:.2f}"
        )
from __future__ import annotations
from Excepciones import ComboInvalidoError


class Combo:
    def __init__(self, p_num_de_combo: int, p_nombre: str, p_precio: float = 0.0):
        self.num_de_combo = p_num_de_combo
        self.nombre = p_nombre
        if p_precio != 0.0:
            self.precio = p_precio
        else:
            self.__precio = 0.0

    @property
    def num_de_combo(self):
        return self.__num_de_combo

    @num_de_combo.setter
    def num_de_combo(self, p_num_de_combo):
        if not (1 <= p_num_de_combo <= 9):
            raise ComboInvalidoError("El número de combo debe estar entre 1 y 9")
        self.__num_de_combo = p_num_de_combo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, p_nombre):
        self.__nombre = p_nombre

    # Getter
    @property
    def precio(self):
        return self.__precio

    # Setter
    @precio.setter
    def precio(self, p_precio):
        esperado = 3000.0 + (self.__num_de_combo * 1000.0)
        if p_precio < 0:
            raise ComboInvalidoError("El precio no puede ser negativo.")
        if p_precio != 0.0 and p_precio != esperado:
            raise ComboInvalidoError(f"El precio debe ser ₡{esperado:.2f} para el combo {self.__num_de_combo}.")
        self.__precio = p_precio

    # ── Lógica de entidad ──────────────────────────────────────────────

    def asignar_precio_segun_numero(self):
        """
        Lógica de entidad: asigna el precio según su propio número de
        combo. Valida invariante (1-9) y modifica su atributo __precio.
        precio = 3000 + (número de combo * 1000)
        """
        if not (1 <= self.__num_de_combo <= 9):
            raise ComboInvalidoError("El número de combo debe estar entre 1 y 9")
        self.__precio = 3000.0 + (self.__num_de_combo * 1000.0)
        return self.__precio

    def __str__(self):
        return (
            f"Combo: número: {self.__num_de_combo}, "
            f"nombre: {self.__nombre}, precio: ₡{self.__precio:.2f}"
        )
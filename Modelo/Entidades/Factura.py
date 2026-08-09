from __future__ import annotations

from typing import List, Optional

from Combo import Combo
from Excepciones import FormatoInvalidoError, ValorNegativoError


class Factura:
    def __init__(
        self,
        p_combos: Optional[List[Combo]] = None,
        p_subtotal: float = 0.0,
        p_costo_del_transporte: float = 0.0,
        p_iva: float = 0.0,
        p_total: float = 0.0,
    ):
        self.combos = [] if p_combos is None else p_combos
        self.subtotal = p_subtotal
        self.costo_del_transporte = p_costo_del_transporte
        self.iva = p_iva
        self.total = p_total

    @property
    def combos(self):
        return self.__combos

    @combos.setter
    def combos(self, p_combos):
        self.__combos = p_combos

    @property
    def subtotal(self):
        return self.__subtotal

    @subtotal.setter
    def subtotal(self, p_subtotal):
        if p_subtotal < 0:
            raise ValorNegativoError("El subtotal no puede ser negativo.")
        self.__subtotal = p_subtotal

    @property
    def costo_del_transporte(self):
        return self.__costo_del_transporte

    @costo_del_transporte.setter
    def costo_del_transporte(self, p_costo_del_transporte):
        if p_costo_del_transporte < 0:
            raise ValorNegativoError("El costo de transporte no puede ser negativo.")
        self.__costo_del_transporte = p_costo_del_transporte

    @property
    def iva(self):
        return self.__iva

    @iva.setter
    def iva(self, p_iva):
        if p_iva < 0:
            raise ValorNegativoError("El IVA no puede ser negativo.")
        self.__iva = p_iva

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, p_total):
        if p_total < 0:
            raise ValorNegativoError("El total no puede ser negativo.")
        self.__total = p_total

    # ── Lógica de entidad ──────────────────────────────────────────────

    def agregar_combo(self, p_combo: Combo):
        """
        Lógica de entidad: agrega un combo a la factura.
        Valida el tipo y modifica su propio atributo __combos.
        """
        if not isinstance(p_combo, Combo):
            raise FormatoInvalidoError("p_combo debe ser una instancia de Combo")
        self.__combos.append(p_combo)

    def calcular_subtotal(self) -> float:
        """Lógica de entidad: suma el precio de todos los combos."""
        self.__subtotal = sum(combo.precio for combo in self.__combos)
        return self.__subtotal

    def calcular_costo_del_transporte(
        self, p_distancia_km: float, p_es_feriado: bool = False
    ) -> float:
        """
        Lógica de entidad: calcula costo del transporte.
        Días hábiles: ₡1000/km, feriados: ₡1500/km.
        """
        if p_distancia_km < 0:
            raise ValorNegativoError("La distancia no puede ser negativa")
        costo_por_km = 1500.0 if p_es_feriado else 1000.0
        self.__costo_del_transporte = p_distancia_km * costo_por_km
        return self.__costo_del_transporte

    def calcular_iva(self) -> float:
        """Lógica de entidad: calcula el IVA (13%) sobre el subtotal."""
        self.__iva = self.__subtotal * 0.13
        return self.__iva

    def calcular_total(self) -> float:
        """Lógica de entidad: total = subtotal + transporte + IVA."""
        self.__total = self.__subtotal + self.__costo_del_transporte + self.__iva
        return self.__total

    def __str__(self):
        combos = "; ".join(str(combo) for combo in self.__combos)
        return (
            f"Factura: combos: [{combos}], "
            f"subtotal: ₡{self.__subtotal:.2f}, "
            f"costo del transporte: ₡{self.__costo_del_transporte:.2f}, "
            f"IVA: ₡{self.__iva:.2f}, total: ₡{self.__total:.2f}"
        )
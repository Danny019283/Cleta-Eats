from __future__ import annotations

from typing import List

from Repartidor import Repartidor
from RepartidorRepositorio import RepartidorRepositorio


class RepartidorServicio:
    """
    Lógica de negocio: coordina el comportamiento del sistema
    relacionado con repartidores, especialmente cuando involucra
    reglas del dominio que no pertenecen a la entidad Repartidor.

    Recibe el repositorio de repartidores por constructor (inyección
    de dependencias) para acceder y persistir datos.
    """

    def __init__(self, p_repartidor_repositorio: RepartidorRepositorio):
        self.__repartidor_repo = p_repartidor_repositorio

    def calcular_pago_diario(
        self, p_repartidor: Repartidor, p_es_feriado: bool = False
    ) -> float:
        """
        Lógica de negocio: calcula el pago del repartidor según los km
        recorridos en el día. Aplica las tarifas del dominio:
        días hábiles ₡1000/km, días feriados ₡1500/km.
        Las tarifas son reglas del dominio externas a la entidad.
        """
        costo_por_km = 1500.0 if p_es_feriado else 1000.0
        return p_repartidor.km_recorridos_hoy * costo_por_km

    # ── Métodos de reporte (delegan al repositorio) ───────────────────

    def obtener_quejas_por_repartidor(self, p_cedula: int) -> List[str]:
        """
        Reporte: retorna la lista de quejas registradas para un
        repartidor específico. Delega al RepartidorRepositorio.
        """
        return self.__repartidor_repo.obtener_quejas_por_repartidor(p_cedula)

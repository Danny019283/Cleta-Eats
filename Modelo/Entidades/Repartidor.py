from __future__ import annotations

from typing import List, Optional

from ClasificaionDelRepartidor import CalificacionDelRepartidor
from Enums import EstadoDeCuenta, Hash
from Enums import EstadoDeCuenta, Hash
from Excepciones import ValorNegativoError
from Usuario import Usuario


# EJEMPLO HERENCIA
# Repartidor hereda de Usuario
class Repartidor(Usuario):
    def __init__(
        self,
        p_cedula: int,
        p_contrasenia: Hash,
        p_nombre: str,
        p_correo: str,
        p_telefono: int,
        p_num_de_tarjeta: int,
        p_estado: EstadoDeCuenta,
        p_num_de_amonestaciones: int,
        p_calificacion: CalificacionDelRepartidor,
        p_disponibilidad: bool,
    ):
        super().__init__(
            p_cedula,
            p_contrasenia,
            p_nombre,
            p_correo,
            p_telefono,
            p_num_de_tarjeta,
            p_estado,
        )
        self.num_de_amonestaciones = p_num_de_amonestaciones
        self.calificacion = p_calificacion
        self.disponibilidad = p_disponibilidad
        # Registro de quejas realizadas por los clientes hacia este repartidor
        self.__quejas: List[str] = []
        # Kilómetros recorridos en el día (para el cálculo de pago/transporte)
        self.__km_recorridos_hoy: float = 0.0

    @property
    def num_de_amonestaciones(self):
        return self.__num_de_amonestaciones

    @num_de_amonestaciones.setter
    def num_de_amonestaciones(self, p_num_de_amonestaciones):
        if p_num_de_amonestaciones < 0:
            raise ValorNegativoError("El número de amonestaciones no puede ser negativo.")
        self.__num_de_amonestaciones = p_num_de_amonestaciones

    @property
    def calificacion(self):
        return self.__calificacion

    @calificacion.setter
    def calificacion(self, p_calificacion):
        self.__calificacion = p_calificacion

    @property
    def disponibilidad(self):
        return self.__disponibilidad

    @disponibilidad.setter
    def disponibilidad(self, p_disponibilidad):
        self.__disponibilidad = p_disponibilidad

    @property
    def quejas(self):
        return self.__quejas

    @property
    def km_recorridos_hoy(self):
        return self.__km_recorridos_hoy

    # ── Lógica de entidad ──────────────────────────────────────────────
    # Comportamientos propios de la entidad, relacionados directamente
    # con su estado, atributos e invariantes.

    def esta_disponible_para_pedido(self) -> bool:
        """
        Lógica de entidad: verifica si el repartidor puede recibir un
        pedido según sus propios atributos (disponibilidad y
        amonestaciones). Invariante de la entidad.
        """
        return self.__disponibilidad and self.__num_de_amonestaciones < 4

    def incrementar_amonestacion(self, p_motivo_queja: Optional[str] = None):
        """
        Lógica de entidad: incrementa el contador de amonestaciones y
        registra opcionalmente una queja. Mantiene el invariante de que
        con 4+ amonestaciones la cuenta se desactiva y deja de estar
        disponible. Opera sobre sus propios atributos.
        """
        self.num_de_amonestaciones += 1
        if p_motivo_queja:
            self.__quejas.append(p_motivo_queja)

        if self.__num_de_amonestaciones >= 4:
            self.__disponibilidad = False
            self.cambiar_estado(EstadoDeCuenta.DESACTIVADO)

    def actualizar_disponibilidad(self, p_disponibilidad: bool):
        """
        Lógica de entidad: cambia si el repartidor está disponible u
        ocupado. Mantiene el invariante de que un repartidor con 4+
        amonestaciones nunca puede quedar disponible.
        """
        if self.__num_de_amonestaciones >= 4:
            self.__disponibilidad = False
            return
        self.__disponibilidad = p_disponibilidad

    def actualizar_calificacion(self, p_calificacion: CalificacionDelRepartidor):
        """
        Lógica de entidad: sustituye/actualiza la calificación del
        repartidor. Valida el tipo antes de modificar su propio atributo.
        """
        if not isinstance(p_calificacion, CalificacionDelRepartidor):
            raise TypeError("p_calificacion debe ser CalificacionDelRepartidor")
        self.__calificacion = p_calificacion

    def registrar_km_recorridos(self, p_km: float):
        """
        Lógica de entidad: acumula kilómetros recorridos en el día.
        Opera sobre su propio atributo __km_recorridos_hoy con
        validación de invariante (no negativo).
        """
        if p_km < 0:
            raise ValorNegativoError("Los kilómetros recorridos no pueden ser negativos.")
        self.__km_recorridos_hoy += p_km

    # EJEMPLO POLIMORFISMO
    # Se redefine lo que se declara en la clase padre (Usuario)
    def __str__(self):
        return (
            f"Repartidor: {super().__str__()}, "
            f"número de amonestaciones: {self.__num_de_amonestaciones}, "
            f"calificación: {self.__calificacion}, "
            f"disponibilidad: {self.__disponibilidad}"
        )
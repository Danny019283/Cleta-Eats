from __future__ import annotations


class CalificacionDelRepartidor:
    def __init__(
        self,
        p_calificacion: float,
        p_amabilidad: int,
        p_tiempo_de_respuesta: int,
        p_presentacion: int,
        p_num_de_pedidos_hechos: int,
    ):
        self.__calificacion = p_calificacion
        self.__amabilidad = p_amabilidad
        self.__tiempo_de_respuesta = p_tiempo_de_respuesta
        self.__presentacion = p_presentacion
        self.__num_de_pedidos_hechos = p_num_de_pedidos_hechos

    @property
    def calificacion(self):
        return self.__calificacion

    @calificacion.setter
    def calificacion(self, p_calificacion):
        self.__calificacion = p_calificacion

    @property
    def amabilidad(self):
        return self.__amabilidad

    @amabilidad.setter
    def amabilidad(self, p_amabilidad):
        self.__amabilidad = p_amabilidad

    @property
    def tiempo_de_respuesta(self):
        return self.__tiempo_de_respuesta

    @tiempo_de_respuesta.setter
    def tiempo_de_respuesta(self, p_tiempo_de_respuesta):
        self.__tiempo_de_respuesta = p_tiempo_de_respuesta

    @property
    def presentacion(self):
        return self.__presentacion

    @presentacion.setter
    def presentacion(self, p_presentacion):
        self.__presentacion = p_presentacion

    @property
    def num_de_pedidos_hechos(self):
        return self.__num_de_pedidos_hechos

    @num_de_pedidos_hechos.setter
    def num_de_pedidos_hechos(self, p_num_de_pedidos_hechos):
        self.__num_de_pedidos_hechos = p_num_de_pedidos_hechos

    # ── Lógica de entidad ──────────────────────────────────────────────

    def calcular_promedio(self) -> float:
        """
        Lógica de entidad: calcula el promedio de calificación con base
        en sus propios atributos (amabilidad, tiempo de respuesta,
        presentación) y actualiza su __calificacion.
        """
        promedio = (
            self.__amabilidad + self.__tiempo_de_respuesta + self.__presentacion
        ) / 3
        self.__calificacion = round(promedio, 2)
        return self.__calificacion

    def incrementar_pedidos(self):
        """
        Lógica de entidad: incrementa el contador de pedidos hechos.
        Modifica su propio atributo __num_de_pedidos_hechos.
        """
        self.__num_de_pedidos_hechos += 1

    def __str__(self):
        return (
            f"Calificación: {self.__calificacion}, "
            f"amabilidad: {self.__amabilidad}, "
            f"tiempo de respuesta: {self.__tiempo_de_respuesta}, "
            f"presentación: {self.__presentacion}, "
            f"número de pedidos hechos: {self.__num_de_pedidos_hechos}"
        )
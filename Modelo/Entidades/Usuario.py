from __future__ import annotations

from abc import ABCMeta, abstractmethod

from Enums import EstadoDeCuenta, Hash
from Excepciones import (
    CedulaInvalidaError,
    CorreoInvalidoError,
    TelefonoInvalidoError,
    TarjetaInvalidaError,
    FormatoInvalidoError
)


class Usuario(metaclass=ABCMeta):#Definimos la clase abstracta usando la metaclase
    def __init__(
        self,
        p_cedula: int,
        p_contrasenia: Hash,
        p_nombre: str,
        p_correo: str,
        p_telefono: int,
        p_num_de_tarjeta: int,
        p_estado: EstadoDeCuenta,
    ):
        # Usar setters para aplicar validaciones
        self.cedula = p_cedula
        self.contrasenia = p_contrasenia
        self.nombre = p_nombre
        self.correo = p_correo
        self.telefono = p_telefono
        self.num_de_tarjeta = p_num_de_tarjeta
        self.estado = p_estado

    # Getter
    @property
    def cedula(self):
        return self.__cedula

    # Setter
    @cedula.setter
    def cedula(self, p_cedula):
        if not p_cedula or p_cedula <= 0:
            raise CedulaInvalidaError("La cédula no puede estar vacía o ser negativa.")
        self.__cedula = p_cedula

    @property
    def contrasenia(self):
        return self.__contrasenia

    @contrasenia.setter
    def contrasenia(self, p_contrasenia):
        self.__contrasenia = p_contrasenia

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, p_nombre):
        self.__nombre = p_nombre

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, p_correo):
        if "@" not in p_correo or "." not in p_correo:
            raise CorreoInvalidoError("El correo electrónico tiene un formato inválido.")
        self.__correo = p_correo

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, p_telefono):
        if p_telefono <= 0 or len(str(p_telefono)) < 8:
            raise TelefonoInvalidoError("El número de teléfono tiene un formato inválido.")
        self.__telefono = p_telefono

    @property
    def num_de_tarjeta(self):
        return self.__num_de_tarjeta

    @num_de_tarjeta.setter
    def num_de_tarjeta(self, p_num_de_tarjeta):
        if p_num_de_tarjeta <= 0 or len(str(p_num_de_tarjeta)) < 12:
            raise TarjetaInvalidaError("El número de tarjeta es inválido.")
        self.__num_de_tarjeta = p_num_de_tarjeta

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, p_estado):
        if not isinstance(p_estado, EstadoDeCuenta):
            raise FormatoInvalidoError("El estado debe ser un valor de EstadoDeCuenta.")
        self.__estado = p_estado

    # ── Lógica de entidad ──────────────────────────────────────────────
    # Comportamientos propios de la entidad, relacionados directamente
    # con su estado, atributos e invariantes.

    # EJEMPLO ACCESO PÚBLICO
    # Los métodos y propiedades que no empiezan con __ son de acceso público
    def autenticar(self, p_contrasenia: Hash) -> bool:
        """
        Lógica de entidad: valida el login comparando la contraseña
        recibida contra la almacenada en el propio usuario.
        Opera exclusivamente sobre su atributo __contrasenia.
        """
        return self.__contrasenia == p_contrasenia

    def cambiar_estado(self, p_estado: EstadoDeCuenta):
        """
        Lógica de entidad: actualiza el estado de la cuenta
        (ACTIVO/DESACTIVADO). Valida el invariante de tipo antes de
        modificar su propio atributo __estado.
        """
        if not isinstance(p_estado, EstadoDeCuenta):
            raise FormatoInvalidoError("p_estado debe ser un valor de EstadoDeCuenta")
        self.estado = p_estado

    def esta_activo(self) -> bool:
        """
        Lógica de entidad: consulta si la cuenta del usuario está activa.
        Opera sobre su propio atributo __estado.
        """
        return self.__estado == EstadoDeCuenta.ACTIVO

    # EJEMPLO POLIMORFISMO Y ABSTRACCIÓN
    # La clase padre lo declara y se redefine en Cliente y Repartidor.
    # Al ser un método abstracto, obliga a las subclases a implementarlo.
    @abstractmethod
    def __str__(self):
        return (
            f"Cédula: {self.__cedula}, nombre: {self.__nombre}, "
            f"correo: {self.__correo}, teléfono: {self.__telefono}, "
            f"número de tarjeta: {self.__num_de_tarjeta}, "
            f"estado: {self.__estado.value}"
        )
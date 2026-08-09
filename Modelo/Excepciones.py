class CletaEatsError(Exception):
    """Excepción base para el sistema CletaEats."""
    pass


class ValidacionError(CletaEatsError):
    """Errores de validación de formato o datos."""
    pass


class CedulaInvalidaError(ValidacionError):
    pass


class CorreoInvalidoError(ValidacionError):
    pass


class TelefonoInvalidoError(ValidacionError):
    pass


class TarjetaInvalidaError(ValidacionError):
    pass


class ComboInvalidoError(ValidacionError):
    pass


class FormatoInvalidoError(ValidacionError):
    pass


class ValorNegativoError(ValidacionError):
    pass


class RegistroDuplicadoError(CletaEatsError):
    """Errores cuando se intenta registrar un elemento que ya existe."""
    pass


class ClienteDuplicadoError(RegistroDuplicadoError):
    pass


class RepartidorDuplicadoError(RegistroDuplicadoError):
    pass


class RestauranteDuplicadoError(RegistroDuplicadoError):
    pass


class ComboDuplicadoError(RegistroDuplicadoError):
    pass


class PedidoDuplicadoError(RegistroDuplicadoError):
    pass


class EstadoInvalidoError(CletaEatsError):
    """Errores relacionados con estados no válidos o transiciones no permitidas."""
    pass


class ClienteSuspendidoError(EstadoInvalidoError):
    pass


class RepartidorNoDisponibleError(EstadoInvalidoError):
    pass


class TransicionEstadoInvalidaError(EstadoInvalidoError):
    pass


class RecursoNoDisponibleError(CletaEatsError):
    """Errores cuando un recurso necesario no se encuentra o no está disponible."""
    pass


class SinRepartidorDisponibleError(RecursoNoDisponibleError):
    pass


class EntidadNoEncontradaError(RecursoNoDisponibleError):
    pass


class ReglaNegocioError(CletaEatsError):
    """Errores que violan reglas de negocio específicas."""
    pass


class RestauranteInconsistenteError(ReglaNegocioError):
    pass


class PedidoSinRepartidorError(ReglaNegocioError):
    pass


class InfraestructuraError(CletaEatsError):
    """Errores relacionados con persistencia, base de datos o archivos."""
    pass


class ArchivoNoEncontradoError(InfraestructuraError):
    pass


class ErrorLecturaEscrituraError(InfraestructuraError):
    pass


class ArchivoCorruptoError(InfraestructuraError):
    pass


class IntegridadDatosError(InfraestructuraError):
    pass

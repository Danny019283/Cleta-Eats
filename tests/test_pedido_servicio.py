import pytest
from unittest.mock import MagicMock

from PedidoServicio import PedidoServicio
from Enums import EstadoDelPedido
from Excepciones import (
    RepartidorNoDisponibleError,
    SinRepartidorDisponibleError,
    RecursoNoDisponibleError
)


def test_asignar_repartidor_no_disponible():
    # Arrange
    pedido_repo_mock = MagicMock()
    servicio = PedidoServicio(pedido_repo_mock)

    pedido_mock = MagicMock()
    repartidor_mock = MagicMock()
    repartidor_mock.esta_disponible_para_pedido.return_value = False
    repartidor_mock.nombre = "Juan"

    # Act & Assert
    with pytest.raises(RepartidorNoDisponibleError):
        servicio.asignar_repartidor(pedido_mock, repartidor_mock)

    pedido_mock.asignar_repartidor_interno.assert_not_called()


def test_asignar_repartidor_exitoso():
    # Arrange
    pedido_repo_mock = MagicMock()
    servicio = PedidoServicio(pedido_repo_mock)

    pedido_mock = MagicMock()
    repartidor_mock = MagicMock()
    repartidor_mock.esta_disponible_para_pedido.return_value = True

    # Act
    resultado = servicio.asignar_repartidor(pedido_mock, repartidor_mock)

    # Assert
    assert resultado is True
    pedido_mock.asignar_repartidor_interno.assert_called_once_with(repartidor_mock)
    repartidor_mock.actualizar_disponibilidad.assert_called_once_with(False)
    pedido_mock.cambiar_estado.assert_called_once_with(EstadoDelPedido.EN_PREPARACION)


def test_asignar_primer_repartidor_disponible_exitoso():
    # Arrange
    pedido_repo_mock = MagicMock()
    servicio = PedidoServicio(pedido_repo_mock)

    rep1 = MagicMock()
    rep1.esta_disponible_para_pedido.return_value = False
    rep2 = MagicMock()
    rep2.esta_disponible_para_pedido.return_value = True
    rep3 = MagicMock()
    rep3.esta_disponible_para_pedido.return_value = True

    repartidores = [rep1, rep2, rep3]

    # Act
    resultado = servicio.asignar_primer_repartidor_disponible(repartidores)

    # Assert
    assert resultado == rep2


def test_asignar_primer_repartidor_disponible_sin_repartidores():
    # Arrange
    pedido_repo_mock = MagicMock()
    servicio = PedidoServicio(pedido_repo_mock)

    rep1 = MagicMock()
    rep1.esta_disponible_para_pedido.return_value = False
    repartidores = [rep1]

    # Act & Assert
    with pytest.raises(SinRepartidorDisponibleError):
        servicio.asignar_primer_repartidor_disponible(repartidores)


def test_generar_factura_exitoso():
    # Arrange
    pedido_repo_mock = MagicMock()
    servicio = PedidoServicio(pedido_repo_mock)

    pedido_mock = MagicMock()
    pedido_mock.distancia_km = 10.0
    pedido_mock.es_feriado = True
    
    factura_mock = MagicMock()
    pedido_mock.factura = factura_mock

    # Act
    resultado = servicio.generar_factura(pedido_mock)

    # Assert
    assert resultado == factura_mock
    factura_mock.calcular_subtotal.assert_called_once()
    factura_mock.calcular_costo_del_transporte.assert_called_once_with(10.0, True)
    factura_mock.calcular_iva.assert_called_once()
    factura_mock.calcular_total.assert_called_once()


def test_entregar_pedido_con_repartidor():
    # Arrange
    pedido_repo_mock = MagicMock()
    servicio = PedidoServicio(pedido_repo_mock)

    pedido_mock = MagicMock()
    pedido_mock.tiene_repartidor.return_value = True
    pedido_mock.distancia_km = 5.0
    
    calificacion_mock = MagicMock()
    calificacion_mock.num_de_pedidos_hechos = 1
    
    repartidor_mock = MagicMock()
    repartidor_mock.calificacion = calificacion_mock
    pedido_mock.repartidor = repartidor_mock

    # Act
    servicio.entregar_pedido(pedido_mock, 9, 8, 7)

    # Assert
    pedido_mock.cambiar_estado.assert_called_once_with(EstadoDelPedido.ENTREGADO)
    repartidor_mock.actualizar_disponibilidad.assert_called_once_with(True)
    repartidor_mock.registrar_km_recorridos.assert_called_once_with(5.0)
    calificacion_mock.calcular_promedio.assert_called_once()


def test_entregar_pedido_sin_repartidor():
    # Arrange
    pedido_repo_mock = MagicMock()
    servicio = PedidoServicio(pedido_repo_mock)

    pedido_mock = MagicMock()
    pedido_mock.tiene_repartidor.return_value = False

    # Act
    servicio.entregar_pedido(pedido_mock)

    # Assert
    pedido_mock.cambiar_estado.assert_called_once_with(EstadoDelPedido.ENTREGADO)


def test_rest_con_mas_pedidos_exitoso():
    # Arrange
    pedido_repo_mock = MagicMock()
    esperado = MagicMock()
    pedido_repo_mock.rest_con_mas_pedidos.return_value = esperado
    servicio = PedidoServicio(pedido_repo_mock)

    # Act
    resultado = servicio.rest_con_mas_pedidos()

    # Assert
    assert resultado == esperado


def test_rest_con_mas_pedidos_vacio():
    # Arrange
    pedido_repo_mock = MagicMock()
    pedido_repo_mock.rest_con_mas_pedidos.return_value = None
    servicio = PedidoServicio(pedido_repo_mock)

    # Act & Assert
    with pytest.raises(RecursoNoDisponibleError):
        servicio.rest_con_mas_pedidos()


def test_rest_con_menos_pedidos_vacio():
    # Arrange
    pedido_repo_mock = MagicMock()
    pedido_repo_mock.rest_con_menos_pedidos.return_value = None
    servicio = PedidoServicio(pedido_repo_mock)

    # Act & Assert
    with pytest.raises(RecursoNoDisponibleError):
        servicio.rest_con_menos_pedidos()


def test_monto_total_vendido_por_rest():
    # Arrange
    pedido_repo_mock = MagicMock()
    pedido_repo_mock.monto_total_vendido_por_rest.return_value = 1500.0
    servicio = PedidoServicio(pedido_repo_mock)

    # Act
    resultado = servicio.monto_total_vendido_por_rest(123)

    # Assert
    assert resultado == 1500.0
    pedido_repo_mock.monto_total_vendido_por_rest.assert_called_once_with(123)


def test_cliente_con_mas_pedidos_vacio():
    # Arrange
    pedido_repo_mock = MagicMock()
    pedido_repo_mock.cliente_con_mas_pedidos.return_value = None
    servicio = PedidoServicio(pedido_repo_mock)

    # Act & Assert
    with pytest.raises(RecursoNoDisponibleError):
        servicio.cliente_con_mas_pedidos()


def test_obtener_hora_pico_vacio():
    # Arrange
    pedido_repo_mock = MagicMock()
    pedido_repo_mock.obtener_hora_pico.return_value = None
    servicio = PedidoServicio(pedido_repo_mock)

    # Act & Assert
    with pytest.raises(RecursoNoDisponibleError):
        servicio.obtener_hora_pico()

import pytest
from unittest.mock import MagicMock

from ClienteServicio import ClienteServicio
from Excepciones import (
    EntidadNoEncontradaError,
    ClienteSuspendidoError,
    RestauranteInconsistenteError,
    RecursoNoDisponibleError,
    ReglaNegocioError
)


def test_realizar_pedido_cliente_no_registrado():
    # Arrange
    cliente_repo_mock = MagicMock()
    pedido_repo_mock = MagicMock()
    cliente_repo_mock.obtener_por_cedula.return_value = None
    servicio = ClienteServicio(cliente_repo_mock, pedido_repo_mock)

    cliente_mock = MagicMock()
    cliente_mock.cedula = 123
    pedido_mock = MagicMock()

    # Act & Assert
    with pytest.raises(EntidadNoEncontradaError):
        servicio.realizar_pedido(cliente_mock, pedido_mock)

    pedido_repo_mock.crear.assert_not_called()


def test_realizar_pedido_cliente_suspendido():
    # Arrange
    cliente_repo_mock = MagicMock()
    pedido_repo_mock = MagicMock()
    cliente_repo_mock.obtener_por_cedula.return_value = MagicMock()
    servicio = ClienteServicio(cliente_repo_mock, pedido_repo_mock)

    cliente_mock = MagicMock()
    cliente_mock.puede_realizar_pedido.return_value = False
    pedido_mock = MagicMock()

    # Act & Assert
    with pytest.raises(ClienteSuspendidoError):
        servicio.realizar_pedido(cliente_mock, pedido_mock)

    pedido_repo_mock.crear.assert_not_called()


def test_realizar_pedido_cliente_no_coincide():
    # Arrange
    cliente_repo_mock = MagicMock()
    pedido_repo_mock = MagicMock()
    cliente_repo_mock.obtener_por_cedula.return_value = MagicMock()
    servicio = ClienteServicio(cliente_repo_mock, pedido_repo_mock)

    cliente_mock = MagicMock()
    cliente_mock.puede_realizar_pedido.return_value = True

    pedido_mock = MagicMock()
    pedido_mock.cliente = MagicMock() # Diferente a cliente_mock

    # Act & Assert
    with pytest.raises(ReglaNegocioError):
        servicio.realizar_pedido(cliente_mock, pedido_mock)

    pedido_repo_mock.crear.assert_not_called()


def test_realizar_pedido_restaurante_inconsistente():
    # Arrange
    cliente_repo_mock = MagicMock()
    pedido_repo_mock = MagicMock()
    cliente_repo_mock.obtener_por_cedula.return_value = MagicMock()
    servicio = ClienteServicio(cliente_repo_mock, pedido_repo_mock)

    cliente_mock = MagicMock()
    cliente_mock.puede_realizar_pedido.return_value = True

    restaurante_mock = MagicMock()
    restaurante_mock.combo_pertenece_al_menu.return_value = False

    combo_mock = MagicMock()
    combo_mock.num_de_combo = 1
    
    factura_mock = MagicMock()
    factura_mock.combos = [combo_mock]

    pedido_mock = MagicMock()
    pedido_mock.cliente = cliente_mock
    pedido_mock.restaurante = restaurante_mock
    pedido_mock.factura = factura_mock

    # Act & Assert
    with pytest.raises(RestauranteInconsistenteError):
        servicio.realizar_pedido(cliente_mock, pedido_mock)

    pedido_repo_mock.crear.assert_not_called()


def test_realizar_pedido_exitoso():
    # Arrange
    cliente_repo_mock = MagicMock()
    pedido_repo_mock = MagicMock()
    cliente_repo_mock.obtener_por_cedula.return_value = MagicMock()
    servicio = ClienteServicio(cliente_repo_mock, pedido_repo_mock)

    cliente_mock = MagicMock()
    cliente_mock.puede_realizar_pedido.return_value = True

    restaurante_mock = MagicMock()
    restaurante_mock.combo_pertenece_al_menu.return_value = True

    combo_mock = MagicMock()
    combo_mock.num_de_combo = 1
    
    factura_mock = MagicMock()
    factura_mock.combos = [combo_mock]
    factura_mock.total = 5000.0

    pedido_mock = MagicMock()
    pedido_mock.cliente = cliente_mock
    pedido_mock.restaurante = restaurante_mock
    pedido_mock.factura = factura_mock

    # Act
    resultado = servicio.realizar_pedido(cliente_mock, pedido_mock)

    # Assert
    assert resultado is True
    # Verifica llamadas de orquestación
    factura_mock.calcular_total.assert_called() # Se llama dentro de generar_factura
    restaurante_mock.registrar_pedido.assert_called_once_with(5000.0)
    cliente_mock.agregar_pedido_al_historial.assert_called_once_with(pedido_mock)
    pedido_repo_mock.crear.assert_called_once_with(pedido_mock)


def test_pedidos_por_cliente_exitoso():
    # Arrange
    cliente_repo_mock = MagicMock()
    pedido_repo_mock = MagicMock()
    esperado = [MagicMock(), MagicMock()]
    pedido_repo_mock.pedidos_por_cliente.return_value = esperado
    servicio = ClienteServicio(cliente_repo_mock, pedido_repo_mock)

    # Act
    resultado = servicio.pedidos_por_cliente(123)

    # Assert
    assert resultado == esperado
    pedido_repo_mock.pedidos_por_cliente.assert_called_once_with(123)


def test_cliente_con_mas_pedidos_exitoso():
    # Arrange
    cliente_repo_mock = MagicMock()
    pedido_repo_mock = MagicMock()
    esperado = MagicMock()
    pedido_repo_mock.cliente_con_mas_pedidos.return_value = esperado
    servicio = ClienteServicio(cliente_repo_mock, pedido_repo_mock)

    # Act
    resultado = servicio.cliente_con_mas_pedidos()

    # Assert
    assert resultado == esperado
    pedido_repo_mock.cliente_con_mas_pedidos.assert_called_once()


def test_cliente_con_mas_pedidos_vacio():
    # Arrange
    cliente_repo_mock = MagicMock()
    pedido_repo_mock = MagicMock()
    pedido_repo_mock.cliente_con_mas_pedidos.return_value = None
    servicio = ClienteServicio(cliente_repo_mock, pedido_repo_mock)

    # Act & Assert
    with pytest.raises(RecursoNoDisponibleError):
        servicio.cliente_con_mas_pedidos()

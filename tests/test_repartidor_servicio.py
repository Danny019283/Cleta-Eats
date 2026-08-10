import pytest
from unittest.mock import MagicMock

from RepartidorServicio import RepartidorServicio


def test_calcular_pago_diario_dia_habil():
    # Arrange
    repartidor_repo_mock = MagicMock()
    servicio = RepartidorServicio(repartidor_repo_mock)
    
    repartidor_mock = MagicMock()
    repartidor_mock.km_recorridos_hoy = 10.0

    # Act
    pago = servicio.calcular_pago_diario(repartidor_mock, p_es_feriado=False)

    # Assert
    assert pago == 10.0 * 1000.0


def test_calcular_pago_diario_dia_feriado():
    # Arrange
    repartidor_repo_mock = MagicMock()
    servicio = RepartidorServicio(repartidor_repo_mock)
    
    repartidor_mock = MagicMock()
    repartidor_mock.km_recorridos_hoy = 10.0

    # Act
    pago = servicio.calcular_pago_diario(repartidor_mock, p_es_feriado=True)

    # Assert
    assert pago == 10.0 * 1500.0


def test_obtener_quejas_por_repartidor():
    # Arrange
    repartidor_repo_mock = MagicMock()
    esperado = ["Queja 1", "Queja 2"]
    repartidor_repo_mock.obtener_quejas_por_repartidor.return_value = esperado
    servicio = RepartidorServicio(repartidor_repo_mock)

    # Act
    resultado = servicio.obtener_quejas_por_repartidor(123)

    # Assert
    assert resultado == esperado
    repartidor_repo_mock.obtener_quejas_por_repartidor.assert_called_once_with(123)

import pytest
from unittest.mock import MagicMock

from RestauranteServicio import RestauranteServicio


def test_registrar_restaurante_nombre_vacio():
    # Arrange
    restaurante_repo_mock = MagicMock()
    servicio = RestauranteServicio(restaurante_repo_mock)

    restaurante_mock = MagicMock()
    restaurante_mock.nombre = "   "
    restaurante_mock.direccion = "Calle 123"

    # Act & Assert
    with pytest.raises(ValueError, match="El nombre del restaurante no puede estar vacío"):
        servicio.registrar_restaurante(restaurante_mock)

    restaurante_repo_mock.crear.assert_not_called()


def test_registrar_restaurante_direccion_vacia():
    # Arrange
    restaurante_repo_mock = MagicMock()
    servicio = RestauranteServicio(restaurante_repo_mock)

    restaurante_mock = MagicMock()
    restaurante_mock.nombre = "Restaurante X"
    restaurante_mock.direccion = ""

    # Act & Assert
    with pytest.raises(ValueError, match="La dirección del restaurante no puede estar vacía"):
        servicio.registrar_restaurante(restaurante_mock)

    restaurante_repo_mock.crear.assert_not_called()


def test_registrar_restaurante_exitoso():
    # Arrange
    restaurante_repo_mock = MagicMock()
    servicio = RestauranteServicio(restaurante_repo_mock)

    restaurante_mock = MagicMock()
    restaurante_mock.nombre = "Restaurante X"
    restaurante_mock.direccion = "Calle 123"

    # Act
    servicio.registrar_restaurante(restaurante_mock)

    # Assert
    restaurante_repo_mock.crear.assert_called_once_with(restaurante_mock)


def test_agregar_combo_a_restaurante_no_encontrado():
    # Arrange
    restaurante_repo_mock = MagicMock()
    restaurante_repo_mock.obtener_por_cedula_juridica.return_value = None
    servicio = RestauranteServicio(restaurante_repo_mock)

    combo_mock = MagicMock()

    # Act
    resultado = servicio.agregar_combo_a_restaurante(123, combo_mock)

    # Assert
    assert resultado is False


def test_agregar_combo_a_restaurante_exitoso():
    # Arrange
    restaurante_repo_mock = MagicMock()
    restaurante_mock = MagicMock()
    restaurante_repo_mock.obtener_por_cedula_juridica.return_value = restaurante_mock
    servicio = RestauranteServicio(restaurante_repo_mock)

    combo_mock = MagicMock()

    # Act
    resultado = servicio.agregar_combo_a_restaurante(123, combo_mock)

    # Assert
    assert resultado is True
    restaurante_mock.agregar_combo.assert_called_once_with(combo_mock)


def test_obtener_menu_no_encontrado():
    # Arrange
    restaurante_repo_mock = MagicMock()
    restaurante_repo_mock.obtener_por_cedula_juridica.return_value = None
    servicio = RestauranteServicio(restaurante_repo_mock)

    # Act
    resultado = servicio.obtener_menu(123)

    # Assert
    assert resultado is None


def test_obtener_menu_exitoso():
    # Arrange
    restaurante_repo_mock = MagicMock()
    restaurante_mock = MagicMock()
    esperado = [MagicMock(), MagicMock()]
    restaurante_mock.menu = esperado
    restaurante_repo_mock.obtener_por_cedula_juridica.return_value = restaurante_mock
    servicio = RestauranteServicio(restaurante_repo_mock)

    # Act
    resultado = servicio.obtener_menu(123)

    # Assert
    assert resultado == esperado

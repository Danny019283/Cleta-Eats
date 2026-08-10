"""
Punto de entrada de la aplicación CletaEats (Streamlit).

Configura las dependencias (repositorios → servicios → controladores)
y renderiza la interfaz de usuario delegando a las vistas.
"""
import sys
import os

# ── Configurar paths del proyecto ────────────────────────────────────────────
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "Modelo", "Entidades"))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "Modelo", "Servicios"))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "Modelo"))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "Acceso a Datos"))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "Controladores"))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "Vistas"))

import streamlit as st

# Repositorios
from ClienteRepositorio import ClienteRepositorio
from PedidoRepositorio import PedidoRepositorio
from RepartidorRepositorio import RepartidorRepositorio
from RestauranteRepositorio import RestauranteRepositorio

# Servicios
from ClienteServicio import ClienteServicio
from PedidoServicio import PedidoServicio
from RepartidorServicio import RepartidorServicio
from RestauranteServicio import RestauranteServicio

# Controladores
from ClienteController import ClienteController
from PedidoController import PedidoController
from RepartidorController import RepartidorController
from RestauranteController import RestauranteController

# Vistas
from cliente_vista import mostrar_vista_clientes
from restaurante_vista import mostrar_vista_restaurantes
from pedido_vista import mostrar_vista_pedidos
from repartidor_vista import mostrar_vista_repartidores
from reportes_vista import mostrar_vista_reportes
from datos_quemados import cargar_datos_quemados


# ── Bootstrap: crear instancias una sola vez por sesión ──────────────────────


def _inicializar_sistema():
    """Crea repositorios, servicios y controladores y los almacena en session_state."""
    if "inicializado" in st.session_state:
        return

    # Repositorios (almacenamiento en memoria)
    cliente_repo = ClienteRepositorio()
    pedido_repo = PedidoRepositorio()
    repartidor_repo = RepartidorRepositorio()
    restaurante_repo = RestauranteRepositorio()

    # Datos quemados (seed data)
    if not restaurante_repo.obtener_todos():
        cargar_datos_quemados(cliente_repo, repartidor_repo, restaurante_repo, pedido_repo)

    # Servicios
    cliente_servicio = ClienteServicio(cliente_repo, pedido_repo)
    pedido_servicio = PedidoServicio(pedido_repo)
    repartidor_servicio = RepartidorServicio(repartidor_repo)
    restaurante_servicio = RestauranteServicio(restaurante_repo)

    # Controladores
    st.session_state.cliente_ctrl = ClienteController(
        cliente_servicio, cliente_repo, pedido_repo, restaurante_repo
    )
    st.session_state.pedido_ctrl = PedidoController(
        pedido_servicio, pedido_repo, repartidor_repo
    )
    st.session_state.repartidor_ctrl = RepartidorController(
        repartidor_servicio, repartidor_repo
    )
    st.session_state.restaurante_ctrl = RestauranteController(
        restaurante_servicio, restaurante_repo
    )

    st.session_state.inicializado = True


# ── Interfaz principal ───────────────────────────────────────────────────────


def main():
    st.set_page_config(
        page_title="CletaEats",
        page_icon="🚴",
        layout="wide",
    )

    _inicializar_sistema()

    # Sidebar con navegación
    st.sidebar.title("🚴 CletaEats")
    st.sidebar.markdown("---")

    pagina = st.sidebar.radio(
        "Navegación",
        [
            "👤 Clientes",
            "🍽️ Restaurantes",
            "🚴 Repartidores",
            "📦 Pedidos",
            "📊 Reportes",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Sistema de gestión de pedidos — Prototipo Lab 1")

    # Renderizar la vista seleccionada
    if pagina == "👤 Clientes":
        mostrar_vista_clientes(
            st.session_state.cliente_ctrl,
            st.session_state.restaurante_ctrl,
        )

    elif pagina == "🍽️ Restaurantes":
        mostrar_vista_restaurantes(st.session_state.restaurante_ctrl)

    elif pagina == "🚴 Repartidores":
        mostrar_vista_repartidores(st.session_state.repartidor_ctrl)

    elif pagina == "📦 Pedidos":
        mostrar_vista_pedidos(
            st.session_state.pedido_ctrl,
            st.session_state.repartidor_ctrl,
        )

    elif pagina == "📊 Reportes":
        mostrar_vista_reportes(
            st.session_state.cliente_ctrl,
            st.session_state.pedido_ctrl,
            st.session_state.repartidor_ctrl,
        )


if __name__ == "__main__":
    main()
